# Copyright (c) 2013, 2025, Oracle and/or its affiliates.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is designed to work with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation. The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have either included with
# the program or referenced in the documentation.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/Python, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

"""Implementing pooling of connections to MySQL servers."""
from __future__ import annotations

import queue
import random
import re
import threading

from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, NoReturn, Optional, Tuple, Type, Union
from uuid import uuid4

try:
    import dns.exception
    import dns.resolver
except ImportError:
    HAVE_DNSPYTHON = False
else:
    HAVE_DNSPYTHON = True

try:
    from .connection_cext import CMySQLConnection
except ImportError:
    CMySQLConnection = None  # type: ignore[misc]

from .connection import MySQLConnection
from .constants import CNX_POOL_ARGS, DEFAULT_CONFIGURATION
from .errors import (
    Error,
    InterfaceError,
    NotSupportedError,
    PoolError,
    ProgrammingError,
)
from .optionfiles import read_option_files

if TYPE_CHECKING:
    from .abstracts import MySQLConnectionAbstract

CONNECTION_POOL_LOCK = threading.RLock()
CNX_POOL_MAXSIZE = 32
CNX_POOL_MAXNAMESIZE = 64
CNX_POOL_NAMEREGEX = re.compile(r"[^a-zA-Z0-9._:\-*$#]")
ERROR_NO_CEXT = "MySQL Connector/Python C Extension not available"
MYSQL_CNX_CLASS: Union[type, Tuple[type, ...]] = (
    MySQLConnection if CMySQLConnection is None else (MySQLConnection, CMySQLConnection)
)

_CONNECTION_POOLS: Dict[str, MySQLConnectionPool] = {}


def _get_pooled_connection(**kwargs: Any) -> PooledMySQLConnection:
    """Return a pooled MySQL connection."""
    # If no pool name specified, generate one
    pool_name = (
        kwargs["pool_name"] if "pool_name" in kwargs else generate_pool_name(**kwargs)
    )

    if kwargs.get("use_pure") is False and CMySQLConnection is None:
        raise ImportError(ERROR_NO_CEXT)

    # Setup the pool, ensuring only 1 thread can update at a time
    with CONNECTION_POOL_LOCK:
        if pool_name not in _CONNECTION_POOLS:
            _CONNECTION_POOLS[pool_name] = MySQLConnectionPool(**kwargs)
        elif isinstance(_CONNECTION_POOLS[pool_name], MySQLConnectionPool):
            # pool_size must be the same
            check_size = _CONNECTION_POOLS[pool_name].pool_size
            if "pool_size" in kwargs and kwargs["pool_size"] != check_size:
                raise PoolError("Size can not be changed for active pools.")

    # Return pooled connection
    try:
        return _CONNECTION_POOLS[pool_name].get_connection()
    except AttributeError:
        raise InterfaceError(
            f"Failed getting connection from pool '{pool_name}'"
        ) from None


