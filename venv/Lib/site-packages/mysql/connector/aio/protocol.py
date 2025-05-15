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

"""Implements the MySQL Client/Server protocol."""

__all__ = ["MySQLProtocol"]

import struct

from typing import Any, Dict, List, Optional, Tuple

from ..constants import ClientFlag, ServerCmd
from ..errors import InterfaceError, ProgrammingError, get_exception
from ..logger import logger
from ..protocol import (
    DEFAULT_CHARSET_ID,
    DEFAULT_MAX_ALLOWED_PACKET,
    MySQLProtocol as _MySQLProtocol,
)
from ..types import BinaryProtocolType, DescriptionType, EofPacketType, HandShakeType
from ..utils import lc_int, read_lc_string_list
from .network import MySQLSocket
from .plugins import MySQLAuthPlugin, get_auth_plugin
from .plugins.caching_sha2_password import MySQLCachingSHA2PasswordAuthPlugin


class MySQLProtocol(_MySQLProtocol):
    """Implements MySQL client/server protocol.

    Create and parses MySQL packets.
    """

    @staticmethod
    def auth_plugin_first_response(  # type: ignore[override]
        auth_data: bytes,
        username: str,
        password: str,
        auth_plugin: str,
        auth_plugin_class: Optional[str] = None,
        ssl_enabled: bool = False,
        plugin_config: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bytes, MySQLAuthPlugin]:
        """Prepare the first authentication response.

        Args:
            auth_data: Authorization data from initial handshake.
            username: Account's username.
            password: Account's password.
            client_flags: Integer representing client capabilities flags.
            auth_plugin: Authorization plugin name.
            auth_plugin_class: Authorization plugin class (has higher precedence
                               than the authorization plugin name).
            ssl_enabled: Whether SSL is enabled or not.
            plugin_config: Custom configuration to be passed to the auth plugin
                           when invoked. The parameters defined here will override
                           the ones defined in the auth plugin itself.

        Returns:
            auth_response: Authorization plugin response.
            auth_strategy: Authorization plugin instance created based
                           on the provided `auth_plugin` and `auth_plugin_class`
                           parameters.

        Raises:
            InterfaceError: If authentication fails or when got a NULL auth response.
        """
        if not password and auth_plugin == "":
            # return auth response and an arbitrary auth strategy
            return b"\x00", MySQLCachingSHA2PasswordAuthPlugin(
                username, password, ssl_enabled=ssl_enabled
            )

        if plugin_config is None:
            plugin_config = {}

        try:
            auth_strategy = get_auth_plugin(auth_plugin, auth_plugin_class)(
                username, password, ssl_enabled=ssl_enabled
            )
            auth_response = auth_strategy.auth_response(auth_data, **plugin_config)
        except (TypeError, InterfaceError) as err:
            raise InterfaceError(f"Failed authentication: {err}") from err

        if auth_response is None:
            raise InterfaceError(
                "Got NULL auth response while authenticating with "
                f"plugin {auth_strategy.name}"
            )

        auth_response = lc_int(len(auth_response)) + auth_response

        return auth_response, auth_strategy

    @staticmethod
    def make_auth(  # type: ignore[override]
        handshake: HandShakeType,
        username: str,
        password: str,
        database: Optional[str] = None,
        charset: int = DEFAULT_CHARSET_ID,
        client_flags: int = 0,
        max_allowed_packet: int = DEFAULT_MAX_ALLOWED_PACKET,
        auth_plugin: Optional[str] = None,
        auth_plugin_class: Optional[str] = None,
        conn_attrs: Optional[Dict[str, str]] = None,
        is_change_user_request: bool = False,
        ssl_enabled: bool = False,
        plugin_config: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bytes, MySQLAuthPlugin]:
        """Make a MySQL Authentication packet.

        Args:
            handshake: Initial handshake.
            username: Account's username.
            password: Account's password.
            database: Initial database name for the connection
            charset: Client charset (see [2]), only the lower 8-bits.
            client_flags: Integer representing client capabilities flags.
            max_allowed_packet: Maximum packet size.
            auth_plugin: Authorization plugin name.
            auth_plugin_class: Authorization plugin class (has higher precedence
                               than the authorization plugin name).
            conn_attrs: Connection attributes.
            is_change_user_request: Whether is a `change user request` operation or not.
            ssl_enabled: Whether SSL is enabled or not.
            plugin_config: Custom configuration to be passed to the auth plugin
                           when invoked. The parameters defined here will override
                           the one defined in the auth plugin itself.

        Returns:
            handshake_response: Handshake response as per [1].
            auth_strategy: Authorization plugin instance created based
                           on the provided `auth_plugin` and `auth_plugin_class`.

        Raises:
            ProgrammingError: Handshake misses authentication info.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_connection_phase_packets_protocol_handshake_response.html

            [2]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_basic_character_set.html#a_protocol_character_set
        """
        b_username = username.encode()
        response_payload = []

        if is_change_user_request:
            logger.debug("Got a `change user` request")

        logger.debug("Starting authorization phase")
        if handshake is None:
            raise ProgrammingError("Got a NULL handshake") from None

        if handshake.get("auth_data") is None:
            raise ProgrammingError("Handshake misses authentication info") from None

        try:
            auth_plugin = auth_plugin or handshake["auth_plugin"]  # type: ignore[assignment]
        except (TypeError, KeyError) as err:
            raise ProgrammingError(
                f"Handshake misses authentication plugin info ({err})"
            ) from None

        logger.debug("The provided initial strategy is %s", auth_plugin)

        if is_change_user_request:
            response_payload.append(
                struct.pack(
                    f"<B{len(b_username)}sx",
                    ServerCmd.CHANGE_USER,
                    b_username,
                )
            )
        else:
            filler = "x" * 23
            response_payload.append(
                struct.pack(
                    f"<IIB{filler}{len(b_username)}sx",
                    client_flags,
                    max_allowed_packet,
                    charset,
                    b_username,
                )
            )

        # auth plugin response
        auth_response, auth_strategy = MySQLProtocol.auth_plugin_first_response(
            auth_data=handshake["auth_data"],  # type: ignore[arg-type]
            username=username,
            password=password,
            auth_plugin=auth_plugin,
            auth_plugin_class=auth_plugin_class,
            ssl_enabled=ssl_enabled,
            plugin_config=plugin_config,
        )
        response_payload.append(auth_response)

        # database name
        response_payload.append(MySQLProtocol.connect_with_db(client_flags, database))

        # charset
        if is_change_user_request:
            response_payload.append(struct.pack("<H", charset))

        # plugin name
        if client_flags & ClientFlag.PLUGIN_AUTH:
            response_payload.append(auth_plugin.encode() + b"\x00")

        # connection attributes
        if (client_flags & ClientFlag.CONNECT_ARGS) and conn_attrs is not None:
            response_payload.append(MySQLProtocol.make_conn_attrs(conn_attrs))

        return b"".join(response_payload), auth_strategy

    # pylint: disable=invalid-overridden-method
    async def read_binary_result(  # type: ignore[override]
        self,
        sock: MySQLSocket,
        columns: List[DescriptionType],
        count: int = 1,
        charset: str = "utf-8",
        read_timeout: Optional[int] = None,
    ) -> Tuple[
        List[Tuple[BinaryProtocolType, ...]],
        Optional[EofPacketType],
    ]:
        """Read MySQL binary protocol result.

        Reads all or given number of binary resultset rows from the socket.
        """
        rows = []
        eof = None
        values = None
        i = 0
        while True:
            if eof or i == count:
                break
            packet = await sock.read(read_timeout)
            if packet[4] == 254:
                eof = self.parse_eof(packet)
                values = None
            elif packet[4] == 0:
                eof = None
                values = self._parse_binary_values(columns, packet[5:], charset)
            if eof is None and values is not None:
                rows.append(values)
            elif eof is None and values is None:
                raise get_exception(packet)
            i += 1
        return (rows, eof)

    # pylint: disable=invalid-overridden-method
    async def read_text_result(  # type: ignore[override]
        self,
        sock: MySQLSocket,
        version: Tuple[int, ...],
        count: int = 1,
        read_timeout: Optional[int] = None,
    ) -> Tuple[
        List[Tuple[Optional[bytes], ...]],
        Optional[EofPacketType],
    ]:
        """Read MySQL text result.

        Reads all or given number of rows from the socket.

        Returns a tuple with 2 elements: a list with all rows and
        the EOF packet.
        """
        # Keep unused 'version' for API backward compatibility
        _ = version
        rows = []
        eof = None
        rowdata = None
        i = 0
        while True:
            if eof or i == count:
                break
            packet = await sock.read(read_timeout)
            if packet.startswith(b"\xff\xff\xff"):
                datas = [packet[4:]]
                packet = await sock.read(read_timeout)
                while packet.startswith(b"\xff\xff\xff"):
                    datas.append(packet[4:])
                    packet = await sock.read(read_timeout)
                datas.append(packet[4:])
                rowdata = read_lc_string_list(b"".join(datas))
            elif packet[4] == 254 and packet[0] < 7:
                eof = self.parse_eof(packet)
                rowdata = None
            else:
                eof = None
                rowdata = read_lc_string_list(bytes(packet[4:]))
            if eof is None and rowdata is not None:
                rows.append(rowdata)
            elif eof is None and rowdata is None:
                raise get_exception(packet)
            i += 1
        return rows, eof
