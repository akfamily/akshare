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

"""Implementing support for MySQL Authentication Plugins."""

from __future__ import annotations

__all__ = ["MySQLAuthenticator"]

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..errors import InterfaceError, NotSupportedError, get_exception
from ..protocol import (
    AUTH_SWITCH_STATUS,
    DEFAULT_CHARSET_ID,
    DEFAULT_MAX_ALLOWED_PACKET,
    ERR_STATUS,
    EXCHANGE_FURTHER_STATUS,
    MFA_STATUS,
    OK_STATUS,
)
from ..types import HandShakeType
from .logger import logger
from .plugins import MySQLAuthPlugin, get_auth_plugin
from .protocol import MySQLProtocol

if TYPE_CHECKING:
    from .network import MySQLSocket


class MySQLAuthenticator:
    """Implements the authentication phase."""

    def __init__(self) -> None:
        """Constructor."""
        self._username: str = ""
        self._passwords: Dict[int, str] = {}
        self._plugin_config: Dict[str, Any] = {}
        self._ssl_enabled: bool = False
        self._auth_strategy: Optional[MySQLAuthPlugin] = None
        self._auth_plugin_class: Optional[str] = None

    @property
    def ssl_enabled(self) -> bool:
        """Signals whether or not SSL is enabled."""
        return self._ssl_enabled

    @property
    def plugin_config(self) -> Dict[str, Any]:
        """Custom arguments that are being provided to the authentication plugin.

        The parameters defined here will override the ones defined in the
        auth plugin itself.

        The plugin config is a read-only property - the plugin configuration
        provided when invoking `authenticate()` is recorded and can be queried
        by accessing this property.

        Returns:
            dict: The latest plugin configuration provided when invoking
                  `authenticate()`.
        """
        return self._plugin_config

    def update_plugin_config(self, config: Dict[str, Any]) -> None:
        """Update the 'plugin_config' instance variable"""
        self._plugin_config.update(config)

    def _switch_auth_strategy(
        self,
        new_strategy_name: str,
        strategy_class: Optional[str] = None,
        username: Optional[str] = None,
        password_factor: int = 1,
    ) -> None:
        """Switch the authorization plugin.

        Args:
            new_strategy_name: New authorization plugin name to switch to.
            strategy_class: New authorization plugin class to switch to
                            (has higher precedence than the authorization plugin name).
            username: Username to be used - if not defined, the username
                      provided when `authentication()` was invoked is used.
            password_factor: Up to three levels of authentication (MFA) are allowed,
                             hence you can choose the password corresponding to the 1st,
                             2nd, or 3rd factor - 1st is the default.
        """
        if username is None:
            username = self._username

        if strategy_class is None:
            strategy_class = self._auth_plugin_class

        logger.debug("Switching to strategy %s", new_strategy_name)
        self._auth_strategy = get_auth_plugin(
            plugin_name=new_strategy_name, auth_plugin_class=strategy_class
        )(
            username,
            self._passwords.get(password_factor, ""),
            ssl_enabled=self.ssl_enabled,
        )

    async def _mfa_n_factor(
        self,
        sock: MySQLSocket,
        pkt: bytes,
    ) -> Optional[bytes]:
        """Handle MFA (Multi-Factor Authentication) response.

        Up to three levels of authentication (MFA) are allowed.

        Args:
            sock: Pointer to the socket connection.
            pkt: MFA response.

        Returns:
            ok_packet: If last server's response is an OK packet.
            None: If last server's response isn't an OK packet and no ERROR was raised.

        Raises:
            InterfaceError: If got an invalid N factor.
            errors.ErrorTypes: If got an ERROR response.
        """
        n_factor = 2
        while pkt[4] == MFA_STATUS:
            if n_factor not in self._passwords:
                raise InterfaceError(
                    "Failed Multi Factor Authentication (invalid N factor)"
                )

            new_strategy_name, auth_data = MySQLProtocol.parse_auth_next_factor(pkt)
            self._switch_auth_strategy(new_strategy_name, password_factor=n_factor)
            logger.debug("MFA %i factor %s", n_factor, self._auth_strategy.name)

            pkt = await self._auth_strategy.auth_switch_response(
                sock, auth_data, **self._plugin_config
            )

            if pkt[4] == EXCHANGE_FURTHER_STATUS:
                auth_data = MySQLProtocol.parse_auth_more_data(pkt)
                pkt = await self._auth_strategy.auth_more_response(
                    sock, auth_data, **self._plugin_config
                )

            if pkt[4] == OK_STATUS:
                logger.debug("MFA completed succesfully")
                return pkt

            if pkt[4] == ERR_STATUS:
                raise get_exception(pkt)

            n_factor += 1

        logger.warning("MFA terminated with a no ok packet")
        return None

    async def _handle_server_response(
        self,
        sock: MySQLSocket,
        pkt: bytes,
    ) -> Optional[bytes]:
        """Handle server's response.

        Args:
            sock: Pointer to the socket connection.
            pkt: Server's response after completing the `HandShakeResponse`.

        Returns:
            ok_packet: If last server's response is an OK packet.
            None: If last server's response isn't an OK packet and no ERROR was raised.

        Raises:
            errors.ErrorTypes: If got an ERROR response.
            NotSupportedError: If got Authentication with old (insecure) passwords.
        """
        if pkt[4] == AUTH_SWITCH_STATUS and len(pkt) == 5:
            raise NotSupportedError(
                "Authentication with old (insecure) passwords "
                "is not supported. For more information, lookup "
                "Password Hashing in the latest MySQL manual"
            )

        if pkt[4] == AUTH_SWITCH_STATUS:
            logger.debug("Server's response is an auth switch request")
            new_strategy_name, auth_data = MySQLProtocol.parse_auth_switch_request(pkt)
            self._switch_auth_strategy(new_strategy_name)
            pkt = await self._auth_strategy.auth_switch_response(
                sock, auth_data, **self._plugin_config
            )

        if pkt[4] == EXCHANGE_FURTHER_STATUS:
            logger.debug("Exchanging further packets")
            auth_data = MySQLProtocol.parse_auth_more_data(pkt)
            pkt = await self._auth_strategy.auth_more_response(
                sock, auth_data, **self._plugin_config
            )

        if pkt[4] == OK_STATUS:
            logger.debug("%s completed succesfully", self._auth_strategy.name)
            return pkt

        if pkt[4] == MFA_STATUS:
            logger.debug("Starting multi-factor authentication")
            logger.debug("MFA 1 factor %s", self._auth_strategy.name)
            return await self._mfa_n_factor(sock, pkt)

        if pkt[4] == ERR_STATUS:
            raise get_exception(pkt)

        return None

    async def authenticate(
        self,
        sock: MySQLSocket,
        handshake: HandShakeType,
        username: str = "",
        password1: str = "",
        password2: str = "",
        password3: str = "",
        database: Optional[str] = None,
        charset: int = DEFAULT_CHARSET_ID,
        client_flags: int = 0,
        ssl_enabled: bool = False,
        max_allowed_packet: int = DEFAULT_MAX_ALLOWED_PACKET,
        auth_plugin: Optional[str] = None,
        auth_plugin_class: Optional[str] = None,
        conn_attrs: Optional[Dict[str, str]] = None,
        is_change_user_request: bool = False,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> bytes:
        """Perform the authentication phase.

        During re-authentication you must set `is_change_user_request` to True.

        Args:
            sock: Pointer to the socket connection.
            handshake: Initial handshake.
            username: Account's username.
            password1: Account's password factor 1.
            password2: Account's password factor 2.
            password3: Account's password factor 3.
            database: Initial database name for the connection.
            charset: Client charset (see [1]), only the lower 8-bits.
            client_flags: Integer representing client capabilities flags.
            ssl_enabled: Boolean indicating whether SSL is enabled,
            max_allowed_packet: Maximum packet size.
            auth_plugin: Authorization plugin name.
            auth_plugin_class: Authorization plugin class (has higher precedence
                               than the authorization plugin name).
            conn_attrs: Connection attributes.
            is_change_user_request: Whether is a `change user request` operation or not.
            read_timeout: Timeout in seconds upto which the connector should wait for
                          the server to reply back before raising an ReadTimeoutError.
            write_timeout: Timeout in seconds upto which the connector should spend to
                           send data to the server before raising an WriteTimeoutError.

        Returns:
            ok_packet: OK packet.

        Raises:
            InterfaceError: If OK packet is NULL.
            ReadTimeoutError: If the time taken for the server to reply back exceeds
                              'read_timeout' (if set).
            WriteTimeoutError: If the time taken to send data packets to the server
                               exceeds 'write_timeout' (if set).

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_basic_character_set.html#a_protocol_character_set
        """
        # update credentials, plugin config and plugin class
        self._username = username
        self._passwords = {1: password1, 2: password2, 3: password3}
        self._ssl_enabled = ssl_enabled
        self._auth_plugin_class = auth_plugin_class

        # client's handshake response
        response_payload, self._auth_strategy = MySQLProtocol.make_auth(
            handshake=handshake,
            username=username,
            password=password1,
            database=database,
            charset=charset,
            client_flags=client_flags,
            max_allowed_packet=max_allowed_packet,
            auth_plugin=auth_plugin,
            auth_plugin_class=auth_plugin_class,
            conn_attrs=conn_attrs,
            is_change_user_request=is_change_user_request,
            ssl_enabled=self.ssl_enabled,
            plugin_config=self.plugin_config,
        )

        # client sends transaction response
        send_args = (
            (0, 0, write_timeout)
            if is_change_user_request
            else (None, None, write_timeout)
        )
        await sock.write(response_payload, *send_args)

        # server replies back
        pkt = bytes(await sock.read(read_timeout))

        ok_pkt = await self._handle_server_response(sock, pkt)
        if ok_pkt is None:
            raise InterfaceError("Got a NULL ok_pkt") from None

        return ok_pkt
