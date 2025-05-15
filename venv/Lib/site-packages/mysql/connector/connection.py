# Copyright (c) 2009, 2025, Oracle and/or its affiliates.
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

# mypy: disable-error-code="arg-type,operator,attr-defined,assignment"

"""Implementing communication with MySQL servers."""
from __future__ import annotations

import datetime
import getpass
import os
import socket
import struct
import sys
import warnings

from decimal import Decimal
from io import IOBase
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    Generator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from . import version
from ._decorating import cmd_refresh_verify_options, handle_read_write_timeout
from ._scripting import get_local_infile_filenames
from .abstracts import MySQLConnectionAbstract
from .authentication import MySQLAuthenticator, get_auth_plugin
from .constants import (
    ClientFlag,
    FieldType,
    RefreshOption,
    ServerCmd,
    ServerFlag,
    flag_is_set,
)
from .conversion import MySQLConverter
from .cursor import (
    MySQLCursor,
    MySQLCursorBuffered,
    MySQLCursorBufferedDict,
    MySQLCursorBufferedRaw,
    MySQLCursorDict,
    MySQLCursorPrepared,
    MySQLCursorPreparedDict,
    MySQLCursorRaw,
)
from .errors import (
    ConnectionTimeoutError,
    DatabaseError,
    Error,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    ReadTimeoutError,
    WriteTimeoutError,
    get_exception,
)
from .logger import logger
from .network import MySQLSocket, MySQLTCPSocket, MySQLUnixSocket
from .opentelemetry.constants import OTEL_ENABLED
from .opentelemetry.context_propagation import with_context_propagation
from .protocol import (
    EOF_STATUS,
    ERR_STATUS,
    LOCAL_INFILE_STATUS,
    OK_STATUS,
    MySQLProtocol,
)
from .types import (
    BinaryProtocolType,
    DescriptionType,
    EofPacketType,
    HandShakeType,
    OkPacketType,
    ResultType,
    RowType,
    StatsPacketType,
    StrOrBytes,
)
from .utils import (
    get_platform,
    int1store,
    int4store,
    lc_int,
    warn_ciphersuites_deprecated,
    warn_tls_version_deprecated,
)

if TYPE_CHECKING:
    from .abstracts import CMySQLPrepStmt

if OTEL_ENABLED:
    from .opentelemetry.instrumentation import end_span, record_exception_event


