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

# mypy: disable-error-code="attr-defined"
# pylint: disable=protected-access

"""Utilities."""

__all__ = ["to_thread", "open_connection"]

import asyncio
import contextvars
import functools

try:
    import ssl
except ImportError:
    ssl = None

from typing import TYPE_CHECKING, Any, Callable, Tuple

if TYPE_CHECKING:
    from mysql.connector.aio.abstracts import MySQLConnectionAbstract

    __all__.append("StreamWriter")


class StreamReaderProtocol(asyncio.StreamReaderProtocol):
    """Extends asyncio.streams.StreamReaderProtocol for adding start_tls().

    The ``start_tls()`` is based on ``asyncio.streams.StreamWriter`` introduced
    in Python 3.11. It provides the same functionality for older Python versions.
    """

    def _replace_writer(self, writer: asyncio.StreamWriter) -> None:
        """Replace stream writer.

        Args:
            writer: Stream Writer.
        """
        transport = writer.transport
        self._stream_writer = writer
        self._transport = transport
        self._over_ssl = transport.get_extra_info("sslcontext") is not None


class StreamWriter(asyncio.streams.StreamWriter):
    """Extends asyncio.streams.StreamWriter for adding start_tls().

    The ``start_tls()`` is based on ``asyncio.streams.StreamWriter`` introduced
    in Python 3.11. It provides the same functionality for older Python versions.
    """

    async def start_tls(
        self,
        ssl_context: ssl.SSLContext,
        *,
        server_hostname: str = None,
        ssl_handshake_timeout: int = None,
    ) -> None:
        """Upgrade an existing stream-based connection to TLS.

        Args:
            ssl_context: Configured SSL context.
            server_hostname: Server host name.
            ssl_handshake_timeout: SSL handshake timeout.
        """
        server_side = self._protocol._client_connected_cb is not None
        protocol = self._protocol
        await self.drain()
        new_transport = await self._loop.start_tls(
            # pylint: disable=access-member-before-definition
            self._transport,  # type: ignore[has-type]
            protocol,
            ssl_context,
            server_side=server_side,
            server_hostname=server_hostname,
            ssl_handshake_timeout=ssl_handshake_timeout,
        )
        self._transport = (  # pylint: disable=attribute-defined-outside-init
            new_transport
        )
        protocol._replace_writer(self)


async def open_connection(
    host: str = None, port: int = None, *, limit: int = 2**16, **kwds: Any
) -> Tuple[asyncio.StreamReader, StreamWriter]:
    """A wrapper for create_connection() returning a (reader, writer) pair.

    This function is based on ``asyncio.streams.open_connection`` and adds a custom
    stream reader.

    MySQL expects TLS negotiation to happen in the middle of a TCP connection, not at
    the start.
    This function in conjunction with ``_StreamReaderProtocol`` and ``_StreamWriter``
    allows the TLS negotiation on an existing connection.

    Args:
        host: Server host name.
        port: Server port.
        limit: The buffer size limit used by the returned ``StreamReader`` instance.
               By default the limit is set to 64 KiB.

    Returns:
        tuple: Returns a pair of reader and writer objects that are instances of
               ``StreamReader`` and ``StreamWriter`` classes.
    """
    loop = asyncio.get_running_loop()
    reader = asyncio.streams.StreamReader(limit=limit, loop=loop)
    protocol = StreamReaderProtocol(reader, loop=loop)
    transport, _ = await loop.create_connection(lambda: protocol, host, port, **kwds)
    writer = StreamWriter(transport, protocol, reader, loop)
    return reader, writer


async def to_thread(func: Callable, *args: Any, **kwargs: Any) -> asyncio.Future:
    """Asynchronously run function ``func`` in a separate thread.

    This function is based on ``asyncio.to_thread()`` introduced in Python 3.9, which
    provides the same functionality for older Python versions.

    Returns:
        coroutine: A coroutine that can be awaited to get the eventual result of
                   ``func``.
    """
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)
