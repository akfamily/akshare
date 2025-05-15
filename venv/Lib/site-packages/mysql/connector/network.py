# Copyright (c) 2012, 2025, Oracle and/or its affiliates.
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

"""Module implementing low-level socket communication with MySQL servers."""

# pylint: disable=overlapping-except

import socket
import struct
import warnings
import zlib

from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Deque, List, Optional, Tuple, Union

try:
    import ssl

    TLS_VERSIONS = {
        "TLSv1": ssl.PROTOCOL_TLSv1,
        "TLSv1.1": ssl.PROTOCOL_TLSv1_1,
        "TLSv1.2": ssl.PROTOCOL_TLSv1_2,
        "TLSv1.3": ssl.PROTOCOL_TLS,
    }
    TLS_V1_3_SUPPORTED = hasattr(ssl, "HAS_TLSv1_3") and ssl.HAS_TLSv1_3
except ImportError:
    # If import fails, we don't have SSL support.
    TLS_V1_3_SUPPORTED = False
    ssl = None

from .errors import (
    ConnectionTimeoutError,
    InterfaceError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    ReadTimeoutError,
    WriteTimeoutError,
)

MIN_COMPRESS_LENGTH = 50
MAX_PAYLOAD_LENGTH = 2**24 - 1
PACKET_HEADER_LENGTH = 4
COMPRESSED_PACKET_HEADER_LENGTH = 7