def _get_failover_connection(
    **kwargs: Any,
) -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
    """Return a MySQL connection and try to failover if needed.

    An InterfaceError is raise when no MySQL is available. ValueError is
    raised when the failover server configuration contains an illegal
    connection argument. Supported arguments are user, password, host, port,
    unix_socket and database. ValueError is also raised when the failover
    argument was not provided.

    Returns MySQLConnection instance.
    """
    config = kwargs.copy()
    try:
        failover = config["failover"]
    except KeyError:
        raise ValueError("failover argument not provided") from None
    del config["failover"]

    support_cnx_args = set(
        [
            "user",
            "password",
            "host",
            "port",
            "unix_socket",
            "database",
            "pool_name",
            "pool_size",
            "priority",
        ]
    )

    # First check if we can add all use the configuration
    priority_count = 0
    for server in failover:
        diff = set(server.keys()) - support_cnx_args
        if diff:
            arg = "s" if len(diff) > 1 else ""
            lst = ", ".join(diff)
            raise ValueError(
                f"Unsupported connection argument {arg} in failover: {lst}"
            )
        if hasattr(server, "priority"):
            priority_count += 1

        server["priority"] = server.get("priority", 100)
        if server["priority"] < 0 or server["priority"] > 100:
            raise InterfaceError(
                "Priority value should be in the range of 0 to 100, "
                f"got : {server['priority']}"
            )
        if not isinstance(server["priority"], int):
            raise InterfaceError(
                "Priority value should be an integer in the range of 0 to "
                f"100, got : {server['priority']}"
            )

    if 0 < priority_count < len(failover):
        raise ProgrammingError(
            "You must either assign no priority to any "
            "of the routers or give a priority for "
            "every router"
        )

    server_directory = {}
    server_priority_list = []
    for server in sorted(failover, key=lambda x: x["priority"], reverse=True):
        if server["priority"] not in server_directory:
            server_directory[server["priority"]] = [server]
            server_priority_list.append(server["priority"])
        else:
            server_directory[server["priority"]].append(server)

    for priority in server_priority_list:
        failover_list = server_directory[priority]
        for _ in range(len(failover_list)):
            last = len(failover_list) - 1
            index = random.randint(0, last)
            server = failover_list.pop(index)
            new_config = config.copy()
            new_config.update(server)
            new_config.pop("priority", None)
            try:
                return connect(**new_config)
            except Error:
                # If we failed to connect, we try the next server
                pass

    raise InterfaceError("Unable to connect to any of the target hosts")


def connect(
    *args: Any, **kwargs: Any
) -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
    """Creates or gets a MySQL connection object.

    In its simpliest form, `connect()` will open a connection to a
    MySQL server and return a `MySQLConnectionAbstract` subclass
    object such as `MySQLConnection` or `CMySQLConnection`.

    When any connection pooling arguments are given, for example `pool_name`
    or `pool_size`, a pool is created or a previously one is used to return
    a `PooledMySQLConnection`.

    Args:
        *args: N/A.
        **kwargs: For a complete list of possible arguments, see [1]. If no arguments
                  are given, it uses the already configured or default values.

    Returns:
        A `MySQLConnectionAbstract` subclass instance (such as `MySQLConnection` or
        `CMySQLConnection`) or a `PooledMySQLConnection` instance.

    Examples:
        A connection with the MySQL server can be established using either the
        `mysql.connector.connect()` method or a `MySQLConnectionAbstract` subclass:
        ```
        >>> from mysql.connector import MySQLConnection, HAVE_CEXT
        >>>
        >>> cnx1 = mysql.connector.connect(user='joe', database='test')
        >>> cnx2 = MySQLConnection(user='joe', database='test')
        >>>
        >>> cnx3 = None
        >>> if HAVE_CEXT:
        >>>     from mysql.connector import CMySQLConnection
        >>>     cnx3 = CMySQLConnection(user='joe', database='test')
        ```

    References:
        [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    """
    # DNS SRV
    dns_srv = kwargs.pop("dns_srv") if "dns_srv" in kwargs else False

    if not isinstance(dns_srv, bool):
        raise InterfaceError("The value of 'dns-srv' must be a boolean")

    if dns_srv:
        if not HAVE_DNSPYTHON:
            raise InterfaceError(
                "MySQL host configuration requested DNS "
                "SRV. This requires the Python dnspython "
                "module. Please refer to documentation"
            )
        if "unix_socket" in kwargs:
            raise InterfaceError(
                "Using Unix domain sockets with DNS SRV lookup is not allowed"
            )
        if "port" in kwargs:
            raise InterfaceError(
                "Specifying a port number with DNS SRV lookup is not allowed"
            )
        if "failover" in kwargs:
            raise InterfaceError(
                "Specifying multiple hostnames with DNS SRV look up is not allowed"
            )
        if "host" not in kwargs:
            kwargs["host"] = DEFAULT_CONFIGURATION["host"]

        try:
            srv_records = dns.resolver.query(kwargs["host"], "SRV")
        except dns.exception.DNSException:
            raise InterfaceError(
                f"Unable to locate any hosts for '{kwargs['host']}'"
            ) from None

        failover = []
        for srv in srv_records:
            failover.append(
                {
                    "host": srv.target.to_text(omit_final_dot=True),
                    "port": srv.port,
                    "priority": srv.priority,
                    "weight": srv.weight,
                }
            )

        failover.sort(key=lambda x: (x["priority"], -x["weight"]))
        kwargs["failover"] = [
            {"host": srv["host"], "port": srv["port"]} for srv in failover
        ]

    # Option files
    if "read_default_file" in kwargs:
        kwargs["option_files"] = kwargs["read_default_file"]
        kwargs.pop("read_default_file")

    if "option_files" in kwargs:
        new_config = read_option_files(**kwargs)
        return connect(**new_config)

    # Failover
    if "failover" in kwargs:
        return _get_failover_connection(**kwargs)

    # Pooled connections
    try:
        if any(key in kwargs for key in CNX_POOL_ARGS):
            return _get_pooled_connection(**kwargs)
    except NameError:
        # No pooling
        pass

    # Use C Extension by default
    use_pure = kwargs.get("use_pure", False)
    if "use_pure" in kwargs:
        del kwargs["use_pure"]  # Remove 'use_pure' from kwargs
        if not use_pure and CMySQLConnection is None:
            raise ImportError(ERROR_NO_CEXT)

    if CMySQLConnection and not use_pure:
        return CMySQLConnection(*args, **kwargs)
    return MySQLConnection(*args, **kwargs)


