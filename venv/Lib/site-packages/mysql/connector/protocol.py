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

"""Implements the MySQL Client/Server protocol."""
from __future__ import annotations

import datetime
import struct

from collections import deque
from decimal import Decimal, DecimalException
from typing import (
    TYPE_CHECKING,
    Any,
    Deque,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from . import utils
from .constants import (
    PARAMETER_COUNT_AVAILABLE,
    ClientFlag,
    FieldFlag,
    FieldType,
    ServerCmd,
)
from .conversion import MySQLConverter
from .errors import DatabaseError, InterfaceError, ProgrammingError, get_exception
from .logger import logger
from .plugins import MySQLAuthPlugin, get_auth_plugin
from .plugins.caching_sha2_password import MySQLCachingSHA2PasswordAuthPlugin
from .types import (
    BinaryProtocolType,
    DescriptionType,
    EofPacketType,
    HandShakeType,
    OkPacketType,
    StatsPacketType,
    StrOrBytes,
)

if TYPE_CHECKING:
    from .network import MySQLSocket


PROTOCOL_VERSION = 10
AUTH_SWITCH_STATUS = 0xFE
EXCHANGE_FURTHER_STATUS = 0x01
OK_STATUS = 0x00
EOF_STATUS = 0xFE
MFA_STATUS = 0x02
ERR_STATUS = 0xFF
LOCAL_INFILE_STATUS = 0xFB
DEFAULT_CHARSET_ID = 45
DEFAULT_MAX_ALLOWED_PACKET = 1073741824


class MySQLProtocol:
    """Implements MySQL client/server protocol

    Create and parses MySQL packets.
    """

    @staticmethod
    def parse_auth_more_data(pkt: bytes) -> bytes:
        """Parse a MySQL auth more data packet.

        Args:
            pkt: Packet representing an `auth more data` response.

        Returns:
            auth_data: Authentication method data (see [1]).

        Raises:
            InterfaceError: If packet's status tag doesn't
                            match `protocol.EXCHANGE_FURTHER_STATUS`.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_connection_phase_packets_protocol_auth_more_data.html
        """
        if not pkt[4] == EXCHANGE_FURTHER_STATUS:
            raise InterfaceError("Failed parsing AuthMoreData packet")
        return pkt[5:]

    @staticmethod
    def parse_auth_switch_request(pkt: bytes) -> Tuple[str, bytes]:
        """Parse a MySQL auth switch request packet.

        Args:
            pkt: Packet representing an `auth switch request` response.

        Returns:
            plugin_name: Name of the client authentication plugin to switch to.
            plugin_provided_data: Plugin provided data (see [1]).

        Raises:
            InterfaceError: If packet's status tag doesn't
                            match `protocol.AUTH_SWITCH_STATUS`.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/\
                latest/page_protocol_connection_phase_packets_protocol_
                auth_switch_request.html
        """
        if pkt[4] != AUTH_SWITCH_STATUS:
            raise InterfaceError("Failed parsing AuthSwitchRequest packet")
        pkt, plugin_name = utils.read_string(pkt[5:], end=b"\x00")
        if pkt and pkt[-1] == 0:
            pkt = pkt[:-1]
        return plugin_name.decode(), pkt

    @staticmethod
    def parse_auth_next_factor(pkt: bytes) -> Tuple[str, bytes]:
        """Parse a MySQL auth next factor packet.

        Args:
            pkt: Packet representing an `auth next factor` response.

        Returns:
            plugin_name: Name of the client authentication plugin.
            plugin_provided_data: Initial authentication data for that
                                  client plugin (see [1]).

        Raises:
            InterfaceError: If packet's packet type doesn't
                            match `protocol.MFA_STATUS`.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_connection_phase_packets_protocol_auth_\
                next_factor_request.html
        """
        pkt, status = utils.read_int(pkt[4:], 1)
        if status != MFA_STATUS:
            raise InterfaceError("Failed parsing AuthNextFactor packet (invalid)")
        pkt, plugin_name = utils.read_string(pkt, end=b"\x00")
        return plugin_name.decode(), pkt

    @staticmethod
    def make_conn_attrs(conn_attrs: Dict[str, str]) -> bytes:
        """Encode the connection attributes.

        Args:
            conn_attrs: Connection attributes.

        Returns:
            serialized_conn_attrs: Serialized connection attributes as per [1].

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_connection_phase_packets_protocol_handshake_response.html
        """
        for attr_name in conn_attrs:
            if conn_attrs[attr_name] is None:
                conn_attrs[attr_name] = ""
        conn_attrs_len = (
            sum(len(x) + len(conn_attrs[x]) for x in conn_attrs)
            + len(conn_attrs.keys())
            + len(conn_attrs.values())
        )

        conn_attrs_packet = [struct.pack("<B", conn_attrs_len)]
        for attr_name in conn_attrs:
            conn_attrs_packet.append(struct.pack("<B", len(attr_name)))
            conn_attrs_packet.append(attr_name.encode())
            conn_attrs_packet.append(struct.pack("<B", len(conn_attrs[attr_name])))
            conn_attrs_packet.append(conn_attrs[attr_name].encode())
        return b"".join(conn_attrs_packet)

    @staticmethod
    def connect_with_db(client_flags: int, database: Optional[str]) -> bytes:
        """Prepare database string for handshake response.

        Args:
            client_flags: Integer representing client capabilities flags.
            database: Initial database name for the connection.

        Returns:
            serialized_database: Serialized database name as per [1].

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_connection_phase_packets_protocol_handshake_response.html
        """
        return (
            database.encode() + b"\x00"
            if client_flags & ClientFlag.CONNECT_WITH_DB and database
            else b"\x00"
        )

    @staticmethod
    def auth_plugin_first_response(
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

        auth_response = utils.lc_int(len(auth_response)) + auth_response

        return auth_response, auth_strategy

    @staticmethod
    def make_auth(
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

    @staticmethod
    def make_auth_ssl(
        charset: int = DEFAULT_CHARSET_ID,
        client_flags: int = 0,
        max_allowed_packet: int = DEFAULT_MAX_ALLOWED_PACKET,
    ) -> bytes:
        """Make a SSL authentication packet (see [1]).

        Args:
            charset: Client charset (see [2]), only the lower 8-bits.
            client_flags: Integer representing client capabilities flags.
            max_allowed_packet: Maximum packet size.

        Returns:
            ssl_request_pkt: SSL connection request packet.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_connection_phase_packets_protocol_ssl_request.html

            [2]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_basic_character_set.html#a_protocol_character_set
        """
        # SSL connection request packet
        return b"".join(
            [
                utils.int4store(client_flags),
                utils.int4store(max_allowed_packet),
                utils.int1store(charset),
                b"\x00" * 23,
            ]
        )

    @staticmethod
    def make_command(command: int, argument: Optional[bytes] = None) -> bytes:
        """Make a MySQL packet containing a command"""
        data = utils.int1store(command)
        return data if argument is None else data + argument

    @staticmethod
    def make_stmt_fetch(statement_id: int, rows: int = 1) -> bytes:
        """Make a MySQL packet with Fetch Statement command"""
        return utils.int4store(statement_id) + utils.int4store(rows)

    @staticmethod
    def parse_handshake(packet: bytes) -> HandShakeType:
        """Parse a MySQL Handshake-packet."""
        res = {}
        res["protocol"] = struct.unpack("<xxxxB", packet[0:5])[0]
        if res["protocol"] != PROTOCOL_VERSION:
            raise DatabaseError(
                f"Protocol mismatch; server version = {res['protocol']}, "
                f"client version = {PROTOCOL_VERSION}"
            )
        packet, res["server_version_original"] = utils.read_string(
            packet[5:], end=b"\x00"
        )

        (
            res["server_threadid"],
            auth_data1,
            capabilities1,
            res["charset"],
            res["server_status"],
            capabilities2,
            auth_data_length,
        ) = struct.unpack("<I8sx2sBH2sBxxxxxxxxxx", packet[0:31])
        res["server_version_original"] = res["server_version_original"].decode()

        packet = packet[31:]

        capabilities = utils.intread(capabilities1 + capabilities2)
        auth_data2 = b""
        if capabilities & ClientFlag.SECURE_CONNECTION:
            size = min(13, auth_data_length - 8) if auth_data_length else 13
            auth_data2 = packet[0:size]
            packet = packet[size:]
            if auth_data2[-1] == 0:
                auth_data2 = auth_data2[:-1]

        if capabilities & ClientFlag.PLUGIN_AUTH:
            if b"\x00" not in packet and res["server_version_original"].startswith(
                "5.5.8"
            ):
                # MySQL server 5.5.8 has a bug where end byte is not send
                (packet, res["auth_plugin"]) = (b"", packet)
            else:
                (packet, res["auth_plugin"]) = utils.read_string(packet, end=b"\x00")
            res["auth_plugin"] = res["auth_plugin"].decode("utf-8")
        else:
            res["auth_plugin"] = "mysql_native_password"

        res["auth_data"] = auth_data1 + auth_data2
        res["capabilities"] = capabilities
        return res

    @staticmethod
    def parse_ok(packet: bytes) -> OkPacketType:
        """Parse a MySQL OK-packet"""
        if not packet[4] == 0:
            raise InterfaceError("Failed parsing OK packet (invalid).")

        ok_packet = {}
        try:
            ok_packet["field_count"] = struct.unpack("<xxxxB", packet[0:5])[0]
            packet, ok_packet["affected_rows"] = utils.read_lc_int(packet[5:])
            packet, ok_packet["insert_id"] = utils.read_lc_int(packet)
            (
                ok_packet["status_flag"],
                ok_packet["warning_count"],
            ) = struct.unpack("<HH", packet[0:4])
            packet = packet[4:]
            if packet:
                packet, ok_packet["info_msg"] = utils.read_lc_string(packet)
                ok_packet["info_msg"] = ok_packet["info_msg"].decode("utf-8")
        except ValueError as err:
            raise InterfaceError("Failed parsing OK packet.") from err
        return ok_packet

    @staticmethod
    def parse_column_count(packet: bytes) -> Optional[int]:
        """Parse a MySQL packet with the number of columns in result set"""
        try:
            count = utils.read_lc_int(packet[4:])[1]
            return count
        except (struct.error, ValueError) as err:
            raise InterfaceError("Failed parsing column count") from err

    @staticmethod
    def parse_column(packet: bytes, encoding: str = "utf-8") -> DescriptionType:
        """Parse a MySQL column-packet."""
        packet, _ = utils.read_lc_string(packet[4:])  # catalog
        packet, _ = utils.read_lc_string(packet)  # db
        packet, _ = utils.read_lc_string(packet)  # table
        packet, _ = utils.read_lc_string(packet)  # org_table
        packet, name = utils.read_lc_string(packet)  # name
        packet, _ = utils.read_lc_string(packet)  # org_name

        try:
            (
                charset,
                _,
                column_type,
                flags,
                _,
            ) = struct.unpack("<xHIBHBxx", packet)
        except struct.error:
            raise InterfaceError("Failed parsing column information") from None

        return (
            name.decode(encoding),
            column_type,
            None,  # display_size
            None,  # internal_size
            None,  # precision
            None,  # scale
            ~flags & FieldFlag.NOT_NULL,  # null_ok
            flags,  # MySQL specific
            charset,
        )

    def parse_eof(self, packet: bytes) -> EofPacketType:
        """Parse a MySQL EOF-packet"""
        if packet[4] == 0:
            # EOF packet deprecation
            return self.parse_ok(packet)

        err_msg = "Failed parsing EOF packet."
        res = {}
        try:
            unpacked = struct.unpack("<xxxBBHH", packet)
        except struct.error as err:
            raise InterfaceError(err_msg) from err

        if not (unpacked[1] == 254 and len(packet) <= 9):
            raise InterfaceError(err_msg)

        res["warning_count"] = unpacked[2]
        res["status_flag"] = unpacked[3]
        return res

    @staticmethod
    def parse_statistics(packet: bytes, with_header: bool = True) -> StatsPacketType:
        """Parse the statistics packet"""
        errmsg = "Failed getting COM_STATISTICS information"
        res: Dict[str, Union[int, Decimal]] = {}
        # Information is separated by 2 spaces
        pairs = [b""]
        lbl: StrOrBytes = b""
        if with_header:
            pairs = packet[4:].split(b"\x20\x20")
        else:
            pairs = packet.split(b"\x20\x20")
        for pair in pairs:
            try:
                lbl, val = [v.strip() for v in pair.split(b":", 2)]
            except ValueError as err:
                raise InterfaceError(errmsg) from err

            # It's either an integer or a decimal
            lbl = lbl.decode("utf-8")
            try:
                res[lbl] = int(val)
            except (KeyError, ValueError):
                try:
                    res[lbl] = Decimal(val.decode("utf-8"))
                except DecimalException as err:
                    raise InterfaceError(f"{errmsg} ({lbl}:{repr(val)})") from err
        return res

    def read_text_result(
        self,
        sock: MySQLSocket,
        version: Tuple[int, ...],
        count: int = 1,
        read_timeout: Optional[int] = None,
    ) -> Tuple[
        List[Tuple[Optional[bytes], ...]],
        Optional[EofPacketType],
    ]:
        """Read MySQL text result

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
            packet = sock.recv(read_timeout)
            if packet.startswith(b"\xff\xff\xff"):
                datas = [packet[4:]]
                packet = sock.recv(read_timeout)
                while packet.startswith(b"\xff\xff\xff"):
                    datas.append(packet[4:])
                    packet = sock.recv(read_timeout)
                datas.append(packet[4:])
                rowdata = utils.read_lc_string_list(b"".join(datas))
            elif packet[4] == 254 and packet[0] < 7:
                eof = self.parse_eof(packet)
                rowdata = None
            else:
                eof = None
                rowdata = utils.read_lc_string_list(bytes(packet[4:]))
            if eof is None and rowdata is not None:
                rows.append(rowdata)
            elif eof is None and rowdata is None:
                raise get_exception(packet)
            i += 1
        return rows, eof

    @staticmethod
    def _parse_binary_integer(
        packet: bytes, field: DescriptionType
    ) -> Tuple[bytes, int]:
        """Parse an integer from a binary packet"""
        if field[1] == FieldType.TINY:
            format_ = "<b"
            length = 1
        elif field[1] == FieldType.SHORT:
            format_ = "<h"
            length = 2
        elif field[1] in (FieldType.INT24, FieldType.LONG):
            format_ = "<i"
            length = 4
        elif field[1] == FieldType.LONGLONG:
            format_ = "<q"
            length = 8
        else:
            # length is undefined
            raise ValueError("Unknown integer type")

        if field[7] & FieldFlag.UNSIGNED:
            format_ = format_.upper()

        return (packet[length:], struct.unpack(format_, packet[0:length])[0])

    @staticmethod
    def _parse_binary_float(
        packet: bytes, field: DescriptionType
    ) -> Tuple[bytes, float]:
        """Parse a float/double from a binary packet"""
        if field[1] == FieldType.DOUBLE:
            length = 8
            format_ = "<d"
        else:
            length = 4
            format_ = "<f"

        return (packet[length:], struct.unpack(format_, packet[0:length])[0])

    @staticmethod
    def _parse_binary_new_decimal(
        packet: bytes, charset: str = "utf8"
    ) -> Tuple[bytes, Decimal]:
        """Parse a New Decimal from a binary packet"""
        (packet, value) = utils.read_lc_string(packet)
        return (packet, Decimal(value.decode(charset)))

    @staticmethod
    def _parse_binary_timestamp(
        packet: bytes,
        field_type: int,
    ) -> Tuple[bytes, Optional[Union[datetime.date, datetime.datetime]]]:
        """Parse a timestamp from a binary packet"""
        length = packet[0]
        value: Optional[Union[datetime.datetime, datetime.date]] = None
        if length == 4:
            year = struct.unpack("<H", packet[1:3])[0]
            month = packet[3]
            day = packet[4]
            if field_type in (FieldType.DATETIME, FieldType.TIMESTAMP):
                value = datetime.datetime(year=year, month=month, day=day)
            else:
                value = datetime.date(year=year, month=month, day=day)
        elif length >= 7:
            mcs = 0
            if length == 11:
                mcs = struct.unpack("<I", packet[8 : length + 1])[0]
            value = datetime.datetime(
                year=struct.unpack("<H", packet[1:3])[0],
                month=packet[3],
                day=packet[4],
                hour=packet[5],
                minute=packet[6],
                second=packet[7],
                microsecond=mcs,
            )

        return (packet[length + 1 :], value)

    @staticmethod
    def _parse_binary_time(packet: bytes) -> Tuple[bytes, datetime.timedelta]:
        """Parse a time value from a binary packet"""
        length = packet[0]
        if not length:
            return (packet[1:], datetime.timedelta())
        data = packet[1 : length + 1]
        mcs = 0
        if length > 8:
            mcs = struct.unpack("<I", data[8:])[0]
        days = struct.unpack("<I", data[1:5])[0]
        if data[0] == 1:
            days *= -1
        tmp = datetime.timedelta(
            days=days,
            seconds=data[7],
            microseconds=mcs,
            minutes=data[6],
            hours=data[5],
        )

        return (packet[length + 1 :], tmp)

    def _parse_binary_values(
        self,
        fields: List[DescriptionType],
        packet: bytes,
        charset: str = "utf-8",
    ) -> Tuple[BinaryProtocolType, ...]:
        """Parse values from a binary result packet"""
        null_bitmap_length = (len(fields) + 7 + 2) // 8
        null_bitmap = [int(i) for i in packet[0:null_bitmap_length]]
        packet = packet[null_bitmap_length:]

        values: List[Any] = []
        value: BinaryProtocolType = None
        for pos, field in enumerate(fields):
            if null_bitmap[int((pos + 2) / 8)] & (1 << (pos + 2) % 8):
                values.append(None)
                continue
            if field[1] in (
                FieldType.TINY,
                FieldType.SHORT,
                FieldType.INT24,
                FieldType.LONG,
                FieldType.LONGLONG,
            ):
                packet, value = self._parse_binary_integer(packet, field)
                values.append(value)
            elif field[1] in (FieldType.DOUBLE, FieldType.FLOAT):
                packet, value = self._parse_binary_float(packet, field)
                values.append(value)
            elif field[1] in (FieldType.DECIMAL, FieldType.NEWDECIMAL):
                packet, value = self._parse_binary_new_decimal(packet, charset)
                values.append(value)
            elif field[1] in (
                FieldType.DATETIME,
                FieldType.DATE,
                FieldType.TIMESTAMP,
            ):
                (packet, value) = self._parse_binary_timestamp(packet, field[1])
                values.append(value)
            elif field[1] == FieldType.TIME:
                (packet, value) = self._parse_binary_time(packet)
                values.append(value)
            elif field[1] == FieldType.VECTOR:
                # pylint: disable=protected-access
                (packet, value) = utils.read_lc_string(packet)
                values.append(MySQLConverter._vector_to_python(value))
            elif field[7] == FieldFlag.BINARY or field[8] == 63:  # "binary" charset
                (packet, value) = utils.read_lc_string(packet)
                values.append(value)
            else:
                (packet, value) = utils.read_lc_string(packet)
                try:
                    values.append(value.decode(charset))
                except UnicodeDecodeError:
                    values.append(value)

        return tuple(values)

    def read_binary_result(
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
        """Read MySQL binary protocol result

        Reads all or given number of binary resultset rows from the socket.
        """
        rows = []
        eof = None
        values = None
        i = 0
        while True:
            if eof is not None:
                break
            if i == count:
                break
            packet = bytes(sock.recv(read_timeout))
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

    @staticmethod
    def parse_binary_prepare_ok(packet: bytes) -> Dict[str, int]:
        """Parse a MySQL Binary Protocol OK packet."""
        if not packet[4] == 0:
            raise InterfaceError("Failed parsing Binary OK packet")

        ok_pkt = {}
        try:
            packet, ok_pkt["statement_id"] = utils.read_int(packet[5:], 4)
            packet, ok_pkt["num_columns"] = utils.read_int(packet, 2)
            packet, ok_pkt["num_params"] = utils.read_int(packet, 2)
            packet = packet[1:]  # Filler 1 * \x00
            packet, ok_pkt["warning_count"] = utils.read_int(packet, 2)
        except ValueError as err:
            raise InterfaceError("Failed parsing Binary OK packet") from err

        return ok_pkt

    @staticmethod
    def prepare_binary_integer(value: int) -> Tuple[bytes, int, int]:
        """Prepare an integer for the MySQL binary protocol"""
        field_type = None
        flags = 0
        if value < 0:
            if value >= -128:
                format_ = "<b"
                field_type = FieldType.TINY
            elif value >= -32768:
                format_ = "<h"
                field_type = FieldType.SHORT
            elif value >= -2147483648:
                format_ = "<i"
                field_type = FieldType.LONG
            else:
                format_ = "<q"
                field_type = FieldType.LONGLONG
        else:
            flags = 128
            if value <= 255:
                format_ = "<B"
                field_type = FieldType.TINY
            elif value <= 65535:
                format_ = "<H"
                field_type = FieldType.SHORT
            elif value <= 4294967295:
                format_ = "<I"
                field_type = FieldType.LONG
            else:
                field_type = FieldType.LONGLONG
                format_ = "<Q"
        return (struct.pack(format_, value), field_type, flags)

    @staticmethod
    def prepare_binary_timestamp(
        value: Union[datetime.date, datetime.datetime],
    ) -> Tuple[bytes, int]:
        """Prepare a timestamp object for the MySQL binary protocol

        This method prepares a timestamp of type datetime.datetime or
        datetime.date for sending over the MySQL binary protocol.
        A tuple is returned with the prepared value and field type
        as elements.

        Raises ValueError when the argument value is of invalid type.

        Returns a tuple.
        """
        if isinstance(value, datetime.datetime):
            field_type = FieldType.DATETIME
        elif isinstance(value, datetime.date):
            field_type = FieldType.DATE
        else:
            raise ValueError("Argument must a datetime.datetime or datetime.date")

        chunks = [
            utils.int2store(value.year),
            utils.int1store(value.month),
            utils.int1store(value.day),
        ]

        if isinstance(value, datetime.datetime):
            chunks.extend(
                [
                    utils.int1store(value.hour),
                    utils.int1store(value.minute),
                    utils.int1store(value.second),
                ]
            )
            if value.microsecond > 0:
                chunks.append(utils.int4store(value.microsecond))

        packed = b"".join(chunks)

        return utils.int1store(len(packed)) + packed, field_type

    @staticmethod
    def prepare_binary_time(
        value: Union[datetime.timedelta, datetime.time],
    ) -> Tuple[bytes, int]:
        """Prepare a time object for the MySQL binary protocol

        This method prepares a time object of type datetime.timedelta or
        datetime.time for sending over the MySQL binary protocol.
        A tuple is returned with the prepared value and field type
        as elements.

        Raises ValueError when the argument value is of invalid type.

        Returns a tuple.
        """
        if not isinstance(value, (datetime.timedelta, datetime.time)):
            raise ValueError("Argument must a datetime.timedelta or datetime.time")

        field_type = FieldType.TIME
        negative = 0
        mcs = None
        chunks: Deque[bytes] = deque([])

        if isinstance(value, datetime.timedelta):
            if value.days < 0:
                negative = 1
            (hours, remainder) = divmod(value.seconds, 3600)
            (mins, secs) = divmod(remainder, 60)
            chunks.extend(
                [
                    utils.int4store(abs(value.days)),
                    utils.int1store(hours),
                    utils.int1store(mins),
                    utils.int1store(secs),
                ]
            )
            mcs = value.microseconds
        else:
            chunks.extend(
                [
                    utils.int4store(0),
                    utils.int1store(value.hour),
                    utils.int1store(value.minute),
                    utils.int1store(value.second),
                ]
            )
            mcs = value.microsecond
        if mcs:
            chunks.append(utils.int4store(mcs))

        chunks.appendleft(utils.int1store(negative))

        packed = b"".join(chunks)

        return utils.int1store(len(packed)) + packed, field_type

    @staticmethod
    def prepare_stmt_send_long_data(statement: int, param: int, data: bytes) -> bytes:
        """Prepare long data for prepared statements

        Returns a string.
        """
        return b"".join([utils.int4store(statement), utils.int2store(param), data])

    def make_stmt_execute(
        self,
        statement_id: int,
        data: Sequence[BinaryProtocolType] = (),
        parameters: Sequence = (),
        flags: int = 0,
        long_data_used: Optional[Dict[int, Tuple[bool]]] = None,
        charset: str = "utf8",
        query_attrs: Optional[List[Tuple[str, BinaryProtocolType]]] = None,
        converter_str_fallback: bool = False,
    ) -> bytes:
        """Make a MySQL packet with the Statement Execute command"""
        iteration_count = 1
        null_bitmap = [0] * ((len(data) + 7) // 8)
        values: List[bytes] = []
        types: List[bytes] = []
        packed = b""
        data_len = len(data)
        query_attr_names: List[bytes] = []
        flags = flags if not query_attrs else flags + PARAMETER_COUNT_AVAILABLE

        if charset == "utf8mb4":
            charset = "utf8"

        if long_data_used is None:
            long_data_used = {}

        if query_attrs:
            data = list(data)
            for _, attr_val in query_attrs:
                data.append(attr_val)
            null_bitmap = [0] * ((len(data) + 7) // 8)

        if parameters or data:
            if data_len != len(parameters):
                raise InterfaceError(
                    "Failed executing prepared statement: data values does not"
                    " match number of parameters"
                )
            for pos, value in enumerate(data):
                _flags = 0
                if value is None:
                    null_bitmap[(pos // 8)] |= 1 << (pos % 8)
                    types.append(
                        utils.int1store(FieldType.NULL) + utils.int1store(_flags)
                    )
                    continue
                if pos in long_data_used:
                    if long_data_used[pos][0]:
                        # We suppose binary data
                        field_type = FieldType.BLOB
                    else:
                        # We suppose text data
                        field_type = FieldType.STRING
                elif isinstance(value, int):
                    (
                        packed,
                        field_type,
                        _flags,
                    ) = self.prepare_binary_integer(value)
                    values.append(packed)
                elif isinstance(value, str):
                    value = value.encode(charset)
                    values.append(utils.lc_int(len(value)) + value)
                    field_type = FieldType.STRING
                elif isinstance(value, bytes):
                    values.append(utils.lc_int(len(value)) + value)
                    field_type = FieldType.STRING
                elif isinstance(value, Decimal):
                    values.append(
                        utils.lc_int(len(str(value).encode(charset)))
                        + str(value).encode(charset)
                    )
                    field_type = FieldType.DECIMAL
                elif isinstance(value, float):
                    values.append(struct.pack("<d", value))
                    field_type = FieldType.DOUBLE
                elif isinstance(value, (datetime.datetime, datetime.date)):
                    (packed, field_type) = self.prepare_binary_timestamp(value)
                    values.append(packed)
                elif isinstance(value, (datetime.timedelta, datetime.time)):
                    (packed, field_type) = self.prepare_binary_time(value)
                    values.append(packed)
                elif converter_str_fallback:
                    value = str(value).encode(charset)
                    values.append(utils.lc_int(len(value)) + value)
                    field_type = FieldType.STRING
                else:
                    raise ProgrammingError(
                        "MySQL binary protocol can not handle "
                        f"'{value.__class__.__name__}' objects"
                    )
                types.append(utils.int1store(field_type) + utils.int1store(_flags))
                if query_attrs and pos + 1 > data_len:
                    name = query_attrs[pos - data_len][0].encode(charset)
                    query_attr_names.append(utils.lc_int(len(name)) + name)
        packet = [
            utils.int4store(statement_id),
            utils.int1store(flags),
            utils.int4store(iteration_count),
        ]

        # if (num_params > 0 || (CLIENT_QUERY_ATTRIBUTES \
        #                        && (flags & PARAMETER_COUNT_AVAILABLE)) {
        if query_attrs is not None:
            parameter_count = data_len + len(query_attrs)
        else:
            parameter_count = data_len
        if parameter_count:
            # if CLIENT_QUERY_ATTRIBUTES is on
            if query_attrs is not None:
                packet.append(utils.lc_int(parameter_count))

            packet.extend([struct.pack("B", bit) for bit in null_bitmap])
            packet.append(utils.int1store(1))

            count = 0
            for a_type in types:
                packet.append(a_type)
                # if CLIENT_QUERY_ATTRIBUTES is on {
                #    string<lenenc>    parameter_name    Name of the parameter
                # or empty if not present
                # } if CLIENT_QUERY_ATTRIBUTES is on
                if query_attrs is not None:
                    if count + 1 > data_len:
                        packet.append(query_attr_names[count - data_len])
                    else:
                        packet.append(b"\x00")
                count += 1

            for a_value in values:
                packet.append(a_value)

        return b"".join(packet)
