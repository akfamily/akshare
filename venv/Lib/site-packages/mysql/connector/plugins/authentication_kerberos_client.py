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

# mypy: disable-error-code="str-bytes-safe,misc"

"""Kerberos Authentication Plugin."""

import getpass
import os
import struct

from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Tuple

from ..authentication import ERR_STATUS
from ..errors import InterfaceError, ProgrammingError
from ..logger import logger

if TYPE_CHECKING:
    from ..network import MySQLSocket

try:
    import gssapi
except ImportError:
    gssapi = None
    if os.name != "nt":
        raise ProgrammingError(
            "Module gssapi is required for GSSAPI authentication "
            "mechanism but was not found. Unable to authenticate "
            "with the server"
        ) from None

try:
    import sspi
    import sspicon
except ImportError:
    sspi = None
    sspicon = None

from . import MySQLAuthPlugin

AUTHENTICATION_PLUGIN_CLASS = (
    "MySQLSSPIKerberosAuthPlugin" if os.name == "nt" else "MySQLKerberosAuthPlugin"
)


class MySQLBaseKerberosAuthPlugin(MySQLAuthPlugin):
    """Base class for the MySQL Kerberos authentication plugin."""

    @property
    def name(self) -> str:
        """Plugin official name."""
        return "authentication_kerberos_client"

    @property
    def requires_ssl(self) -> bool:
        """Signals whether or not SSL is required."""
        return False

    @abstractmethod
    def auth_continue(
        self, tgt_auth_challenge: Optional[bytes]
    ) -> Tuple[Optional[bytes], bool]:
        """Continue with the Kerberos TGT service request.

        With the TGT authentication service given response generate a TGT
        service request. This method must be invoked sequentially (in a loop)
        until the security context is completed and an empty response needs to
        be send to acknowledge the server.

        Args:
            tgt_auth_challenge: the challenge for the negotiation.

        Returns:
            tuple (bytearray TGS service request,
            bool True if context is completed otherwise False).
        """

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
        logger.debug("# auth_data: %s", auth_data)
        response = self.auth_response(auth_data, ignore_auth_data=False, **kwargs)
        if response is None:
            raise InterfaceError("Got a NULL auth response")

        logger.debug("# request: %s size: %s", response, len(response))
        sock.send(response)

        packet = sock.recv()
        logger.debug("# server response packet: %s", packet)

        if packet != ERR_STATUS:
            rcode_size = 5  # Reader size for the response status code
            logger.debug("# Continue with GSSAPI authentication")
            logger.debug("# Response header: %s", packet[: rcode_size + 1])
            logger.debug("# Response size: %s", len(packet))
            logger.debug("# Negotiate a service request")
            complete = False
            tries = 0

            while not complete and tries < 5:
                logger.debug("%s Attempt %s %s", "-" * 20, tries + 1, "-" * 20)
                logger.debug("<< Server response: %s", packet)
                logger.debug("# Response code: %s", packet[: rcode_size + 1])
                token, complete = self.auth_continue(packet[rcode_size:])
                if token:
                    sock.send(token)
                if complete:
                    break
                packet = sock.recv()

                logger.debug(">> Response to server: %s", token)
                tries += 1

            if not complete:
                raise InterfaceError(
                    f"Unable to fulfill server request after {tries} "
                    f"attempts. Last server response: {packet}"
                )

            logger.debug(
                "Last response from server: %s length: %d",
                packet,
                len(packet),
            )

            # Receive OK packet from server.
            packet = sock.recv()
            logger.debug("<< Ok packet from server: %s", packet)

        return bytes(packet)


