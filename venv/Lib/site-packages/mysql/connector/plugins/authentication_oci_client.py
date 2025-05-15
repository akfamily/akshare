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

# mypy: disable-error-code="arg-type,union-attr,call-arg"

"""OCI Authentication Plugin."""

import json
import os

from base64 import b64encode
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

from .. import errors
from ..logger import logger

if TYPE_CHECKING:
    from ..network import MySQLSocket

try:
    from cryptography.exceptions import UnsupportedAlgorithm
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.asymmetric.types import PRIVATE_KEY_TYPES
except ImportError:
    raise errors.ProgrammingError("Package 'cryptography' is not installed") from None

try:
    from oci import config, exceptions
except ImportError:
    raise errors.ProgrammingError(
        "Package 'oci' (Oracle Cloud Infrastructure Python SDK) is not installed"
    ) from None

from . import MySQLAuthPlugin

AUTHENTICATION_PLUGIN_CLASS = "MySQLOCIAuthPlugin"
OCI_SECURITY_TOKEN_MAX_SIZE = 10 * 1024  # In bytes
OCI_SECURITY_TOKEN_TOO_LARGE = "Ephemeral security token is too large (10KB max)"
OCI_SECURITY_TOKEN_FILE_NOT_AVAILABLE = (
    "Ephemeral security token file ('security_token_file') could not be read"
)
OCI_PROFILE_MISSING_PROPERTIES = (
    "OCI configuration file does not contain a 'fingerprint' or 'key_file' entry"
)


class MySQLOCIAuthPlugin(MySQLAuthPlugin):
    """Implement the MySQL OCI IAM authentication plugin."""

    context: Any = None
    oci_config_profile: str = "DEFAULT"
    oci_config_file: str = config.DEFAULT_LOCATION

    @staticmethod
    def _prepare_auth_response(signature: bytes, oci_config: Dict[str, Any]) -> str:
        """Prepare client's authentication response

        Prepares client's authentication response in JSON format
        Args:
            signature (bytes):  server's nonce to be signed by client.
            oci_config (dict): OCI configuration object.

        Returns:
            str: JSON string with the following format:
                 {"fingerprint": str, "signature": str, "token": base64.base64.base64}

        Raises:
            ProgrammingError: If the ephemeral security token file can't be open or the
                              token is too large.
        """
        signature_64 = b64encode(signature)
        auth_response = {
            "fingerprint": oci_config["fingerprint"],
            "signature": signature_64.decode(),
        }

        # The security token, if it exists, should be a JWT (JSON Web Token), consisted
        # of a base64-encoded header, body, and signature, separated by '.',
        # e.g. "Base64.Base64.Base64", stored in a file at the path specified by the
        # security_token_file configuration property
        if oci_config.get("security_token_file"):
            try:
                security_token_file = Path(oci_config["security_token_file"])
                # Check if token exceeds the maximum size
                if security_token_file.stat().st_size > OCI_SECURITY_TOKEN_MAX_SIZE:
                    raise errors.ProgrammingError(OCI_SECURITY_TOKEN_TOO_LARGE)
                auth_response["token"] = security_token_file.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as err:
                raise errors.ProgrammingError(
                    OCI_SECURITY_TOKEN_FILE_NOT_AVAILABLE
                ) from err
        return json.dumps(auth_response, separators=(",", ":"))

    @staticmethod
    def _get_private_key(key_path: str) -> PRIVATE_KEY_TYPES:
        """Get the private_key form the given location"""
        try:
            with open(os.path.expanduser(key_path), "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                )
        except (TypeError, OSError, ValueError, UnsupportedAlgorithm) as err:
            raise errors.ProgrammingError(
                "An error occurred while reading the API_KEY from "
                f'"{key_path}": {err}'
            )

        return private_key

    def _get_valid_oci_config(self) -> Dict[str, Any]:
        """Get a valid OCI config from the given configuration file path"""
        error_list = []
        req_keys = {
            "fingerprint": (lambda x: len(x) > 32),
            "key_file": (lambda x: os.path.exists(os.path.expanduser(x))),
        }

        oci_config: Dict[str, Any] = {}
        try:
            # key_file is validated by oci.config if present
            oci_config = config.from_file(
                self.oci_config_file or config.DEFAULT_LOCATION,
                self.oci_config_profile or "DEFAULT",
            )
            for req_key, req_value in req_keys.items():
                try:
                    # Verify parameter in req_key is present and valid
                    if oci_config[req_key] and not req_value(oci_config[req_key]):
                        error_list.append(f'Parameter "{req_key}" is invalid')
                except KeyError:
                    error_list.append(f"Does not contain parameter {req_key}")
        except (
            exceptions.ConfigFileNotFound,
            exceptions.InvalidConfig,
            exceptions.InvalidKeyFilePath,
            exceptions.InvalidPrivateKey,
            exceptions.ProfileNotFound,
        ) as err:
            error_list.append(str(err))

        # Raise errors if any
        if error_list:
            raise errors.ProgrammingError(
                f"Invalid oci-config-file: {self.oci_config_file}. "
                f"Errors found: {error_list}"
            )

        return oci_config

    @property
    def name(self) -> str:
        """Plugin official name."""
        return "authentication_oci_client"

    @property
    def requires_ssl(self) -> bool:
        """Signals whether or not SSL is required."""
        return False

    def auth_response(self, auth_data: bytes, **kwargs: Any) -> Optional[bytes]:
        """Prepare authentication string for the server."""
        logger.debug("server nonce: %s, len %d", auth_data, len(auth_data))

        oci_config = self._get_valid_oci_config()

        private_key = self._get_private_key(oci_config["key_file"])
        signature = private_key.sign(auth_data, padding.PKCS1v15(), hashes.SHA256())

        auth_response = self._prepare_auth_response(signature, oci_config)
        logger.debug("authentication response: %s", auth_response)
        return auth_response.encode()

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
        self.oci_config_file = kwargs.get("oci_config_file", "DEFAULT")
        self.oci_config_profile = kwargs.get(
            "oci_config_profile", config.DEFAULT_LOCATION
        )
        logger.debug("# oci configuration file path: %s", self.oci_config_file)

        response = self.auth_response(auth_data, **kwargs)
        if response is None:
            raise errors.InterfaceError("Got a NULL auth response")

        logger.debug("# request: %s size: %s", response, len(response))
        sock.send(response)

        packet = sock.recv()
        logger.debug("# server response packet: %s", packet)

        return bytes(packet)
