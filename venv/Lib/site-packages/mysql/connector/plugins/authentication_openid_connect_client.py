# Copyright (c) 2024, Oracle and/or its affiliates.
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

"""OpenID Authentication Plugin."""

import re

from pathlib import Path
from typing import Any, List

from mysql.connector import utils

from .. import errors
from ..logger import logger
from ..network import MySQLSocket
from . import MySQLAuthPlugin

AUTHENTICATION_PLUGIN_CLASS = "MySQLOpenIDConnectAuthPlugin"
OPENID_TOKEN_MAX_SIZE = 10 * 1024  # In bytes


class MySQLOpenIDConnectAuthPlugin(MySQLAuthPlugin):
    """Class implementing the MySQL OpenID Connect Authentication Plugin."""

    _openid_capability_flag: bytes = utils.int1store(1)

    @property
    def name(self) -> str:
        """Plugin official name."""
        return "authentication_openid_connect_client"

    @property
    def requires_ssl(self) -> bool:
        """Signals whether or not SSL is required."""
        return True

    @staticmethod
    def _validate_openid_token(token: str) -> bool:
        """Helper method used to validate OpenID Connect token

        The Token is represented as a JSON Web Token (JWT) consists of a
        base64-encoded header, body, and signature, separated by '.' e.g.,
        "Base64url.Base64url.Base64url". The First part of the token contains
        the header, the second part contains payload and the third part contains
        signature. These token parts should be Base64 URLSafe i.e., Token cannot
        contain characters other than a-z, A-Z, 0-9 and special characters '-', '_'.

        Args:
            token (str): Base64url-encoded OpenID connect token fetched from
                         the file path passed via `openid_token_file` connection
                         argument.

        Returns:
            bool: Signal indicating whether the token is valid or not.
        """
        header_payload_sig: List[str] = token.split(".")
        if len(header_payload_sig) != 3:
            # invalid structure
            return False
        urlsafe_pattern = re.compile("^[a-zA-Z0-9-_]*$")
        return all(
            (
                len(token_part) and urlsafe_pattern.search(token_part) is not None
                for token_part in header_payload_sig
            )
        )

    def auth_response(self, auth_data: bytes, **kwargs: Any) -> bytes:
        """Prepares authentication string for the server.
        Args:
            auth_data: Authorization data.
            kwargs: Custom configuration to be passed to the auth plugin
                    when invoked.

        Returns:
            packet: Client's authorization response.
            The OpenID Connect authorization response follows the pattern :-
            int<1>           capability flag
            string<lenenc>   id token

        Raises:
            InterfaceError: If the connection is insecure or the OpenID Token is too large,
                            invalid or non-existent.
            ProgrammingError: If the OpenID Token file could not be read.
        """
        try:
            # Check if the connection is secure
            if self.requires_ssl and not self._ssl_enabled:
                raise errors.InterfaceError(f"{self.name} requires SSL")

            # Validate the file
            token_file_path: str = kwargs.get("openid_token_file", None)
            openid_token_file: Path = Path(token_file_path)
            # Check if token exceeds the maximum size
            if openid_token_file.stat().st_size > OPENID_TOKEN_MAX_SIZE:
                raise errors.InterfaceError(
                    "The OpenID Connect token file size is too large (> 10KB)"
                )
            openid_token: str = openid_token_file.read_text(encoding="utf-8")
            openid_token = openid_token.strip()
            # Validate the JWT Token
            if not self._validate_openid_token(openid_token):
                raise errors.InterfaceError("The OpenID Connect Token is invalid")

            # build the auth_response packet
            auth_response: List[bytes] = [
                self._openid_capability_flag,
                utils.lc_int(len(openid_token)),
                openid_token.encode(),
            ]
            return b"".join(auth_response)
        except (SyntaxError, TypeError, OSError, UnicodeError) as err:
            raise errors.ProgrammingError(
                "The OpenID Connect Token File (openid_token_file) could not be read"
            ) from err

    def auth_switch_response(
        self, sock: MySQLSocket, auth_data: bytes, **kwargs: Any
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

        Raises:
            InterfaceError: If a NULL auth response is received from auth_response method.
        """
        response = self.auth_response(auth_data, **kwargs)

        if response is None:
            raise errors.InterfaceError("Got a NULL auth response")

        logger.debug("# request: %s size: %s", response, len(response))
        sock.send(response)

        packet = sock.recv()
        logger.debug("# server response packet: %s", packet)

        return bytes(packet)