# pylint: disable=c-extension-no-member,no-member
class MySQLKerberosAuthPlugin(MySQLBaseKerberosAuthPlugin):
    """Implement the MySQL Kerberos authentication plugin."""

    context: Optional[gssapi.SecurityContext] = None

    @staticmethod
    def get_user_from_credentials() -> str:
        """Get user from credentials without realm."""
        try:
            creds = gssapi.Credentials(usage="initiate")
            user = str(creds.name)
            if user.find("@") != -1:
                user, _ = user.split("@", 1)
            return user
        except gssapi.raw.misc.GSSError:
            return getpass.getuser()

    @staticmethod
    def get_store() -> dict:
        """Get a credentials store dictionary.

        Returns:
            dict: Credentials store dictionary with the krb5 ccache name.

        Raises:
            InterfaceError: If 'KRB5CCNAME' environment variable is empty.
        """
        krb5ccname = os.environ.get(
            "KRB5CCNAME",
            (
                f"/tmp/krb5cc_{os.getuid()}"
                if os.name == "posix"
                else Path("%TEMP%").joinpath("krb5cc")
            ),
        )
        if not krb5ccname:
            raise InterfaceError(
                "The 'KRB5CCNAME' environment variable is set to empty"
            )
        logger.debug("Using krb5 ccache name: FILE:%s", krb5ccname)
        store = {b"ccache": f"FILE:{krb5ccname}".encode("utf-8")}
        return store

    def _acquire_cred_with_password(self, upn: str) -> gssapi.raw.creds.Creds:
        """Acquire and store credentials through provided password.

        Args:
            upn (str): User Principal Name.

        Returns:
            gssapi.raw.creds.Creds: GSSAPI credentials.
        """
        logger.debug("Attempt to acquire credentials through provided password")
        user = gssapi.Name(upn, gssapi.NameType.user)
        password = self._password.encode("utf-8")

        try:
            acquire_cred_result = gssapi.raw.acquire_cred_with_password(
                user, password, usage="initiate"
            )
            creds = acquire_cred_result.creds
            gssapi.raw.store_cred_into(
                self.get_store(),
                creds=creds,
                mech=gssapi.MechType.kerberos,
                overwrite=True,
                set_default=True,
            )
        except gssapi.raw.misc.GSSError as err:
            raise ProgrammingError(
                f"Unable to acquire credentials with the given password: {err}"
            ) from err
        return creds

    @staticmethod
    def _parse_auth_data(packet: bytes) -> Tuple[str, str]:
        """Parse authentication data.

        Get the SPN and REALM from the authentication data packet.

        Format:
            SPN string length two bytes <B1> <B2> +
            SPN string +
            UPN realm string length two bytes <B1> <B2> +
            UPN realm string

        Returns:
            tuple: With 'spn' and 'realm'.
        """
        spn_len = struct.unpack("<H", packet[:2])[0]
        packet = packet[2:]

        spn = struct.unpack(f"<{spn_len}s", packet[:spn_len])[0]
        packet = packet[spn_len:]

        realm_len = struct.unpack("<H", packet[:2])[0]
        realm = struct.unpack(f"<{realm_len}s", packet[2:])[0]

        return spn.decode(), realm.decode()

    def auth_response(
        self, auth_data: Optional[bytes] = None, **kwargs: Any
    ) -> Optional[bytes]:
        """Prepare the first message to the server."""
        spn = None
        realm = None

        if auth_data and not kwargs.get("ignore_auth_data", True):
            try:
                spn, realm = self._parse_auth_data(auth_data)
            except struct.error as err:
                raise InterruptedError(f"Invalid authentication data: {err}") from err

        if spn is None:
            return self._password.encode() + b"\x00"

        upn = f"{self._username}@{realm}" if self._username else None

        logger.debug("Service Principal: %s", spn)
        logger.debug("Realm: %s", realm)

        try:
            # Attempt to retrieve credentials from cache file
            creds: Any = gssapi.Credentials(usage="initiate")
            creds_upn = str(creds.name)

            logger.debug("Cached credentials found")
            logger.debug("Cached credentials UPN: %s", creds_upn)

            # Remove the realm from user
            if creds_upn.find("@") != -1:
                creds_user, creds_realm = creds_upn.split("@", 1)
            else:
                creds_user = creds_upn
                creds_realm = None

            upn = f"{self._username}@{realm}" if self._username else creds_upn

            # The user from cached credentials matches with the given user?
            if self._username and self._username != creds_user:
                logger.debug(
                    "The user from cached credentials doesn't match with the "
                    "given user"
                )
                if self._password is not None:
                    creds = self._acquire_cred_with_password(upn)
            if creds_realm and creds_realm != realm and self._password is not None:
                creds = self._acquire_cred_with_password(upn)
        except gssapi.raw.exceptions.ExpiredCredentialsError as err:
            if upn and self._password is not None:
                creds = self._acquire_cred_with_password(upn)
            else:
                raise InterfaceError(f"Credentials has expired: {err}") from err
        except gssapi.raw.misc.GSSError as err:
            if upn and self._password is not None:
                creds = self._acquire_cred_with_password(upn)
            else:
                raise InterfaceError(
                    f"Unable to retrieve cached credentials error: {err}"
                ) from err

        flags = (
            gssapi.RequirementFlag.mutual_authentication,
            gssapi.RequirementFlag.extended_error,
            gssapi.RequirementFlag.delegate_to_peer,
        )
        name = gssapi.Name(spn, name_type=gssapi.NameType.kerberos_principal)
        cname = name.canonicalize(gssapi.MechType.kerberos)
        self.context = gssapi.SecurityContext(
            name=cname, creds=creds, flags=sum(flags), usage="initiate"
        )

        try:
            initial_client_token: Optional[bytes] = self.context.step()
        except gssapi.raw.misc.GSSError as err:
            raise InterfaceError(f"Unable to initiate security context: {err}") from err

        logger.debug("Initial client token: %s", initial_client_token)
        return initial_client_token

    def auth_continue(
        self, tgt_auth_challenge: Optional[bytes]
    ) -> Tuple[Optional[bytes], bool]:
        """Continue with the Kerberos TGT service request.

        With the TGT authentication service given response generate a TGT
        service request. This method must be invoked sequentially (in a loop)
        until the security context is completed and an empty response needs to
        be send to acknowledge the server.

        Args:
            tgt_auth_challenge: the challenge for the negotiation.

        Returns:
            tuple (bytearray TGS service request,
            bool True if context is completed otherwise False).
        """
        logger.debug("tgt_auth challenge: %s", tgt_auth_challenge)

        resp: Optional[bytes] = self.context.step(tgt_auth_challenge)

        logger.debug("Context step response: %s", resp)
        logger.debug("Context completed?: %s", self.context.complete)

        return resp, self.context.complete

    def auth_accept_close_handshake(self, message: bytes) -> bytes:
        """Accept handshake and generate closing handshake message for server.

        This method verifies the server authenticity from the given message
        and included signature and generates the closing handshake for the
        server.

        When this method is invoked the security context is already established
        and the client and server can send GSSAPI formated secure messages.

        To finish the authentication handshake the server sends a message
        with the security layer availability and the maximum buffer size.

        Since the connector only uses the GSSAPI authentication mechanism to
        authenticate the user with the server, the server will verify clients
        message signature and terminate the GSSAPI authentication and send two
        messages; an authentication acceptance b'\x01\x00\x00\x08\x01' and a
        OK packet (that must be received after sent the returned message from
        this method).

        Args:
            message: a wrapped gssapi message from the server.

        Returns:
            bytearray (closing handshake message to be send to the server).
        """
        if not self.context.complete:
            raise ProgrammingError("Security context is not completed")
        logger.debug("Server message: %s", message)
        logger.debug("GSSAPI flags in use: %s", self.context.actual_flags)
        try:
            unwraped = self.context.unwrap(message)
            logger.debug("Unwraped: %s", unwraped)
        except gssapi.raw.exceptions.BadMICError as err:
            logger.debug("Unable to unwrap server message: %s", err)
            raise InterfaceError(f"Unable to unwrap server message: {err}") from err

        logger.debug("Unwrapped server message: %s", unwraped)
        # The message contents for the clients closing message:
        #   - security level 1 byte, must be always 1.
        #   - conciliated buffer size 3 bytes, without importance as no
        #     further GSSAPI messages will be sends.
        response = bytearray(b"\x01\x00\x00\00")
        # Closing handshake must not be encrypted.
        logger.debug("Message response: %s", response)
        wraped = self.context.wrap(response, encrypt=False)
        logger.debug(
            "Wrapped message response: %s, length: %d",
            wraped[0],
            len(wraped[0]),
        )

        return wraped.message


