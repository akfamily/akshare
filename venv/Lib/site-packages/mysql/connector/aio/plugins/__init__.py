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

"""Base Authentication Plugin class."""

__all__ = ["MySQLAuthPlugin", "get_auth_plugin"]

import importlib

from abc import ABC, abstractmethod
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Optional, Type

from mysql.connector.errors import NotSupportedError, ProgrammingError
from mysql.connector.logger import logger

if TYPE_CHECKING:
    from ..network import MySQLSocket

DEFAULT_PLUGINS_PKG = "mysql.connector.aio.plugins"


class MySQLAuthPlugin(ABC):
    """Authorization plugin interface."""

    def __init__(
        self,
        username: str,
        password: str,
        ssl_enabled: bool = False,
    ) -> None:
        """Constructor."""
        self._username: str = "" if username is None else username
        self._password: str = "" if password is None else password
        self._ssl_enabled: bool = ssl_enabled

    @property
    def ssl_enabled(self) -> bool:
        """Signals whether or not SSL is enabled."""
        return self._ssl_enabled

    @property
    @abstractmethod
    def requires_ssl(self) -> bool:
        """Signals whether or not SSL is required."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin official name."""

    @abstractmethod
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
            packet: Last server's response after back-and-forth communication.
        """
        raise NotImplementedError

    @abstractmethod
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
            packet: Last server's response after back-and-forth communication.
        """


@lru_cache(maxsize=10, typed=False)
def get_auth_plugin(
    plugin_name: str,
    auth_plugin_class: Optional[str] = None,
) -> Type[MySQLAuthPlugin]:
    """Return authentication class based on plugin name

    This function returns the class for the authentication plugin plugin_name.
    The returned class is a subclass of BaseAuthPlugin.

    Args:
        plugin_name (str): Authentication plugin name.
        auth_plugin_class (str): Authentication plugin class name.

    Raises:
        NotSupportedError: When plugin_name is not supported.

    Returns:
        Subclass of `MySQLAuthPlugin`.
    """
    package = DEFAULT_PLUGINS_PKG
    if plugin_name:
        try:
            logger.info("package: %s", package)
            logger.info("plugin_name: %s", plugin_name)
            plugin_module = importlib.import_module(f".{plugin_name}", package)
            if not auth_plugin_class or not hasattr(plugin_module, auth_plugin_class):
                auth_plugin_class = plugin_module.AUTHENTICATION_PLUGIN_CLASS
            logger.info("AUTHENTICATION_PLUGIN_CLASS: %s", auth_plugin_class)
            return getattr(plugin_module, auth_plugin_class)
        except ModuleNotFoundError as err:
            logger.warning("Requested Module was not found: %s", err)
        except ValueError as err:
            raise ProgrammingError(f"Invalid module name: {err}") from err
    raise NotSupportedError(f"Authentication plugin '{plugin_name}' is not supported")
