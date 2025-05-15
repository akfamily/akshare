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

"""Native Password Authentication Plugin."""

import struct

from hashlib import sha1
from typing import TYPE_CHECKING, Any, Optional

from mysql.connector.errors import InterfaceError
from mysql.connector.logger import logger

from . import MySQLAuthPlugin

if TYPE_CHECKING:
    from ..network import MySQLSocket

AUTHENTICATION_PLUGIN_CLASS = "MySQLNativePasswordAuthPlugin"


class MySQLNativePasswordAuthPlugin(MySQLAuthPlugin):
    """Class implementing the MySQL Native Password authentication plugin"""

    def _prepare_password(self, auth_data: bytes) -> bytes:
        """Prepares and returns password as native MySQL 4.1+ password"""
        if not auth_data:
            raise InterfaceError("Missing authentication data (seed)")

        if not self._password:
            return b""

        hash4 = None
        try:
            hash1 = sha1(self._password.encode()).digest()
            hash2 = sha1(hash1).digest()
            hash3 = sha1(auth_data + hash2).digest()
            xored = [h1 ^ h3 for (h1, h3) in zip(hash1, hash3)]
            hash4 = struct.pack("20B", *xored)
        except (struct.error, TypeError) as err:
            raise InterfaceError(f"Failed scrambling password; {err}") from err

        return hash4

    @property
    def name(self) -> str:
        """Plugin official name."""
        return "mysql_native_password"

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
        return self._prepare_password(auth_data)

    async def auth_switch_response(
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
        await sock.write(response)

        pkt = bytes(await sock.read())
        logger.debug("# server response packet: %s", pkt)

        return pkt
