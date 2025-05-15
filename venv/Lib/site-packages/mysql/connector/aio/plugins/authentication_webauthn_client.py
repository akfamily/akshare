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

"""WebAuthn Authentication Plugin."""


from typing import TYPE_CHECKING, Any, Callable, Optional

from mysql.connector import errors, utils

from ..logger import logger
from . import MySQLAuthPlugin

if TYPE_CHECKING:
    from ..network import MySQLSocket

try:
    from fido2.cbor import dump_bytes as cbor_dump_bytes
    from fido2.client import Fido2Client, UserInteraction
    from fido2.hid import CtapHidDevice
    from fido2.webauthn import PublicKeyCredentialRequestOptions
except ImportError as import_err:
    raise errors.ProgrammingError(
        "Module fido2 is required for WebAuthn authentication mechanism but was "
        "not found. Unable to authenticate with the server"
    ) from import_err

try:
    from fido2.pcsc import CtapPcscDevice

    CTAP_PCSC_DEVICE_AVAILABLE = True
except ModuleNotFoundError:
    CTAP_PCSC_DEVICE_AVAILABLE = False


AUTHENTICATION_PLUGIN_CLASS = "MySQLWebAuthnAuthPlugin"


class ClientInteraction(UserInteraction):
    """Provides user interaction to the Client."""

    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
        self.msg = (
            "Please insert FIDO device and perform gesture action for authentication "
            "to complete."
        )

    def prompt_up(self) -> None:
        """Prompt message for the user interaction with the FIDO device."""
        if self.callback is None:
            print(self.msg)
        else:
            self.callback(self.msg)


class MySQLWebAuthnAuthPlugin(MySQLAuthPlugin):
    """Class implementing the MySQL WebAuthn authentication plugin."""

    client: Optional[Fido2Client] = None
    callback: Optional[Callable] = None
    options: dict = {"rpId": None, "challenge": None, "allowCredentials": []}

    @property
    def name(self) -> str:
        """Plugin official name."""
        return "authentication_webauthn_client"

    @property
    def requires_ssl(self) -> bool:
        """Signals whether or not SSL is required."""
        return False

    def get_assertion_response(
        self, credential_id: Optional[bytearray] = None
    ) -> bytes:
        """Get assertion from authenticator and return the response.

        Args:
            credential_id (Optional[bytearray]): The credential ID.

        Returns:
            bytearray: The response packet with the data from the assertion.
        """
        if self.client is None:
            raise errors.InterfaceError("No WebAuthn client found")

        if credential_id is not None:
            # If credential_id is not None, it's because the FIDO device does not
            # support resident keys and the credential_id was requested from the server
            self.options["allowCredentials"] = [
                {
                    "id": credential_id,
                    "type": "public-key",
                }
            ]

        # Get assertion from authenticator
        assertion = self.client.get_assertion(
            PublicKeyCredentialRequestOptions.from_dict(self.options)
        )
        number_of_assertions = len(assertion.get_assertions())
        client_data_json = b""

        # Build response packet
        #
        # Format:
        #   int<1>       0x02 (2)              status tag
        #   int<lenenc>  number of assertions  length encoded number of assertions
        #   string       authenticator data    variable length raw binary string
        #   string       signed challenge      variable length raw binary string
        #   ...
        #   ...
        #   string       authenticator data    variable length raw binary string
        #   string       signed challenge      variable length raw binary string
        #   string       ClientDataJSON        variable length raw binary string
        packet = utils.lc_int(2)
        packet += utils.lc_int(number_of_assertions)

        # Add authenticator data and signed challenge for each assertion
        for i in range(number_of_assertions):
            assertion_response = assertion.get_response(i)

            # string<lenenc>   authenticator_data
            authenticator_data = cbor_dump_bytes(assertion_response.authenticator_data)

            # string<lenenc>   signed_challenge
            signature = assertion_response.signature

            packet += utils.lc_int(len(authenticator_data))
            packet += authenticator_data
            packet += utils.lc_int(len(signature))
            packet += signature

            # string<lenenc>   client_data_json
            client_data_json = assertion_response.client_data

        packet += utils.lc_int(len(client_data_json))
        packet += client_data_json

        logger.debug("WebAuthn - payload response packet: %s", packet)
        return packet

    def auth_response(self, auth_data: bytes, **kwargs: Any) -> Optional[bytes]:
        """Find authenticator device and check if supports resident keys.

        It also creates a Fido2Client using the relying party ID from the server.

        Raises:
            InterfaceError: When the FIDO device is not found.

        Returns:
            bytes: 2 if the authenticator supports resident keys else 1.
        """
        try:
            packets, capability = utils.read_int(auth_data, 1)
            challenge, rp_id = utils.read_lc_string_list(packets)
            self.options["challenge"] = challenge
            self.options["rpId"] = rp_id.decode()
            logger.debug("WebAuthn - capability: %d", capability)
            logger.debug("WebAuthn - challenge: %s", self.options["challenge"])
            logger.debug("WebAuthn - relying party id: %s", self.options["rpId"])
        except ValueError as err:
            raise errors.InterfaceError(
                "Unable to parse MySQL WebAuthn authentication data"
            ) from err

        # Locate a device
        device = next(CtapHidDevice.list_devices(), None)
        if device is not None:
            logger.debug("WebAuthn - Use USB HID channel")
        elif CTAP_PCSC_DEVICE_AVAILABLE:
            device = next(CtapPcscDevice.list_devices(), None)  # type: ignore[arg-type]

        if device is None:
            raise errors.InterfaceError("No FIDO device found")

        # Set up a FIDO 2 client using the origin relying party id
        self.client = Fido2Client(
            device,
            f"https://{self.options['rpId']}",
            user_interaction=ClientInteraction(self.callback),
        )

        if not self.client.info.options.get("rk"):
            logger.debug("WebAuthn - Authenticator doesn't support resident keys")
            return b"1"

        logger.debug("WebAuthn - Authenticator with support for resident key found")
        return b"2"

    async def auth_more_response(
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
        _, credential_id = utils.read_lc_string(auth_data)

        response = self.get_assertion_response(credential_id)

        logger.debug("WebAuthn - request: %s size: %s", response, len(response))
        await sock.write(response)

        pkt = bytes(await sock.read())
        logger.debug("WebAuthn - server response packet: %s", pkt)

        return pkt

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
        webauth_callback = kwargs.get("webauthn_callback") or kwargs.get(
            "fido_callback"
        )
        self.callback = (
            utils.import_object(webauth_callback)
            if isinstance(webauth_callback, str)
            else webauth_callback
        )

        response = self.auth_response(auth_data)
        credential_id = None

        if response == b"1":
            # Authenticator doesn't support resident keys, request credential_id
            logger.debug("WebAuthn - request credential_id")
            await sock.write(utils.lc_int(int(response)))

            # return a packet representing an `auth more data` response
            return bytes(await sock.read())

        response = self.get_assertion_response(credential_id)

        logger.debug("WebAuthn - request: %s size: %s", response, len(response))
        await sock.write(response)

        pkt = bytes(await sock.read())
        logger.debug("WebAuthn - server response packet: %s", pkt)

        return pkt
