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

"""Caching SHA2 Password Authentication Plugin."""

import struct

from hashlib import sha256
from typing import TYPE_CHECKING, Any, Optional

from ..errors import InterfaceError
from ..logger import logger
from . import MySQLAuthPlugin

if TYPE_CHECKING:
    from ..network import MySQLSocket

AUTHENTICATION_PLUGIN_CLASS = "MySQLCachingSHA2PasswordAuthPlugin"


class MySQLCachingSHA2PasswordAuthPlugin(MySQLAuthPlugin):
    """Class implementing the MySQL caching_sha2_password authentication plugin

    Note that encrypting using RSA is not supported since the Python
    Standard Library does not provide this OpenSSL functionality.
    """

    perform_full_authentication: int = 4

    def _scramble(self, auth_data: bytes) -> bytes:
        """Return a scramble of the password using a Nonce sent by the
        server.

        The scramble is of the form:
        XOR(SHA2(password), SHA2(SHA2(SHA2(password)), Nonce))
        """
        if not auth_data:
            raise InterfaceError("Missing authentication data (seed)")

        if not self._password:
            return b""

        hash1 = sha256(self._password.encode()).digest()
        hash2 = sha256()
        hash2.update(sha256(hash1).digest())
        hash2.update(auth_data)
        hash2_digest = hash2.digest()
        xored = [h1 ^ h2 for (h1, h2) in zip(hash1, hash2_digest)]
        hash3 = struct.pack("32B", *xored)
        return hash3

    @property
    def name(self) -> str:
        """Plugin official name."""
        return "caching_sha2_password"

    @property
    def requires_ssl(self) -> bool:
        """Signals whether or not SSL is required."""
        return False

    def auth_response(self, auth_data: bytes, **kwargs: Any) -> Optional[bytes]:
        """Make the client's authorization response.

        Args:
            auth_data: Authorization data.
            kwargs: Custom configuration to be passed to the auth plugin
                    when invoked. The parameters defined here will override the ones
                    defined in the auth plugin itself.

        Returns:
            packet: Client's authorization response.
        """
        if not auth_data:
            return None
        if len(auth_data) > 1:
            return self._scramble(auth_data)
        if auth_data[0] == self.perform_full_authentication:
            # return password as clear text.
            return self._password.encode() + b"\x00"

        return None

    def auth_more_response(
        self, sock: "MySQLSocket", auth_data: bytes, **kwargs: Any
    ) -> bytes:
        """Handles server's `auth more data` response.

        Args:
            sock: Pointer to the socket connection.
            auth_data: Authentication method data (from a packet representing
                       an `auth more data` response).
            kwargs: Custom configuration to be passed to the auth plugin
                    when invoked. The parameters defined here will override the ones
                    defined in the auth plugin itself.

        Returns:
            packet: Last server's response after back-and-forth
                    communication.
        """
        response = self.auth_response(auth_data, **kwargs)
        if response:
            sock.send(response)

        return bytes(sock.recv())

    def auth_switch_response(
        self, sock: "MySQLSocket", auth_data: bytes, **kwargs: Any
    ) -> bytes:
        """Handles server's `auth switch request` response.

        Args:
            sock: Pointer to the socket connection.
            auth_data: Plugin provided data (extracted from a packet
                       representing an `auth switch request` response).
            kwargs: Custom configuration to be passed to the auth plugin
                    when invoked. The parameters defined here will override the ones
                    defined in the auth plugin itself.

        Returns:
            packet: Last server's response after back-and-forth
                    communication.
        """
        response = self.auth_response(auth_data, **kwargs)
        if response is None:
            raise InterfaceError("Got a NULL auth response")

        logger.debug("# request: %s size: %s", response, len(response))
        sock.send(response)

        pkt = bytes(sock.recv())
        logger.debug("# server response packet: %s", pkt)

        return pkt
