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

# pylint: disable=dangerous-default-value

"""Module implementing low-level socket communication with MySQL servers."""


__all__ = ["MySQLTcpSocket", "MySQLUnixSocket"]

import asyncio
import struct
import zlib

try:
    import ssl

    TLS_VERSIONS = {
        "TLSv1": ssl.PROTOCOL_TLSv1,
        "TLSv1.1": ssl.PROTOCOL_TLSv1_1,
        "TLSv1.2": ssl.PROTOCOL_TLSv1_2,
        "TLSv1.3": ssl.PROTOCOL_TLS,
    }
except ImportError:
    ssl = None

from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Deque, List, Optional, Tuple

from ..errors import (
    InterfaceError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    ReadTimeoutError,
    WriteTimeoutError,
)
from ..network import (
    COMPRESSED_PACKET_HEADER_LENGTH,
    MAX_PAYLOAD_LENGTH,
    MIN_COMPRESS_LENGTH,
    PACKET_HEADER_LENGTH,
)
from .utils import StreamWriter, open_connection


def _strioerror(err: IOError) -> str:
    """Reformat the IOError error message.

    This function reformats the IOError error message.
    """
    return str(err) if not err.errno else f"{err.errno} {err.strerror}"


class NetworkBroker(ABC):
    """Broker class interface.

    The network object is a broker used as a delegate by a socket object. Whenever the
    socket wants to deliver or get packets to or from the MySQL server it needs to rely
    on its network broker (netbroker).

    The netbroker sends `payloads` and receives `packets`.

    A packet is a bytes sequence, it has a header and body (referred to as payload).
    The first `PACKET_HEADER_LENGTH` or `COMPRESSED_PACKET_HEADER_LENGTH`
    (as appropriate) bytes correspond to the `header`, the remaining ones represent the
    `payload`.

    The maximum payload length allowed to be sent per packet to the server is
    `MAX_PAYLOAD_LENGTH`. When  `send` is called with a payload whose length is greater
    than `MAX_PAYLOAD_LENGTH` the netbroker breaks it down into packets, so the caller
    of `send` can provide payloads of arbitrary length.

    Finally, data received by the netbroker comes directly from the server, expect to
    get a packet for each call to `recv`. The received packet contains a header and
    payload, the latter respecting `MAX_PAYLOAD_LENGTH`.
    """

    @abstractmethod
    async def write(
        self,
        writer: StreamWriter,
        address: str,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> None:
        """Send `payload` to the MySQL server.

        If provided a payload whose length is greater than `MAX_PAYLOAD_LENGTH`, it is
        broken down into packets.

        Args:
            sock: Object holding the socket connection.
            address: Socket's location.
            payload: Packet's body to send.
            packet_number: Sequence id (packet ID) to attach to the header when sending
                           plain packets.
            compressed_packet_number: Same as `packet_number` but used when sending
                                      compressed packets.
            write_timeout: Timeout in seconds before which sending a packet to the server
                           should finish else WriteTimeoutError is raised.


        Raises:
            :class:`OperationalError`: If something goes wrong while sending packets to
                                       the MySQL server.
        """

    @abstractmethod
    async def read(
        self,
        reader: asyncio.StreamReader,
        address: str,
        read_timeout: Optional[int] = None,
    ) -> bytearray:
        """Get the next available packet from the MySQL server.

        Args:
            sock: Object holding the socket connection.
            address: Socket's location.
            read_timeout: Timeout in seconds before which reading a packet from the server
                          should finish.

        Returns:
            packet: A packet from the MySQL server.

        Raises:
            :class:`OperationalError`: If something goes wrong while receiving packets
                                       from the MySQL server.
            :class:`ReadTimeoutError`: If the time to receive a packet from the server takes
                                       longer than `read_timeout`.
            :class:`InterfaceError`: If something goes wrong while receiving packets
                                     from the MySQL server.
        """


class NetworkBrokerPlain(NetworkBroker):
    """Broker class for MySQL socket communication."""

    def __init__(self) -> None:
        self._pktnr: int = -1  # packet number

    @staticmethod
    def get_header(pkt: bytes) -> Tuple[int, int]:
        """Recover the header information from a packet."""
        if len(pkt) < PACKET_HEADER_LENGTH:
            raise ValueError("Can't recover header info from an incomplete packet")

        pll, seqid = (
            struct.unpack("<I", pkt[0:3] + b"\x00")[0],
            pkt[3],
        )
        # payload length, sequence id
        return pll, seqid

    def _set_next_pktnr(self, next_id: Optional[int] = None) -> None:
        """Set the given packet id, if any, else increment packet id."""
        if next_id is None:
            self._pktnr += 1
        else:
            self._pktnr = next_id
        self._pktnr %= 256

    async def _write_pkt(
        self,
        writer: StreamWriter,
        address: str,
        pkt: bytes,
    ) -> None:
        """Write packet to the comm channel."""
        try:
            writer.write(pkt)
            await writer.drain()
        except IOError as err:
            raise OperationalError(
                errno=2055, values=(address, _strioerror(err))
            ) from err
        except AttributeError as err:
            raise OperationalError(errno=2006) from err

    async def _read_chunk(
        self,
        reader: asyncio.StreamReader,
        size: int = 0,
        read_timeout: Optional[int] = None,
    ) -> bytearray:
        """Read `size` bytes from the comm channel."""
        try:
            pkt = bytearray(b"")
            while len(pkt) < size:
                chunk = await asyncio.wait_for(
                    reader.read(size - len(pkt)), read_timeout
                )
                if not chunk:
                    raise InterfaceError(errno=2013)
                pkt += chunk
            return pkt
        except (asyncio.CancelledError, asyncio.TimeoutError) as err:
            raise ReadTimeoutError(errno=3024) from err

    async def write(
        self,
        writer: StreamWriter,
        address: str,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> None:
        """Send payload to the MySQL server.

        If provided a payload whose length is greater than `MAX_PAYLOAD_LENGTH`, it is
        broken down into packets.
        """
        self._set_next_pktnr(packet_number)
        # If the payload is larger than or equal to MAX_PAYLOAD_LENGTH the length is
        # set to 2^24 - 1 (ff ff ff) and additional packets are sent with the rest of
        # the payload until the payload of a packet is less than MAX_PAYLOAD_LENGTH.
        offset = 0
        try:
            for _ in range(len(payload) // MAX_PAYLOAD_LENGTH):
                # payload_len, sequence_id, payload
                await asyncio.wait_for(
                    self._write_pkt(
                        writer,
                        address,
                        b"\xff" * 3
                        + struct.pack("<B", self._pktnr)
                        + payload[offset : offset + MAX_PAYLOAD_LENGTH],
                    ),
                    write_timeout,
                )
                self._set_next_pktnr()
                offset += MAX_PAYLOAD_LENGTH
            await asyncio.wait_for(
                self._write_pkt(
                    writer,
                    address,
                    struct.pack("<I", len(payload) - offset)[0:3]
                    + struct.pack("<B", self._pktnr)
                    + payload[offset:],
                ),
                write_timeout,
            )
        except (asyncio.CancelledError, asyncio.TimeoutError) as err:
            raise WriteTimeoutError(errno=3024) from err

    async def read(
        self,
        reader: asyncio.StreamReader,
        address: str,
        read_timeout: Optional[int] = None,
    ) -> bytearray:
        """Receive `one` packet from the MySQL server."""
        try:
            # Read the header of the MySQL packet.
            header = await self._read_chunk(reader, PACKET_HEADER_LENGTH, read_timeout)

            # Pull the payload length and sequence id.
            payload_len, self._pktnr = self.get_header(header)

            # Read the payload, and return packet.
            return header + await self._read_chunk(reader, payload_len, read_timeout)
        except IOError as err:
            raise OperationalError(
                errno=2055, values=(address, _strioerror(err))
            ) from err


class NetworkBrokerCompressed(NetworkBrokerPlain):
    """Broker class for MySQL socket communication."""

    def __init__(self) -> None:
        super().__init__()
        self._compressed_pktnr = -1
        self._queue_read: Deque[bytearray] = deque()

    @staticmethod
    def _prepare_packets(payload: bytes, pktnr: int) -> List[bytes]:
        """Prepare a payload for sending to the MySQL server."""
        offset = 0
        pkts = []

        # If the payload is larger than or equal to MAX_PAYLOAD_LENGTH the length is
        # set to 2^24 - 1 (ff ff ff) and additional packets are sent with the rest of
        # the payload until the payload of a packet is less than MAX_PAYLOAD_LENGTH.
        for _ in range(len(payload) // MAX_PAYLOAD_LENGTH):
            # payload length + sequence id + payload
            pkts.append(
                b"\xff" * 3
                + struct.pack("<B", pktnr)
                + payload[offset : offset + MAX_PAYLOAD_LENGTH]
            )
            pktnr = (pktnr + 1) % 256
            offset += MAX_PAYLOAD_LENGTH
        pkts.append(
            struct.pack("<I", len(payload) - offset)[0:3]
            + struct.pack("<B", pktnr)
            + payload[offset:]
        )
        return pkts

    @staticmethod
    def get_header(pkt: bytes) -> Tuple[int, int, int]:  # type: ignore[override]
        """Recover the header information from a packet."""
        if len(pkt) < COMPRESSED_PACKET_HEADER_LENGTH:
            raise ValueError("Can't recover header info from an incomplete packet")

        compressed_pll, seqid, uncompressed_pll = (
            struct.unpack("<I", pkt[0:3] + b"\x00")[0],
            pkt[3],
            struct.unpack("<I", pkt[4:7] + b"\x00")[0],
        )
        # compressed payload length, sequence id, uncompressed payload length
        return compressed_pll, seqid, uncompressed_pll

    def _set_next_compressed_pktnr(self, next_id: Optional[int] = None) -> None:
        """Set the given packet id, if any, else increment packet id."""
        if next_id is None:
            self._compressed_pktnr += 1
        else:
            self._compressed_pktnr = next_id
        self._compressed_pktnr %= 256

    async def _write_pkt(
        self,
        writer: StreamWriter,
        address: str,
        pkt: bytes,
    ) -> None:
        """Compress packet and write it to the comm channel."""
        compressed_pkt = zlib.compress(pkt)
        pkt = (
            struct.pack("<I", len(compressed_pkt))[0:3]
            + struct.pack("<B", self._compressed_pktnr)
            + struct.pack("<I", len(pkt))[0:3]
            + compressed_pkt
        )
        return await super()._write_pkt(writer, address, pkt)

    async def write(
        self,
        writer: StreamWriter,
        address: str,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> None:
        """Send `payload` as compressed packets to the MySQL server.

        If provided a payload whose length is greater than `MAX_PAYLOAD_LENGTH`, it is
        broken down into packets.
        """
        # Get next packet numbers.
        self._set_next_pktnr(packet_number)
        self._set_next_compressed_pktnr(compressed_packet_number)
        try:
            payload_prep = bytearray(b"").join(
                self._prepare_packets(payload, self._pktnr)
            )
            if len(payload) >= MAX_PAYLOAD_LENGTH - PACKET_HEADER_LENGTH:
                # Sending a MySQL payload of the size greater or equal to 2^24 - 5 via
                # compression leads to at least one extra compressed packet WHY? let's say
                # len(payload) is MAX_PAYLOAD_LENGTH - 3; when preparing the payload, a
                # header of size PACKET_HEADER_LENGTH is pre-appended to the payload.
                # This means that len(payload_prep) is
                # MAX_PAYLOAD_LENGTH - 3 + PACKET_HEADER_LENGTH = MAX_PAYLOAD_LENGTH + 1
                # surpassing the maximum allowed payload size per packet.
                offset = 0

                # Send several MySQL packets.
                for _ in range(len(payload_prep) // MAX_PAYLOAD_LENGTH):
                    await asyncio.wait_for(
                        self._write_pkt(
                            writer,
                            address,
                            payload_prep[offset : offset + MAX_PAYLOAD_LENGTH],
                        ),
                        write_timeout,
                    )
                    self._set_next_compressed_pktnr()
                    offset += MAX_PAYLOAD_LENGTH
                await asyncio.wait_for(
                    self._write_pkt(writer, address, payload_prep[offset:]),
                    write_timeout,
                )
            else:
                # Send one MySQL packet.
                # For small packets it may be too costly to compress the packet.
                # Usually payloads less than 50 bytes (MIN_COMPRESS_LENGTH) aren't
                # compressed (see MySQL source code Documentation).
                if len(payload) > MIN_COMPRESS_LENGTH:
                    # Perform compression.
                    await asyncio.wait_for(
                        self._write_pkt(writer, address, payload_prep), write_timeout
                    )
                else:
                    # Skip compression.
                    await asyncio.wait_for(
                        super()._write_pkt(
                            writer,
                            address,
                            struct.pack("<I", len(payload_prep))[0:3]
                            + struct.pack("<B", self._compressed_pktnr)
                            + struct.pack("<I", 0)[0:3]
                            + payload_prep,
                        ),
                        write_timeout,
                    )
        except (asyncio.CancelledError, asyncio.TimeoutError) as err:
            raise WriteTimeoutError(errno=3024) from err

    async def _read_compressed_pkt(
        self,
        reader: asyncio.StreamReader,
        compressed_pll: int,
        read_timeout: Optional[int] = None,
    ) -> None:
        """Handle reading of a compressed packet."""
        # compressed_pll stands for compressed payload length.
        pkt = bytearray(
            zlib.decompress(
                await super()._read_chunk(reader, compressed_pll, read_timeout)
            )
        )
        offset = 0
        while offset < len(pkt):
            # pll stands for payload length
            pll = struct.unpack(
                "<I", pkt[offset : offset + PACKET_HEADER_LENGTH - 1] + b"\x00"
            )[0]
            if PACKET_HEADER_LENGTH + pll > len(pkt) - offset:
                # More bytes need to be consumed.
                # Read the header of the next MySQL packet.
                header = await super()._read_chunk(
                    reader, COMPRESSED_PACKET_HEADER_LENGTH, read_timeout
                )

                # compressed payload length, sequence id, uncompressed payload length.
                (
                    compressed_pll,
                    self._compressed_pktnr,
                    uncompressed_pll,
                ) = self.get_header(header)
                compressed_pkt = await super()._read_chunk(
                    reader, compressed_pll, read_timeout
                )

                # Recalling that if uncompressed payload length == 0, the packet comes
                # in uncompressed, so no decompression is needed.
                pkt += (
                    compressed_pkt
                    if uncompressed_pll == 0
                    else zlib.decompress(compressed_pkt)
                )

            self._queue_read.append(pkt[offset : offset + PACKET_HEADER_LENGTH + pll])
            offset += PACKET_HEADER_LENGTH + pll

    async def read(
        self,
        reader: asyncio.StreamReader,
        address: str,
        read_timeout: Optional[int] = None,
    ) -> bytearray:
        """Receive `one` or `several` packets from the MySQL server, enqueue them, and
        return the packet at the head.
        """

        if not self._queue_read:
            try:
                # Read the header of the next MySQL packet.
                header = await super()._read_chunk(
                    reader, COMPRESSED_PACKET_HEADER_LENGTH, read_timeout
                )

                # compressed payload length, sequence id, uncompressed payload length
                (
                    compressed_pll,
                    self._compressed_pktnr,
                    uncompressed_pll,
                ) = self.get_header(header)

                if uncompressed_pll == 0:
                    # Packet is not compressed, so just store it.
                    self._queue_read.append(
                        await super()._read_chunk(reader, compressed_pll, read_timeout)
                    )
                else:
                    # Packet comes in compressed, further action is needed.
                    await self._read_compressed_pkt(
                        reader, compressed_pll, read_timeout
                    )
            except IOError as err:
                raise OperationalError(
                    errno=2055, values=(address, _strioerror(err))
                ) from err

        if not self._queue_read:
            return None

        pkt = self._queue_read.popleft()
        self._pktnr = pkt[3]

        return pkt


class MySQLSocket(ABC):
    """MySQL socket communication interface.

    Examples:
        Subclasses: network.MySQLTCPSocket and network.MySQLUnixSocket.
    """

    def __init__(self) -> None:
        """Network layer where transactions are made with plain (uncompressed) packets
        is enabled by default.
        """
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[StreamWriter] = None
        self._connection_timeout: Optional[int] = None
        self._address: Optional[str] = None
        self._netbroker: NetworkBroker = NetworkBrokerPlain()
        self._is_connected: bool = False

    @property
    def address(self) -> str:
        """Socket location."""
        return self._address

    @abstractmethod
    async def open_connection(self, **kwargs: Any) -> None:
        """Open the socket."""

    async def close_connection(self) -> None:
        """Close the connection."""
        if self._writer:
            try:
                self._writer.close()
                # Without transport.abort(), an error is raised when using SSL
                if self._writer.transport is not None:
                    self._writer.transport.abort()
                await self._writer.wait_closed()
            except Exception as _:  # pylint: disable=broad-exception-caught)
                # we can ignore issues like ConnectionRefused or ConnectionAborted
                # as these instances might popup if the connection was closed due to timeout issues
                pass
        self._is_connected = False

    def is_connected(self) -> bool:
        """Check if the socket is connected.

        Return:
            bool: Returns `True` if the socket is connected to MySQL server.
        """
        return self._is_connected

    def set_connection_timeout(self, timeout: int) -> None:
        """Set the connection timeout."""
        self._connection_timeout = timeout

    def switch_to_compressed_mode(self) -> None:
        """Enable network layer where transactions are made with compressed packets."""
        self._netbroker = NetworkBrokerCompressed()

    async def switch_to_ssl(self, ssl_context: ssl.SSLContext) -> None:
        """Upgrade an existing stream-based connection to TLS.

        The `start_tls()` method from `asyncio.streams.StreamWriter` is only available
        in Python 3.11. This method is used as a workaround.

        The MySQL TLS negotiation happens in the middle of the TCP connection.
        Therefore, passing a socket to open connection will cause it to negotiate
        TLS on an existing connection.

        Args:
            ssl_context: The SSL Context to be used.

        Raises:
            RuntimeError: If the transport does not expose the socket instance.
        """
        # Ensure that self._writer is already created
        assert self._writer is not None

        socket = self._writer.transport.get_extra_info("socket")
        if socket.family == 1:  # socket.AF_UNIX
            raise ProgrammingError("SSL is not supported when using Unix sockets")

        await self._writer.start_tls(ssl_context)

    async def write(
        self,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> None:
        """Send packets to the MySQL server."""
        await self._netbroker.write(
            self._writer,
            self.address,
            payload,
            packet_number=packet_number,
            compressed_packet_number=compressed_packet_number,
            write_timeout=write_timeout,
        )

    async def read(self, read_timeout: Optional[int] = None) -> bytearray:
        """Read packets from the MySQL server."""
        return await self._netbroker.read(self._reader, self.address, read_timeout)

    def build_ssl_context(
        self,
        ssl_ca: Optional[str] = None,
        ssl_cert: Optional[str] = None,
        ssl_key: Optional[str] = None,
        ssl_verify_cert: Optional[bool] = False,
        ssl_verify_identity: Optional[bool] = False,
        tls_versions: Optional[List[str]] = [],
        tls_cipher_suites: Optional[List[str]] = [],
    ) -> ssl.SSLContext:
        """Build a SSLContext."""
        tls_version: Optional[str] = None

        if not self._reader:
            raise InterfaceError(errno=2048)

        if ssl is None:
            raise RuntimeError("Python installation has no SSL support")

        try:
            if tls_versions:
                tls_versions.sort(reverse=True)
                tls_version = tls_versions[0]
                ssl_protocol = TLS_VERSIONS[tls_version]
                context = ssl.SSLContext(ssl_protocol)

                if tls_version == "TLSv1.3":
                    if "TLSv1.2" not in tls_versions:
                        context.options |= ssl.OP_NO_TLSv1_2
                    if "TLSv1.1" not in tls_versions:
                        context.options |= ssl.OP_NO_TLSv1_1
                    if "TLSv1" not in tls_versions:
                        context.options |= ssl.OP_NO_TLSv1
            else:
                context = ssl.create_default_context()

            context.check_hostname = ssl_verify_identity

            if ssl_verify_cert:
                context.verify_mode = ssl.CERT_REQUIRED
            elif ssl_verify_identity:
                context.verify_mode = ssl.CERT_OPTIONAL
            else:
                context.verify_mode = ssl.CERT_NONE

            context.load_default_certs()

            if ssl_ca:
                try:
                    context.load_verify_locations(ssl_ca)
                except (IOError, ssl.SSLError) as err:
                    raise InterfaceError(f"Invalid CA Certificate: {err}") from err
            if ssl_cert:
                try:
                    context.load_cert_chain(ssl_cert, ssl_key)
                except (IOError, ssl.SSLError) as err:
                    raise InterfaceError(f"Invalid Certificate/Key: {err}") from err

            # TLSv1.3 ciphers cannot be disabled with `SSLContext.set_ciphers(...)`,
            # see https://docs.python.org/3/library/ssl.html#ssl.SSLContext.set_ciphers.
            if tls_cipher_suites and tls_version == "TLSv1.2":
                context.set_ciphers(":".join(tls_cipher_suites))

            return context
        except NameError as err:
            raise NotSupportedError("Python installation has no SSL support") from err
        except (
            IOError,
            NotImplementedError,
            ssl.CertificateError,
            ssl.SSLError,
        ) as err:
            raise InterfaceError(str(err)) from err


class MySQLTcpSocket(MySQLSocket):
    """MySQL socket class using TCP/IP.

    Args:
        host: MySQL host name.
        port: MySQL port.
        force_ipv6: Force IPv6 usage.
    """

    def __init__(
        self, host: str = "127.0.0.1", port: int = 3306, force_ipv6: bool = False
    ):
        super().__init__()
        self._host: str = host
        self._port: int = port
        self._force_ipv6: bool = force_ipv6
        self._address: str = f"{host}:{port}"

    async def open_connection(self, **kwargs: Any) -> None:
        """Open TCP/IP connection."""
        self._reader, self._writer = await open_connection(
            host=self._host, port=self._port, **kwargs
        )
        self._is_connected = True


class MySQLUnixSocket(MySQLSocket):
    """MySQL socket class using UNIX sockets.

    Args:
        unix_socket: UNIX socket file path.
    """

    def __init__(self, unix_socket: str = "/tmp/mysql.sock"):
        super().__init__()
        self._address: str = unix_socket

    async def open_connection(self, **kwargs: Any) -> None:
        """Open UNIX socket connection."""
        (
            self._reader,
            self._writer,
        ) = await asyncio.open_unix_connection(  # type: ignore[assignment]
            path=self._address, **kwargs
        )
        self._is_connected = True