class MySQLConnection(MySQLConnectionAbstract):
    """Connection to a MySQL Server"""

    def __init__(self, **kwargs: Any) -> None:
        self._protocol: Optional[MySQLProtocol] = None
        self._socket: Optional[MySQLSocket] = None
        self._handshake: Optional[HandShakeType] = None
        super().__init__()

        self._converter_class: Type[MySQLConverter] = MySQLConverter

        self._client_flags: int = ClientFlag.get_default()
        self._sql_mode: Optional[str] = None
        self._time_zone: Optional[str] = None
        self._autocommit: bool = False

        self._user: str = ""
        self._password: str = ""
        self._database: str = ""
        self._host: str = "127.0.0.1"
        self._port: int = 3306
        self._unix_socket: Optional[str] = None
        self._client_host: str = ""
        self._client_port: int = 0
        self._ssl: Dict[str, Optional[Union[str, bool, List[str]]]] = {}
        self._force_ipv6: bool = False

        self._use_unicode: bool = True
        self._get_warnings: bool = False
        self._raise_on_warnings: bool = False
        self._buffered: bool = False
        self._unread_result: bool = False
        self._have_next_result: bool = False
        self._raw: bool = False
        self._in_transaction: bool = False

        self._prepared_statements: Any = None

        self._ssl_active: bool = False
        self._auth_plugin: Optional[str] = None
        self._krb_service_principal: Optional[str] = None
        self._pool_config_version: Any = None
        self._query_attrs_supported: int = False

        self._columns_desc: List[DescriptionType] = []
        self._mfa_nfactor: int = 1

        self._authenticator: MySQLAuthenticator = MySQLAuthenticator()

        if kwargs:
            try:
                self.connect(**kwargs)
            except Exception:
                # Tidy-up underlying socket on failure
                self.close()
                self._socket = None
                raise

    def _add_default_conn_attrs(self) -> None:
        """Add the default connection attributes."""
        platform = get_platform()
        license_chunks = version.LICENSE.split(" ")
        if license_chunks[0] == "GPLv2":
            client_license = "GPL-2.0"
        else:
            client_license = "Commercial"
        default_conn_attrs = {
            "_pid": str(os.getpid()),
            "_platform": platform["arch"],
            "_source_host": socket.gethostname(),
            "_client_name": "mysql-connector-python",
            "_client_license": client_license,
            "_client_version": ".".join([str(x) for x in version.VERSION[0:3]]),
            "_os": platform["version"],
        }

        self._conn_attrs.update((default_conn_attrs))

    def _do_handshake(self) -> None:
        """Get the handshake from the MySQL server"""
        packet = bytes(self._socket.recv())
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)

        self._handshake = None
        handshake = self._protocol.parse_handshake(packet)

        server_version = handshake["server_version_original"]

        self._server_version = self._check_server_version(
            server_version
            if isinstance(server_version, (str, bytes, bytearray))
            else "Unknown"
        )
        self._character_set.set_mysql_version(self._server_version)

        if not handshake["capabilities"] & ClientFlag.SSL:
            if not self.is_secure:
                if self._auth_plugin == "mysql_clear_password":
                    raise InterfaceError(
                        "Clear password authentication is not supported over "
                        "insecure channels"
                    )
                if self._auth_plugin == "authentication_openid_connect_client":
                    raise InterfaceError(
                        "OpenID Connect authentication is not supported over "
                        "insecure channels"
                    )
            if self._ssl.get("verify_cert"):
                raise InterfaceError(
                    "SSL is required but the server doesn't support it",
                    errno=2026,
                )
            self._client_flags &= ~ClientFlag.SSL
        elif not self._ssl_disabled:
            self._client_flags |= ClientFlag.SSL

        if handshake["capabilities"] & ClientFlag.PLUGIN_AUTH:
            self.client_flags = [ClientFlag.PLUGIN_AUTH]

        if handshake["capabilities"] & ClientFlag.CLIENT_QUERY_ATTRIBUTES:
            self._query_attrs_supported = True
            self.client_flags = [ClientFlag.CLIENT_QUERY_ATTRIBUTES]

        if handshake["capabilities"] & ClientFlag.MULTI_FACTOR_AUTHENTICATION:
            self.client_flags = [ClientFlag.MULTI_FACTOR_AUTHENTICATION]

        self._handshake = handshake

    def _do_auth(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        client_flags: int = 0,
        ssl_options: Optional[Dict[str, Optional[Union[str, bool, List[str]]]]] = None,
        conn_attrs: Optional[Dict[str, str]] = None,
    ) -> bool:
        """Authenticate with the MySQL server

        Authentication happens in two parts. We first send a response to the
        handshake. The MySQL server will then send either an AuthSwitchRequest
        or an error packet.

        Raises NotSupportedError when we get the old, insecure password
        reply back. Raises any error coming from MySQL.
        """
        if (
            self._auth_plugin.startswith("authentication_oci")
            or (
                self._auth_plugin.startswith("authentication_kerberos")
                and os.name == "nt"
            )
        ) and not username:
            username = getpass.getuser()
            logger.debug(
                "MySQL user is empty, OS user: %s will be used for %s",
                username,
                self._auth_plugin,
            )

        if self._password1 and password != self._password1:
            password = self._password1

        self._ssl_active = False
        if not self._ssl_disabled and (client_flags & ClientFlag.SSL):
            self._authenticator.setup_ssl(
                self._socket,
                self.server_host,
                ssl_options,
                charset=self._charset_id,
                client_flags=client_flags,
            )
            self._ssl_active = True

        # Add the custom configurations required by specific auth plugins
        self._authenticator.update_plugin_config(
            config={
                "krb_service_principal": self._krb_service_principal,
                "oci_config_file": self._oci_config_file,
                "oci_config_profile": self._oci_config_profile,
                "webauthn_callback": self._webauthn_callback,
                "openid_token_file": self._openid_token_file,
            }
        )

        ok_pkt = self._authenticator.authenticate(
            sock=self._socket,
            handshake=self._handshake,
            username=username,
            password1=password,
            password2=self._password2,
            password3=self._password3,
            database=database,
            charset=self._charset_id,
            client_flags=client_flags,
            auth_plugin=self._auth_plugin,
            auth_plugin_class=self._auth_plugin_class,
            conn_attrs=conn_attrs,
        )
        self._handle_ok(ok_pkt)

        if not (client_flags & ClientFlag.CONNECT_WITH_DB) and database:
            self.cmd_init_db(database)

        return True

    def _get_connection(self) -> MySQLSocket:
        """Get connection based on configuration

        This method will return the appropriated connection object using
        the connection parameters.

        Returns subclass of MySQLBaseSocket.
        """
        conn = None
        if self._unix_socket and os.name == "posix":
            conn = MySQLUnixSocket(unix_socket=self.unix_socket)
        else:
            conn = MySQLTCPSocket(
                host=self.server_host,
                port=self.server_port,
                force_ipv6=self._force_ipv6,
            )

        conn.set_connection_timeout(self._connection_timeout)
        return conn

    def _open_connection(self) -> None:
        """Open the connection to the MySQL server

        This method sets up and opens the connection to the MySQL server.

        Raises on errors.
        """
        # setting connection's read and write timeout to None temporarily
        # till connections is established successfully.
        stored_read_timeout = self.read_timeout
        stored_write_timeout = self.write_timeout
        self.read_timeout = self.write_timeout = None

        if self._auth_plugin == "authentication_kerberos_client" and not self._user:
            cls = get_auth_plugin(self._auth_plugin, self._auth_plugin_class)
            self._user = cls.get_user_from_credentials()

        self._protocol = MySQLProtocol()
        self._socket = self._get_connection()
        try:
            self._socket.open_connection()

            # do initial handshake
            self._do_handshake()

            # start authentication negotiation
            self._do_auth(
                self._user,
                self._password,
                self._database,
                self._client_flags,
                self._ssl,
                self._conn_attrs,
            )
            self.converter_class = self._converter_class

            if self._client_flags & ClientFlag.COMPRESS:
                # update the network layer accordingly
                self._socket.switch_to_compressed_mode()

            self._socket.set_connection_timeout(None)
        except Exception as err:
            # close socket
            self._socket.close_connection()
            if isinstance(err, (ReadTimeoutError, WriteTimeoutError)):
                raise ConnectionTimeoutError(
                    errno=err.errno,
                    msg=err.msg,
                ) from err
            raise err
        finally:
            # as the connection is established, set back the read
            # and write timeouts to the original value
            self.read_timeout = stored_read_timeout
            self.write_timeout = stored_write_timeout

        if (
            not self._ssl_disabled
            and hasattr(self._socket.sock, "cipher")
            and callable(self._socket.sock.cipher)
        ):
            # Raise a deprecation warning if deprecated TLS version
            # or cipher is being used.

            # `cipher()` returns a three-value tuple containing the name
            # of the cipher being used, the version of the SSL protocol
            # that defines its use, and the number of secret bits being used.
            cipher, tls_version, _ = self._socket.sock.cipher()
            warn_tls_version_deprecated(tls_version)
            warn_ciphersuites_deprecated(cipher, tls_version)

    def shutdown(self) -> None:
        """Shut down connection to MySQL Server.

        This method closes the socket. It raises no exceptions.

        Unlike `disconnect()`, `shutdown()` closes the client connection without
        attempting to send a QUIT command to the server first. Thus, it will not
        block if the connection is disrupted for some reason such as network failure.
        """
        if not self._socket:
            return

        try:
            self._socket.shutdown()
        except (AttributeError, Error):
            pass  # Getting an exception would mean we are disconnected.

    def close(self) -> None:
        if self._span and self._span.is_recording():
            # pylint: disable=possibly-used-before-assignment
            record_exception_event(self._span, sys.exc_info()[1])

        if not self._socket:
            return

        try:
            self.cmd_quit()
        except (AttributeError, Error):
            pass  # Getting an exception would mean we are disconnected.

        try:
            self._socket.close_connection()
        except Exception as err:
            if OTEL_ENABLED:
                record_exception_event(self._span, err)
            raise
        finally:
            if OTEL_ENABLED:
                end_span(self._span)

        self._handshake = None

    disconnect = close

    @handle_read_write_timeout()
    def _send_cmd(
        self,
        command: int,
        argument: Optional[bytes] = None,
        packet_number: int = 0,
        packet: Optional[bytes] = None,
        expect_response: bool = True,
        compressed_packet_number: int = 0,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> Optional[bytearray]:
        """Send a command to the MySQL server

        This method sends a command with an optional argument.
        If packet is not None, it will be sent and the argument will be
        ignored.

        The packet_number is optional and should usually not be used.

        Some commands might not result in the MySQL server returning
        a response. If a command does not return anything, you should
        set expect_response to False. The _send_cmd method will then
        return None instead of a MySQL packet.

        Returns a MySQL packet or None.
        """
        self.handle_unread_result()

        try:
            self._socket.send(
                self._protocol.make_command(command, packet or argument),
                packet_number,
                compressed_packet_number,
                write_timeout or self._write_timeout,
            )
            return (
                self._socket.recv(read_timeout or self._read_timeout)
                if expect_response
                else None
            )
        except AttributeError as err:
            raise OperationalError("MySQL Connection not available") from err

    @handle_read_write_timeout()
    def _send_data(
        self,
        data_file: BinaryIO,
        send_empty_packet: bool = False,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> bytearray:
        """Send data to the MySQL server

        This method accepts a file-like object and sends its data
        as is to the MySQL server. If the send_empty_packet is
        True, it will send an extra empty package (for example
        when using LOAD LOCAL DATA INFILE).

        Returns a MySQL packet.
        """
        self.handle_unread_result()

        if not hasattr(data_file, "read"):
            raise ValueError("expecting a file-like object")

        chunk_size = 131072  # 128 KB
        try:
            buf = data_file.read(chunk_size - 16)
            while buf:
                self._socket.send(
                    buf, write_timeout=write_timeout or self._write_timeout
                )
                buf = data_file.read(chunk_size - 16)
        except AttributeError as err:
            raise OperationalError("MySQL Connection not available") from err

        if send_empty_packet:
            try:
                self._socket.send(
                    b"", write_timeout=write_timeout or self._write_timeout
                )
            except WriteTimeoutError as err:
                raise err
            except AttributeError as err:
                raise OperationalError("MySQL Connection not available") from err

        return self._socket.recv(read_timeout or self._read_timeout)

    def _handle_server_status(self, flags: int) -> None:
        """Handle the server flags found in MySQL packets

        This method handles the server flags send by MySQL OK and EOF
        packets. It, for example, checks whether there exists more result
        sets or whether there is an ongoing transaction.
        """
        self._have_next_result = flag_is_set(ServerFlag.MORE_RESULTS_EXISTS, flags)
        self._in_transaction = flag_is_set(ServerFlag.STATUS_IN_TRANS, flags)

    @property
    def in_transaction(self) -> bool:
        """MySQL session has started a transaction"""
        return self._in_transaction

    def _handle_ok(self, packet: bytes) -> OkPacketType:
        """Handle a MySQL OK packet

        This method handles a MySQL OK packet. When the packet is found to
        be an Error packet, an error will be raised. If the packet is neither
        an OK or an Error packet, InterfaceError will be raised.

        Returns a dict()
        """
        if packet[4] == OK_STATUS:
            ok_pkt = self._protocol.parse_ok(packet)
            self._handle_server_status(ok_pkt["status_flag"])
            return ok_pkt
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)
        raise InterfaceError("Expected OK packet")

    def _handle_eof(self, packet: bytes) -> EofPacketType:
        """Handle a MySQL EOF packet

        This method handles a MySQL EOF packet. When the packet is found to
        be an Error packet, an error will be raised. If the packet is neither
        and OK or an Error packet, InterfaceError will be raised.

        Returns a dict()
        """
        if packet[4] == EOF_STATUS:
            eof = self._protocol.parse_eof(packet)
            self._handle_server_status(eof["status_flag"])
            return eof
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)
        raise InterfaceError("Expected EOF packet")

    @handle_read_write_timeout()
    def _handle_load_data_infile(
        self,
        filename: str,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> OkPacketType:
        """Handle a LOAD DATA INFILE LOCAL request"""
        if self._local_infile_filenames is None:
            self._local_infile_filenames = get_local_infile_filenames(self._query)
            if not self._local_infile_filenames:
                raise InterfaceError(
                    "No `LOCAL INFILE` statements found in the client's request. "
                    "Check your request includes valid `LOCAL INFILE` statements."
                )
        elif not self._local_infile_filenames:
            raise InterfaceError(
                "Got more `LOCAL INFILE` responses than number of `LOCAL INFILE` "
                "statements specified in the client's request. Please, report this "
                "issue to the development team."
            )

        file_name = os.path.abspath(filename)
        file_name_from_request = os.path.abspath(self._local_infile_filenames.popleft())

        # Verify the file location specified by `filename` from client's request exists
        if not os.path.exists(file_name_from_request):
            raise InterfaceError(
                f"Location specified by filename {file_name_from_request} "
                "from client's request does not exist."
            )

        # Verify the file location specified by `filename` from server's response exists
        if not os.path.exists(file_name):
            raise InterfaceError(
                f"Location specified by filename {file_name} from server's "
                "response does not exist."
            )

        # Verify the `filename` specified by server's response matches the one from
        # the client's request.
        try:
            if not os.path.samefile(file_name, file_name_from_request):
                raise InterfaceError(
                    f"Filename {file_name} from the server's response is not the same "
                    f"as filename {file_name_from_request} from the "
                    "client's request."
                )
        except OSError as err:
            raise InterfaceError from err

        if os.path.islink(file_name):
            raise OperationalError("Use of symbolic link is not allowed")
        if not self._allow_local_infile and not self._allow_local_infile_in_path:
            raise DatabaseError(
                "LOAD DATA LOCAL INFILE file request rejected due to "
                "restrictions on access."
            )
        if not self._allow_local_infile and self._allow_local_infile_in_path:
            # validate filename is inside of allow_local_infile_in_path path.
            infile_path = os.path.abspath(self._allow_local_infile_in_path)
            c_path = None
            try:
                c_path = os.path.commonpath([infile_path, file_name])
            except ValueError as err:
                err_msg = (
                    "{} while loading file `{}` and path `{}` given"
                    " in allow_local_infile_in_path"
                )
                raise InterfaceError(
                    err_msg.format(str(err), file_name, infile_path)
                ) from err

            if c_path != infile_path:
                err_msg = (
                    "The file `{}` is not found in the given "
                    "allow_local_infile_in_path {}"
                )
                raise DatabaseError(err_msg.format(file_name, infile_path))

        try:
            data_file = open(file_name, "rb")  # pylint: disable=consider-using-with
            return self._handle_ok(
                self._send_data(data_file, True, read_timeout, write_timeout)
            )
        except IOError:
            # Send a empty packet to cancel the operation
            try:
                self._socket.send(
                    b"", write_timeout=write_timeout or self._write_timeout
                )
            except AttributeError as err:
                raise OperationalError("MySQL Connection not available") from err
            raise InterfaceError(f"File '{file_name}' could not be read") from None
        finally:
            try:
                data_file.close()
            except (IOError, NameError):
                pass

    @handle_read_write_timeout()
    def _handle_result(
        self,
        packet: bytes,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> ResultType:
        """Handle a MySQL Result

        This method handles a MySQL result, for example, after sending the
        query command. OK and EOF packets will be handled and returned. If
        the packet is an Error packet, an Error-exception will be
        raised.

        The dictionary returned of:
        - columns: column information
        - eof: the EOF-packet information

        Returns a dict()
        """
        if not packet or len(packet) < 4:
            raise InterfaceError("Empty response")
        if packet[4] == OK_STATUS:
            return self._handle_ok(packet)
        if packet[4] == LOCAL_INFILE_STATUS:
            filename = packet[5:].decode()
            return self._handle_load_data_infile(filename, read_timeout, write_timeout)
        if packet[4] == EOF_STATUS:
            return self._handle_eof(packet)
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)

        # We have a text result set
        column_count = self._protocol.parse_column_count(packet)
        if not column_count or not isinstance(column_count, int):
            raise InterfaceError("Illegal result set")

        self._columns_desc = [
            None,
        ] * column_count
        for i in range(0, column_count):
            self._columns_desc[i] = self._protocol.parse_column(
                self._socket.recv(read_timeout or self._read_timeout),
                self.python_charset,
            )

        eof = self._handle_eof(self._socket.recv(read_timeout or self._read_timeout))
        self.unread_result = True
        return {"columns": self._columns_desc, "eof": eof}

    def get_row(
        self,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[RowType], Optional[EofPacketType]]:
        """Get the next rows returned by the MySQL server

        This method gets one row from the result set after sending, for
        example, the query command. The result is a tuple consisting of the
        row and the EOF packet.
        If no row was available in the result set, the row data will be None.

        Returns a tuple.
        """
        read_timeout = kwargs.get("read_timeout", None)
        (rows, eof) = self.get_rows(
            count=1,
            binary=binary,
            columns=columns,
            raw=raw,
            read_timeout=read_timeout,
        )
        if rows:
            return (rows[0], eof)
        return (None, eof)

    @handle_read_write_timeout()
    def get_rows(
        self,
        count: Optional[int] = None,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[List[RowType], Optional[EofPacketType]]:
        """Get all rows returned by the MySQL server

        This method gets all rows returned by the MySQL server after sending,
        for example, the query command. The result is a tuple consisting of
        a list of rows and the EOF packet.

        Returns a tuple()
        """
        if raw is None:
            raw = self._raw

        if not self.unread_result:
            raise InternalError("No result set available")

        rows: Tuple[List[Tuple], Optional[EofPacketType]] = ([], None)
        try:
            read_timeout = kwargs.get("read_timeout", None)
            if binary:
                charset = self.charset
                if charset == "utf8mb4":
                    charset = "utf8"
                rows = self._protocol.read_binary_result(
                    self._socket,
                    columns,
                    count,
                    charset,
                    read_timeout or self._read_timeout,
                )
            else:
                rows = self._protocol.read_text_result(
                    self._socket,
                    self._server_version,
                    count,
                    read_timeout or self._read_timeout,
                )
        except Error as err:
            self.unread_result = False
            raise err

        rows, eof_p = rows
        if (
            not (binary or raw)
            and self._columns_desc is not None
            and rows
            and hasattr(self, "converter")
        ):
            row_to_python = self.converter.row_to_python
            rows = [row_to_python(row, self._columns_desc) for row in rows]

        if eof_p is not None:
            self._handle_server_status(
                eof_p["status_flag"]
                if "status_flag" in eof_p
                else eof_p["server_status"]
            )
            self.unread_result = False

        return rows, eof_p

    def consume_results(self) -> None:
        """Consume results"""
        if self.unread_result:
            self.get_rows()

    def cmd_init_db(self, database: str) -> OkPacketType:
        """Change the current database

        This method changes the current (default) database by sending the
        INIT_DB command. The result is a dictionary containing the OK packet
        information.

        Returns a dict()
        """
        return self._handle_ok(
            self._send_cmd(ServerCmd.INIT_DB, database.encode("utf-8"))
        )

    @with_context_propagation
    @handle_read_write_timeout()
    def cmd_query(
        self,
        query: StrOrBytes,
        raw: bool = False,
        buffered: bool = False,
        raw_as_string: bool = False,
        **kwargs: Any,
    ) -> ResultType:
        if not isinstance(query, bytearray):
            if isinstance(query, str):
                query = query.encode("utf-8")
            query = bytearray(query)

        # Set/Reset internal state related to query execution
        self._query = query
        self._local_infile_filenames = None

        # Prepare query attrs
        charset = self.charset if self.charset != "utf8mb4" else "utf8"
        packet = bytearray()
        if not self._query_attrs_supported and self._query_attrs:
            warnings.warn(
                "This version of the server does not support Query Attributes",
                category=Warning,
            )
        if self._client_flags & ClientFlag.CLIENT_QUERY_ATTRIBUTES:
            names = []
            types = []
            values: List[bytes] = []
            null_bitmap = [0] * ((len(self._query_attrs) + 7) // 8)
            for pos, attr_tuple in enumerate(self._query_attrs.items()):
                value = attr_tuple[1]
                flags = 0
                if value is None:
                    null_bitmap[(pos // 8)] |= 1 << (pos % 8)
                    types.append(int1store(FieldType.NULL) + int1store(flags))
                    continue
                if isinstance(value, int):
                    (
                        packed,
                        field_type,
                        flags,
                    ) = self._protocol.prepare_binary_integer(value)
                    values.append(packed)
                elif isinstance(value, str):
                    value = value.encode(charset)
                    values.append(lc_int(len(value)) + value)
                    field_type = FieldType.STRING
                elif isinstance(value, bytes):
                    values.append(lc_int(len(value)) + value)
                    field_type = FieldType.STRING
                elif isinstance(value, Decimal):
                    values.append(
                        lc_int(len(str(value).encode(charset)))
                        + str(value).encode(charset)
                    )
                    field_type = FieldType.DECIMAL
                elif isinstance(value, float):
                    values.append(struct.pack("<d", value))
                    field_type = FieldType.DOUBLE
                elif isinstance(value, (datetime.datetime, datetime.date)):
                    (
                        packed,
                        field_type,
                    ) = self._protocol.prepare_binary_timestamp(value)
                    values.append(packed)
                elif isinstance(value, (datetime.timedelta, datetime.time)):
                    (packed, field_type) = self._protocol.prepare_binary_time(value)
                    values.append(packed)
                else:
                    raise ProgrammingError(
                        "MySQL binary protocol can not handle "
                        f"'{value.__class__.__name__}' objects"
                    )
                types.append(int1store(field_type) + int1store(flags))
                name = attr_tuple[0].encode(charset)
                names.append(lc_int(len(name)) + name)

            # int<lenenc>    parameter_count    Number of parameters
            packet.extend(lc_int(len(self._query_attrs)))
            # int<lenenc>    parameter_set_count    Number of parameter sets.
            # Currently always 1
            packet.extend(lc_int(1))
            if values:
                packet.extend(
                    b"".join([struct.pack("B", bit) for bit in null_bitmap])
                    + int1store(1)
                )
                for _type, name in zip(types, names):
                    packet.extend(_type)
                    packet.extend(name)

                for value in values:
                    packet.extend(value)

        packet.extend(query)
        query = bytes(packet)
        try:
            read_timeout = kwargs.get("read_timeout", None)
            write_timeout = kwargs.get("write_timeout", None)

            result = self._handle_result(
                self._send_cmd(
                    ServerCmd.QUERY,
                    query,
                    read_timeout=read_timeout,
                    write_timeout=write_timeout,
                ),
                read_timeout,
                write_timeout,
            )
        except ProgrammingError as err:
            if err.errno == 3948 and "Loading local data is disabled" in err.msg:
                err_msg = (
                    "LOAD DATA LOCAL INFILE file request rejected due "
                    "to restrictions on access."
                )
                raise DatabaseError(err_msg) from err
            raise
        return result

    @handle_read_write_timeout()
    def cmd_query_iter(
        self,
        statements: StrOrBytes,
        **kwargs: Any,
    ) -> Generator[ResultType, None, None]:
        """Send one or more statements to the MySQL server

        Similar to the cmd_query method, but instead returns a generator
        object to iterate through results. It sends the statements to the
        MySQL server and through the iterator you can get the results.

        statement = 'SELECT 1; INSERT INTO t1 VALUES (); SELECT 2'
        for result in cnx.cmd_query(statement, iterate=True):
            if 'columns' in result:
                columns = result['columns']
                rows = cnx.get_rows()
            else:
                # do something useful with INSERT result

        Returns a generator.
        """
        read_timeout = kwargs.get("read_timeout", None)
        write_timeout = kwargs.get("write_timeout", None)
        packet = bytearray()
        if not isinstance(statements, bytearray):
            if isinstance(statements, str):
                statements = statements.encode("utf8")
            statements = bytearray(statements)

        if self._client_flags & ClientFlag.CLIENT_QUERY_ATTRIBUTES:
            # int<lenenc>    parameter_count    Number of parameters
            packet.extend(lc_int(0))
            # int<lenenc>    parameter_set_count    Number of parameter sets.
            # Currently always 1
            packet.extend(lc_int(1))

        packet.extend(statements)
        query = bytes(packet)
        # Handle the first query result
        yield self._handle_result(
            self._send_cmd(
                ServerCmd.QUERY,
                query,
                read_timeout=read_timeout,
                write_timeout=write_timeout,
            ),
            read_timeout,
            write_timeout,
        )

        # Handle next results, if any
        while self._have_next_result:
            self.handle_unread_result()
            yield self._handle_result(
                self._socket.recv(read_timeout=read_timeout or self._read_timeout),
                read_timeout,
                write_timeout,
            )

    @cmd_refresh_verify_options()
    def cmd_refresh(self, options: int) -> OkPacketType:
        if not options & (
            RefreshOption.GRANT
            | RefreshOption.LOG
            | RefreshOption.TABLES
            | RefreshOption.HOST
            | RefreshOption.STATUS
            | RefreshOption.REPLICA
        ):
            raise ValueError("Invalid command REFRESH option")

        res = None
        if options & RefreshOption.GRANT:
            res = self.cmd_query("FLUSH PRIVILEGES")
        if options & RefreshOption.LOG:
            res = self.cmd_query("FLUSH LOGS")
        if options & RefreshOption.TABLES:
            res = self.cmd_query("FLUSH TABLES")
        if options & RefreshOption.HOST:
            res = self.cmd_query("TRUNCATE TABLE performance_schema.host_cache")
        if options & RefreshOption.STATUS:
            res = self.cmd_query("FLUSH STATUS")
        if options & RefreshOption.REPLICA:
            res = self.cmd_query(
                "RESET SLAVE" if self._server_version < (8, 0, 22) else "RESET REPLICA"
            )

        return res

    def cmd_quit(self) -> bytes:
        """Close the current connection with the server

        This method sends the `QUIT` command to the MySQL server, closing the
        current connection. Since there is no response from the MySQL server,
        the packet that was sent is returned.

        Returns a str()
        """
        self.handle_unread_result()

        packet = self._protocol.make_command(ServerCmd.QUIT)
        try:
            self._socket.send(packet, 0, 0, self._write_timeout)
        except WriteTimeoutError as _:
            pass
        return packet

    def cmd_shutdown(self, shutdown_type: Optional[int] = None) -> None:
        """Shut down the MySQL Server

        This method sends the SHUTDOWN command to the MySQL server.
        The `shutdown_type` is not used, and it's kept for backward compatibility.
        """
        self.cmd_query("SHUTDOWN")

    @handle_read_write_timeout()
    def cmd_statistics(self) -> StatsPacketType:
        """Send the statistics command to the MySQL Server

        This method sends the STATISTICS command to the MySQL server. The
        result is a dictionary with various statistical information.

        Returns a dict()
        """
        self.handle_unread_result()

        packet = self._protocol.make_command(ServerCmd.STATISTICS)
        self._socket.send(packet, 0, 0, self._write_timeout)
        return self._protocol.parse_statistics(self._socket.recv(self._read_timeout))

    def cmd_process_kill(self, mysql_pid: int) -> OkPacketType:
        """Kill a MySQL process

        This method send the PROCESS_KILL command to the server along with
        the process ID. The result is a dictionary with the OK packet
        information.
        """
        if not isinstance(mysql_pid, int):
            raise ValueError("MySQL PID must be int")
        return self.cmd_query(f"KILL {mysql_pid}")

    def cmd_debug(self) -> EofPacketType:
        """Send the DEBUG command

        This method sends the DEBUG command to the MySQL server, which
        requires the MySQL user to have SUPER privilege. The output will go
        to the MySQL server error log and the result of this method is a
        dictionary with EOF packet information.

        Returns a dict()
        """
        return self._handle_eof(self._send_cmd(ServerCmd.DEBUG))

    def cmd_ping(self) -> OkPacketType:
        """Send the PING command

        This method sends the PING command to the MySQL server. It is used to
        check if the the connection is still valid. The result of this
        method is dictionary with OK packet information.

        Returns a dict()
        """
        return self._handle_ok(self._send_cmd(ServerCmd.PING))

    @handle_read_write_timeout()
    def cmd_change_user(
        self,
        username: str = "",
        password: str = "",
        database: str = "",
        charset: Optional[int] = None,
        password1: str = "",
        password2: str = "",
        password3: str = "",
        oci_config_file: str = "",
        oci_config_profile: str = "",
        openid_token_file: str = "",
    ) -> Optional[OkPacketType]:
        """Change the current logged in user

        This method allows to change the current logged in user information.
        The result is a dictionary with OK packet information.

        Returns a dict()
        """
        # If charset isn't defined, we use the same charset ID defined previously,
        # otherwise, we run a verification and update the charset ID.
        if charset is not None:
            if not isinstance(charset, int):
                raise ValueError("charset must be an integer")
            if charset < 0:
                raise ValueError("charset should be either zero or a postive integer")
            self._charset_id = charset

        self._mfa_nfactor = 1
        self._user = username
        self._password = password
        self._password1 = password1
        self._password2 = password2
        self._password3 = password3

        if self._password1 and password != self._password1:
            self._password = self._password1

        self.handle_unread_result()

        if self._compress:
            raise NotSupportedError("Change user is not supported with compression")

        if oci_config_file:
            self._oci_config_file = oci_config_file
        if openid_token_file:
            self._openid_token_file = openid_token_file
        self._oci_config_profile = oci_config_profile

        # Update the custom configurations needed by specific auth plugins
        self._authenticator.update_plugin_config(
            config={
                "oci_config_file": self._oci_config_file,
                "oci_config_profile": self._oci_config_profile,
                "openid_token_file": self._openid_token_file,
            }
        )

        ok_pkt = self._authenticator.authenticate(
            sock=self._socket,
            handshake=self._handshake,
            username=self._user,
            password1=self._password,
            password2=self._password2,
            password3=self._password3,
            database=database,
            charset=self._charset_id,
            client_flags=self._client_flags,
            auth_plugin=self._auth_plugin,
            auth_plugin_class=self._auth_plugin_class,
            conn_attrs=self._conn_attrs,
            is_change_user_request=True,
            read_timeout=self._read_timeout,
            write_timeout=self._write_timeout,
        )

        if not (self._client_flags & ClientFlag.CONNECT_WITH_DB) and database:
            self.cmd_init_db(database)

        self._post_connection()

        # return ok_pkt
        return self._handle_ok(ok_pkt)

    @property
    def database(self) -> str:
        """Get the current database"""
        return self.info_query("SELECT DATABASE()")[0]  # type: ignore[return-value]

    @database.setter
    def database(self, value: str) -> None:
        """Set the current database"""
        self.cmd_init_db(value)

    def is_connected(self) -> bool:
        """Reports whether the connection to MySQL Server is available

        This method checks whether the connection to MySQL is available.
        It is similar to ping(), but unlike the ping()-method, either True
        or False is returned and no exception is raised.

        Returns True or False.
        """
        try:
            self.cmd_ping()
        except Error:
            return False  # This method does not raise
        return True

    def set_allow_local_infile_in_path(self, path: str) -> None:
        """Set the path that user can upload files.

        Args:
            path (str): Path that user can upload files.
        """
        self._allow_local_infile_in_path = path

    @MySQLConnectionAbstract.use_unicode.setter  # type: ignore
    def use_unicode(self, value: bool) -> None:
        self._use_unicode = value
        if self.converter:
            self.converter.set_unicode(value)

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
                    self._openid_token_file,
                )
            except ProgrammingError:
                self.reconnect()

        cur = self.cursor()
        if user_variables:
            for key, value in user_variables.items():
                cur.execute(f"SET @`{key}` = %s", (value,))
        if session_variables:
            for key, value in session_variables.items():
                cur.execute(f"SET SESSION `{key}` = %s", (value,))

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
        try:
            self.cmd_ping()
        except Error as err:
            if reconnect:
                self.reconnect(attempts=attempts, delay=delay)
            else:
                raise InterfaceError("Connection to MySQL is not available") from err

    @property
    def connection_id(self) -> Optional[int]:
        """MySQL connection ID"""
        if self._handshake:
            return self._handshake.get("server_threadid")  # type: ignore[return-value]
        return None

    def cursor(
        self,
        buffered: Optional[bool] = None,
        raw: Optional[bool] = None,
        prepared: Optional[bool] = None,
        cursor_class: Optional[Type[MySQLCursor]] = None,  # type: ignore[override]
        dictionary: Optional[bool] = None,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> MySQLCursor:
        """Instantiates and returns a cursor

        By default, MySQLCursor is returned. Depending on the options
        while connecting, a buffered and/or raw cursor is instantiated
        instead. Also depending upon the cursor options, rows can be
        returned as a dictionary or a tuple.

        Dictionary based cursors are available with buffered
        output but not raw.

        It is possible to also give a custom cursor through the
        cursor_class parameter, but it needs to be a subclass of
        mysql.connector.cursor.MySQLCursor.

        Raises ProgrammingError when cursor_class is not a subclass of
        MySQLCursor. Raises ValueError when cursor is not available.
        Raises InterfaceError when read_timeout or write_timeout is not
        a positive integer.

        Returns a cursor-object
        """
        self.handle_unread_result()

        if not self.is_connected():
            raise OperationalError("MySQL Connection not available")
        if read_timeout is not None and (
            not isinstance(read_timeout, int) or read_timeout < 0
        ):
            raise InterfaceError("Option read_timeout must be a positive integer")
        if write_timeout is not None and (
            not isinstance(write_timeout, int) or write_timeout < 0
        ):
            raise InterfaceError("Option write_timeout must be a positive integer")
        if cursor_class is not None:
            if not issubclass(cursor_class, MySQLCursor):
                raise ProgrammingError(
                    "Cursor class needs be to subclass of MySQLCursor"
                )
            return (cursor_class)(self, read_timeout, write_timeout)

        buffered = buffered if buffered is not None else self._buffered
        raw = raw if raw is not None else self._raw

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
            0: MySQLCursor,  # 0
            1: MySQLCursorBuffered,
            2: MySQLCursorRaw,
            3: MySQLCursorBufferedRaw,
            4: MySQLCursorDict,
            5: MySQLCursorBufferedDict,
            16: MySQLCursorPrepared,
            20: MySQLCursorPreparedDict,
        }
        try:
            return (types[cursor_type])(self, read_timeout, write_timeout)
        except KeyError:
            args = ("buffered", "raw", "dictionary", "prepared")
            raise ValueError(
                "Cursor not available with given criteria: "
                + ", ".join([args[i] for i in range(4) if cursor_type & (1 << i) != 0])
            ) from None

    def commit(self) -> None:
        """Commit current transaction"""
        self._execute_query("COMMIT")

    def rollback(self) -> None:
        """Rollback current transaction"""
        if self.unread_result:
            self.get_rows()

        self._execute_query("ROLLBACK")

    def _execute_query(self, query: str) -> None:
        """Execute a query

        This method simply calls cmd_query() after checking for unread
        result. If there are still unread result, an InterfaceError
        is raised. Otherwise whatever cmd_query() returns is returned.

        Returns a dict()
        """
        self.handle_unread_result()
        self.cmd_query(query)

    def info_query(self, query: str) -> Optional[RowType]:
        """Send a query which only returns 1 row"""
        cursor = self.cursor(
            buffered=True,
            read_timeout=self._read_timeout,
            write_timeout=self._write_timeout,
        )
        cursor.execute(query)
        return cursor.fetchone()

    def _handle_binary_ok(self, packet: bytes) -> Dict[str, int]:
        """Handle a MySQL Binary Protocol OK packet

        This method handles a MySQL Binary Protocol OK packet. When the
        packet is found to be an Error packet, an error will be raised. If
        the packet is neither an OK or an Error packet, InterfaceError
        will be raised.

        Returns a dict()
        """
        if packet[4] == OK_STATUS:
            return self._protocol.parse_binary_prepare_ok(packet)
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)
        raise InterfaceError("Expected Binary OK packet")

    @handle_read_write_timeout()
    def _handle_binary_result(
        self, packet: bytes, read_timeout: Optional[int] = None
    ) -> Union[OkPacketType, Tuple[int, List[DescriptionType], EofPacketType]]:
        """Handle a MySQL Result

        This method handles a MySQL result, for example, after sending the
        query command. OK and EOF packets will be handled and returned. If
        the packet is an Error packet, an Error exception will be raised.

        The tuple returned by this method consist of:
        - the number of columns in the result,
        - a list of tuples with information about the columns,
        - the EOF packet information as a dictionary.

        Returns tuple() or dict()
        """
        if not packet or len(packet) < 4:
            raise InterfaceError("Empty response")
        if packet[4] == OK_STATUS:
            return self._handle_ok(packet)
        if packet[4] == EOF_STATUS:
            return self._handle_eof(packet)
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)

        # We have a binary result set
        column_count = self._protocol.parse_column_count(packet)
        if not column_count or not isinstance(column_count, int):
            raise InterfaceError("Illegal result set.")

        columns: List[DescriptionType] = [None] * column_count
        for i in range(0, column_count):
            columns[i] = self._protocol.parse_column(
                self._socket.recv(read_timeout or self._read_timeout),
                self.python_charset,
            )

        eof = self._handle_eof(self._socket.recv(read_timeout or self._read_timeout))
        return (column_count, columns, eof)

    def cmd_stmt_fetch(
        self,
        statement_id: int,
        rows: int = 1,
        **kwargs: Any,
    ) -> None:
        """Fetch a MySQL statement Result Set

        This method will send the FETCH command to MySQL together with the
        given statement id and the number of rows to fetch.
        """
        read_timeout = kwargs.get("read_timeout", None)
        write_timeout = kwargs.get("write_timeout", None)
        packet = self._protocol.make_stmt_fetch(statement_id, rows)
        self.unread_result = False
        self._send_cmd(
            ServerCmd.STMT_FETCH,
            packet,
            expect_response=False,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
        )
        self.unread_result = True

    @handle_read_write_timeout()
    def cmd_stmt_prepare(
        self,
        statement: bytes,
        **kwargs: Any,
    ) -> Mapping[str, Union[int, List[DescriptionType]]]:
        """Prepare a MySQL statement

        This method will send the PREPARE command to MySQL together with the
        given statement.

        Returns a dict()
        """
        read_timeout = kwargs.get("read_timeout", None)
        write_timeout = kwargs.get("write_timeout", None)

        packet = self._send_cmd(
            ServerCmd.STMT_PREPARE,
            statement,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
        )
        result = self._handle_binary_ok(packet)

        result["columns"] = []
        result["parameters"] = []
        if result["num_params"] > 0:
            for _ in range(0, result["num_params"]):
                result["parameters"].append(
                    self._protocol.parse_column(
                        self._socket.recv(read_timeout or self._read_timeout),
                        self.python_charset,
                    )
                )
            self._handle_eof(self._socket.recv(read_timeout or self._read_timeout))
        if result["num_columns"] > 0:
            for _ in range(0, result["num_columns"]):
                result["columns"].append(
                    self._protocol.parse_column(
                        self._socket.recv(read_timeout or self._read_timeout),
                        self.python_charset,
                    )
                )
            self._handle_eof(self._socket.recv(read_timeout or self._read_timeout))
        return result

    @with_context_propagation
    def cmd_stmt_execute(
        self,
        statement_id: int,
        data: Sequence[BinaryProtocolType] = (),
        parameters: Sequence = (),
        flags: int = 0,
        **kwargs: Any,
    ) -> Union[OkPacketType, Tuple[int, List[DescriptionType], EofPacketType]]:
        """Execute a prepared MySQL statement"""
        parameters = list(parameters)
        long_data_used = {}
        read_timeout = kwargs.get("read_timeout", None)
        write_timeout = kwargs.get("write_timeout", None)

        if data:
            for param_id, _ in enumerate(parameters):
                if isinstance(data[param_id], IOBase):
                    binary = True
                    try:
                        binary = "b" not in data[param_id].mode  # type: ignore[union-attr]
                    except AttributeError:
                        pass
                    self.cmd_stmt_send_long_data(
                        statement_id,
                        param_id,
                        data[param_id],
                        read_timeout=read_timeout,
                        write_timeout=write_timeout,
                    )
                    long_data_used[param_id] = (binary,)
        if not self._query_attrs_supported and self._query_attrs:
            warnings.warn(
                "This version of the server does not support Query Attributes",
                category=Warning,
            )
        if self._client_flags & ClientFlag.CLIENT_QUERY_ATTRIBUTES:
            execute_packet = self._protocol.make_stmt_execute(
                statement_id,
                data,
                tuple(parameters),
                flags,
                long_data_used,
                self.charset,
                self.query_attrs,
                self._converter_str_fallback,
            )
        else:
            execute_packet = self._protocol.make_stmt_execute(
                statement_id,
                data,
                tuple(parameters),
                flags,
                long_data_used,
                self.charset,
                converter_str_fallback=self._converter_str_fallback,
            )
        packet = self._send_cmd(
            ServerCmd.STMT_EXECUTE,
            packet=execute_packet,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
        )
        result = self._handle_binary_result(packet, read_timeout)
        return result

    def cmd_stmt_close(
        self,
        statement_id: int,  # type: ignore[override]
        **kwargs: Any,
    ) -> None:
        """Deallocate a prepared MySQL statement

        This method deallocates the prepared statement using the
        statement_id. Note that the MySQL server does not return
        anything.
        """
        self._send_cmd(
            ServerCmd.STMT_CLOSE,
            int4store(statement_id),
            expect_response=False,
            read_timeout=kwargs.get("read_timeout", None),
            write_timeout=kwargs.get("write_timeout", None),
        )

    def cmd_stmt_send_long_data(
        self,
        statement_id: int,  # type: ignore[override]
        param_id: int,
        data: BinaryIO,
        **kwargs: Any,
    ) -> int:
        """Send data for a column

        This methods send data for a column (for example BLOB) for statement
        identified by statement_id. The param_id indicate which parameter
        the data belongs too.
        The data argument should be a file-like object.

        Since MySQL does not send anything back, no error is raised. When
        the MySQL server is not reachable, an OperationalError is raised.

        cmd_stmt_send_long_data should be called before cmd_stmt_execute.

        The total bytes send is returned.

        Returns int.
        """
        chunk_size = 131072  # 128 KB
        total_sent = 0
        try:
            buf = data.read(chunk_size)
            while buf:
                packet = self._protocol.prepare_stmt_send_long_data(
                    statement_id, param_id, buf
                )
                self._send_cmd(
                    ServerCmd.STMT_SEND_LONG_DATA,
                    packet=packet,
                    expect_response=False,
                    read_timeout=kwargs.get("read_timeout", None),
                    write_timeout=kwargs.get("write_timeout", None),
                )
                total_sent += len(buf)
                buf = data.read(chunk_size)
        except AttributeError as err:
            raise OperationalError("MySQL Connection not available") from err

        return total_sent

    def cmd_stmt_reset(
        self,
        statement_id: int,  # type: ignore[override]
        **kwargs: Any,
    ) -> None:
        """Reset data for prepared statement sent as long data

        The result is a dictionary with OK packet information.

        Returns a dict()
        """
        self._handle_ok(
            self._send_cmd(
                ServerCmd.STMT_RESET,
                int4store(statement_id),
                read_timeout=kwargs.get("read_timeout", None),
                write_timeout=kwargs.get("write_timeout", None),
            )
        )

    def cmd_reset_connection(self) -> bool:
        """Resets the session state without re-authenticating

        Reset command only works on MySQL server 5.7.3 or later.
        The result is True for a successful reset otherwise False.

        Returns bool
        """
        try:
            self._handle_ok(self._send_cmd(ServerCmd.RESET_CONNECTION))
            self._post_connection()
            return True
        except (NotSupportedError, OperationalError):
            return False

    def handle_unread_result(self) -> None:
        """Check whether there is an unread result"""
        if self.can_consume_results:
            self.consume_results()
        elif self.unread_result:
            raise InternalError("Unread result found")