def _strioerror(err: IOError) -> str:
    """Reformat the IOError error message.

    This function reformats the IOError error message.
    """
    return str(err) if not err.errno else f"Errno {err.errno}: {err.strerror}"


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
    def send(
        self,
        sock: socket.socket,
        address: str,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
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

        Raises:
            :class:`OperationalError`: If something goes wrong while sending packets to
                                       the MySQL server.
        """

    @abstractmethod
    def recv(self, sock: socket.socket, address: str) -> bytearray:
        """Get the next available packet from the MySQL server.

        Args:
            sock: Object holding the socket connection.
            address: Socket's location.

        Returns:
            packet: A packet from the MySQL server.

        Raises:
            :class:`OperationalError`: If something goes wrong while receiving packets
                                       from the MySQL server.
            :class:`InterfaceError`: If something goes wrong while receiving packets
                                     from the MySQL server.
        """


class NetworkBrokerPlain(NetworkBroker):
    """Broker class for MySQL socket communication."""

    def __init__(self) -> None:
        self._pktnr: int = -1  # packet number

    def _set_next_pktnr(self) -> None:
        """Increment packet id."""
        self._pktnr = (self._pktnr + 1) % 256

    def _send_pkt(self, sock: socket.socket, address: str, pkt: bytes) -> None:
        """Write packet to the comm channel."""
        try:
            sock.sendall(pkt)
        except (socket.timeout, TimeoutError) as err:
            raise WriteTimeoutError(errno=3024) from err
        except IOError as err:
            raise OperationalError(
                errno=2055, values=(address, _strioerror(err))
            ) from err
        except AttributeError as err:
            raise OperationalError(errno=2006) from err

    def _recv_chunk(self, sock: socket.socket, size: int = 0) -> bytearray:
        """Read `size` bytes from the comm channel."""
        pkt = bytearray(size)
        pkt_view = memoryview(pkt)
        while size:
            read = sock.recv_into(pkt_view, size)
            if read == 0 and size > 0:
                raise InterfaceError(errno=2013)
            pkt_view = pkt_view[read:]
            size -= read
        return pkt

    def send(
        self,
        sock: socket.socket,
        address: str,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
    ) -> None:
        """Send payload to the MySQL server.

        If provided a payload whose length is greater than `MAX_PAYLOAD_LENGTH`, it is
        broken down into packets.
        """
        if packet_number is None:
            self._set_next_pktnr()
        else:
            self._pktnr = packet_number

        # If the payload is larger than or equal to MAX_PAYLOAD_LENGTH
        # the length is set to 2^24 - 1 (ff ff ff) and additional
        # packets are sent with the rest of the payload until the
        # payload of a packet is less than MAX_PAYLOAD_LENGTH.
        if len(payload) >= MAX_PAYLOAD_LENGTH:
            offset = 0
            for _ in range(len(payload) // MAX_PAYLOAD_LENGTH):
                # payload_len, sequence_id, payload
                self._send_pkt(
                    sock,
                    address,
                    b"\xff\xff\xff"
                    + struct.pack("<B", self._pktnr)
                    + payload[offset : offset + MAX_PAYLOAD_LENGTH],
                )
                self._set_next_pktnr()
                offset += MAX_PAYLOAD_LENGTH
            payload = payload[offset:]
        self._send_pkt(
            sock,
            address,
            struct.pack("<I", len(payload))[0:3]
            + struct.pack("<B", self._pktnr)
            + payload,
        )

    def recv(self, sock: socket.socket, address: str) -> bytearray:
        """Receive `one` packet from the MySQL server."""
        try:
            # Read the header of the MySQL packet
            header = self._recv_chunk(sock, size=PACKET_HEADER_LENGTH)

            # Pull the payload length and sequence id
            payload_len, self._pktnr = (
                struct.unpack("<I", header[0:3] + b"\x00")[0],
                header[3],
            )

            # Read the payload, and return packet
            return header + self._recv_chunk(sock, size=payload_len)
        except (socket.timeout, TimeoutError) as err:
            raise ReadTimeoutError(errno=3024, msg=err.strerror) from err
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
        pkts = []

        # If the payload is larger than or equal to MAX_PAYLOAD_LENGTH
        # the length is set to 2^24 - 1 (ff ff ff) and additional
        # packets are sent with the rest of the payload until the
        # payload of a packet is less than MAX_PAYLOAD_LENGTH.
        if len(payload) >= MAX_PAYLOAD_LENGTH:
            offset = 0
            for _ in range(len(payload) // MAX_PAYLOAD_LENGTH):
                # payload length + sequence id + payload
                pkts.append(
                    b"\xff\xff\xff"
                    + struct.pack("<B", pktnr)
                    + payload[offset : offset + MAX_PAYLOAD_LENGTH]
                )
                pktnr = (pktnr + 1) % 256
                offset += MAX_PAYLOAD_LENGTH
            payload = payload[offset:]
        pkts.append(
            struct.pack("<I", len(payload))[0:3] + struct.pack("<B", pktnr) + payload
        )
        return pkts

    def _set_next_compressed_pktnr(self) -> None:
        """Increment packet id."""
        self._compressed_pktnr = (self._compressed_pktnr + 1) % 256

    def _send_pkt(self, sock: socket.socket, address: str, pkt: bytes) -> None:
        """Compress packet and write it to the comm channel."""
        compressed_pkt = zlib.compress(pkt)
        pkt = (
            struct.pack("<I", len(compressed_pkt))[0:3]
            + struct.pack("<B", self._compressed_pktnr)
            + struct.pack("<I", len(pkt))[0:3]
            + compressed_pkt
        )
        return super()._send_pkt(sock, address, pkt)

    def send(
        self,
        sock: socket.socket,
        address: str,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
    ) -> None:
        """Send `payload` as compressed packets to the MySQL server.

        If provided a payload whose length is greater than `MAX_PAYLOAD_LENGTH`, it is
        broken down into packets.
        """
        # get next packet numbers
        if packet_number is None:
            self._set_next_pktnr()
        else:
            self._pktnr = packet_number
        if compressed_packet_number is None:
            self._set_next_compressed_pktnr()
        else:
            self._compressed_pktnr = compressed_packet_number

        payload_prep = bytearray(b"").join(self._prepare_packets(payload, self._pktnr))
        if len(payload) >= MAX_PAYLOAD_LENGTH - PACKET_HEADER_LENGTH:
            # sending a MySQL payload of the size greater or equal to 2^24 - 5
            # via compression leads to at least one extra compressed packet
            # WHY? let's say len(payload) is MAX_PAYLOAD_LENGTH - 3; when preparing
            # the payload, a header of size PACKET_HEADER_LENGTH is pre-appended
            # to the payload. This means that len(payload_prep) is
            # MAX_PAYLOAD_LENGTH - 3 + PACKET_HEADER_LENGTH = MAX_PAYLOAD_LENGTH + 1
            # surpassing the maximum allowed payload size per packet.
            offset = 0

            # send several MySQL packets
            for _ in range(len(payload_prep) // MAX_PAYLOAD_LENGTH):
                self._send_pkt(
                    sock, address, payload_prep[offset : offset + MAX_PAYLOAD_LENGTH]
                )
                self._set_next_compressed_pktnr()
                offset += MAX_PAYLOAD_LENGTH
            self._send_pkt(sock, address, payload_prep[offset:])
        else:
            # send one MySQL packet
            # For small packets it may be too costly to compress the packet.
            # Usually payloads less than 50 bytes (MIN_COMPRESS_LENGTH)
            # aren't compressed (see MySQL source code Documentation).
            if len(payload) > MIN_COMPRESS_LENGTH:
                # perform compression
                self._send_pkt(sock, address, payload_prep)
            else:
                # skip compression
                super()._send_pkt(
                    sock,
                    address,
                    struct.pack("<I", len(payload_prep))[0:3]
                    + struct.pack("<B", self._compressed_pktnr)
                    + struct.pack("<I", 0)[0:3]
                    + payload_prep,
                )

    def _recv_compressed_pkt(
        self, sock: socket.socket, compressed_pll: int, uncompressed_pll: int
    ) -> None:
        """Handle reading of a compressed packet."""
        # compressed_pll stands for compressed payload length.
        # Recalling that if uncompressed payload length == 0, the packet
        # comes in uncompressed, so no decompression is needed.
        compressed_pkt = super()._recv_chunk(sock, size=compressed_pll)
        pkt = (
            compressed_pkt
            if uncompressed_pll == 0
            else bytearray(zlib.decompress(compressed_pkt))
        )

        offset = 0
        while offset < len(pkt):
            # pll stands for payload length
            pll = struct.unpack(
                "<I", pkt[offset : offset + PACKET_HEADER_LENGTH - 1] + b"\x00"
            )[0]
            if PACKET_HEADER_LENGTH + pll > len(pkt) - offset:
                # More bytes need to be consumed
                # Read the header of the next MySQL packet
                header = super()._recv_chunk(sock, size=COMPRESSED_PACKET_HEADER_LENGTH)

                # compressed payload length, sequence id, uncompressed payload length
                (
                    compressed_pll,
                    self._compressed_pktnr,
                    uncompressed_pll,
                ) = (
                    struct.unpack("<I", header[0:3] + b"\x00")[0],
                    header[3],
                    struct.unpack("<I", header[4:7] + b"\x00")[0],
                )
                compressed_pkt = super()._recv_chunk(sock, size=compressed_pll)

                # recalling that if uncompressed payload length == 0, the packet
                # comes in uncompressed, so no decompression is needed.
                pkt += (
                    compressed_pkt
                    if uncompressed_pll == 0
                    else zlib.decompress(compressed_pkt)
                )

            self._queue_read.append(pkt[offset : offset + PACKET_HEADER_LENGTH + pll])
            offset += PACKET_HEADER_LENGTH + pll

    def recv(self, sock: socket.socket, address: str) -> bytearray:
        """Receive `one` or `several` packets from the MySQL server, enqueue them, and
        return the packet at the head.
        """
        if not self._queue_read:
            try:
                # Read the header of the next MySQL packet
                header = super()._recv_chunk(sock, size=COMPRESSED_PACKET_HEADER_LENGTH)

                # compressed payload length, sequence id, uncompressed payload length
                (
                    compressed_pll,
                    self._compressed_pktnr,
                    uncompressed_pll,
                ) = (
                    struct.unpack("<I", header[0:3] + b"\x00")[0],
                    header[3],
                    struct.unpack("<I", header[4:7] + b"\x00")[0],
                )
                self._recv_compressed_pkt(sock, compressed_pll, uncompressed_pll)
            except (socket.timeout, TimeoutError) as err:
                raise ReadTimeoutError(errno=3024) from err
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
        # holds the socket connection
        self.sock: Optional[socket.socket] = None
        self._connection_timeout: Optional[int] = None
        self.server_host: Optional[str] = None
        self._netbroker: NetworkBroker = NetworkBrokerPlain()

    def switch_to_compressed_mode(self) -> None:
        """Enable network layer where transactions are made with compressed packets."""
        self._netbroker = NetworkBrokerCompressed()

    def shutdown(self) -> None:
        """Shut down the socket before closing it."""
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except (AttributeError, OSError):
            pass

    def close_connection(self) -> None:
        """Close the socket."""
        try:
            self.sock.close()
        except (AttributeError, OSError):
            pass

    def __del__(self) -> None:
        self.shutdown()

    def set_connection_timeout(self, timeout: Optional[int]) -> None:
        """Set the connection timeout."""
        self._connection_timeout = timeout
        if self.sock:
            self.sock.settimeout(timeout)

    def switch_to_ssl(self, ssl_context: Any, host: str) -> None:
        """Upgrade an existing connection to TLS.

        Args:
            ssl_context (ssl.SSLContext): The SSL Context to be used.
            host (str): Server host name.

        Returns:
            None.

        Raises:
            ProgrammingError: If the transport does not expose the socket instance.
            NotSupportedError: If Python installation has no SSL support.
        """
        # Ensure that self.sock is already created
        assert self.sock is not None

        if self.sock.family == 1:  # socket.AF_UNIX
            raise ProgrammingError("SSL is not supported when using Unix sockets")

        if ssl is None:
            raise NotSupportedError("Python installation has no SSL support")

        try:
            self.sock = ssl_context.wrap_socket(self.sock, server_hostname=host)
        except NameError as err:
            raise NotSupportedError("Python installation has no SSL support") from err
        except (ssl.SSLError, IOError) as err:
            raise InterfaceError(
                errno=2055, values=(self.address, _strioerror(err))
            ) from err
        except ssl.CertificateError as err:
            raise InterfaceError(str(err)) from err
        except NotImplementedError as err:
            raise InterfaceError(str(err)) from err

    def build_ssl_context(
        self,
        ssl_ca: Optional[str] = None,
        ssl_cert: Optional[str] = None,
        ssl_key: Optional[str] = None,
        ssl_verify_cert: Optional[bool] = False,
        ssl_verify_identity: Optional[bool] = False,
        tls_versions: Optional[List[str]] = None,
        tls_cipher_suites: Optional[List[str]] = None,
    ) -> Any:
        """Build a SSLContext.

        Args:
            ssl_ca: Certificate authority, opptional.
            ssl_cert: SSL certificate, optional.
            ssl_key: Private key, optional.
            ssl_verify_cert: Verify the SSL certificate if `True`.
            ssl_verify_identity: Verify host identity if `True`.
            tls_versions: TLS protocol versions, optional.
            tls_cipher_suites: Set of steps that helps to establish a secure connection.

        Returns:
            ssl_context (ssl.SSLContext): An SSL Context ready be used.

        Raises:
            NotSupportedError: Python installation has no SSL support.
            InterfaceError: Socket undefined or invalid ssl data.
        """
        tls_version: Optional[str] = None

        if not self.sock:
            raise InterfaceError(errno=2048)

        if ssl is None:
            raise NotSupportedError("Python installation has no SSL support")

        if tls_versions is None:
            tls_versions = []

        if tls_cipher_suites is None:
            tls_cipher_suites = []

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
                # `check_hostname` is True by default
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

    def send(
        self,
        payload: bytes,
        packet_number: Optional[int] = None,
        compressed_packet_number: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> None:
        """Send `payload` to the MySQL server.

        NOTE: if `payload` is an instance of `bytearray`, then `payload` might be
        changed by this method - `bytearray` is similar to passing a variable by
        reference.

        If you're sure you won't read `payload` after invoking `send()`,
        then you can use `bytearray.` Otherwise, you must use `bytes`.
        """
        try:
            if (
                not self._connection_timeout and self.sock is not None
            ):  # can't update the timeout during connection phase
                self.sock.settimeout(float(write_timeout) if write_timeout else None)
        except OSError as _:
            # Ignore the OSError as the socket might not be setup properly
            pass
        self._netbroker.send(
            self.sock,
            self.address,
            payload,
            packet_number=packet_number,
            compressed_packet_number=compressed_packet_number,
        )

    def recv(self, read_timeout: Optional[int] = None) -> bytearray:
        """Get packet from the MySQL server comm channel."""
        try:
            if (
                not self._connection_timeout and self.sock is not None
            ):  # can't update the timeout during connection phase
                self.sock.settimeout(float(read_timeout) if read_timeout else None)
        except OSError as _:
            # Ignore the OSError as the socket might not be setup properly
            pass
        return self._netbroker.recv(self.sock, self.address)

    @abstractmethod
    def open_connection(self) -> None:
        """Open the socket."""

    @property
    @abstractmethod
    def address(self) -> str:
        """Get the location of the socket."""


class MySQLUnixSocket(MySQLSocket):
    """MySQL socket class using UNIX sockets.

    Opens a connection through the UNIX socket of the MySQL Server.
    """

    def __init__(self, unix_socket: str = "/tmp/mysql.sock") -> None:
        super().__init__()
        self.unix_socket: str = unix_socket
        self._address: str = unix_socket

    @property
    def address(self) -> str:
        return self._address

    def open_connection(self) -> None:
        try:
            self.sock = socket.socket(
                # pylint: disable=no-member
                socket.AF_UNIX,
                socket.SOCK_STREAM,
            )
            self.sock.settimeout(self._connection_timeout)
            self.sock.connect(self.unix_socket)
        except (socket.timeout, TimeoutError) as err:
            raise ConnectionTimeoutError(
                errno=2002,
                values=(
                    self.address,
                    _strioerror(err),
                ),
            ) from err
        except IOError as err:
            raise InterfaceError(
                errno=2002, values=(self.address, _strioerror(err))
            ) from err
        except Exception as err:
            raise InterfaceError(str(err)) from err

    def switch_to_ssl(
        self, *args: Any, **kwargs: Any  # pylint: disable=unused-argument
    ) -> None:
        """Switch the socket to use SSL."""
        warnings.warn(
            "SSL is disabled when using unix socket connections",
            Warning,
        )


class MySQLTCPSocket(MySQLSocket):
    """MySQL socket class using TCP/IP.

    Opens a TCP/IP connection to the MySQL Server.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3306,
        force_ipv6: bool = False,
    ) -> None:
        super().__init__()
        self.server_host: str = host
        self.server_port: int = port
        self.force_ipv6: bool = force_ipv6
        self._family: int = 0
        self._address: str = f"{host}:{port}"

    @property
    def address(self) -> str:
        return self._address

    def open_connection(self) -> None:
        """Open the TCP/IP connection to the MySQL server."""
        # pylint: disable=no-member
        # Get address information
        addrinfo: Tuple[
            socket.AddressFamily,
            socket.SocketKind,
            int,
            str,
            Union[tuple[str, int], tuple[str, int, int, int], tuple[int, bytes]],
        ] = (None, None, None, None, None)
        try:
            addrinfos = socket.getaddrinfo(
                self.server_host,
                self.server_port,
                0,
                socket.SOCK_STREAM,
                socket.SOL_TCP,
            )
            # If multiple results we favor IPv4, unless IPv6 was forced.
            for info in addrinfos:
                if self.force_ipv6 and info[0] == socket.AF_INET6:
                    addrinfo = info
                    break
                if info[0] == socket.AF_INET:
                    addrinfo = info
                    break
            if self.force_ipv6 and addrinfo[0] is None:
                raise InterfaceError(f"No IPv6 address found for {self.server_host}")
            if addrinfo[0] is None:
                addrinfo = addrinfos[0]
        except IOError as err:
            raise InterfaceError(
                errno=2003,
                values=(self.server_host, self.server_port, _strioerror(err)),
            ) from err

        (self._family, socktype, proto, _, sockaddr) = addrinfo

        # Instantiate the socket and connect
        try:
            self.sock = socket.socket(self._family, socktype, proto)
            self.sock.settimeout(self._connection_timeout)
            self.sock.connect(sockaddr)
        except (socket.timeout, TimeoutError) as err:
            raise ConnectionTimeoutError(
                errno=2003,
                values=(
                    self.server_host,
                    self.server_port,
                    _strioerror(err),
                ),
            ) from err
        except IOError as err:
            raise InterfaceError(
                errno=2003,
                values=(self.server_host, self.server_port, _strioerror(err)),
            ) from err
        except Exception as err:
            raise InterfaceError(str(err)) from err