def generate_pool_name(**kwargs: Any) -> str:
    """Generate a pool name

    This function takes keyword arguments, usually the connection
    arguments for MySQLConnection, and tries to generate a name for
    a pool.

    Raises PoolError when no name can be generated.

    Returns a string.
    """
    parts = []
    for key in ("host", "port", "user", "database"):
        try:
            parts.append(str(kwargs[key]))
        except KeyError:
            pass

    if not parts:
        raise PoolError("Failed generating pool name; specify pool_name")

    return "_".join(parts)


class PooledMySQLConnection:
    """Class holding a MySQL Connection in a pool

    PooledMySQLConnection is used by MySQLConnectionPool to return an
    instance holding a MySQL connection. It works like a MySQLConnection
    except for methods like close() and config().

    The close()-method will add the connection back to the pool rather
    than disconnecting from the MySQL server.

    Configuring the connection have to be done through the MySQLConnectionPool
    method set_config(). Using config() on pooled connection will raise a
    PoolError.

    Attributes:
        pool_name (str): Returns the name of the connection pool to which the
                         connection belongs.
    """

    def __init__(self, pool: MySQLConnectionPool, cnx: MySQLConnectionAbstract) -> None:
        """Constructor.

        Args:
            pool: A `MySQLConnectionPool` instance.
            cnx: A `MySQLConnectionAbstract` subclass instance.
        """
        if not isinstance(pool, MySQLConnectionPool):
            raise AttributeError("pool should be a MySQLConnectionPool")
        if not isinstance(cnx, MYSQL_CNX_CLASS):
            raise AttributeError("cnx should be a MySQLConnection")
        self._cnx_pool: MySQLConnectionPool = pool
        self._cnx: MySQLConnectionAbstract = cnx

    def __enter__(self) -> PooledMySQLConnection:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.close()

    def __getattr__(self, attr: Any) -> Any:
        """Calls attributes of the MySQLConnection instance"""
        return getattr(self._cnx, attr)

    def close(self) -> None:
        """Do not close, but adds connection back to pool.

        For a pooled connection, close() does not actually close it but returns it
        to the pool and makes it available for subsequent connection requests. If the
        pool configuration parameters are changed, a returned connection is closed
        and reopened with the new configuration before being returned from the pool
        again in response to a connection request.
        """
        try:
            cnx = self._cnx
            if self._cnx_pool.reset_session:
                cnx.reset_session()
        finally:
            self._cnx_pool.add_connection(cnx)
            self._cnx = None

    @staticmethod
    def config(**kwargs: Any) -> NoReturn:
        """Configuration is done through the pool.

        For pooled connections, the `config()` method raises a `PoolError`
        exception. Configuration for pooled connections should be done
        using the pool object.
        """
        raise PoolError(
            "Configuration for pooled connections should be done through the "
            "pool itself"
        )

    @property
    def pool_name(self) -> str:
        """Returns the name of the connection pool to which the connection belongs."""
        return self._cnx_pool.pool_name


