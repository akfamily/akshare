# Copyright (c) 2023, 2025, Oracle and/or its affiliates.
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

"""Implemention of the communication with MySQL servers in pure Python."""

__all__ = ["MySQLConnection"]

import asyncio
import contextlib
import datetime
import getpass
import os
import socket
import struct
import warnings

from decimal import Decimal
from io import IOBase
from typing import (
    Any,
    AsyncGenerator,
    BinaryIO,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from .. import version
from .._scripting import get_local_infile_filenames
from ..constants import (
    ClientFlag,
    FieldType,
    RefreshOption,
    ServerCmd,
    ServerFlag,
    flag_is_set,
)
from ..errors import (
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
from ..protocol import EOF_STATUS, ERR_STATUS, LOCAL_INFILE_STATUS, OK_STATUS
from ..types import (
    BinaryProtocolType,
    DescriptionType,
    EofPacketType,
    OkPacketType,
    ResultType,
    RowType,
    StatsPacketType,
    StrOrBytes,
)
from ..utils import (
    get_platform,
    int1store,
    int4store,
    lc_int,
    warn_ciphersuites_deprecated,
    warn_tls_version_deprecated,
)
from ._decorating import cmd_refresh_verify_options, handle_read_write_timeout
from .abstracts import MySQLConnectionAbstract, MySQLCursorAbstract, ServerInfo
from .charsets import charsets
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
from .logger import logger
from .network import MySQLTcpSocket, MySQLUnixSocket


class MySQLConnection(MySQLConnectionAbstract):
    """Implementation of the pure Python MySQL connection."""

    _mfa_nfactor: int = 1

    @property
    def connection_id(self) -> Optional[int]:
        """MySQL connection ID."""
        if self._handshake:
            return self._handshake.get("server_threadid")  # type: ignore[return-value]
        return None

    async def connect(self) -> None:
        try:
            if self._unix_socket and os.name == "posix":
                self._socket = MySQLUnixSocket(unix_socket=self._unix_socket)
            else:
                self._socket = MySQLTcpSocket(host=self._host, port=self._port)
            await asyncio.wait_for(
                self._socket.open_connection(), self._connection_timeout
            )
            await self._do_handshake()
            await self._do_auth()
        except Exception as err:
            await self._socket.close_connection()
            if isinstance(err, (asyncio.CancelledError, asyncio.TimeoutError)):
                raise ConnectionTimeoutError(
                    errno=2003,
                    msg=f"Can't connect to MySQL server on {self._host}:{self._port} (timed out)",
                ) from err
            raise

        if self._client_flags & ClientFlag.COMPRESS:
            # Update the network layer accordingly
            self._socket.switch_to_compressed_mode()

        # Set converter class
        try:
            self.converter_class = self._converter_class
        except TypeError as err:
            raise AttributeError(
                "Converter classA should be a subclass of "
                "conversion.MySQLConverterBase"
            ) from err

        # Post connection settings
        await self._post_connection()

        # pylint: disable=protected-access
        if (
            not self._ssl_disabled
            and hasattr(self._socket._writer, "get_extra_info")
            and callable(self._socket._writer.get_extra_info)
        ):
            # Raise a deprecation warning if deprecated TLS version
            # or cipher is being used.

            # `get_extra_info("cipher")` returns a three-value tuple containing the name
            # of the cipher being used, the version of the SSL protocol
            # that defines its use, and the number of secret bits being used.
            cipher, tls_version, _ = self._socket._writer.get_extra_info("cipher")
            warn_tls_version_deprecated(tls_version)
            warn_ciphersuites_deprecated(cipher, tls_version)

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

        self._connection_attrs.update((default_conn_attrs))

    async def _execute_query(self, query: str) -> ResultType:
        """Execute a query.

        This method simply calls cmd_query() after checking for unread result. If there
        are still unread result, an InterfaceError is raised. Otherwise whatever
        cmd_query() returns is returned.
        """
        await self.handle_unread_result()
        return await self.cmd_query(query)

    async def _do_handshake(self) -> None:
        """Get the handshake from the MySQL server."""
        packet = await self._socket.read()
        logger.debug("Protocol::Handshake packet: %s", packet)
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)

        self._handshake = self._protocol.parse_handshake(packet)

        self._server_info = ServerInfo(
            protocol=self._handshake["protocol"],
            version=self._handshake["server_version_original"],
            thread_id=self._handshake["server_threadid"],
            charset=self._handshake["charset"],
            status_flags=self._handshake["server_status"],
            auth_plugin=self._handshake["auth_plugin"],
            auth_data=self._handshake["auth_data"],
            capabilities=self._handshake["capabilities"],
        )

        # Set the charsets for the correspondent server major version
        charsets.set_mysql_major_version(self._server_info.version_tuple[0])
        logger.debug("Protocol::Handshake charset: %s", self._server_info.charset)

        # Set charset if provided else use the server default
        if self._charset_name and self._charset_collation:
            self._charset = charsets.get_by_name_and_collation(
                self._charset_name, self._charset_collation
            )
        elif self._charset_name:
            self._charset = charsets.get_by_name(self._charset_name)
        elif self._charset_collation:
            self._charset = charsets.get_by_collation(self._charset_collation)

        if not self._handshake["capabilities"] & ClientFlag.SSL:
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
            if self._ssl_verify_cert:
                raise InterfaceError(
                    "SSL is required but the server doesn't support it",
                    errno=2026,
                )
            self._client_flags &= ~ClientFlag.SSL
        elif not self._ssl_disabled:
            self._client_flags |= ClientFlag.SSL

        if self._handshake["capabilities"] & ClientFlag.PLUGIN_AUTH:
            self.client_flags = [ClientFlag.PLUGIN_AUTH]

        if self._handshake["capabilities"] & ClientFlag.CLIENT_QUERY_ATTRIBUTES:
            self._server_info.query_attrs_is_supported = True
            self.client_flags = [ClientFlag.CLIENT_QUERY_ATTRIBUTES]

        if self._handshake["capabilities"] & ClientFlag.MULTI_FACTOR_AUTHENTICATION:
            self.client_flags = [ClientFlag.MULTI_FACTOR_AUTHENTICATION]

    async def _do_auth(self) -> None:
        """Authenticate with the MySQL server.

        Authentication happens in two parts. We first send a response to the
        handshake. The MySQL server will then send either an AuthSwitchRequest
        or an error packet.

        Raises NotSupportedError when we get the old, insecure password
        reply back. Raises any error coming from MySQL.
        """
        if (  # pylint: disable=too-many-boolean-expressions
            self._auth_plugin
            and self._auth_plugin.startswith("authentication_oci")
            or (
                self._auth_plugin
                and self._auth_plugin.startswith("authentication_kerberos")
                and os.name == "nt"
            )
        ) and not self._user:
            self._user = getpass.getuser()
            logger.debug(
                "MySQL user is empty, OS user: %s will be used for %s",
                self._user,
                self._auth_plugin,
            )

        password = (
            self._password1
            if self._password1 and self._password != self._password1
            else self._password
        )

        self._ssl_active = False
        if not self._ssl_disabled and (self._client_flags & ClientFlag.SSL):
            ssl_context = self._socket.build_ssl_context(
                ssl_ca=self._ssl_ca,
                ssl_cert=self._ssl_cert,
                ssl_key=self._ssl_key,
                ssl_verify_cert=self._ssl_verify_cert,
                ssl_verify_identity=self._ssl_verify_identity,
                tls_versions=self._tls_versions,
                tls_cipher_suites=self._tls_ciphersuites,
            )
            packet: bytes = self._protocol.make_auth_ssl(
                charset=self._charset.charset_id, client_flags=self._client_flags
            )
            await self._socket.write(packet)
            await self._socket.switch_to_ssl(ssl_context)
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

        ok_pkt = await self._authenticator.authenticate(
            sock=self._socket,
            handshake=self._handshake,
            username=self._user,
            password1=password,
            password2=self._password2,
            password3=self._password3,
            database=self._database,
            charset=self._charset.charset_id,
            client_flags=self._client_flags,
            ssl_enabled=self._ssl_active,
            auth_plugin=self._auth_plugin,
            auth_plugin_class=self._auth_plugin_class,
            conn_attrs=self._connection_attrs,
        )
        self._handle_ok(ok_pkt)

        if not (self._client_flags & ClientFlag.CONNECT_WITH_DB) and self._database:
            await self.cmd_init_db(self._database)

    def _handle_ok(self, packet: bytes) -> OkPacketType:
        """Handle a MySQL OK packet.

        This method handles a MySQL OK packet. When the packet is found to be an Error
        packet, an error will be raised. If the packet is neither an OK or an Error
        packet, InterfaceError will be raised.
        """
        if packet[4] == OK_STATUS:
            ok_pkt = self._protocol.parse_ok(packet)
            self._handle_server_status(ok_pkt["status_flag"])
            return ok_pkt
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)
        raise InterfaceError("Expected OK packet")

    def _handle_server_status(self, flags: int) -> None:
        """Handle the server flags found in MySQL packets.

        This method handles the server flags send by MySQL OK and EOF packets.
        It, for example, checks whether there exists more result sets or whether there
        is an ongoing transaction.
        """
        self._have_next_result = flag_is_set(ServerFlag.MORE_RESULTS_EXISTS, flags)
        self._in_transaction = flag_is_set(ServerFlag.STATUS_IN_TRANS, flags)

    def _handle_eof(self, packet: bytes) -> EofPacketType:
        """Handle a MySQL EOF packet.

        This method handles a MySQL EOF packet. When the packet is found to be an Error
        packet, an error will be raised. If the packet is neither and OK or an Error
        packet, InterfaceError will be raised.
        """
        if packet[4] == EOF_STATUS:
            eof = self._protocol.parse_eof(packet)
            self._handle_server_status(eof["status_flag"])
            return eof
        if packet[4] == ERR_STATUS:
            raise get_exception(packet)
        raise InterfaceError("Expected EOF packet")

    @handle_read_write_timeout()
    async def _handle_load_data_infile(
        self,
        filename: str,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> OkPacketType:
        """Handle a LOAD DATA INFILE LOCAL request."""
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
            # Validate filename is inside of allow_local_infile_in_path path.
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
                await self._send_data(data_file, True, read_timeout, write_timeout)
            )
        except IOError:
            # Send a empty packet to cancel the operation
            try:
                await self._socket.write(
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
    async def _handle_result(
        self,
        packet: bytes,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> ResultType:
        """Handle a MySQL Result.

        This method handles a MySQL result, for example, after sending the query
        command. OK and EOF packets will be handled and returned.
        If the packet is an Error packet, an Error-exception will be raised.

        The dictionary returned of:
        - columns: column information
        - eof: the EOF-packet information
        """
        if not packet or len(packet) < 4:
            raise InterfaceError("Empty response")
        if packet[4] == OK_STATUS:
            return self._handle_ok(packet)
        if packet[4] == LOCAL_INFILE_STATUS:
            filename = packet[5:].decode()
            return await self._handle_load_data_infile(
                filename, read_timeout, write_timeout
            )
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
                await self._socket.read(read_timeout or self._read_timeout),
                self.python_charset,
            )

        eof = self._handle_eof(
            await self._socket.read(read_timeout or self._read_timeout)
        )
        self.unread_result = True
        return {"columns": self._columns_desc, "eof": eof}

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
    async def _handle_binary_result(
        self, packet: bytes
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
                await self._socket.read(self._read_timeout), self.python_charset
            )

        eof = self._handle_eof(await self._socket.read(self._read_timeout))
        return (column_count, columns, eof)

    @handle_read_write_timeout()
    async def _send_cmd(
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
        """Send a command to the MySQL server.

        This method sends a command with an optional argument.
        If packet is not None, it will be sent and the argument will be ignored.

        The packet_number is optional and should usually not be used.

        Some commands might not result in the MySQL server returning a response. If a
        command does not return anything, you should set expect_response to False.
        The _send_cmd method will then return None instead of a MySQL packet.
        """
        await self.handle_unread_result()

        try:
            await self._socket.write(
                self._protocol.make_command(command, packet or argument),
                packet_number,
                compressed_packet_number,
                write_timeout or self._write_timeout,
            )
        except AttributeError as err:
            raise OperationalError("MySQL Connection not available") from err

        if not expect_response:
            return None
        return await self._socket.read(read_timeout or self._read_timeout)

    @handle_read_write_timeout()
    async def _send_data(
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
        await self.handle_unread_result()

        if not hasattr(data_file, "read"):
            raise ValueError("expecting a file-like object")

        chunk_size = 131072  # 128 KB
        try:
            buf = data_file.read(chunk_size - 16)
            while buf:
                await self._socket.write(
                    buf, write_timeout=write_timeout or self._write_timeout
                )
                buf = data_file.read(chunk_size - 16)
        except AttributeError as err:
            raise OperationalError("MySQL Connection not available") from err

        if send_empty_packet:
            try:
                await self._socket.write(b"", write_timeout or self._write_timeout)
            except AttributeError as err:
                raise OperationalError("MySQL Connection not available") from err

        res = await self._socket.read(read_timeout or self._read_timeout)
        return res

    def is_socket_connected(self) -> bool:
        """Reports whether the socket is connected.

        Instead of ping the server like ``is_connected()``, it only checks if the
        socket connection flag is set.
        """
        return bool(self._socket and self._socket.is_connected())

    async def is_connected(self) -> bool:
        """Reports whether the connection to MySQL Server is available.

        This method checks whether the connection to MySQL is available.
        It is similar to ``ping()``, but unlike the ``ping()`` method, either `True`
        or `False` is returned and no exception is raised.
        """
        try:
            await self.cmd_ping()
        except Error:
            return False
        return True

    async def ping(
        self, reconnect: bool = False, attempts: int = 1, delay: int = 0
    ) -> None:
        """Check availability of the MySQL server.

        When reconnect is set to `True`, one or more attempts are made to try to
        reconnect to the MySQL server using the ``reconnect()`` method.

        ``delay`` is the number of seconds to wait between each retry.

        When the connection is not available, an InterfaceError is raised. Use the
        ``is_connected()`` method if you just want to check the connection without
        raising an error.

        Raises:
            InterfaceError: On errors.
        """
        try:
            await self.cmd_ping()
        except Error as err:
            if reconnect:
                await self.reconnect(attempts=attempts, delay=delay)
            else:
                raise InterfaceError("Connection to MySQL is not available") from err

    async def shutdown(self) -> None:
        """Shut down connection to MySQL Server.

        This method closes the socket. It raises no exceptions.

        Unlike `disconnect()`, `shutdown()` closes the client connection without
        attempting to send a QUIT command to the server first. Thus, it will not
        block if the connection is disrupted for some reason such as network failure.
        """
        if not self._socket:
            return

        try:
            await self._socket.close_connection()
        except Exception:  # pylint: disable=broad-exception-caught
            pass  # Getting an exception would mean we are disconnected.

    async def close(self) -> None:
        with contextlib.suppress(Error):
            for cursor in tuple(self._cursors):
                await cursor.close()
            self._cursors.clear()

            if self._socket and self._socket.is_connected():
                await self.cmd_quit()

        if self._socket:
            await self._socket.close_connection()
        self._socket = None

    disconnect = close

    async def cursor(
        self,
        buffered: Optional[bool] = None,
        raw: Optional[bool] = None,
        prepared: Optional[bool] = None,
        cursor_class: Optional[Type[MySQLCursorAbstract]] = None,
        dictionary: Optional[bool] = None,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> MySQLCursor:
        """Instantiate and return a cursor.

        By default, MySQLCursor is returned. Depending on the options while
        connecting, a buffered and/or raw cursor is instantiated instead.
        Also depending upon the cursor options, rows can be returned as a dictionary
        or a tuple.

        It is possible to also give a custom cursor through the cursor_class
        parameter, but it needs to be a subclass of
        mysql.connector.aio.abstracts.MySQLCursorAbstract.

        Raises:
            ProgrammingError: When cursor_class is not a subclass of
                              MySQLCursor.
            ValueError: When cursor is not available.
            InterfaceError: When read or write timeout is not a positive integer.
        """
        if not self._socket or not self._socket.is_connected():
            raise OperationalError("MySQL Connection not available")

        if read_timeout is not None and (
            not isinstance(read_timeout, int) or read_timeout < 0
        ):
            raise InterfaceError("Option read_timeout must be a positive integer")
        if write_timeout is not None and (
            not isinstance(write_timeout, int) or write_timeout < 0
        ):
            raise InterfaceError("Option write_timeout must be a positive integer")

        await self.handle_unread_result()

        if cursor_class is not None:
            if not issubclass(cursor_class, MySQLCursor):
                raise ProgrammingError(
                    "Cursor class needs be to subclass of MySQLCursorAbstract"
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
            0: MySQLCursor,
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
            criteria = ", ".join(
                [args[i] for i in range(4) if cursor_type & (1 << i) != 0]
            )
            raise ValueError(
                f"Cursor not available with given criteria: {criteria}"
            ) from None

    @handle_read_write_timeout()
    async def get_row(
        self,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[RowType], Optional[EofPacketType]]:
        """Get the next rows returned by the MySQL server.

        This method gets one row from the result set after sending, for example, the
        query command. The result is a tuple consisting of the row and the EOF packet.
        If no row was available in the result set, the row data will be None.
        """
        rows, eof = await self.get_rows(
            count=1,
            binary=binary,
            columns=columns,
            raw=raw,
            **kwargs,
        )
        if rows:
            return (rows[0], eof)
        return (None, eof)

    @handle_read_write_timeout()
    async def get_rows(
        self,
        count: Optional[int] = None,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Any = None,
        **kwargs: Any,
    ) -> Tuple[List[RowType], Optional[EofPacketType]]:
        """Get all rows returned by the MySQL server.

        This method gets all rows returned by the MySQL server after sending, for
        example, the query command. The result is a tuple consisting of a list of rows
        and the EOF packet.
        """
        if raw is None:
            raw = self._raw

        if not self.unread_result:
            raise InternalError("No result set available")

        rows: Tuple[List[Tuple[Any, ...]], Optional[EofPacketType]] = ([], None)
        try:
            read_timeout = kwargs.get("read_timeout", None)
            if binary:
                charset = self.charset
                if charset == "utf8mb4":
                    charset = "utf8"
                rows = await self._protocol.read_binary_result(
                    self._socket,
                    columns,
                    count,
                    charset,
                    read_timeout or self._read_timeout,
                )
            else:
                rows = await self._protocol.read_text_result(
                    self._socket,
                    self._server_info.version,
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

    async def commit(self) -> None:
        """Commit current transaction."""
        await self._execute_query("COMMIT")

    async def rollback(self) -> None:
        """Rollback current transaction."""
        if self.unread_result:
            await self.get_rows()
        await self._execute_query("ROLLBACK")

    async def cmd_reset_connection(self) -> bool:
        """Resets the session state without re-authenticating.

        Reset command only works on MySQL server 5.7.3 or later.
        The result is True for a successful reset otherwise False.
        """
        try:
            self._handle_ok(await self._send_cmd(ServerCmd.RESET_CONNECTION))
            await self._post_connection()
            return True
        except (NotSupportedError, OperationalError):
            return False

    async def cmd_init_db(self, database: str) -> OkPacketType:
        """Change the current database.

        This method changes the current (default) database by sending the INIT_DB
        command. The result is a dictionary containing the OK packet infawaitormation.
        """
        return self._handle_ok(
            await self._send_cmd(ServerCmd.INIT_DB, database.encode("utf-8"))
        )

    async def cmd_query(
        self,
        query: StrOrBytes,
        raw: bool = False,
        buffered: bool = False,
        raw_as_string: bool = False,
        **kwargs: Any,
    ) -> ResultType:
        if not isinstance(query, bytearray):
            if isinstance(query, str):
                query = query.encode()
            query = bytearray(query)

        # Set/Reset internal state related to query execution
        self._query = query
        self._local_infile_filenames = None

        # Prepare query attrs
        charset = self._charset.name if self._charset.name != "utf8mb4" else "utf8"
        packet = bytearray()
        if not self._server_info.query_attrs_is_supported and self._query_attrs:
            warnings.warn(
                "This version of the server does not support Query Attributes",
                category=Warning,
            )
        if self._client_flags & ClientFlag.CLIENT_QUERY_ATTRIBUTES:
            names = []
            types = []
            values: List[bytes] = []
            null_bitmap = [0] * ((len(self._query_attrs) + 7) // 8)
            for pos, attr_tuple in enumerate(self._query_attrs):
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
                    field_type = FieldType.VARCHAR
                elif isinstance(value, bytes):
                    values.append(lc_int(len(value)) + value)
                    field_type = FieldType.BLOB
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
            result = await self._handle_result(
                await self._send_cmd(
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

    async def cmd_query_iter(  # type: ignore[override]
        self,
        statements: StrOrBytes,
        **kwargs: Any,
    ) -> AsyncGenerator[ResultType, None]:
        """Send one or more statements to the MySQL server.

        Similar to the cmd_query method, but instead returns a generator
        object to iterate through results. It sends the statements to the
        MySQL server and through the iterator you can get the results.

        statement = 'SELECT 1; INSERT INTO t1 VALUES (); SELECT 2'
        for result in await cnx.cmd_query(statement, iterate=True):
            if 'columns' in result:
                columns = result['columns']
                rows = await cnx.get_rows()
            else:
                # do something useful with INSERT result
        """
        try:
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
            yield await self._handle_result(
                await self._send_cmd(
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
                await self.handle_unread_result()
                yield await self._handle_result(
                    await self._socket.read(read_timeout or self._read_timeout),
                    read_timeout,
                    write_timeout,
                )
        except (ReadTimeoutError, WriteTimeoutError) as err:
            raise err

    async def cmd_stmt_fetch(
        self, statement_id: int, rows: int = 1, **kwargs: Any
    ) -> None:
        """Fetch a MySQL statement Result Set.

        This method will send the FETCH command to MySQL together with the given
        statement id and the number of rows to fetch.
        """
        read_timeout = kwargs.get("read_timeout", None)
        write_timeout = kwargs.get("write_timeout", None)
        packet = self._protocol.make_stmt_fetch(statement_id, rows)
        self.unread_result = False
        await self._send_cmd(
            ServerCmd.STMT_FETCH,
            packet,
            expect_response=False,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
        )
        self.unread_result = True

    @handle_read_write_timeout()
    async def cmd_stmt_prepare(
        self,
        statement: bytes,
        **kwargs: Any,
    ) -> Mapping[str, Union[int, List[DescriptionType]]]:
        """Prepare a MySQL statement.

        This method will send the PREPARE command to MySQL together with the given
        statement.
        """
        read_timeout = kwargs.get("read_timeout", None)
        write_timeout = kwargs.get("write_timeout", None)
        packet = await self._send_cmd(
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
                        await self._socket.read(read_timeout or self._read_timeout),
                        self.python_charset,
                    )
                )
            self._handle_eof(
                await self._socket.read(read_timeout or self._read_timeout)
            )
        if result["num_columns"] > 0:
            for _ in range(0, result["num_columns"]):
                result["columns"].append(
                    self._protocol.parse_column(
                        await self._socket.read(read_timeout or self._read_timeout),
                        self.python_charset,
                    )
                )
            self._handle_eof(
                await self._socket.read(read_timeout or self._read_timeout)
            )

        return result

    async def cmd_stmt_execute(
        self,
        statement_id: int,  # type: ignore[override]
        data: Sequence[BinaryProtocolType] = (),
        parameters: Sequence[Any] = (),
        flags: int = 0,
        **kwargs: Any,
    ) -> Union[OkPacketType, Tuple[int, List[DescriptionType], EofPacketType]]:
        """Execute a prepared MySQL statement."""
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
                    await self.cmd_stmt_send_long_data(
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
                self._query_attrs,
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
        packet = await self._send_cmd(
            ServerCmd.STMT_EXECUTE,
            packet=execute_packet,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
        )
        result = await self._handle_binary_result(packet)
        return result

    async def cmd_stmt_reset(self, statement_id: int, **kwargs: Any) -> None:
        """Reset data for prepared statement sent as long data.

        The result is a dictionary with OK packet information.
        """
        self._handle_ok(
            await self._send_cmd(
                ServerCmd.STMT_RESET,
                int4store(statement_id),
                read_timeout=kwargs.get("read_timeout", None),
                write_timeout=kwargs.get("write_timeout", None),
            ),
        )

    async def cmd_stmt_close(self, statement_id: int, **kwargs: Any) -> None:
        """Deallocate a prepared MySQL statement.

        This method deallocates the prepared statement using the statement_id.
        Note that the MySQL server does not return anything.
        """
        await self._send_cmd(
            ServerCmd.STMT_CLOSE,
            int4store(statement_id),
            expect_response=False,
            read_timeout=kwargs.get("read_timeout", None),
            write_timeout=kwargs.get("write_timeout", None),
        )

    @cmd_refresh_verify_options()
    async def cmd_refresh(self, options: int) -> OkPacketType:
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
            res = await self.cmd_query("FLUSH PRIVILEGES")
        if options & RefreshOption.LOG:
            res = await self.cmd_query("FLUSH LOGS")
        if options & RefreshOption.TABLES:
            res = await self.cmd_query("FLUSH TABLES")
        if options & RefreshOption.HOST:
            res = await self.cmd_query("TRUNCATE TABLE performance_schema.host_cache")
        if options & RefreshOption.STATUS:
            res = await self.cmd_query("FLUSH STATUS")
        if options & RefreshOption.REPLICA:
            res = await self.cmd_query(
                "RESET SLAVE"
                if self._server_info.version_tuple < (8, 0, 22)
                else "RESET REPLICA"
            )

        return res  # type: ignore[return-value]

    async def cmd_stmt_send_long_data(
        self,
        statement_id: int,
        param_id: int,
        data: BinaryIO,
        **kwargs: Any,
    ) -> int:
        """Send data for a column.

        This methods send data for a column (for example BLOB) for statement identified
        by statement_id. The param_id indicate which parameter the data belongs too.
        The data argument should be a file-like object.

        Since MySQL does not send anything back, no error is raised. When the MySQL
        server is not reachable, an OperationalError is raised.

        cmd_stmt_send_long_data should be called before cmd_stmt_execute.

        The total bytes send is returned.
        """
        chunk_size = 131072  # 128 KB
        total_sent = 0
        try:
            buf = data.read(chunk_size)
            while buf:
                packet = self._protocol.prepare_stmt_send_long_data(
                    statement_id, param_id, buf
                )
                await self._send_cmd(
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

    async def cmd_quit(self) -> bytes:
        """Close the current connection with the server.

        Send the QUIT command to the MySQL server, closing the current connection.
        """
        await self.handle_unread_result()
        packet = self._protocol.make_command(ServerCmd.QUIT)
        try:
            await self._socket.write(packet, write_timeout=self._write_timeout)
        except WriteTimeoutError as _:
            pass
        return packet

    async def cmd_shutdown(self, shutdown_type: Optional[int] = None) -> None:
        """Shut down the MySQL Server.

        This method sends the SHUTDOWN command to the MySQL server.
        The `shutdown_type` is not used, and it's kept for backward compatibility.
        """
        await self.cmd_query("SHUTDOWN")

    async def cmd_statistics(self) -> StatsPacketType:
        """Send the statistics command to the MySQL Server.

        This method sends the STATISTICS command to the MySQL server. The result is a
        dictionary with various statistical information.
        """
        await self.handle_unread_result()

        packet = self._protocol.make_command(ServerCmd.STATISTICS)
        await self._socket.write(packet, 0, 0, self._write_timeout)
        return self._protocol.parse_statistics(
            await self._socket.read(self._read_timeout)
        )

    async def cmd_process_kill(self, mysql_pid: int) -> OkPacketType:
        """Kill a MySQL process.

        This method send the PROCESS_KILL command to the server along with the
        process ID. The result is a dictionary with the OK packet information.
        """
        if not isinstance(mysql_pid, int):
            raise ValueError("MySQL PID must be int")
        return await self.cmd_query(f"KILL {mysql_pid}")  # type: ignore[return-value]

    async def cmd_debug(self) -> EofPacketType:
        """Send the DEBUG command.

        This method sends the DEBUG command to the MySQL server, which requires the
        MySQL user to have SUPER privilege. The output will go to the MySQL server
        error log and the result of this method is a dictionary with EOF packet
        information.
        """
        return self._handle_eof(await self._send_cmd(ServerCmd.DEBUG))

    async def cmd_ping(self) -> OkPacketType:
        """Send the PING command.

        This method sends the PING command to the MySQL server. It is used to check
        if the the connection is still valid. The result of this method is dictionary
        with OK packet information.
        """
        return self._handle_ok(await self._send_cmd(ServerCmd.PING))

    async def cmd_change_user(
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
        """Change the current logged in user.

        This method allows to change the current logged in user information.
        The result is a dictionary with OK packet information.
        """
        # If charset isn't defined, we use the same charset ID defined previously,
        # otherwise, we run a verification and update the charset ID.
        if charset is not None:
            if not isinstance(charset, int):
                raise ValueError("charset must be an integer")
            if charset < 0:
                raise ValueError("charset should be either zero or a postive integer")
            self._charset = charsets.get_by_id(charset)

        self._mfa_nfactor = 1
        self._user = username
        self._password = password
        self._password1 = password1
        self._password2 = password2
        self._password3 = password3

        if self._password1 and password != self._password1:
            self._password = self._password1

        await self.handle_unread_result()

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

        ok_packet: bytes = await self._authenticator.authenticate(
            sock=self._socket,
            handshake=self._handshake,
            username=self._user,
            password1=self._password,
            password2=self._password2,
            password3=self._password3,
            database=self._database,
            charset=self._charset.charset_id,
            client_flags=self._client_flags,
            ssl_enabled=self._ssl_active,
            auth_plugin=self._auth_plugin,
            conn_attrs=self._connection_attrs,
            is_change_user_request=True,
            read_timeout=self._read_timeout,
            write_timeout=self._write_timeout,
        )

        if not (self._client_flags & ClientFlag.CONNECT_WITH_DB) and database:
            await self.cmd_init_db(database)

        # return ok_pkt
        return self._handle_ok(ok_packet)