class MySQLSSPIKerberosAuthPlugin(MySQLBaseKerberosAuthPlugin):
    """Implement the MySQL Kerberos authentication plugin with Windows SSPI"""

    context: Any = None
    clientauth: Any = None

    @staticmethod
    def _parse_auth_data(packet: bytes) -> Tuple[str, str]:
        """Parse authentication data.

        Get the SPN and REALM from the authentication data packet.

        Format:
            SPN string length two bytes <B1> <B2> +
            SPN string +
            UPN realm string length two bytes <B1> <B2> +
            UPN realm string

        Returns:
            tuple: With 'spn' and 'realm'.
        """
        spn_len = struct.unpack("<H", packet[:2])[0]
        packet = packet[2:]

        spn = struct.unpack(f"<{spn_len}s", packet[:spn_len])[0]
        packet = packet[spn_len:]

        realm_len = struct.unpack("<H", packet[:2])[0]
        realm = struct.unpack(f"<{realm_len}s", packet[2:])[0]

        return spn.decode(), realm.decode()

    def auth_response(
        self, auth_data: Optional[bytes] = None, **kwargs: Any
    ) -> Optional[bytes]:
        """Prepare the first message to the server.

        Args:
            kwargs:
                ignore_auth_data (bool): if True, the provided auth data is ignored.
        """
        logger.debug("auth_response for sspi")
        spn = None
        realm = None

        if auth_data and not kwargs.get("ignore_auth_data", True):
            try:
                spn, realm = self._parse_auth_data(auth_data)
            except struct.error as err:
                raise InterruptedError(f"Invalid authentication data: {err}") from err

        logger.debug("Service Principal: %s", spn)
        logger.debug("Realm: %s", realm)

        if sspicon is None or sspi is None:
            raise ProgrammingError(
                'Package "pywin32" (Python for Win32 (pywin32) extensions)'
                " is not installed."
            )

        flags = (sspicon.ISC_REQ_MUTUAL_AUTH, sspicon.ISC_REQ_DELEGATE)

        if self._username and self._password:
            _auth_info = (self._username, realm, self._password)
        else:
            _auth_info = None

        targetspn = spn
        logger.debug("targetspn: %s", targetspn)
        logger.debug("_auth_info is None: %s", _auth_info is None)

        # The Security Support Provider Interface (SSPI) is an interface
        # that allows us to choose from a set of SSPs available in the
        # system; the idea of SSPI is to keep interface consistent no
        # matter what back end (a.k.a., SSP) we choose.

        # When using SSPI we should not use Kerberos directly as SSP,
        # as remarked in [2], but we can use it indirectly via another
        # SSP named Negotiate that acts as an application layer between
        # SSPI and the other SSPs [1].

        # Negotiate can select between Kerberos and NTLM on the fly;
        # it chooses Kerberos unless it cannot be used by one of the
        # systems involved in the authentication or the calling
        # application did not provide sufficient information to use
        # Kerberos.

        # prefix: https://docs.microsoft.com/en-us/windows/win32/secauthn
        # [1] prefix/microsoft-negotiate?source=recommendations
        # [2] prefix/microsoft-kerberos?source=recommendations
        self.clientauth = sspi.ClientAuth(
            "Negotiate",
            targetspn=targetspn,
            auth_info=_auth_info,
            scflags=sum(flags),
            datarep=sspicon.SECURITY_NETWORK_DREP,
        )

        try:
            data = None
            err, out_buf = self.clientauth.authorize(data)
            logger.debug("Context step err: %s", err)
            logger.debug("Context step out_buf: %s", out_buf)
            logger.debug("Context completed?: %s", self.clientauth.authenticated)
            initial_client_token = out_buf[0].Buffer
            logger.debug("pkg_info: %s", self.clientauth.pkg_info)
        except Exception as err:
            raise InterfaceError(f"Unable to initiate security context: {err}") from err

        logger.debug("Initial client token: %s", initial_client_token)
        return initial_client_token

    def auth_continue(
        self, tgt_auth_challenge: Optional[bytes]
    ) -> Tuple[Optional[bytes], bool]:
        """Continue with the Kerberos TGT service request.

        With the TGT authentication service given response generate a TGT
        service request. This method must be invoked sequentially (in a loop)
        until the security context is completed and an empty response needs to
        be send to acknowledge the server.

        Args:
            tgt_auth_challenge: the challenge for the negotiation.

        Returns:
            tuple (bytearray TGS service request,
            bool True if context is completed otherwise False).
        """
        logger.debug("tgt_auth challenge: %s", tgt_auth_challenge)

        err, out_buf = self.clientauth.authorize(tgt_auth_challenge)

        logger.debug("Context step err: %s", err)
        logger.debug("Context step out_buf: %s", out_buf)
        resp = out_buf[0].Buffer
        logger.debug("Context step resp: %s", resp)
        logger.debug("Context completed?: %s", self.clientauth.authenticated)

        return resp, self.clientauth.authenticated
