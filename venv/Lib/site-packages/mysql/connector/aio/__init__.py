# Copyright (c) 2023, 2024, Oracle and/or its affiliates.
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

"""MySQL Connector/Python - MySQL driver written in Python."""

__all__ = ["CMySQLConnection", "MySQLConnection", "connect"]

import random

from typing import Any

from ..constants import DEFAULT_CONFIGURATION
from ..errors import Error, InterfaceError, ProgrammingError
from ..pooling import ERROR_NO_CEXT
from .abstracts import MySQLConnectionAbstract
from .connection import MySQLConnection

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
    CMySQLConnection = None


async def connect(*args: Any, **kwargs: Any) -> MySQLConnectionAbstract:
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
        a `CMySQLConnection`) instance.

    Examples:
        A connection with the MySQL server can be established using either the
        `mysql.connector.connect()` method or a `MySQLConnectionAbstract` subclass:
        ```
        >>> from mysql.connector.aio import MySQLConnection, HAVE_CEXT
        >>>
        >>> cnx1 = await mysql.connector.aio.connect(user='joe', database='test')
        >>> cnx2 = MySQLConnection(user='joe', database='test')
        >>> await cnx2.connect()
        >>>
        >>> cnx3 = None
        >>> if HAVE_CEXT:
        >>>     from mysql.connector.aio import CMySQLConnection
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

    # Failover
    if "failover" in kwargs:
        return await _get_failover_connection(**kwargs)

    # Use C Extension by default
    use_pure = kwargs.get("use_pure", False)
    if "use_pure" in kwargs:
        del kwargs["use_pure"]  # Remove 'use_pure' from kwargs
        if not use_pure and CMySQLConnection is None:
            raise ImportError(ERROR_NO_CEXT)

    if CMySQLConnection and not use_pure:
        cnx = CMySQLConnection(*args, **kwargs)
    else:
        cnx = MySQLConnection(*args, **kwargs)
    await cnx.connect()
    return cnx


async def _get_failover_connection(**kwargs: Any) -> MySQLConnectionAbstract:
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
                return await connect(**new_config)
            except Error:
                # If we failed to connect, we try the next server
                pass

    raise InterfaceError("Unable to connect to any of the target hosts")