class MySQLConnectionPool:
    """Class defining a pool of MySQL connections"""

    def __init__(
        self,
        pool_size: int = 5,
        pool_name: Optional[str] = None,
        pool_reset_session: bool = True,
        **kwargs: Any,
    ) -> None:
        """Constructor.

        Initialize a MySQL connection pool with a maximum number of
        connections set to `pool_size`. The rest of the keywords
        arguments, kwargs, are configuration arguments for MySQLConnection
        instances.

        Args:
            pool_name: The pool name. If this argument is not given, Connector/Python
                       automatically generates the name, composed from whichever of
                       the host, port, user, and database connection arguments are
                       given in kwargs, in that order.
            pool_size:  The pool size. If this argument is not given, the default is 5.
            pool_reset_session: Whether to reset session variables when the connection
                                is returned to the pool.
            **kwargs: Optional additional connection arguments, as described in [1].

        Examples:
            ```
            >>> dbconfig = {
            >>>     "database": "test",
            >>>     "user":     "joe",
            >>> }
            >>> cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
            >>>                                                       pool_size = 3,
            >>>                                                       **dbconfig)
            ```

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        """
        self._pool_size: Optional[int] = None
        self._pool_name: Optional[str] = None
        self._reset_session = pool_reset_session
        self._set_pool_size(pool_size)
        self._set_pool_name(pool_name or generate_pool_name(**kwargs))
        self._cnx_config: Dict[str, Any] = {}
        self._cnx_queue: queue.Queue[MySQLConnectionAbstract] = queue.Queue(
            self._pool_size
        )
        self._config_version = uuid4()

        if kwargs:
            self.set_config(**kwargs)
            cnt = 0
            while cnt < self._pool_size:
                self.add_connection()
                cnt += 1

    @property
    def pool_name(self) -> str:
        """Returns the name of the connection pool."""
        return self._pool_name

    @property
    def pool_size(self) -> int:
        """Returns number of connections managed by the pool."""
        return self._pool_size

    @property
    def reset_session(self) -> bool:
        """Returns whether to reset session."""
        return self._reset_session

    def set_config(self, **kwargs: Any) -> None:
        """Set the connection configuration for `MySQLConnectionAbstract` subclass instances.

        This method sets the configuration used for creating `MySQLConnectionAbstract`
        subclass instances such as `MySQLConnection`. See [1] for valid
        connection arguments.

        Args:
            **kwargs: Connection arguments - for a complete list of possible
                      arguments, see [1].

        Raises:
            PoolError: When a connection argument is not valid, missing
                       or not supported by `MySQLConnectionAbstract`.

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        """
        if not kwargs:
            return

        with CONNECTION_POOL_LOCK:
            try:
                test_cnx = connect()
                test_cnx.config(**kwargs)
                self._cnx_config = kwargs
                self._config_version = uuid4()
            except AttributeError as err:
                raise PoolError(f"Connection configuration not valid: {err}") from err

    def _set_pool_size(self, pool_size: int) -> None:
        """Set the size of the pool

        This method sets the size of the pool but it will not resize the pool.

        Raises an AttributeError when the pool_size is not valid. Invalid size
        is 0, negative or higher than pooling.CNX_POOL_MAXSIZE.
        """
        if pool_size <= 0 or pool_size > CNX_POOL_MAXSIZE:
            raise AttributeError(
                "Pool size should be higher than 0 and lower or equal to "
                f"{CNX_POOL_MAXSIZE}"
            )
        self._pool_size = pool_size

    def _set_pool_name(self, pool_name: str) -> None:
        r"""Set the name of the pool.

        This method checks the validity and sets the name of the pool.

        Raises an AttributeError when pool_name contains illegal characters
        ([^a-zA-Z0-9._\-*$#]) or is longer than pooling.CNX_POOL_MAXNAMESIZE.
        """
        if CNX_POOL_NAMEREGEX.search(pool_name):
            raise AttributeError(f"Pool name '{pool_name}' contains illegal characters")
        if len(pool_name) > CNX_POOL_MAXNAMESIZE:
            raise AttributeError(f"Pool name '{pool_name}' is too long")
        self._pool_name = pool_name

    def _queue_connection(self, cnx: MySQLConnectionAbstract) -> None:
        """Put connection back in the queue

        This method is putting a connection back in the queue. It will not
        acquire a lock as the methods using _queue_connection() will have it
        set.

        Raises `PoolError` on errors.
        """
        if not isinstance(cnx, MYSQL_CNX_CLASS):
            raise PoolError(
                "Connection instance not subclass of MySQLConnectionAbstract"
            )

        try:
            self._cnx_queue.put(cnx, block=False)
        except queue.Full as err:
            raise PoolError("Failed adding connection; queue is full") from err

    def add_connection(self, cnx: Optional[MySQLConnectionAbstract] = None) -> None:
        """Adds a connection to the pool.

        This method instantiates a `MySQLConnection` using the configuration
        passed when initializing the `MySQLConnectionPool` instance or using
        the `set_config()` method.
        If cnx is a `MySQLConnection` instance, it will be added to the
        queue.

        Args:
            cnx: The `MySQLConnectionAbstract` subclass object to be added to
                 the pool. If this argument is missing (aka `None`), the pool
                 creates a new connection and adds it.

        Raises:
            PoolError: When no configuration is set, when no more
                       connection can be added (maximum reached) or when the connection
                       can not be instantiated.
        """
        with CONNECTION_POOL_LOCK:
            if not self._cnx_config:
                raise PoolError("Connection configuration not available")

            if self._cnx_queue.full():
                raise PoolError("Failed adding connection; queue is full")

            if not cnx:
                cnx = connect(**self._cnx_config)  # type: ignore[assignment]
                try:
                    if (
                        self._reset_session
                        and self._cnx_config["compress"]
                        and cnx.server_version < (5, 7, 3)
                    ):
                        raise NotSupportedError(
                            "Pool reset session is not supported with "
                            "compression for MySQL server version 5.7.2 "
                            "or earlier"
                        )
                except KeyError:
                    pass

                cnx.pool_config_version = self._config_version
            else:
                if not isinstance(cnx, MYSQL_CNX_CLASS):
                    raise PoolError(
                        "Connection instance not subclass of MySQLConnectionAbstract"
                    )

            self._queue_connection(cnx)

    def get_connection(self) -> PooledMySQLConnection:
        """Gets a connection from the pool.

        This method returns an PooledMySQLConnection instance which
        has a reference to the pool that created it, and the next available
        MySQL connection.

        When the MySQL connection is not connect, a reconnect is attempted.

        Returns:
            A `PooledMySQLConnection` instance.

        Raises:
            PoolError: On errors.
        """
        with CONNECTION_POOL_LOCK:
            try:
                cnx = self._cnx_queue.get(block=False)
            except queue.Empty as err:
                raise PoolError("Failed getting connection; pool exhausted") from err

            if (
                not cnx.is_connected()
                or self._config_version != cnx.pool_config_version
            ):
                cnx.config(**self._cnx_config)
                try:
                    cnx.reconnect()
                except InterfaceError:
                    # Failed to reconnect, give connection back to pool
                    self._queue_connection(cnx)
                    raise
                cnx.pool_config_version = self._config_version

            return PooledMySQLConnection(self, cnx)

    def _remove_connections(self) -> int:
        """Close all connections

        This method closes all connections. It returns the number
        of connections it closed.

        Used mostly for tests.

        Returns int.
        """
        with CONNECTION_POOL_LOCK:
            cnt = 0
            cnxq = self._cnx_queue
            while cnxq.qsize():
                try:
                    cnx = cnxq.get(block=False)
                    cnx.disconnect()
                    cnt += 1
                except queue.Empty:
                    return cnt
                except PoolError:
                    raise
                except Error:
                    # Any other error when closing means connection is closed
                    pass

            return cnt
