# Copyright (c) 2014, 2025, Oracle and/or its affiliates.
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

# mypy: disable-error-code="arg-type"

"""Connection class using the C Extension."""

import os
import platform
import socket
import sys
import warnings

from typing import (
    Any,
    BinaryIO,
    Dict,
    List,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from . import version
from ._decorating import cmd_refresh_verify_options
from .abstracts import CMySQLPrepStmt, MySQLConnectionAbstract
from .constants import ClientFlag, FieldFlag, FieldType, ServerFlag, ShutdownType
from .conversion import MySQLConverter
from .errors import (
    InterfaceError,
    InternalError,
    OperationalError,
    ProgrammingError,
    get_mysql_exception,
)
from .protocol import MySQLProtocol
from .types import (
    CextEofPacketType,
    CextResultType,
    DescriptionType,
    ParamsSequenceOrDictType,
    RowType,
    StatsPacketType,
    StrOrBytes,
)
from .utils import (
    import_object,
    warn_ciphersuites_deprecated,
    warn_tls_version_deprecated,
)

HAVE_CMYSQL = False

try:
    import _mysql_connector

    from _mysql_connector import MySQLInterfaceError

    from .cursor_cext import (
        CMySQLCursor,
        CMySQLCursorBuffered,
        CMySQLCursorBufferedDict,
        CMySQLCursorBufferedRaw,
        CMySQLCursorDict,
        CMySQLCursorPrepared,
        CMySQLCursorPreparedDict,
        CMySQLCursorRaw,
    )

    HAVE_CMYSQL = True
except ImportError as exc:
    raise ImportError(
        f"MySQL Connector/Python C Extension not available ({exc})"
    ) from exc

from .opentelemetry.constants import OTEL_ENABLED
from .opentelemetry.context_propagation import with_context_propagation

if OTEL_ENABLED:
    from .opentelemetry.instrumentation import end_span, record_exception_event


class CMySQLConnection(MySQLConnectionAbstract):
    """Class initiating a MySQL Connection using Connector/C."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialization"""
        if not HAVE_CMYSQL:
            raise RuntimeError("MySQL Connector/Python C Extension not available")
        self._cmysql: Optional[
            _mysql_connector.MySQL  # pylint: disable=c-extension-no-member
        ] = None
        self._columns: List[DescriptionType] = []
        self._plugin_dir: str = os.path.join(
            os.path.dirname(os.path.abspath(_mysql_connector.__file__)),
            "mysql",
            "vendor",
            "plugin",
        )
        if platform.system() == "Linux":
            # Use the authentication plugins from system if they aren't bundled
            if not os.path.exists(self._plugin_dir):
                self._plugin_dir = (
                    "/usr/lib64/mysql/plugin"
                    if os.path.exists("/usr/lib64/mysql/plugin")
                    else "/usr/lib/mysql/plugin"
                )

        self.converter: Optional[MySQLConverter] = None
        super().__init__()

        if kwargs:
            try:
                self.connect(**kwargs)
            except Exception:
                self.close()
                raise

    def _add_default_conn_attrs(self) -> None:
        """Add default connection attributes"""
        license_chunks = version.LICENSE.split(" ")
        if license_chunks[0] == "GPLv2":
            client_license = "GPL-2.0"
        else:
            client_license = "Commercial"

        self._conn_attrs.update(
            {
                "_connector_name": "mysql-connector-python",
                "_connector_license": client_license,
                "_connector_version": ".".join([str(x) for x in version.VERSION[0:3]]),
                "_source_host": socket.gethostname(),
            }
        )

    def _do_handshake(self) -> None:
        """Gather information of the MySQL server before authentication"""
        self._handshake = {
            "protocol": self._cmysql.get_proto_info(),
            "server_version_original": self._cmysql.get_server_info(),
            "server_threadid": self._cmysql.thread_id(),
            "charset": None,
            "server_status": None,
            "auth_plugin": None,
            "auth_data": None,
            "capabilities": self._cmysql.st_server_capabilities(),
        }

        self._server_version = self._check_server_version(
            self._handshake["server_version_original"]
        )
        self._character_set.set_mysql_version(self._server_version)

    @property
    def _server_status(self) -> int:
        """Returns the server status attribute of MYSQL structure"""
        return self._cmysql.st_server_status()

    def set_allow_local_infile_in_path(self, path: str) -> None:
        """set local_infile_in_path

        Set allow_local_infile_in_path.
        """

        if self._cmysql:
            self._cmysql.set_load_data_local_infile_option(path)

    @MySQLConnectionAbstract.use_unicode.setter  # type: ignore
    def use_unicode(self, value: bool) -> None:
        self._use_unicode = value
        if self._cmysql:
            self._cmysql.use_unicode(value)
        if self.converter:
            self.converter.set_unicode(value)

    @property
    def autocommit(self) -> bool:
        """Get whether autocommit is on or off"""
        value = self.info_query("SELECT @@session.autocommit")[0]
        return value == 1

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        """Toggle autocommit"""
        try:
            self._cmysql.autocommit(value)
            self._autocommit = value
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @property
    def read_timeout(self) -> Optional[int]:
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, timeout: int) -> None:
        raise ProgrammingError(
            """
            The use of read_timeout after the connection has been established is unsupported
            in the C-Extension
            """
        )

    @property
    def write_timeout(self) -> Optional[int]:
        return self._write_timeout

    @write_timeout.setter
    def write_timeout(self, timeout: int) -> None:
        raise ProgrammingError(
            """
            Changes in write_timeout after the connection has been established is unsupported
            in the C-Extension
            """
        )

    @property
    def database(self) -> str:
        """Get the current database"""
        return self.info_query("SELECT DATABASE()")[0]  # type: ignore[return-value]

    @database.setter
    def database(self, value: str) -> None:
        """Set the current database"""
        try:
            self._cmysql.select_db(value)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @property
    def in_transaction(self) -> bool:
        """MySQL session has started a transaction"""
        return bool(self._server_status & ServerFlag.STATUS_IN_TRANS)

    def _open_connection(self) -> None:
        charset_name = self._character_set.get_info(self._charset_id)[0]
        # pylint: disable=c-extension-no-member
        self._cmysql = _mysql_connector.MySQL(
            buffered=self._buffered,
            raw=self._raw,
            charset_name=charset_name,
            connection_timeout=(self._connection_timeout or 0),
            use_unicode=self.use_unicode,
            auth_plugin=self._auth_plugin,
            plugin_dir=self._plugin_dir,
        )
        # pylint: enable=c-extension-no-member
        if not self.isset_client_flag(ClientFlag.CONNECT_ARGS):
            self._conn_attrs = {}

        cnx_kwargs = {
            "host": self._host,
            "user": self._user,
            "password": self._password,
            "password1": self._password1,
            "password2": self._password2,
            "password3": self._password3,
            "database": self._database,
            "port": self._port,
            "client_flags": self.client_flags,
            "unix_socket": self._unix_socket,
            "compress": self._compress,
            "ssl_disabled": True,
            "conn_attrs": self._conn_attrs,
            "local_infile": self._allow_local_infile,
            "load_data_local_dir": self._allow_local_infile_in_path,
            "oci_config_file": self._oci_config_file,
            "oci_config_profile": self._oci_config_profile,
            "webauthn_callback": (
                import_object(self._webauthn_callback)
                if isinstance(self._webauthn_callback, str)
                else self._webauthn_callback
            ),
            "openid_token_file": self._openid_token_file,
            "read_timeout": self._read_timeout if self._read_timeout else 0,
            "write_timeout": self._write_timeout if self._write_timeout else 0,
        }

        tls_versions = self._ssl.get("tls_versions")
        if tls_versions is not None:
            tls_versions.sort(reverse=True)  # type: ignore[union-attr]
            tls_versions = ",".join(tls_versions)
        if self._ssl.get("tls_ciphersuites") is not None:
            ssl_ciphersuites = (
                self._ssl.get("tls_ciphersuites")[0] or None  # type: ignore[index]
            )  # if it's the empty string, then use `None` instead
            tls_ciphersuites = self._ssl.get("tls_ciphersuites")[  # type: ignore[index]
                1
            ]
        else:
            ssl_ciphersuites = None
            tls_ciphersuites = None
        if (
            tls_versions is not None
            and "TLSv1.3" in tls_versions
            and not tls_ciphersuites
        ):
            tls_ciphersuites = "TLS_AES_256_GCM_SHA384"
        if not self._ssl_disabled:
            cnx_kwargs.update(
                {
                    "ssl_ca": self._ssl.get("ca"),
                    "ssl_cert": self._ssl.get("cert"),
                    "ssl_key": self._ssl.get("key"),
                    "ssl_cipher_suites": ssl_ciphersuites,
                    "tls_versions": tls_versions,
                    "tls_cipher_suites": tls_ciphersuites,
                    "ssl_verify_cert": self._ssl.get("verify_cert") or False,
                    "ssl_verify_identity": self._ssl.get("verify_identity") or False,
                    "ssl_disabled": self._ssl_disabled,
                }
            )

        if os.name == "nt" and self._auth_plugin_class == "MySQLKerberosAuthPlugin":
            cnx_kwargs["use_kerberos_gssapi"] = True

        try:
            self._cmysql.connect(**cnx_kwargs)
            self._cmysql.converter_str_fallback = self._converter_str_fallback
            if self.converter:
                self.converter.str_fallback = self._converter_str_fallback
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        self._do_handshake()

        if (
            not self._ssl_disabled
            and hasattr(self._cmysql, "get_ssl_cipher")
            and callable(self._cmysql.get_ssl_cipher)
        ):
            # Raise a deprecation warning if deprecated TLS version
            # or cipher is being used.

            # `get_ssl_cipher()` returns the name of the cipher being used.
            cipher = self._cmysql.get_ssl_cipher()
            for tls_version in set(self._ssl.get("tls_versions", [])):
                warn_tls_version_deprecated(tls_version)
                warn_ciphersuites_deprecated(cipher, tls_version)

    def close(self) -> None:
        if self._span and self._span.is_recording():
            # pylint: disable=possibly-used-before-assignment
            record_exception_event(self._span, sys.exc_info()[1])

        if not self._cmysql:
            return

        try:
            self.free_result()
            self._cmysql.close()
        except MySQLInterfaceError as err:
            if OTEL_ENABLED:
                record_exception_event(self._span, err)
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err
        finally:
            if OTEL_ENABLED:
                end_span(self._span)

    disconnect = close

    def is_closed(self) -> bool:
        """Return True if the connection to MySQL Server is closed."""
        return not self._cmysql.connected()

    def is_connected(self) -> bool:
        """Reports whether the connection to MySQL Server is available"""
        if self._cmysql:
            self.handle_unread_result()
            return self._cmysql.ping()

        return False

    def ping(self, reconnect: bool = False, attempts: int = 1, delay: int = 0) -> None:
        """Check availability of the MySQL server

        When reconnect is set to True, one or more attempts are made to try
        to reconnect to the MySQL server using the reconnect()-method.

        delay is the number of seconds to wait between each retry.

        When the connection is not available, an InterfaceError is raised. Use
        the is_connected()-method if you just want to check the connection
        without raising an error.

        Raises InterfaceError on errors.
        """
        self.handle_unread_result()

        try:
            connected = self._cmysql.ping()
        except AttributeError:
            pass  # Raise or reconnect later
        else:
            if connected:
                return

        if reconnect:
            self.reconnect(attempts=attempts, delay=delay)
        else:
            raise InterfaceError("Connection to MySQL is not available")

    def set_character_set_name(self, charset: str) -> None:
        """Sets the default character set name for current connection."""
        self._cmysql.set_character_set(charset)

    def info_query(self, query: StrOrBytes) -> Optional[RowType]:
        """Send a query which only returns 1 row"""
        first_row = ()
        try:
            self._cmysql.query(query)
            if self._cmysql.have_result_set:
                first_row = self._cmysql.fetch_row()
                if self._cmysql.fetch_row():
                    self._cmysql.free_result()
                    raise InterfaceError("Query should not return more than 1 row")
            self._cmysql.free_result()
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        return first_row

    @property
    def connection_id(self) -> Optional[int]:
        """MySQL connection ID"""
        try:
            return self._cmysql.thread_id()
        except MySQLInterfaceError:
            pass  # Just return None

        return None

    def get_rows(
        self,
        count: Optional[int] = None,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[List[RowType], Optional[CextEofPacketType]]:
        """Get all or a subset of rows returned by the MySQL server"""
        unread_result = prep_stmt.have_result_set if prep_stmt else self.unread_result
        if not (self._cmysql and unread_result):
            raise InternalError("No result set available")

        if raw is None:
            raw = self._raw

        rows: List[Tuple] = []
        if count is not None and count <= 0:
            raise AttributeError("count should be 1 or higher, or None")

        counter = 0
        try:
            fetch_row = prep_stmt.fetch_row if prep_stmt else self._cmysql.fetch_row
            if self.converter or raw:
                # When using a converter class or `raw`, the C extension should not
                # convert the values. This can be accomplished by setting
                # the raw option to True.
                self._cmysql.raw(True)

            row = fetch_row()
            while row:
                row = list(row)

                if not self._cmysql.raw() and not raw:
                    # `not _cmysql.raw()` means the c-ext conversion layer will happen.
                    # `not raw` means the caller wants conversion to happen.
                    # For a VECTOR type, the c-ext conversion layer cannot return
                    # an array.array type since such a type isn't part of the Python/C
                    # API. Therefore, the c-ext will treat VECTOR types as if they
                    # were BLOB types - be returned as `bytes` always.
                    # Hence, a VECTOR type must be cast to an array.array type using the
                    # built-in python conversion layer.
                    # pylint: disable=protected-access
                    for i, dsc in enumerate(self._columns):
                        if dsc[1] == FieldType.VECTOR:
                            row[i] = MySQLConverter._vector_to_python(row[i])

                if not self._raw and self.converter:
                    for i, _ in enumerate(row):
                        if not raw:
                            row[i] = self.converter.to_python(self._columns[i], row[i])

                rows.append(tuple(row))
                counter += 1

                if count and counter == count:
                    break

                row = fetch_row()
            if not row:
                _eof: Optional[CextEofPacketType] = self.fetch_eof_columns(prep_stmt)[
                    "eof"
                ]  # type: ignore[assignment]
                if prep_stmt:
                    prep_stmt.free_result()
                    self._unread_result = False
                else:
                    self.free_result()
            else:
                _eof = None
        except MySQLInterfaceError as err:
            if prep_stmt:
                prep_stmt.free_result()
            else:
                self.free_result()
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        return rows, _eof

    def get_row(
        self,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[RowType], Optional[CextEofPacketType]]:
        """Get the next rows returned by the MySQL server"""
        try:
            rows, eof = self.get_rows(
                count=1,
                binary=binary,
                columns=columns,
                raw=raw,
                prep_stmt=prep_stmt,
            )
            if rows:
                return (rows[0], eof)
            return (None, eof)
        except IndexError:
            # No row available
            return (None, None)

    def next_result(self) -> Optional[bool]:
        """Reads the next result"""
        if self._cmysql:
            self._cmysql.consume_result()
            return self._cmysql.next_result()
        return None

    def free_result(self) -> None:
        """Frees the result"""
        if self._cmysql:
            self._cmysql.free_result()

    def commit(self) -> None:
        """Commit current transaction"""
        if self._cmysql:
            self.handle_unread_result()
            self._cmysql.commit()

    def rollback(self) -> None:
        """Rollback current transaction"""
        if self._cmysql:
            self._cmysql.consume_result()
            self._cmysql.rollback()

    def cmd_init_db(self, database: str) -> None:
        """Change the current database"""
        try:
            self._cmysql.select_db(database)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    def fetch_eof_columns(
        self, prep_stmt: Optional[CMySQLPrepStmt] = None
    ) -> CextResultType:
        """Fetch EOF and column information"""
        have_result_set = (
            prep_stmt.have_result_set if prep_stmt else self._cmysql.have_result_set
        )
        if not have_result_set:
            raise InterfaceError("No result set")

        fields = prep_stmt.fetch_fields() if prep_stmt else self._cmysql.fetch_fields()
        self._columns = []
        for col in fields:
            self._columns.append(
                (
                    col[4],
                    int(col[8]),
                    None,
                    None,
                    None,
                    None,
                    ~int(col[9]) & FieldFlag.NOT_NULL,
                    int(col[9]),
                    int(col[6]),
                )
            )

        return {
            "eof": {
                "status_flag": self._server_status,
                "warning_count": self._cmysql.st_warning_count(),
            },
            "columns": self._columns,
        }

    def fetch_eof_status(self) -> Optional[CextEofPacketType]:
        """Fetch EOF and status information"""
        if self._cmysql:
            return {
                "warning_count": self._cmysql.st_warning_count(),
                "field_count": self._cmysql.st_field_count(),
                "insert_id": self._cmysql.insert_id(),
                "affected_rows": self._cmysql.affected_rows(),
                "server_status": self._server_status,
            }

        return None

    def cmd_stmt_prepare(
        self,
        statement: bytes,
        **kwargs: Any,
    ) -> CMySQLPrepStmt:
        """Prepares the SQL statement"""
        if not self._cmysql:
            raise OperationalError("MySQL Connection not available")

        try:
            stmt = self._cmysql.stmt_prepare(statement)
            stmt.converter_str_fallback = self._converter_str_fallback
            return CMySQLPrepStmt(stmt)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @with_context_propagation
    def cmd_stmt_execute(
        self,
        statement_id: CMySQLPrepStmt,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Union[CextEofPacketType, CextResultType]]:
        """Executes the prepared statement"""
        try:
            statement_id.stmt_execute(*args, query_attrs=self.query_attrs)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        self._columns = []
        if not statement_id.have_result_set:
            # No result
            self._unread_result = False
            return self.fetch_eof_status()

        self._unread_result = True
        return self.fetch_eof_columns(statement_id)

    def cmd_stmt_close(
        self,
        statement_id: CMySQLPrepStmt,  # type: ignore[override]
        **kwargs: Any,
    ) -> None:
        """Closes the prepared statement"""
        if self._unread_result:
            raise InternalError("Unread result found")
        try:
            statement_id.stmt_close()
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    def cmd_stmt_reset(
        self,
        statement_id: CMySQLPrepStmt,  # type: ignore[override]
        **kwargs: Any,
    ) -> None:
        """Resets the prepared statement"""
        if self._unread_result:
            raise InternalError("Unread result found")
        try:
            statement_id.stmt_reset()
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @with_context_propagation
    def cmd_query(
        self,
        query: StrOrBytes,
        raw: Optional[bool] = None,
        buffered: bool = False,
        raw_as_string: bool = False,
        **kwargs: Any,
    ) -> Optional[Union[CextEofPacketType, CextResultType]]:
        self.handle_unread_result()
        if raw is None:
            raw = self._raw
        try:
            if not isinstance(query, bytes):
                query = query.encode("utf-8")

            # Set/Reset internal state related to query execution
            self._query = query
            self._local_infile_filenames = None

            self._cmysql.query(
                query,
                raw=raw,
                buffered=buffered,
                raw_as_string=raw_as_string,
                query_attrs=self.query_attrs,
            )
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err
        except AttributeError as err:
            addr = (
                self._unix_socket if self._unix_socket else f"{self._host}:{self._port}"
            )
            raise OperationalError(
                errno=2055, values=(addr, "Connection not available.")
            ) from err

        self._columns = []
        if not self._cmysql.have_result_set:
            # No result
            return self.fetch_eof_status()

        return self.fetch_eof_columns()

    _execute_query = cmd_query

    def cursor(
        self,
        buffered: Optional[bool] = None,
        raw: Optional[bool] = None,
        prepared: Optional[bool] = None,
        cursor_class: Optional[Type[CMySQLCursor]] = None,  # type: ignore[override]
        dictionary: Optional[bool] = None,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> CMySQLCursor:
        """Instantiates and returns a cursor using C Extension

        By default, CMySQLCursor is returned. Depending on the options
        while connecting, a buffered and/or raw cursor is instantiated
        instead. Also depending upon the cursor options, rows can be
        returned as a dictionary or a tuple.

        Dictionary based cursors are available with buffered
        output but not raw.

        It is possible to also give a custom cursor through the
        cursor_class parameter, but it needs to be a subclass of
        mysql.connector.cursor_cext.CMySQLCursor.

        Raises ProgrammingError when cursor_class is not a subclass of
        CMySQLCursor. Raises ValueError when cursor is not available.

        Returns instance of CMySQLCursor or subclass.

        :param buffered: Return a buffering cursor
        :param raw: Return a raw cursor
        :param prepared: Return a cursor which uses prepared statements
        :param cursor_class: Use a custom cursor class
        :param dictionary: Rows are returned as dictionary
        :return: Subclass of CMySQLCursor
        :rtype: CMySQLCursor or subclass
        """
        self.handle_unread_result(prepared)
        if not self.is_connected():
            raise OperationalError("MySQL Connection not available.")
        if read_timeout or write_timeout:
            warnings.warn(
                """The use of read_timeout after the connection has been established is unsupported
                in the C-Extension""",
                category=Warning,
            )
        if cursor_class is not None:
            if not issubclass(cursor_class, CMySQLCursor):
                raise ProgrammingError(
                    "Cursor class needs be to subclass of cursor_cext.CMySQLCursor"
                )
            return (cursor_class)(self)

        buffered = buffered or self._buffered
        raw = raw or self._raw

        cursor_type = 0
        if buffered is True:
            cursor_type |= 1
        if raw is True:
            cursor_type |= 2
        if dictionary is True:
            cursor_type |= 4
        if prepared is True:
            cursor_type |= 16

        types = {
            0: CMySQLCursor,  # 0
            1: CMySQLCursorBuffered,
            2: CMySQLCursorRaw,
            3: CMySQLCursorBufferedRaw,
            4: CMySQLCursorDict,
            5: CMySQLCursorBufferedDict,
            16: CMySQLCursorPrepared,
            20: CMySQLCursorPreparedDict,
        }
        try:
            return (types[cursor_type])(self)
        except KeyError:
            args = ("buffered", "raw", "dictionary", "prepared")
            raise ValueError(
                "Cursor not available with given criteria: "
                + ", ".join([args[i] for i in range(4) if cursor_type & (1 << i) != 0])
            ) from None

    @property
    def num_rows(self) -> int:
        """Returns number of rows of current result set"""
        if not self._cmysql.have_result_set:
            raise InterfaceError("No result set")

        return self._cmysql.num_rows()

    @property
    def warning_count(self) -> int:
        """Returns number of warnings"""
        if not self._cmysql:
            return 0

        return self._cmysql.warning_count()

    @property
    def result_set_available(self) -> bool:
        """Check if a result set is available"""
        if not self._cmysql:
            return False

        return self._cmysql.have_result_set

    @property  # type: ignore[misc]
    def unread_result(self) -> bool:
        """Check if there are unread results or rows"""
        return self.result_set_available

    @property
    def more_results(self) -> bool:
        """Check if there are more results"""
        return self._cmysql.more_results()

    def prepare_for_mysql(
        self, params: ParamsSequenceOrDictType
    ) -> Union[Sequence[bytes], Dict[bytes, bytes]]:
        """Prepare parameters for statements

        This method is use by cursors to prepared parameters found in the
        list (or tuple) params.

        Returns dict.
        """
        result: Union[List[bytes], Dict[bytes, bytes]] = []
        if isinstance(params, (list, tuple)):
            if self.converter:
                result = [
                    self.converter.quote(
                        self.converter.escape(
                            self.converter.to_mysql(value), self._sql_mode
                        )
                    )
                    for value in params
                ]
            else:
                result = self._cmysql.convert_to_mysql(*params)
        elif isinstance(params, dict):
            result = {}
            if self.converter:
                for key, value in params.items():
                    result[key.encode()] = self.converter.quote(
                        self.converter.escape(
                            self.converter.to_mysql(value), self._sql_mode
                        )
                    )
            else:
                for key, value in params.items():
                    result[key.encode()] = self._cmysql.convert_to_mysql(value)[0]
        else:
            raise ProgrammingError(
                f"Could not process parameters: {type(params).__name__}({params}),"
                " it must be of type list, tuple or dict"
            )

        return result

    def consume_results(self) -> None:
        """Consume the current result

        This method consume the result by reading (consuming) all rows.
        """
        self._cmysql.consume_result()

    def cmd_change_user(
        self,
        username: str = "",
        password: str = "",
        database: str = "",
        charset: Optional[int] = None,
        password1: str = "",
        password2: str = "",
        password3: str = "",
        oci_config_file: Optional[str] = None,
        oci_config_profile: Optional[str] = None,
        openid_token_file: Optional[str] = None,
    ) -> None:
        """Change the current logged in user"""
        try:
            self._cmysql.change_user(
                username,
                password,
                database,
                password1,
                password2,
                password3,
                oci_config_file,
                oci_config_profile,
                openid_token_file,
            )

        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        # If charset isn't defined, we use the same charset ID defined previously,
        # otherwise, we run a verification and update the charset ID.
        if charset is not None:
            if not isinstance(charset, int):
                raise ValueError("charset must be an integer")
            if charset < 0:
                raise ValueError("charset should be either zero or a postive integer")
            self._charset_id = charset
        self._user = username  # updating user accordingly
        self._post_connection()

    def cmd_reset_connection(self) -> bool:
        """Resets the session state without re-authenticating

        Reset command only works on MySQL server 5.7.3 or later.
        The result is True for a successful reset otherwise False.

        Returns bool
        """
        res = self._cmysql.reset_connection()
        if res:
            self._post_connection()
        return res

    @cmd_refresh_verify_options()
    def cmd_refresh(self, options: int) -> Optional[CextEofPacketType]:
        try:
            self.handle_unread_result()
            self._cmysql.refresh(options)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        return self.fetch_eof_status()

    def cmd_quit(self) -> None:
        """Close the current connection with the server"""
        self.close()

    def cmd_shutdown(self, shutdown_type: Optional[int] = None) -> None:
        """Shut down the MySQL Server

        This method sends the SHUTDOWN command to the MySQL server.
        The `shutdown_type` is not used, and it's kept for backward compatibility.
        """
        if not self._cmysql:
            raise OperationalError("MySQL Connection not available")

        if shutdown_type:
            if not ShutdownType.get_info(shutdown_type):
                raise InterfaceError("Invalid shutdown type")
            level = shutdown_type
        else:
            level = ShutdownType.SHUTDOWN_DEFAULT

        try:
            self._cmysql.shutdown(level)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err
        self.close()

    def cmd_statistics(self) -> StatsPacketType:
        """Return statistics from the MySQL server"""
        self.handle_unread_result()

        try:
            stat = self._cmysql.stat()
            return MySQLProtocol().parse_statistics(stat, with_header=False)
        except (MySQLInterfaceError, InterfaceError) as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    def cmd_process_kill(self, mysql_pid: int) -> None:
        """Kill a MySQL process"""
        if not isinstance(mysql_pid, int):
            raise ValueError("MySQL PID must be int")
        self.cmd_query(f"KILL {mysql_pid}")

    def cmd_debug(self) -> NoReturn:
        """Send the DEBUG command"""
        raise NotImplementedError

    def cmd_ping(self) -> NoReturn:
        """Send the PING command"""
        raise NotImplementedError

    def cmd_query_iter(self, statements: str, **kwargs: Any) -> NoReturn:
        """Send one or more statements to the MySQL server"""
        raise NotImplementedError

    def cmd_stmt_send_long_data(
        self,
        statement_id: CMySQLPrepStmt,  # type: ignore[override]
        param_id: int,
        data: BinaryIO,
        **kwargs: Any,
    ) -> NoReturn:
        """Send data for a column"""
        raise NotImplementedError

    def handle_unread_result(self, prepared: bool = False) -> None:
        """Check whether there is an unread result"""
        unread_result = self._unread_result if prepared is True else self.unread_result
        if self.can_consume_results:
            self.consume_results()
        elif unread_result:
            raise InternalError("Unread result found")

    def reset_session(
        self,
        user_variables: Optional[Dict[str, Any]] = None,
        session_variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Clears the current active session

        This method resets the session state, if the MySQL server is 5.7.3
        or later active session will be reset without re-authenticating.
        For other server versions session will be reset by re-authenticating.

        It is possible to provide a sequence of variables and their values to
        be set after clearing the session. This is possible for both user
        defined variables and session variables.
        This method takes two arguments user_variables and session_variables
        which are dictionaries.

        Raises OperationalError if not connected, InternalError if there are
        unread results and InterfaceError on errors.
        """
        if not self.is_connected():
            raise OperationalError("MySQL Connection not available.")

        if not self.cmd_reset_connection():
            try:
                self.cmd_change_user(
                    self._user,
                    self._password,
                    self._database,
                    self._charset_id,
                    self._password1,
                    self._password2,
                    self._password3,
                    self._oci_config_file,
                    self._oci_config_profile,
                )
            except ProgrammingError:
                self.reconnect()

        if user_variables or session_variables:
            cur = self.cursor()
            if user_variables:
                for key, value in user_variables.items():
                    cur.execute(f"SET @`{key}` = %s", (value,))
            if session_variables:
                for key, value in session_variables.items():
                    cur.execute(f"SET SESSION `{key}` = %s", (value,))
            cur.close()
