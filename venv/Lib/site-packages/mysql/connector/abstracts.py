# Copyright (c) 2014, 2025, Oracle and/or its affiliates.
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

# mypy: disable-error-code="assignment,attr-defined"

"""Module gathering all abstract base classes."""

from __future__ import annotations

import os
import re
import weakref

from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from inspect import signature
from time import sleep
from types import TracebackType
from typing import (
    Any,
    BinaryIO,
    Callable,
    ClassVar,
    Deque,
    Dict,
    Generator,
    Iterator,
    List,
    Mapping,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

TLS_V1_3_SUPPORTED = False
try:
    import ssl

    if hasattr(ssl, "HAS_TLSv1_3") and ssl.HAS_TLSv1_3:
        TLS_V1_3_SUPPORTED = True
except ImportError:
    # If import fails, we don't have SSL support.
    pass

from .constants import (
    CONN_ATTRS_DN,
    DEFAULT_CONFIGURATION,
    DEPRECATED_METHOD_WARNING,
    MYSQL_DEFAULT_CHARSET_ID_57,
    MYSQL_DEFAULT_CHARSET_ID_80,
    OPENSSL_CS_NAMES,
    TLS_CIPHER_SUITES,
    TLS_VERSIONS,
    CharacterSet,
    ClientFlag,
)
from .conversion import MySQLConverter, MySQLConverterBase
from .errors import (
    DatabaseError,
    Error,
    InterfaceError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)
from .opentelemetry.constants import (
    CONNECTION_SPAN_NAME,
    OPTION_CNX_SPAN,
    OPTION_CNX_TRACER,
    OTEL_ENABLED,
)

if OTEL_ENABLED:
    from .opentelemetry.instrumentation import (
        end_span,
        record_exception_event,
        set_connection_span_attrs,
        trace,
    )

from ._decorating import deprecated
from .optionfiles import read_option_files
from .tls_ciphers import UNACCEPTABLE_TLS_CIPHERSUITES, UNACCEPTABLE_TLS_VERSIONS
from .types import (
    BinaryProtocolType,
    CextEofPacketType,
    DescriptionType,
    EofPacketType,
    HandShakeType,
    MySQLConvertibleType,
    MySQLScriptPartition,
    RowItemType,
    RowType,
    StrOrBytes,
    WarningType,
)
from .utils import GenericWrapper, import_object

DUPLICATED_IN_LIST_ERROR = (
    "The '{list}' list must not contain repeated values, the value "
    "'{value}' is duplicated."
)

TLS_VERSION_ERROR = (
    "The given tls_version: '{}' is not recognized as a valid "
    "TLS protocol version (should be one of {})."
)

TLS_VERSION_UNACCEPTABLE_ERROR = (
    "The given tls_version: '{}' are no longer allowed (should be one of {})."
)

TLS_VER_NO_SUPPORTED = (
    "No supported TLS protocol version found in the 'tls-versions' list '{}'. "
)

KRB_SERVICE_PRINCIPAL_ERROR = (
    'Option "krb_service_principal" {error}, must be a string in the form '
    '"primary/instance@realm" e.g "ldap/ldapauth@MYSQL.COM" where "@realm" '
    "is optional and if it is not given will be assumed to belong to the "
    "default realm, as configured in the krb5.conf file."
)

OPENID_TOKEN_FILE_ERROR = (
    'Option "openid_token_file" {error}, it must be a string in the form '
    '"path/to/openid/token/file".'
)

MYSQL_PY_TYPES = (
    Decimal,
    bytes,
    date,
    datetime,
    float,
    int,
    str,
    time,
    timedelta,
)


class CMySQLPrepStmt(GenericWrapper):
    """Structure to represent a result from `CMySQLConnection.cmd_stmt_prepare`.
    It can be used consistently as a type hint.

    `_mysql_connector.MySQLPrepStmt` isn't available when the C-ext isn't built.

    In this regard, `CmdStmtPrepareResult` acts as a proxy/wrapper entity for a
    `_mysql_connector.MySQLPrepStmt` instance.
    """


class MySQLConnectionAbstract(ABC):
    """Abstract class for classes connecting to a MySQL server."""

    def __init__(self) -> None:
        """Initialize"""
        # private (shouldn't be manipulated directly internally)
        self.__charset_id: Optional[int] = None
        """It shouldn't be manipulated directly, even internally. If you need
        to manipulate the charset ID, use the property `_charset_id` (read & write)
        instead. Similarly, `_charset_id` shouldn't be manipulated externally,
        in this case, use property `charset_id` (read-only).
        """

        # protected (can be manipulated directly internally)
        self._tracer: Any = None  # opentelemetry related
        self._span: Any = None  # opentelemetry related
        self.otel_context_propagation: bool = True  # opentelemetry related

        self._client_flags: int = ClientFlag.get_default()
        self._sql_mode: Optional[str] = None
        self._time_zone: Optional[str] = None
        self._autocommit: bool = False
        self._server_version: Optional[Tuple[int, ...]] = None
        self._handshake: Optional[HandShakeType] = None
        self._conn_attrs: Dict[str, str] = {}

        self._user: str = ""
        self._password: str = ""
        self._password1: str = ""
        self._password2: str = ""
        self._password3: str = ""
        self._database: str = ""
        self._host: str = "127.0.0.1"
        self._port: int = 3306
        self._unix_socket: Optional[str] = None
        self._client_host: str = ""
        self._client_port: int = 0
        self._ssl: Dict[str, Optional[Union[str, bool, List[str]]]] = {}
        self._ssl_disabled: bool = DEFAULT_CONFIGURATION["ssl_disabled"]
        self._force_ipv6: bool = False
        self._oci_config_file: Optional[str] = None
        self._oci_config_profile: Optional[str] = None
        self._webauthn_callback: Optional[Union[str, Callable[[str], None]]] = None
        self._krb_service_principal: Optional[str] = None
        self._openid_token_file: Optional[str] = None

        self._use_unicode: bool = True
        self._get_warnings: bool = False
        self._raise_on_warnings: bool = False
        self._connection_timeout: Optional[int] = DEFAULT_CONFIGURATION[
            "connect_timeout"
        ]
        self._read_timeout: Optional[int] = DEFAULT_CONFIGURATION["read_timeout"]
        self._write_timeout: Optional[int] = DEFAULT_CONFIGURATION["write_timeout"]
        self._buffered: bool = False
        self._unread_result: bool = False
        self._have_next_result: bool = False
        self._raw: bool = False
        self._in_transaction: bool = False
        self._allow_local_infile: bool = DEFAULT_CONFIGURATION["allow_local_infile"]
        self._allow_local_infile_in_path: Optional[str] = DEFAULT_CONFIGURATION[
            "allow_local_infile_in_path"
        ]

        self._prepared_statements: Any = None
        self._query_attrs: Dict[str, BinaryProtocolType] = {}

        self._ssl_active: bool = False
        self._auth_plugin: Optional[str] = None
        self._auth_plugin_class: Optional[str] = None
        self._pool_config_version: Any = None
        self.converter: Optional[MySQLConverter] = None
        self._converter_class: Optional[Type[MySQLConverter]] = None
        self._converter_str_fallback: bool = False
        self._compress: bool = False

        self._consume_results: bool = False
        self._init_command: Optional[str] = None
        self._character_set: CharacterSet = CharacterSet()

        self._local_infile_filenames: Optional[Deque[str]] = None
        """Stores the filenames from `LOCAL INFILE` requests
        found in the executed query."""

        self._query: Optional[bytes] = None
        """The query being processed."""

    def __enter__(self) -> MySQLConnectionAbstract:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.close()

    def get_self(self) -> MySQLConnectionAbstract:
        """Returns self for `weakref.proxy`.

        This method is used when the original object is needed when using
        `weakref.proxy`.
        """
        return self

    @property
    def is_secure(self) -> bool:
        """Returns `True` if is a secure connection."""
        return self._ssl_active or (
            self._unix_socket is not None and os.name == "posix"
        )

    @property
    def have_next_result(self) -> bool:
        """Returns If have next result."""
        return self._have_next_result

    @property
    def query_attrs(self) -> List[Tuple[str, BinaryProtocolType]]:
        """Returns query attributes list."""
        return list(self._query_attrs.items())

    def query_attrs_append(self, value: Tuple[str, BinaryProtocolType]) -> None:
        """Adds element to the query attributes list on the connector's side.

        If an element in the query attributes list already matches
        the attribute name provided, the new element will NOT be added.

        Args:
            value: key-value as a 2-tuple.
        """
        attr_name, attr_value = value
        if attr_name not in self._query_attrs:
            self._query_attrs[attr_name] = attr_value

    def query_attrs_remove(self, name: str) -> BinaryProtocolType:
        """Removes element by name from the query attributes list on the connector's side.

        If no match, `None` is returned, else the corresponding value is returned.

        Args:
            name: key name.
        """
        return self._query_attrs.pop(name, None)

    def query_attrs_clear(self) -> None:
        """Clears query attributes list on the connector's side."""
        self._query_attrs = {}

    def _validate_tls_ciphersuites(self) -> None:
        """Validates the tls_ciphersuites option."""
        tls_ciphersuites = []
        tls_cs = self._ssl["tls_ciphersuites"]

        if isinstance(tls_cs, str):
            if not (tls_cs.startswith("[") and tls_cs.endswith("]")):
                raise AttributeError(
                    f"tls_ciphersuites must be a list, found: '{tls_cs}'"
                )
            tls_css = tls_cs[1:-1].split(",")
            if not tls_css:
                raise AttributeError(
                    "No valid cipher suite found in 'tls_ciphersuites' list"
                )
            for _tls_cs in tls_css:
                _tls_cs = tls_cs.strip().upper()
                if _tls_cs:
                    tls_ciphersuites.append(_tls_cs)

        elif isinstance(tls_cs, (list, set)):
            tls_ciphersuites = [tls_cs for tls_cs in tls_cs if tls_cs]
        else:
            raise AttributeError(
                "tls_ciphersuites should be a list with one or more "
                f"ciphersuites. Found: '{tls_cs}'"
            )

        tls_versions = (
            TLS_VERSIONS[:]
            if self._ssl.get("tls_versions", None) is None
            else self._ssl["tls_versions"][:]  # type: ignore[index]
        )

        # A newer TLS version can use a cipher introduced on
        # an older version.
        tls_versions.sort(reverse=True)  # type: ignore[union-attr]
        newer_tls_ver = tls_versions[0]
        # translated_names[0] are TLSv1.2 only
        # translated_names[1] are TLSv1.3 only
        translated_names: List[List[str]] = [[], []]
        iani_cipher_suites_names = {}
        ossl_cipher_suites_names: List[str] = []

        # Old ciphers can work with new TLS versions.
        # Find all the ciphers introduced on previous TLS versions.
        for tls_ver in TLS_VERSIONS[: TLS_VERSIONS.index(newer_tls_ver) + 1]:
            iani_cipher_suites_names.update(TLS_CIPHER_SUITES[tls_ver])
            ossl_cipher_suites_names.extend(OPENSSL_CS_NAMES[tls_ver])

        for name in tls_ciphersuites:
            if "-" in name and name in ossl_cipher_suites_names:
                if name in OPENSSL_CS_NAMES["TLSv1.3"]:
                    translated_names[1].append(name)
                else:
                    translated_names[0].append(name)
            elif name in iani_cipher_suites_names:
                translated_name = iani_cipher_suites_names[name]
                if translated_name in translated_names:
                    raise AttributeError(
                        DUPLICATED_IN_LIST_ERROR.format(
                            list="tls_ciphersuites", value=translated_name
                        )
                    )
                if name in TLS_CIPHER_SUITES["TLSv1.3"]:
                    translated_names[1].append(iani_cipher_suites_names[name])
                else:
                    translated_names[0].append(iani_cipher_suites_names[name])
            else:
                raise AttributeError(
                    f"The value '{name}' in tls_ciphersuites is not a valid "
                    "cipher suite"
                )
        if not translated_names[0] and not translated_names[1]:
            raise AttributeError(
                "No valid cipher suite found in the 'tls_ciphersuites' list"
            )

        # raise an error when using an unacceptable cipher
        for cipher_as_ossl in translated_names[0]:
            if cipher_as_ossl in UNACCEPTABLE_TLS_CIPHERSUITES["TLSv1.2"].values():
                raise NotSupportedError(
                    f"Cipher {cipher_as_ossl} when used with TLSv1.2 is unacceptable."
                )
        for cipher_as_ossl in translated_names[1]:
            if cipher_as_ossl in UNACCEPTABLE_TLS_CIPHERSUITES["TLSv1.3"].values():
                raise NotSupportedError(
                    f"Cipher {cipher_as_ossl} when used with TLSv1.3 is unacceptable."
                )

        self._ssl["tls_ciphersuites"] = [
            ":".join(translated_names[0]),
            ":".join(translated_names[1]),
        ]

    def _validate_tls_versions(self) -> None:
        """Validates the tls_versions option."""
        tls_versions = []
        tls_version = self._ssl["tls_versions"]

        if isinstance(tls_version, str):
            if not (tls_version.startswith("[") and tls_version.endswith("]")):
                raise AttributeError(
                    f"tls_versions must be a list, found: '{tls_version}'"
                )
            tls_vers = tls_version[1:-1].split(",")
            for tls_ver in tls_vers:
                tls_version = tls_ver.strip()
                if tls_version == "":
                    continue
                if tls_version in tls_versions:
                    raise AttributeError(
                        DUPLICATED_IN_LIST_ERROR.format(
                            list="tls_versions", value=tls_version
                        )
                    )
                tls_versions.append(tls_version)
            if tls_vers == ["TLSv1.3"] and not TLS_V1_3_SUPPORTED:
                raise AttributeError(
                    TLS_VER_NO_SUPPORTED.format(tls_version, TLS_VERSIONS)
                )
        elif isinstance(tls_version, list):
            if not tls_version:
                raise AttributeError(
                    "At least one TLS protocol version must be specified in "
                    "'tls_versions' list"
                )
            for tls_ver in tls_version:
                if tls_ver in tls_versions:
                    raise AttributeError(
                        DUPLICATED_IN_LIST_ERROR.format(
                            list="tls_versions", value=tls_ver
                        )
                    )
                tls_versions.append(tls_ver)
        elif isinstance(tls_version, set):
            for tls_ver in tls_version:
                tls_versions.append(tls_ver)
        else:
            raise AttributeError(
                "tls_versions should be a list with one or more of versions "
                f"in {', '.join(TLS_VERSIONS)}. found: '{tls_versions}'"
            )

        if not tls_versions:
            raise AttributeError(
                "At least one TLS protocol version must be specified "
                "in 'tls_versions' list when this option is given"
            )

        use_tls_versions = []
        unacceptable_tls_versions = []
        invalid_tls_versions = []
        for tls_ver in tls_versions:
            if tls_ver in TLS_VERSIONS:
                use_tls_versions.append(tls_ver)
            if tls_ver in UNACCEPTABLE_TLS_VERSIONS:
                unacceptable_tls_versions.append(tls_ver)
            else:
                invalid_tls_versions.append(tls_ver)

        if use_tls_versions:
            if use_tls_versions == ["TLSv1.3"] and not TLS_V1_3_SUPPORTED:
                raise NotSupportedError(
                    TLS_VER_NO_SUPPORTED.format(tls_version, TLS_VERSIONS)
                )
            self._ssl["tls_versions"] = use_tls_versions
        elif unacceptable_tls_versions:
            raise NotSupportedError(
                TLS_VERSION_UNACCEPTABLE_ERROR.format(
                    unacceptable_tls_versions, TLS_VERSIONS
                )
            )
        elif invalid_tls_versions:
            raise AttributeError(TLS_VERSION_ERROR.format(tls_ver, TLS_VERSIONS))

    @property
    def user(self) -> str:
        """The user name used for connecting to the MySQL server."""
        return self._user

    @property
    def server_host(self) -> str:
        """MySQL server IP address or name."""
        return self._host

    @property
    def server_port(self) -> int:
        "MySQL server TCP/IP port."
        return self._port

    @property
    def unix_socket(self) -> Optional[str]:
        "The Unix socket file for connecting to the MySQL server."
        return self._unix_socket

    @property
    @abstractmethod
    def database(self) -> str:
        """The current database."""

    @database.setter
    def database(self, value: str) -> None:
        """Sets the current database."""
        self.cmd_query(f"USE {value}")

    @property
    def can_consume_results(self) -> bool:
        """Returns whether to consume results."""
        return self._consume_results

    @can_consume_results.setter
    def can_consume_results(self, value: bool) -> None:
        """Sets if can consume results."""
        assert isinstance(value, bool)
        self._consume_results = value

    @property
    def pool_config_version(self) -> Any:
        """Returns the pool configuration version."""
        return self._pool_config_version

    @pool_config_version.setter
    def pool_config_version(self, value: Any) -> None:
        """Sets the pool configuration version"""
        self._pool_config_version = value

    def config(self, **kwargs: Any) -> None:
        """Configures the MySQL Connection.

        This method allows you to configure the `MySQLConnection`
        instance after it has been instantiated.

        Args:
            **kwargs: For a complete list of possible arguments, see [1].

        Raises:
            AttributeError: When provided unsupported connection arguments.
            InterfaceError: When the provided connection argument is invalid.

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        """
        # opentelemetry related
        self._span = kwargs.pop(OPTION_CNX_SPAN, None)
        self._tracer = kwargs.pop(OPTION_CNX_TRACER, None)

        config = kwargs.copy()
        if "dsn" in config:
            raise NotSupportedError("Data source name is not supported")

        # Read option files
        config = read_option_files(**config)

        # Configure how we handle MySQL warnings
        try:
            self.get_warnings = config["get_warnings"]
            del config["get_warnings"]
        except KeyError:
            pass  # Leave what was set or default
        try:
            self.raise_on_warnings = config["raise_on_warnings"]
            del config["raise_on_warnings"]
        except KeyError:
            pass  # Leave what was set or default

        # Configure client flags
        try:
            default = ClientFlag.get_default()
            self.client_flags = config["client_flags"] or default
            del config["client_flags"]
        except KeyError:
            pass  # Missing client_flags-argument is OK

        try:
            if config["compress"]:
                self._compress = True
                self.client_flags = [ClientFlag.COMPRESS]
        except KeyError:
            pass  # Missing compress argument is OK

        self._allow_local_infile = config.get(
            "allow_local_infile", DEFAULT_CONFIGURATION["allow_local_infile"]
        )
        self._allow_local_infile_in_path = config.get(
            "allow_local_infile_in_path",
            DEFAULT_CONFIGURATION["allow_local_infile_in_path"],
        )
        infile_in_path = None
        if self._allow_local_infile_in_path:
            infile_in_path = os.path.abspath(self._allow_local_infile_in_path)
            if (
                infile_in_path
                and os.path.exists(infile_in_path)
                and not os.path.isdir(infile_in_path)
                or os.path.islink(infile_in_path)
            ):
                raise AttributeError("allow_local_infile_in_path must be a directory")
        if self._allow_local_infile or self._allow_local_infile_in_path:
            self.client_flags = [ClientFlag.LOCAL_FILES]
        else:
            self.client_flags = [-ClientFlag.LOCAL_FILES]

        try:
            if not config["consume_results"]:
                self._consume_results = False
            else:
                self._consume_results = True
        except KeyError:
            self._consume_results = False

        # Configure auth_plugin
        try:
            self._auth_plugin = config["auth_plugin"]
            del config["auth_plugin"]
        except KeyError:
            self._auth_plugin = ""

        # Disallow the usage of some default authentication plugins
        if self._auth_plugin == "authentication_webauthn_client":
            raise InterfaceError(
                f"'{self._auth_plugin}' cannot be used as the default authentication "
                "plugin"
            )

        # Set converter class
        try:
            self.converter_class = config["converter_class"]
        except KeyError:
            pass  # Using default converter class
        except TypeError as err:
            raise AttributeError(
                "Converter class should be a subclass of "
                "conversion.MySQLConverterBase"
            ) from err

        # Compatible configuration with other drivers
        compat_map = [
            # (<other driver argument>,<translates to>)
            ("db", "database"),
            ("username", "user"),
            ("passwd", "password"),
            ("connect_timeout", "connection_timeout"),
            ("read_default_file", "option_files"),
        ]
        for compat, translate in compat_map:
            try:
                if translate not in config:
                    config[translate] = config[compat]
                del config[compat]
            except KeyError:
                pass  # Missing compat argument is OK

        # Configure login information
        if "user" in config or "password" in config:
            try:
                user = config["user"]
                del config["user"]
            except KeyError:
                user = self._user
            try:
                password = config["password"]
                del config["password"]
            except KeyError:
                password = self._password
            self.set_login(user, password)

        # Configure host information
        if "host" in config and config["host"]:
            self._host = config["host"]

        # Check network locations
        try:
            self._port = int(config["port"])
            del config["port"]
        except KeyError:
            pass  # Missing port argument is OK
        except ValueError as err:
            raise InterfaceError("TCP/IP port number should be an integer") from err

        if "ssl_disabled" in config:
            self._ssl_disabled = config.pop("ssl_disabled")

        # If an init_command is set, keep it, so we can execute it in _post_connection
        if "init_command" in config:
            self._init_command = config["init_command"]
            del config["init_command"]

        # Other configuration
        set_ssl_flag = False
        for key, value in config.items():
            try:
                DEFAULT_CONFIGURATION[key]
            except KeyError:
                raise AttributeError(f"Unsupported argument '{key}'") from None
            # SSL Configuration
            if key.startswith("ssl_"):
                set_ssl_flag = True
                self._ssl.update({key.replace("ssl_", ""): value})
            elif key.startswith("tls_"):
                set_ssl_flag = True
                self._ssl.update({key: value})
            else:
                attribute = "_" + key
                try:
                    setattr(self, attribute, value.strip())
                except AttributeError:
                    setattr(self, attribute, value)

        # Disable SSL for unix socket connections
        if self._unix_socket and os.name == "posix":
            self._ssl_disabled = True

        if self._ssl_disabled:
            if self._auth_plugin == "mysql_clear_password":
                raise InterfaceError(
                    "Clear password authentication is not supported over insecure channels"
                )
            if self._auth_plugin == "authentication_openid_connect_client":
                raise InterfaceError(
                    "OpenID Connect authentication is not supported over insecure channels"
                )

        if set_ssl_flag:
            if "verify_cert" not in self._ssl:
                self._ssl["verify_cert"] = DEFAULT_CONFIGURATION["ssl_verify_cert"]
            if "verify_identity" not in self._ssl:
                self._ssl["verify_identity"] = DEFAULT_CONFIGURATION[
                    "ssl_verify_identity"
                ]
            # Make sure both ssl_key/ssl_cert are set, or neither (XOR)
            if "ca" not in self._ssl or self._ssl["ca"] is None:
                self._ssl["ca"] = ""
            if bool("key" in self._ssl) != bool("cert" in self._ssl):
                raise AttributeError(
                    "ssl_key and ssl_cert need to be both specified, or neither"
                )
            # Make sure key/cert are set to None
            if not set(("key", "cert")) <= set(self._ssl):
                self._ssl["key"] = None
                self._ssl["cert"] = None
            elif (self._ssl["key"] is None) != (self._ssl["cert"] is None):
                raise AttributeError(
                    "ssl_key and ssl_cert need to be both set, or neither"
                )
            if self._ssl.get("tls_versions") is not None:
                self._validate_tls_versions()

            if self._ssl.get("tls_ciphersuites") is not None:
                self._validate_tls_ciphersuites()

        if self._conn_attrs is None:
            self._conn_attrs = {}
        elif not isinstance(self._conn_attrs, dict):
            raise InterfaceError("conn_attrs must be of type dict")
        else:
            for attr_name, attr_value in self._conn_attrs.items():
                if attr_name in CONN_ATTRS_DN:
                    continue
                # Validate name type
                if not isinstance(attr_name, str):
                    raise InterfaceError(
                        "Attribute name should be a string, found: "
                        f"'{attr_name}' in '{self._conn_attrs}'"
                    )
                # Validate attribute name limit 32 characters
                if len(attr_name) > 32:
                    raise InterfaceError(
                        f"Attribute name '{attr_name}' exceeds 32 characters limit size"
                    )
                # Validate names in connection attributes cannot start with "_"
                if attr_name.startswith("_"):
                    raise InterfaceError(
                        "Key names in connection attributes cannot start with "
                        "'_', found: '{attr_name}'"
                    )
                # Validate value type
                if not isinstance(attr_value, str):
                    raise InterfaceError(
                        f"Attribute '{attr_name}' value: '{attr_value}' must "
                        "be a string type"
                    )
                # Validate attribute value limit 1024 characters
                if len(attr_value) > 1024:
                    raise InterfaceError(
                        f"Attribute '{attr_name}' value: '{attr_value}' "
                        "exceeds 1024 characters limit size"
                    )

        if self._client_flags & ClientFlag.CONNECT_ARGS:
            self._add_default_conn_attrs()

        if "kerberos_auth_mode" in config and config["kerberos_auth_mode"] is not None:
            if not isinstance(config["kerberos_auth_mode"], str):
                raise InterfaceError("'kerberos_auth_mode' must be of type str")
            kerberos_auth_mode = config["kerberos_auth_mode"].lower()
            if kerberos_auth_mode == "sspi":
                if os.name != "nt":
                    raise InterfaceError(
                        "'kerberos_auth_mode=SSPI' is only available on Windows"
                    )
                self._auth_plugin_class = "MySQLSSPIKerberosAuthPlugin"
            elif kerberos_auth_mode == "gssapi":
                self._auth_plugin_class = "MySQLKerberosAuthPlugin"
            else:
                raise InterfaceError(
                    "Invalid 'kerberos_auth_mode' mode. Please use 'SSPI' or 'GSSAPI'"
                )

        if (
            "krb_service_principal" in config
            and config["krb_service_principal"] is not None
        ):
            self._krb_service_principal = config["krb_service_principal"]
            if not isinstance(self._krb_service_principal, str):
                raise InterfaceError(
                    KRB_SERVICE_PRINCIPAL_ERROR.format(error="is not a string")
                )
            if self._krb_service_principal == "":
                raise InterfaceError(
                    KRB_SERVICE_PRINCIPAL_ERROR.format(
                        error="can not be an empty string"
                    )
                )
            if "/" not in self._krb_service_principal:
                raise InterfaceError(
                    KRB_SERVICE_PRINCIPAL_ERROR.format(error="is incorrectly formatted")
                )

        if self._webauthn_callback:
            self._validate_callable("webauth_callback", self._webauthn_callback, 1)

        if config.get("openid_token_file") is not None:
            self._openid_token_file = config["openid_token_file"]
            if not isinstance(self._openid_token_file, str):
                raise InterfaceError(
                    OPENID_TOKEN_FILE_ERROR.format(error="is not a string")
                )
            if self._openid_token_file == "":
                raise InterfaceError(
                    OPENID_TOKEN_FILE_ERROR.format(error="cannot be an empty string")
                )
            if not os.path.exists(self._openid_token_file):
                raise InterfaceError(
                    f"The path '{self._openid_token_file}' provided via 'openid_token_file' "
                    "does not exist"
                )

        if config.get("read_timeout") is not None:
            self._read_timeout = config["read_timeout"]
            if not isinstance(self._read_timeout, int) or self._read_timeout < 0:
                raise InterfaceError("Option read_timeout must be a positive integer")
        if config.get("write_timeout") is not None:
            self._write_timeout = config["write_timeout"]
            if not isinstance(self._write_timeout, int) or self._write_timeout < 0:
                raise InterfaceError("Option write_timeout must be a positive integer")

    def _add_default_conn_attrs(self) -> None:
        """Adds the default connection attributes."""

    @staticmethod
    def _validate_callable(
        option_name: str, callback: Union[str, Callable], num_args: int = 0
    ) -> None:
        """Validates if it's a Python callable.

         Args:
             option_name (str): Connection option name.
             callback (str or callable): The fully qualified path to the callable or
                                         a callable.
             num_args (int): Number of positional arguments allowed.

        Raises:
             ProgrammingError: If `callback` is not valid or wrong number of positional
                               arguments.

        .. versionadded:: 8.2.0
        """
        if isinstance(callback, str):
            try:
                callback = import_object(callback)
            except ValueError as err:
                raise ProgrammingError(f"{err}") from err

        if not callable(callback):
            raise ProgrammingError(f"Expected a callable for '{option_name}'")

        # Check if the callable signature has <num_args> positional arguments
        num_params = len(signature(callback).parameters)
        if num_params != num_args:
            raise ProgrammingError(
                f"'{option_name}' requires {num_args} positional argument, but the "
                f"callback provided has {num_params}"
            )

    @staticmethod
    def _check_server_version(server_version: StrOrBytes) -> Tuple[int, ...]:
        """Checks the MySQL version.

        This method will check the MySQL version and raise an InterfaceError
        when it is not supported or invalid. It will return the version
        as a tuple with major, minor and patch.

        Raises InterfaceError if invalid server version.

        Returns tuple
        """
        if isinstance(server_version, (bytearray, bytes)):
            server_version = server_version.decode()

        regex_ver = re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{1,3})(.*)")
        match = regex_ver.match(server_version)
        if not match:
            raise InterfaceError("Failed parsing MySQL version")

        version = tuple(int(v) for v in match.groups()[0:3])
        if version < (4, 1):
            raise InterfaceError(f"MySQL Version '{server_version}' is not supported")

        return version

    @deprecated(DEPRECATED_METHOD_WARNING.format(property_name="server_version"))
    def get_server_version(self) -> Optional[Tuple[int, ...]]:
        """Gets the MySQL version.

        Returns:
            The MySQL server version as a tuple. If not previously connected, it will
            return `None`.
        """
        return self._server_version

    @deprecated(DEPRECATED_METHOD_WARNING.format(property_name="server_info"))
    def get_server_info(self) -> Optional[str]:
        """Gets the original MySQL version information.

        Returns:
            The original MySQL server as text. If not previously connected, it will
            return `None`.
        """
        return self.server_info

    @property
    def server_version(self) -> Optional[Tuple[int, ...]]:
        """Gets the MySQL Server version the connector is connected to.

        Returns:
            The MySQL server version as a tuple. If not previously connected, it will
            return `None`.
        """
        return self._server_version

    @property
    def server_info(self) -> Optional[str]:
        """Gets the original MySQL server version information.

        Returns:
            The original MySQL server as text. If not previously connected, it will
            return `None`.
        """
        try:
            return self._handshake["server_version_original"]  # type: ignore[return-value]
        except (TypeError, KeyError):
            return None

    @property
    @abstractmethod
    def in_transaction(self) -> bool:
        """Returns bool to indicate whether a transaction is active for the connection.

        The value is `True` regardless of whether you start a transaction using the
        `start_transaction()` API call or by directly executing an SQL statement such
        as START TRANSACTION or BEGIN.

        `in_transaction` was added in MySQL Connector/Python 1.1.0.

        Examples:
            ```
            >>> cnx.start_transaction()
            >>> cnx.in_transaction
            True
            >>> cnx.commit()
            >>> cnx.in_transaction
            False
            ```
        """

    @deprecated(DEPRECATED_METHOD_WARNING.format(property_name="client_flags"))
    def set_client_flags(self, flags: Union[int, Sequence[int]]) -> int:
        """Sets the client flags.

        The flags-argument can be either an int or a list (or tuple) of
        ClientFlag-values. If it is an integer, it will set client_flags
        to flags as is.

        If flags is a sequence, each item in the sequence sets the flag when the
        value is positive or unsets it when negative (see example below).

        Args:
            flags: A list (or tuple), each flag will be set or unset when it's negative.

        Returns:
            integer: Client flags.

        Raises:
            ProgrammingError: When the flags argument is not a set or an integer
                              bigger than 0.

        Examples:
            ```
            For example, to unset `LONG_FLAG` and set the `FOUND_ROWS` flags:
            >>> from mysql.connector.constants import ClientFlag
            >>> cnx.set_client_flags([ClientFlag.FOUND_ROWS, -ClientFlag.LONG_FLAG])
            >>> cnx.reconnect()
            ```
        """
        self.client_flags = flags
        return self.client_flags

    @property
    def client_flags(self) -> int:
        """Gets the client flags of the current session."""
        return self._client_flags

    @client_flags.setter
    def client_flags(self, flags: Union[int, Sequence[int]]) -> None:
        """Sets the client flags.

        The flags-argument can be either an int or a list (or tuple) of
        ClientFlag-values. If it is an integer, it will set client_flags
        to flags as is.

        If flags is a sequence, each item in the sequence sets the flag when the
        value is positive or unsets it when negative (see example below).

        Args:
            flags: A list (or tuple), each flag will be set or unset when it's negative.

        Raises:
            ProgrammingError: When the flags argument is not a set or an integer
                              bigger than 0.

        Examples:
            ```
            For example, to unset `LONG_FLAG` and set the `FOUND_ROWS` flags:
            >>> from mysql.connector.constants import ClientFlag
            >>> cnx.client_flags = [ClientFlag.FOUND_ROWS, -ClientFlag.LONG_FLAG]
            >>> cnx.reconnect()
            ```
        """
        if isinstance(flags, int) and flags > 0:
            self._client_flags = flags
        elif isinstance(flags, (tuple, list)):
            for flag in flags:
                if flag < 0:
                    self._client_flags &= ~abs(flag)
                else:
                    self._client_flags |= flag
        else:
            raise ProgrammingError("client_flags setter expect integer (>0) or set")

    def shutdown(self) -> NoReturn:
        """Shuts down connection to MySQL Server.

        This method closes the socket. It raises no exceptions.

        Unlike `disconnect()`, `shutdown()` closes the client connection without
        attempting to send a `QUIT` command to the server first. Thus, it will not
        block if the connection is disrupted for some reason such as network failure.
        """
        raise NotImplementedError

    def isset_client_flag(self, flag: int) -> bool:
        """Checks if a client flag is set.

        Returns:
            `True` if the client flag was set, `False` otherwise.
        """
        return (self._client_flags & flag) > 0

    @property
    def time_zone(self) -> str:
        """Gets the current time zone."""
        return self.info_query("SELECT @@session.time_zone")[
            0
        ]  # type: ignore[return-value]

    @time_zone.setter
    def time_zone(self, value: str) -> None:
        """Sets the time zone."""
        self.cmd_query(f"SET @@session.time_zone = '{value}'")
        self._time_zone = value

    @property
    def sql_mode(self) -> str:
        """Gets the SQL mode."""
        if self._sql_mode is None:
            self._sql_mode = self.info_query("SELECT @@session.sql_mode")[0]
        return self._sql_mode

    @sql_mode.setter
    def sql_mode(self, value: Union[str, Sequence[int]]) -> None:
        """Sets the SQL mode.

        This method sets the SQL Mode for the current connection. The value
        argument can be either a string with comma separate mode names, or
        a sequence of mode names.

        It is good practice to use the constants class `SQLMode`:
        ```
        >>> from mysql.connector.constants import SQLMode
        >>> cnx.sql_mode = [SQLMode.NO_ZERO_DATE, SQLMode.REAL_AS_FLOAT]
        ```
        """
        if isinstance(value, (list, tuple)):
            value = ",".join(value)
        self.cmd_query(f"SET @@session.sql_mode = '{value}'")
        self._sql_mode = value

    @abstractmethod
    def info_query(self, query: str) -> Optional[RowType]:
        """Sends a query which only returns 1 row.

        Shortcut for:

        ```
        cursor = self.cursor(buffered=True)
        cursor.execute(query)
        return cursor.fetchone()
        ```

        Args:
            query: Statement to execute.

        Returns:
            row: A tuple (RowType).
        """

    def set_login(
        self, username: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        """Sets login information for MySQL.

        Sets the username and/or password for the user connecting to the MySQL Server.

        Args:
            username: Account's user name.
            password: Account's password.
        """
        if username is not None:
            self._user = username.strip()
        else:
            self._user = ""
        if password is not None:
            self._password = password
        else:
            self._password = ""

    @deprecated(DEPRECATED_METHOD_WARNING.format(property_name="use_unicode"))
    def set_unicode(self, value: bool = True) -> None:
        """Sets whether we return string fields as unicode or not.

        Args:
            value: A boolean - default is `True`.
        """
        self.use_unicode = value

    @property
    def use_unicode(self) -> bool:
        """Gets whether we return string fields as unicode or not."""
        return self._use_unicode

    @use_unicode.setter
    @abstractmethod
    def use_unicode(self, value: bool) -> None:
        """Sets whether we return string fields as unicode or not.

        Args:
            value: A boolean - default is `True`.
        """

    @property
    def autocommit(self) -> bool:
        """Gets whether autocommit is on or off."""
        value = self.info_query("SELECT @@session.autocommit")[0]
        return value == 1

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        """Toggles autocommit."""
        switch = "ON" if value else "OFF"
        self.cmd_query(f"SET @@session.autocommit = {switch}")
        self._autocommit = value

    @property
    def get_warnings(self) -> bool:
        """Gets whether this connection retrieves warnings automatically.

        This method returns whether this connection retrieves warnings
        automatically.

        Returns `True`, or `False` when warnings are not retrieved.
        """
        return self._get_warnings

    @get_warnings.setter
    def get_warnings(self, value: bool) -> None:
        """Sets whether warnings should be automatically retrieved.

        The toggle-argument must be a boolean. When True, cursors for this
        connection will retrieve information about warnings (if any).

        Raises `ValueError` on error.
        """
        if not isinstance(value, bool):
            raise ValueError("Expected a boolean type")
        self._get_warnings = value

    @property
    def raise_on_warnings(self) -> bool:
        """Gets whether this connection raises an error on warnings.

        This method returns whether this connection will raise errors when
        MySQL reports warnings.

        Returns `True` or `False`.
        """
        return self._raise_on_warnings

    @raise_on_warnings.setter
    def raise_on_warnings(self, value: bool) -> None:
        """Sets whether warnings raise an error.

        The toggle-argument must be a boolean. When True, cursors for this
        connection will raise an error when MySQL reports warnings.

        Raising on warnings implies retrieving warnings automatically. In
        other words: warnings will be set to True. If set to False, warnings
        will be also set to False.

        Raises `ValueError` on error.
        """
        if not isinstance(value, bool):
            raise ValueError("Expected a boolean type")
        self._raise_on_warnings = value
        # Don't disable warning retrieval if raising explicitly disabled
        if value:
            self._get_warnings = value

    @property
    def unread_result(self) -> bool:
        """Gets whether there is an unread result.

        This method is used by cursors to check whether another cursor still
        needs to retrieve its result set.

        Returns `True`, or `False` when there is no unread result.
        """
        return self._unread_result

    @unread_result.setter
    def unread_result(self, value: bool) -> None:
        """Sets whether there is an unread result.

        This method is used by cursors to let other cursors know there is
        still a result set that needs to be retrieved.

        Raises `ValueError` on errors.
        """
        if not isinstance(value, bool):
            raise ValueError("Expected a boolean type")
        self._unread_result = value

    @property
    def collation(self) -> str:
        """Returns the collation for current connection.

        This property returns the collation name of the current connection.
        The server is queried when the connection is active. If not connected,
        the configured collation name is returned.

        Returns a string.
        """
        return self._character_set.get_charset_info(self._charset_id)[2]

    @property
    def charset(self) -> str:
        """Returns the character set for current connection.

        This property returns the character set name of the current connection.
        The server is queried when the connection is active. If not connected,
        the configured character set name is returned.

        Returns a string.
        """
        return self._character_set.get_info(self._charset_id)[0]

    @property
    def charset_id(self) -> int:
        """The charset ID utilized during the connection phase.

        If the charset ID hasn't been set, the default charset ID is returned.
        """
        return self._charset_id

    @property
    def _charset_id(self) -> int:
        """The charset ID utilized during the connection phase.

        If the charset ID hasn't been set, the default charset ID is returned.
        """
        if self.__charset_id is None:
            if self._server_version is None:
                # We mustn't set the private since we still don't know
                # the server version. We temporarily return the default
                # charset for undefined scenarios - eventually, the server
                # info will be available and the private variable will be set.
                return MYSQL_DEFAULT_CHARSET_ID_57

            self.__charset_id = (
                MYSQL_DEFAULT_CHARSET_ID_57
                if self._server_version < (8, 0)
                else MYSQL_DEFAULT_CHARSET_ID_80
            )

        return self.__charset_id

    @_charset_id.setter
    def _charset_id(self, value: int) -> None:
        """Sets the charset ID utilized during the connection phase."""
        self.__charset_id = value

    @property
    def python_charset(self) -> str:
        """Returns the Python character set for current connection.

        This property returns the character set name of the current connection.
        Note that, unlike property charset, this checks if the previously set
        character set is supported by Python and if not, it returns the
        equivalent character set that Python supports.

        Returns a string.
        """
        encoding = self._character_set.get_info(self._charset_id)[0]
        if encoding in ("utf8mb4", "utf8mb3", "binary"):
            return "utf8"
        return encoding

    def set_charset_collation(
        self, charset: Optional[Union[int, str]] = None, collation: Optional[str] = None
    ) -> None:
        """Sets the character set and collation for the current connection.

        This method sets the character set and collation to be used for
        the current connection. The charset argument can be either the
        name of a character set as a string, or the numerical equivalent
        as defined in constants.CharacterSet.

        When the collation is not given, the default will be looked up and
        used.

        Args:
            charset: Can be either the name of a character set, or the numerical
                     equivalent as defined in `constants.CharacterSet`.
            collation: When collation is `None`, the default collation for the
                       character set is used.

        Examples:
            The following will set the collation for the latin1 character set to
            `latin1_general_ci`:
            ```
            >>> cnx = mysql.connector.connect(user='scott')
            >>> cnx.set_charset_collation('latin1', 'latin1_general_ci')
            ```
        """
        err_msg = "{} should be either integer, string or None"
        if not isinstance(charset, (int, str)) and charset is not None:
            raise ValueError(err_msg.format("charset"))
        if not isinstance(collation, str) and collation is not None:
            raise ValueError("collation should be either string or None")

        if charset:
            if isinstance(charset, int):
                (
                    self._charset_id,
                    charset_name,
                    collation_name,
                ) = self._character_set.get_charset_info(charset)
            elif isinstance(charset, str):
                (
                    self._charset_id,
                    charset_name,
                    collation_name,
                ) = self._character_set.get_charset_info(charset, collation)
            else:
                raise ValueError(err_msg.format("charset"))
        elif collation:
            (
                self._charset_id,
                charset_name,
                collation_name,
            ) = self._character_set.get_charset_info(collation=collation)
        else:
            charset = DEFAULT_CONFIGURATION["charset"]
            (
                self._charset_id,
                charset_name,
                collation_name,
            ) = self._character_set.get_charset_info(charset, collation=None)

        self._execute_query(f"SET NAMES '{charset_name}' COLLATE '{collation_name}'")

        if self.converter:
            self.converter.set_charset(charset_name, character_set=self._character_set)

    @property
    def read_timeout(self) -> Optional[int]:
        """
        Gets the connection context's timeout in seconds for each attempt
        to read any data from the server.

        `read_timeout` is number of seconds upto which the connector should wait
        for the server to reply back before raising an ReadTimeoutError. We can set
        this option to None, which would signal the connector to wait indefinitely
        till the read operation is completed or stopped abruptly.
        """
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, timeout: Optional[int]) -> None:
        """
        Sets or updates the connection context's timeout in seconds for each attempt
        to read any data from the server.

        `read_timeout` is number of seconds upto which the connector should wait
        for the server to reply back before raising an ReadTimeoutError. We can set
        this option to None, which would signal the connector to wait indefinitely
        till the read operation is completed or stopped abruptly.

        Args:
            timeout: Accepts a non-negative integer which is the timeout to be set
                     in seconds or None.
        Raises:
            InterfaceError: If a positive integer or None is not passed via the
                            timeout parameter.
        Examples:
            The following will set the read_timeout of the current session to
            5 seconds:
            ```
            >>> cnx = mysql.connector.connect(user='scott')
            >>> cnx.read_timeout = 5
            ```
        """
        if timeout is not None:
            if not isinstance(timeout, int) or timeout < 0:
                raise InterfaceError(
                    "Option read_timeout must be a positive integer or None"
                )
        self._read_timeout = timeout

    @property
    def write_timeout(self) -> Optional[int]:
        """
        Gets the connection context's timeout in seconds for each attempt
        to send data to the server.

        `write_timeout` is number of seconds upto which the connector should spend to
        write to the server before raising an WriteTimeoutError. We can set this option
        to None, which would signal the connector to wait indefinitely till the write
        operation is completed or stopped abruptly.
        """
        return self._write_timeout

    @write_timeout.setter
    def write_timeout(self, timeout: Optional[int]) -> None:
        """
        Sets or updates the connection context's timeout in seconds for each attempt
        to send data to the server.

        `write_timeout` is number of seconds upto which the connector should spend to
        write to the server before raising an WriteTimeoutError. We can set this option
        to None, which would signal the connector to wait indefinitely till the write
        operation is completed or stopped abruptly.

        Args:
            timeout: Accepts a non-negative integer which is the timeout to be set in
                     seconds or None.
        Raises:
            InterfaceError: If a positive integer or None is not passed via the
                            timeout parameter.
        Examples:
            The following will set the write_timeout of the current
            session to 5 seconds:
            ```
            >>> cnx = mysql.connector.connect(user='scott')
            >>> cnx.write_timeout = 5
            ```
        """
        if timeout is not None:
            if not isinstance(timeout, int) or timeout < 0:
                raise InterfaceError(
                    "Option write_timeout must be a positive integer or None"
                )
        self._write_timeout = timeout

    @property
    @abstractmethod
    def connection_id(self) -> Optional[int]:
        """MySQL connection ID."""

    @abstractmethod
    def _do_handshake(self) -> None:
        """Gathers information of the MySQL server before authentication."""

    @abstractmethod
    def _open_connection(self) -> None:
        """Opens the connection to the MySQL server."""

    def _post_connection(self) -> None:
        """Executes commands after connection has been established.

        This method executes commands after the connection has been
        established. Some setting like autocommit, character set, and SQL mode
        are set using this method.
        """
        self.set_charset_collation(charset=self._charset_id)
        self.autocommit = self._autocommit
        if self._time_zone:
            self.time_zone = self._time_zone
        if self._sql_mode:
            self.sql_mode = self._sql_mode
        if self._init_command:
            self._execute_query(self._init_command)

    @abstractmethod
    def close(self) -> None:
        """Disconnects from the MySQL server.

        This method tries to send a `QUIT` command and close the socket. It raises
        no exceptions.

        `MySQLConnection.close()` is a synonymous for `MySQLConnection.disconnect()`
        method name and more commonly used.

        To shut down the connection without sending a `QUIT` command first,
        use `shutdown()`.
        """

    disconnect: ClassVar[Callable[["MySQLConnectionAbstract"], None]] = close

    def connect(self, **kwargs: Any) -> None:
        """Connects to the MySQL server.

        This method sets up the connection to the MySQL server. If no
        arguments are given, it will use the already configured or default
        values.

        Args:
            **kwargs: For a complete list of possible arguments, see [1].

        Examples:
            ```
            >>> cnx = MySQLConnection(user='joe', database='test')
            ```

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        """
        # open connection using the default charset id
        if kwargs:
            self.config(**kwargs)

        self.disconnect()
        self._open_connection()

        charset, collation = (
            kwargs.pop("charset", None),
            kwargs.pop("collation", None),
        )
        if charset or collation:
            self._charset_id = self._character_set.get_charset_info(charset, collation)[
                0
            ]

        if not self._client_flags & ClientFlag.CAN_HANDLE_EXPIRED_PASSWORDS:
            self._post_connection()
        else:
            # the server does not allow to run any other statement different from
            # ALTER when user's password has been expired - the server either
            # disconnects the client or restricts the client to "sandbox mode" [1].
            # [1]: https://dev.mysql.com/doc/refman/5.7/en/expired-password-handling.html
            try:
                self.set_charset_collation(charset=self._charset_id)
            except DatabaseError:
                # get out of sandbox mode - with no FOR user clause, the statement sets
                # the password for the current user.
                self.cmd_query(f"SET PASSWORD = '{self._password1 or self._password}'")

                # Set charset and collation.
                self.set_charset_collation(charset=self._charset_id)

                # go back to sandbox mode.
                self.cmd_query("ALTER USER CURRENT_USER() PASSWORD EXPIRE")

    def reconnect(self, attempts: int = 1, delay: int = 0) -> None:
        """Attempts to reconnect to the MySQL server.

        The argument `attempts` should be the number of times a reconnect
        is tried. The `delay` argument is the number of seconds to wait between
        each retry.

        You may want to set the number of attempts higher and use delay when
        you expect the MySQL server to be down for maintenance or when you
        expect the network to be temporary unavailable.

        Args:
            attempts: Number of attempts to make when reconnecting.
            delay: Use it (defined in seconds) if you want to wait between each retry.

        Raises:
            InterfaceError: When reconnection fails.
        """
        counter = 0
        span = None

        if self._tracer:
            # pylint: disable=possibly-used-before-assignment
            span = self._tracer.start_span(
                name=CONNECTION_SPAN_NAME, kind=trace.SpanKind.CLIENT
            )

        try:
            while counter != attempts:
                counter = counter + 1
                try:
                    self.disconnect()
                    self.connect()
                    if self.is_connected():
                        break
                except (Error, IOError) as err:
                    if counter == attempts:
                        msg = (
                            f"Can not reconnect to MySQL after {attempts} "
                            f"attempt(s): {err}"
                        )
                        raise InterfaceError(msg) from err
                if delay > 0:
                    sleep(delay)
        except InterfaceError as interface_err:
            if OTEL_ENABLED:
                set_connection_span_attrs(self, span)
                record_exception_event(span, interface_err)
                end_span(span)
            raise

        self._span = span
        if OTEL_ENABLED:
            set_connection_span_attrs(self, self._span)

    @abstractmethod
    def is_connected(self) -> bool:
        """Reports whether the connection to MySQL Server is available or not.

        Checks whether the connection to MySQL is available using the `ping()` method,
        but unlike `ping()`, `is_connected()` returns `True` when the connection is
        available, `False` otherwise
        """

    @abstractmethod
    def ping(self, reconnect: bool = False, attempts: int = 1, delay: int = 0) -> None:
        """Checks availability of the MySQL server.

        When reconnect is set to `True`, one or more attempts are made to try
        to reconnect to the MySQL server using the reconnect()-method.

        `delay` is the number of seconds to wait between each retry.

        When the connection is not available, an InterfaceError is raised.

        Args:
            reconnect: If True, one or more `attempts` are made to try to reconnect
                       to the MySQL server, and these options are forwarded to the
                       `reconnect()` method.
            attempts: Number of attempts to make when reconnecting.
            delay: Use it (defined in seconds) if you want to wait between each retry.

        Raises:
            InterfaceError: When the connection is not available. Use the
                            `is_connected()` method if you just want to check the
                            connection without raising an error.
        """

    @abstractmethod
    def commit(self) -> None:
        """Commits current transaction.

        This method is part of PEP 249 - Python Database API Specification v2.0.

        This method sends a COMMIT statement to the MySQL server, committing the
        current transaction. Since by default Connector/Python does not autocommit.

        It is important to call this method after every transaction that modifies
        data for tables that use transactional storage engines.

        Examples:
            ```
            >>> stmt = "INSERT INTO employees (first_name) VALUES (%s), (%s)"
            >>> cursor.execute(stmt, ('Jane', 'Mary'))
            >>> cnx.commit()
            ```
        """

    @abstractmethod
    def cursor(
        self,
        buffered: Optional[bool] = None,
        raw: Optional[bool] = None,
        prepared: Optional[bool] = None,
        cursor_class: Optional[Type["MySQLCursorAbstract"]] = None,
        dictionary: Optional[bool] = None,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> "MySQLCursorAbstract":
        """Instantiates and returns a cursor.

        By default, `MySQLCursor` or `CMySQLCursor` is returned. Depending on the
        options while connecting, a buffered and/or raw cursor is instantiated
        instead. Also depending upon the cursor options, rows can be returned as
        a dictionary or a tuple.

        Dictionary based cursors are available with buffered output
        but not raw.

        It is possible to also give a custom cursor through the `cursor_class`
        parameter, but it needs to be a subclass of `mysql.connector.cursor.MySQLCursor`
        or `mysql.connector.cursor_cext.CMySQLCursor` according to the type of
        connection that's being used.

        **NOTE: The parameters read and write timeouts in cursors are unsupported for
        C-Extension.**

        Args:
            buffered: If `True`, the cursor fetches all rows from the server after an
                      operation is executed. This is useful when queries return small
                      result sets.
            raw: If `True`, the cursor skips the conversion from MySQL data types to
                 Python types when fetching rows. A raw cursor is usually used to get
                 better performance or when you want to do the conversion yourself.
            prepared: If `True`, the cursor is used for executing prepared statements.
            cursor_class: It can be used to pass a class to use for instantiating a
                          new cursor. It must be a subclass of `cursor.MySQLCursor`
                          or `cursor_cext.CMySQLCursor` according to the type of
                          connection that's being used.
            dictionary: If `True`, the cursor returns rows as dictionaries.
            read_timeout: A positive integer representing timeout in seconds for each
                          attempt to read any data from the server.
            write_timeout: A positive integer representing timeout in seconds for each
                           attempt to send any data to the server.

        Returns:
            cursor: A cursor object.

        Raises:
            ProgrammingError: When `cursor_class` is not a subclass of
                              `MySQLCursorAbstract`.
            ValueError: When cursor is not available.
            InterfaceError: When read_timeout or write_timeout is not a positive integer.
        """

    @abstractmethod
    def _execute_query(self, query: str) -> None:
        """Executes a query."""

    @abstractmethod
    def rollback(self) -> None:
        """Rollbacks current transaction.

        Sends a ROLLBACK statement to the MySQL server, undoing all data changes
        from the current transaction. By default, Connector/Python does not
        autocommit, so it is possible to cancel transactions when using
        transactional storage engines such as `InnoDB`.

        Examples:
            ```
            >>> stmt = "INSERT INTO employees (first_name) VALUES (%s), (%s)"
            >>> cursor.execute(stmt, ('Jane', 'Mary'))
            >>> cnx.rollback()
            ```
        """

    def start_transaction(
        self,
        consistent_snapshot: bool = False,
        isolation_level: Optional[str] = None,
        readonly: Optional[bool] = None,
    ) -> None:
        """Starts a transaction.

        This method explicitly starts a transaction sending the
        START TRANSACTION statement to the MySQL server. You can optionally
        set whether there should be a consistent snapshot, which
        isolation level you need or which access mode i.e. READ ONLY or
        READ WRITE.

        Args:
            consistent_snapshot: If `True`, Connector/Python sends WITH CONSISTENT
                                 SNAPSHOT with the statement. MySQL ignores this for
                                 isolation levels for which that option does not apply.
            isolation_level: Permitted values are 'READ UNCOMMITTED', 'READ COMMITTED',
                             'REPEATABLE READ', and 'SERIALIZABLE'. If the value is
                             `None`, no isolation level is sent, so the default level
                             applies.
            readonly: Can be `True` to start the transaction in READ ONLY mode or
                      `False` to start it in READ WRITE mode. If readonly is omitted,
                      the server's default access mode is used.

        Raises:
            ProgrammingError: When a transaction is already in progress
                              and when `ValueError` when `isolation_level`
                              specifies an Unknown level.

        Examples:
            For example, to start a transaction with isolation level `SERIALIZABLE`,
            you would do the following:
            ```
            >>> cnx = mysql.connector.connect(...)
            >>> cnx.start_transaction(isolation_level='SERIALIZABLE')
            ```
        """
        if self.in_transaction:
            raise ProgrammingError("Transaction already in progress")

        if isolation_level:
            level = isolation_level.strip().replace("-", " ").upper()
            levels = [
                "READ UNCOMMITTED",
                "READ COMMITTED",
                "REPEATABLE READ",
                "SERIALIZABLE",
            ]

            if level not in levels:
                raise ValueError(f'Unknown isolation level "{isolation_level}"')

            self._execute_query(f"SET TRANSACTION ISOLATION LEVEL {level}")

        if readonly is not None:
            if self._server_version < (5, 6, 5):
                raise ValueError(
                    f"MySQL server version {self._server_version} does not "
                    "support this feature"
                )

            if readonly:
                access_mode = "READ ONLY"
            else:
                access_mode = "READ WRITE"
            self._execute_query(f"SET TRANSACTION {access_mode}")

        query = "START TRANSACTION"
        if consistent_snapshot:
            query += " WITH CONSISTENT SNAPSHOT"
        self.cmd_query(query)

    def reset_session(
        self,
        user_variables: Optional[Dict[str, Any]] = None,
        session_variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Clears the current active session.

        This method resets the session state, if the MySQL server is 5.7.3
        or later active session will be reset without re-authenticating.
        For other server versions session will be reset by re-authenticating.

        It is possible to provide a sequence of variables and their values to
        be set after clearing the session. This is possible for both user
        defined variables and session variables.

        Args:
            user_variables: User variables map.
            session_variables: System variables map.

        Raises:
            OperationalError: If not connected.
            InternalError: If there are unread results and InterfaceError on errors.

        Examples:
            ```
            >>> user_variables = {'var1': '1', 'var2': '10'}
            >>> session_variables = {'wait_timeout': 100000, 'sql_mode': 'TRADITIONAL'}
            >>> cnx.reset_session(user_variables, session_variables)
            ```
        """
        if not self.is_connected():
            raise OperationalError("MySQL Connection not available")

        try:
            self.cmd_reset_connection()
        except (NotSupportedError, NotImplementedError):
            if self._compress:
                raise NotSupportedError(
                    "Reset session is not supported with compression for "
                    "MySQL server version 5.7.2 or earlier"
                ) from None
            self.cmd_change_user(
                self._user,
                self._password,
                self._database,
                self._charset_id,
            )

        if user_variables or session_variables:
            cur = self.cursor()
            if user_variables:
                for key, value in user_variables.items():
                    cur.execute(f"SET @`{key}` = {value}")
            if session_variables:
                for key, value in session_variables.items():
                    cur.execute(f"SET SESSION `{key}` = {value}")
            cur.close()

    @deprecated(DEPRECATED_METHOD_WARNING.format(property_name="converter_class"))
    def set_converter_class(self, convclass: Optional[Type[MySQLConverter]]) -> None:
        """
        Sets the converter class to be used.

        Args:
            convclass: Should be a class overloading methods and members of
                       `conversion.MySQLConverter`.
        """
        self.converter_class = convclass

    @property
    def converter_class(self) -> Optional[Type[MySQLConverter]]:
        """Gets the converter class set for the current session."""
        return self._converter_class

    @converter_class.setter
    def converter_class(self, convclass: Optional[Type[MySQLConverter]]) -> None:
        """
        Sets the converter class to be used.

        Args:
            convclass: Should be a class overloading methods and members of
                       `conversion.MySQLConverter`.
        """
        if convclass and issubclass(convclass, MySQLConverterBase):
            charset_name = self._character_set.get_info(self._charset_id)[0]
            self._converter_class = convclass
            self.converter = convclass(charset_name, self.use_unicode)
            self.converter.str_fallback = self._converter_str_fallback
        else:
            raise TypeError(
                "Converter class should be a subclass of conversion.MySQLConverterBase."
            )

    @abstractmethod
    def get_row(
        self,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[RowType], Optional[Dict[str, Any]]]:
        """Retrieves the next row of a query result set.

        Args:
            binary: If `True`, read as binary result (only meaningful for pure Python
                    connections).
            columns: Field types (only meaningful for pure Python connections and when
                     `binary=True`).
            raw: If `True`, the converter class does not convert the parsed values.
            prep_stmt: Prepared statement object (only meaningful for
                       C-ext connections).

        Returns:
            tuple: The row as a tuple (RowType) containing byte objects, or `None` when
                   no more rows are available. (at position 0). EOF packet
                   information as a dictionary containing `status_flag` and
                   `warning_count` (at position 1).

        Raises:
            InterfaceError: When all rows have been retrieved.
        """

    @abstractmethod
    def get_rows(
        self,
        count: Optional[int] = None,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[List[RowType], Optional[Dict[str, Any]]]:
        """Gets all rows returned by the MySQL server.

        Args:
            count: Used to obtain a given number of rows. If set to `None`, all
                   rows are fetched.
            binary: If `True`, read as binary result (only meaningful for pure Python
                    connections).
            columns: Field types (only meaningful for pure Python connections and when
                     `binary=True`).
            raw: If `True`, the converter class does not convert the parsed values.
            prep_stmt: Prepared statement object (only meaningful for
                       C-ext connections).

        Returns:
            tuple: A list of tuples (RowType) containing the row data as byte objects,
                   or an empty list when no rows are available (at position 0).
                   EOF packet information as a dictionary containing `status_flag`
                   and `warning_count` (at position 1).

        Raises:
            InterfaceError: When all rows have been retrieved.
        """

    @abstractmethod
    def cmd_init_db(self, database: str) -> Optional[Dict[str, Any]]:
        """Changes the current database.

        This method makes specified database the default (current) database.
        In subsequent queries, this database is the default for table references
        that include no explicit database qualifier.

        Args:
            database: Database to become the default (current) database.

        Returns:
            ok_packet: Dictionary containing the OK packet information.
        """

    @abstractmethod
    def cmd_query(
        self,
        query: str,
        raw: Optional[bool] = False,
        buffered: bool = False,
        raw_as_string: bool = False,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """Sends a query to the MySQL server.

        This method sends the query to the MySQL server and returns the result.
        To **send multiple statements, use the `cmd_query_iter()` method instead**.

        The returned dictionary contains information depending on what kind of query
        was executed. If the query is a `SELECT` statement, the result contains
        information about columns. Other statements return a dictionary containing
        OK or EOF packet information.

        Errors received from the MySQL server are raised as exceptions.

        **Arguments `raw`, `buffered` and `raw_as_string` are only meaningful
        for `C-ext` connections**.

        Args:
            query: Statement to be executed.
            raw: If `True`, the cursor skips the conversion from MySQL data types to
                 Python types when fetching rows. A raw cursor is usually used to get
                 better performance or when you want to do the conversion yourself. If
                 not provided, take its value from the MySQL instance.
            buffered: If `True`, the cursor fetches all rows from the server after an
                      operation is executed. This is useful when queries return small
                      result sets.
            raw_as_string: Is a special argument for Python v2 and returns `str`
                           instead of `bytearray`.

        Returns:
            dictionary: `Result` or `OK packet` information
        """

    @abstractmethod
    def cmd_query_iter(
        self,
        statements: str,
        **kwargs: Any,
    ) -> Generator[Mapping[str, Any], None, None]:
        """Sends one or more statements to the MySQL server.

        Similar to the `cmd_query()` method, but instead returns a generator
        object to iterate through results. It sends the statements to the
        MySQL server and through the iterator you can get the results.

        Use `cmd_query_iter()` when sending multiple statements, and separate
        the statements with semicolons.

        Args:
            statements: Statements to be executed separated with semicolons.

        Returns:
            generator: Generator object with `Result` or `OK packet` information.

        Examples:
            The following example shows how to iterate through the results after
            sending multiple statements:
            ```
            >>> statement = 'SELECT 1; INSERT INTO t1 VALUES (); SELECT 2'
            >>> for result in cnx.cmd_query_iter(statement):
            >>> if 'columns' in result:
            >>>     columns = result['columns']
            >>>     rows = cnx.get_rows()
            >>> else:
            >>>     # do something useful with INSERT result
            ```
        """

    @abstractmethod
    def cmd_refresh(self, options: int) -> Dict[str, Any]:
        """Send the Refresh command to the MySQL server.

        This method sends the Refresh command to the MySQL server. The options
        argument should be a bitwise value using constants.RefreshOption.

        Typical usage example:
            ```
           RefreshOption = mysql.connector.RefreshOption
           refresh = RefreshOption.LOG | RefreshOption.INFO
           cnx.cmd_refresh(refresh)
           ```

        Args:
            options: Bitmask value constructed using constants from
                     the `constants.RefreshOption` class.

        Returns:
            A dictionary representing the OK packet got as response when executing
            the command.

        Raises:
            ValueError: If an invalid command `refresh options` is provided.
            DeprecationWarning: If one of the options is deprecated for the server you
                                are connecting to.
        """

    @abstractmethod
    def cmd_quit(self) -> Optional[bytes]:
        """Closes the current connection with the server.

        This method sends the `QUIT` command to the MySQL server, closing the
        current connection. Since there is no response from the MySQL server,
        the packet that was sent is returned.

        Returns:
            packet_sent: `None` when using a C-ext connection,
                         else the actual packet that was sent.
        """

    @abstractmethod
    def cmd_shutdown(self, shutdown_type: Optional[int] = None) -> None:
        """Shuts down the MySQL Server.

        This method sends the SHUTDOWN command to the MySQL server.
        The `shutdown_type` is not used, and it's kept for backward compatibility.
        """

    @abstractmethod
    def cmd_statistics(self) -> Optional[Dict[str, Any]]:
        """Sends the statistics command to the MySQL Server.

        Returns:
            dict: Stats packet information about the MySQL server including uptime
                  in seconds and the number of running threads, questions, reloads, and
                  open tables.
        """

    @staticmethod
    def cmd_process_info() -> NoReturn:
        """Get the process list of the MySQL Server.

        This method is a placeholder to notify that the PROCESS_INFO command
        is not supported by raising the `NotSupportedError`.

        The command
        "SHOW PROCESSLIST" should be send using the cmd_query()-method or
        using the `INFORMATION_SCHEMA` database.

        Raises `NotSupportedError` exception.
        """
        raise NotSupportedError(
            "Not implemented. Use SHOW PROCESSLIST or INFORMATION_SCHEMA"
        )

    @abstractmethod
    def cmd_process_kill(self, mysql_pid: int) -> Optional[Dict[str, Any]]:
        """Kills a MySQL process.

        Asks the server to kill the thread specified by `mysql_pid`. Although
        still available, it is better to use the KILL SQL statement.

        Args:
            mysql_pid: Process ID to be killed.

        Returns:
            ok_packet: Dictionary containing the OK packet information.

        Examples:
            ```
            >>> cnx.cmd_process_kill(123)  # using cmd_process_kill()
            >>> cnx.cmd_query('KILL 123')  # alternatively (recommended)
            ```
        """

    @abstractmethod
    def cmd_debug(self) -> Optional[Dict[str, Any]]:
        """Instructs the server to write debugging information to the error log.

        The connected user must have the `SUPER` privilege.

        Returns:
            ok_packet: Dictionary containing the EOF (end-of-file) packet information.
        """

    @abstractmethod
    def cmd_ping(self) -> Optional[Dict[str, Any]]:
        """Checks whether the connection to the server is working.

        This method is not to be used directly. Use `ping()` or
        `is_connected()` instead.

        Returns:
            ok_packet: Dictionary containing the OK packet information.
        """

    @abstractmethod
    def cmd_change_user(
        self,
        username: str = "",
        password: str = "",
        database: str = "",
        charset: Optional[int] = None,
        password1: str = "",
        password2: str = "",
        password3: str = "",
        oci_config_file: str = "",
        oci_config_profile: str = "",
        openid_token_file: str = "",
    ) -> Optional[Dict[str, Any]]:
        """Changes the current logged in user.

        It also causes the specified database to become the default (current)
        database. It is also possible to change the character set using the
        charset argument. The character set passed during initial connection
        is reused if no value of charset is passed via this method.

        Args:
            username: New account's username.
            password: New account's password.
            database: Database to become the default (current) database.
            charset: Client charset (see [1]), only the lower 8-bits.
            password1: New account's password factor 1 - it's used instead
                       of `password` if set (higher precedence).
            password2: New account's password factor 2.
            password3: New account's password factor 3.
            oci_config_file: OCI configuration file location (path-like string).
            oci_config_profile: OCI configuration profile location (path-like string).
            openid_token_file: OpenID Connect token file location (path-like string).

        Returns:
            ok_packet: Dictionary containing the OK packet information.

        Examples:
            ```
            >>> cnx.cmd_change_user(username='', password='', database='', charset=33)
            ```

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_basic_character_set.html#a_protocol_character_set
        """

    @abstractmethod
    def cmd_stmt_prepare(
        self,
        statement: bytes,
        **kwargs: Any,
    ) -> Union[Mapping[str, Any], CMySQLPrepStmt]:
        """Prepares a MySQL statement.

        Args:
            statement: statement to prepare.

        Returns:
            prepared_stmt: A `Prepared Statement` structure - a dictionary
                           is returned when using a pure Python connection, and a
                           `_mysql_connector.MySQLPrepStmt` object is returned when
                           using a C-ext connection.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/
                page_protocol_com_stmt_prepare.html
        """

    @abstractmethod
    def cmd_stmt_execute(
        self,
        statement_id: Union[int, CMySQLPrepStmt],
        data: Sequence[BinaryProtocolType] = (),
        parameters: Sequence = (),
        flags: int = 0,
        **kwargs: Any,
    ) -> Optional[Union[Dict[str, Any], Tuple]]:
        """Executes a prepared MySQL statement.

        Args:
            statement_id: Statement ID found in the dictionary returned by
                          `MySQLConnection.cmd_stmt_prepare` when using a pure Python
                          connection, or a `_mysql_connector.MySQLPrepStmt` instance
                          as returned by `CMySQLConnection.cmd_stmt_prepare` when
                          using a C-ext connection.
            data: Data sequence against which the prepared statement will be executed.
            parameters: Currently unused!
            flags: see [1].

        Returns:
            dictionary or tuple: `OK packet` or `Result` information.

        Notes:
            The previous method's signature applies to pure Python, the C-ext has
            the following signature:

            ```
            def cmd_stmt_execute(
                self, statement_id: CMySQLPrepStmt, *args: Any
            ) -> Optional[Union[Dict[str, Any], Tuple]]:
            ```

            You should expect a similar returned value type, however, the input
            is different. In this case `data` must be provided as positional
            arguments instead of a sequence.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_com_stmt_execute.html
        """

    @abstractmethod
    def cmd_stmt_close(
        self,
        statement_id: Union[int, CMySQLPrepStmt],
        **kwargs: Any,
    ) -> None:
        """Deallocates a prepared MySQL statement.

        Args:
            statement_id: Statement ID found in the dictionary returned by
                          `MySQLConnection.cmd_stmt_prepare` when using a pure Python
                          connection, or a `_mysql_connector.MySQLPrepStmt` instance
                          as returned by `CMySQLConnection.cmd_stmt_prepare` when
                          using a C-ext connection.
        """

    @abstractmethod
    def cmd_stmt_send_long_data(
        self,
        statement_id: Union[int, CMySQLPrepStmt],
        param_id: int,
        data: BinaryIO,
        **kwargs: Any,
    ) -> int:
        """Sends data for a column.

        Currently, not implemented for the C-ext.

        Args:
            statement_id: Statement ID found in the dictionary returned by
                          `MySQLConnection.cmd_stmt_prepare` when using a pure Python
                          connection, or a `_mysql_connector.MySQLPrepStmt` instance
                          as returned by `CMySQLConnection.cmd_stmt_prepare` when
                          using a C-ext connection.
            param_id: The parameter to supply data to [1].
            data: The actual payload to send [1].

        Returns:
            total_sent: The total number of bytes that were sent is returned.

        References:
            [1]: https://dev.mysql.com/doc/dev/mysql-server/latest/\
                page_protocol_com_stmt_send_long_data.html
        """

    @abstractmethod
    def cmd_stmt_reset(
        self,
        statement_id: Union[int, CMySQLPrepStmt],
        **kwargs: Any,
    ) -> None:
        """Resets data for prepared statement sent as long data.

        Args:
            statement_id: Statement ID found in the dictionary returned by
                          `MySQLConnection.cmd_stmt_prepare` when using a pure Python
                          connection, or a `_mysql_connector.MySQLPrepStmt` instance
                          as returned by `CMySQLConnection.cmd_stmt_prepare` when
                          using a C-ext connection.
        """

    @abstractmethod
    def cmd_reset_connection(self) -> bool:
        """Resets the session state without re-authenticating.

        Reset command only works on MySQL server 5.7.3 or later.

        This method permits the session state to be cleared without reauthenticating.
        For MySQL servers older than 5.7.3 (when `COM_RESET_CONNECTION` was introduced)
        , the `reset_session()` method can be used instead - that method resets the
        session state by reauthenticating, which is more expensive.

        This method was added in Connector/Python 1.2.1.

        Returns:
            `True` for a successful reset otherwise `False`.
        """


class MySQLCursorAbstract(ABC):
    """Abstract cursor class

    Abstract class defining cursor class with method and members
    required by the Python Database API Specification v2.0.
    """

    def __init__(
        self,
        connection: Optional[MySQLConnectionAbstract] = None,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> None:
        """Defines the MySQL cursor interface."""

        self._connection: Optional[MySQLConnectionAbstract] = connection
        if connection is not None:
            if not isinstance(connection, MySQLConnectionAbstract):
                raise InterfaceError(errno=2048)
            self._connection = weakref.proxy(connection)

        self._description: Optional[List[DescriptionType]] = None
        self._rowcount: int = -1
        self._last_insert_id: Optional[int] = None
        self._warnings: Optional[List[WarningType]] = None
        self._warning_count: int = 0
        self._executed: Optional[bytes] = None
        self._executed_list: List[bytes] = []
        self._stored_results: List[MySQLCursorAbstract] = []
        self.arraysize: int = 1
        self._binary: bool = False
        self._raw: bool = False
        self._nextrow: Tuple[
            Optional[RowType], Optional[Union[EofPacketType, CextEofPacketType]]
        ] = (
            None,
            None,
        )
        self._read_timeout: Optional[int] = read_timeout
        self._write_timeout: Optional[int] = write_timeout

        # multi statement execution
        self._stmt_partitions: Optional[Generator[MySQLScriptPartition, None, None]] = (
            None
        )
        self._stmt_partition: Optional[MySQLScriptPartition] = None
        self._stmt_map_results: bool = False

    def __enter__(self) -> MySQLCursorAbstract:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.close()

    @property
    def read_timeout(self) -> Optional[int]:
        """
        Gets the cursor context's timeout in seconds for each attempt
        to read any data from the server.

        `read_timeout` is number of seconds upto which the connector should wait
        for the server to reply back before raising an ReadTimeoutError. We can set
        this option to None, which would signal the connector to wait indefinitely
        till the read operation is completed or stopped abruptly.
        """
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, timeout: Optional[int]) -> None:
        """
        Sets or updates the cursor context's timeout in seconds for each attempt
        to read any data from the server.

        `read_timeout` is number of seconds upto which the connector should wait
        for the server to reply back before raising an ReadTimeoutError. We can set
        this option to None, which would signal the connector to wait indefinitely
        till the read operation is completed or stopped abruptly.

        Args:
            timeout: Accepts a non-negative integer which is the timeout to be set
                     in seconds or None.
        Raises:
            InterfaceError: If a positive integer or None is not passed via the
                            timeout parameter.
        Examples:
            The following will set the read_timeout of the current session to
            5 seconds:
            ```
            >>> cnx = mysql.connector.connect(user='scott')
            >>> cur = cnx.cursor()
            >>> cur.read_timeout = 5
            ```
        """
        if timeout is not None:
            if not isinstance(timeout, int) or timeout < 0:
                raise InterfaceError(
                    "Option read_timeout must be a positive integer or None"
                )
        self._read_timeout = timeout

    @property
    def write_timeout(self) -> Optional[int]:
        """
        Gets the connection context's timeout in seconds for each attempt
        to send data to the server.

        `write_timeout` is number of seconds upto which the connector should spend to
        write to the server before raising an WriteTimeoutError. We can set this option
        to None, which would signal the connector to wait indefinitely till the write
        operation is completed or stopped abruptly.
        """
        return self._write_timeout

    @write_timeout.setter
    def write_timeout(self, timeout: Optional[int]) -> None:
        """
        Sets or updates the connection context's timeout in seconds for each attempt
        to send data to the server.

        `write_timeout` is number of seconds upto which the connector should spend to
        write to the server before raising an WriteTimeoutError. We can set this option
        to None, which would signal the connector to wait indefinitely till the write
        operation is completed or stopped abruptly.

        Args:
            timeout: Accepts a non-negative integer which is the timeout to be set in
                     seconds or None.
        Raises:
            InterfaceError: If a positive integer or None is not passed via the
                            timeout parameter.
        Examples:
            The following will set the write_timeout of the current
            session to 5 seconds:
            ```
            >>> cnx = mysql.connector.connect(user='scott')
            >>> cur = cnx.cursor()
            >>> cur.write_timeout = 5
            ```
        """
        if timeout is not None:
            if not isinstance(timeout, int) or timeout < 0:
                raise InterfaceError(
                    "Option write_timeout must be a positive integer or None"
                )
        self._write_timeout = timeout

    @abstractmethod
    def callproc(
        self, procname: str, args: Sequence = ()
    ) -> Optional[Union[Dict[str, RowItemType], RowType]]:
        """Calls a stored procedure with the given arguments.

        The arguments will be set during this session, meaning they will be called like
        _<procname>__arg<nr> where <nr> is an enumeration (+1) of the arguments.

        Args:
            procname: The stored procedure name.
            args: Sequence of parameters - it must contain one entry for each argument
                  that the procedure expects.

        Returns:
            Does not return a value, but a result set will be available when the
            CALL-statement executes successfully.

            `callproc()` returns a modified copy of the input sequence. `Input`
            parameters are left untouched. `Output` and `input/output` parameters may
            be replaced with new values.

            Result sets produced by the stored procedure are automatically fetched and
            stored as `MySQLCursorBuffered` instances.

            The value returned (if any) is a `Dict` when cursor's subclass is
            `MySQLCursorDict`, else a `Tuple` (RowType).

        Raises:
            InterfaceError: When something is wrong

        Examples:
            1) Defining the Stored Routine in MySQL:
            ```
            CREATE PROCEDURE multiply(IN pFac1 INT, IN pFac2 INT, OUT pProd INT)
            BEGIN
            SET pProd := pFac1 * pFac2;
            END;
            ```

            2) Executing in Python:
            ```
            >>> args = (5, 6, 0) # 0 is to hold value of the OUT parameter pProd
            >>> cursor.callproc('multiply', args)
            ('5', '6', 30L)
            ```

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/\
                connector-python-api-mysqlcursor-callproc.html
        """

    @abstractmethod
    def close(self) -> None:
        """Close the cursor.

        Use close() when you are done using a cursor. This method closes the cursor,
        resets all results, and ensures that the cursor object has no reference to its
        original connection object.

        This method is part of PEP 249 - Python Database API Specification v2.0.
        """

    @abstractmethod
    def execute(
        self,
        operation: str,
        params: Union[
            Sequence[MySQLConvertibleType], Dict[str, MySQLConvertibleType]
        ] = (),
        map_results: bool = False,
    ) -> None:
        """Executes the given operation (a MySQL script) substituting any markers
        with the given parameters.

        For example, getting all rows where id is 5:
        ```
        cursor.execute("SELECT * FROM t1 WHERE id = %s", (5,))
        ```

        If you want each single statement in the script to be related
        to its corresponding result set, you should enable the `map_results`
        switch - see workflow example below.

        If the given script uses `DELIMITER` statements (which are not recognized
        by MySQL Server), the connector will parse such statements to remove them
        from the script and substitute delimiters as needed. This pre-processing
        may cause a performance hit when using long scripts. Note that when enabling
        `map_results`, the script is expected to use `DELIMITER` statements in order
        to split the script into multiple query strings.

        The following characters are currently not supported by the connector in
        `DELIMITER` statements: `"`, `'`, #`, `/*` and `*/`.

        If warnings were generated, and `connection.get_warnings` is
        `True`, then `self.warnings` will be a list containing these
        warnings.

        Args:
            operation: Operation to be executed - it can be a single or a
                       multi statement.
            params: The parameters found in the tuple or dictionary params are bound
                    to the variables in the operation. Specify variables using `%s` or
                    `%(name)s` parameter style (that is, using format or pyformat style).
            map_results: It is `False` by default. If `True`, it allows you to know what
                        statement caused what result set - see workflow example below.
                        Only relevant when working with multi statements.

        Returns:
            `None`.

        Example (basic usage):
            The following example runs many single statements in a
            single go and loads the corresponding result sets
            sequentially:

            ```
            sql_operation = '''
            SET @a=1, @b='2024-02-01';
            SELECT @a, LENGTH('hello'), @b;
            SELECT @@version;
            '''
            with cnx.cursor() as cur:
                cur.execute(sql_operation)

                result_set = cur.fetchall()
                # do something with result set
                ...

                while cur.nextset():
                    result_set = cur.fetchall()
                    # do something with result set
                    ...
            ```

            In case the operation is a single statement, you may skip the
            looping section as no more result sets are to be expected.

        Example (statement-result mapping):
            The following example runs many single statements in a
            single go and loads the corresponding result sets
            sequentially. Additionally, each result set gets related
            to the statement that caused it:

            ```
            sql_operation = '''
            SET @a=1, @b='2024-02-01';
            SELECT @a, LENGTH('hello'), @b;
            SELECT @@version;
            '''
            with cnx.cursor() as cur:
                cur.execute(sql_operation, map_results=True)

                # statement 1 is `SET @a=1, @b='2024-02-01'`,
                # result set from statement 1 is `[]` - aka, an empty set.
                result_set, statement = cur.fetchall(), cur.statement
                # do something with result set
                ...

                # 1st call to `nextset()` will laod the result set from statement 2,
                # statement 2 is `SELECT @a, LENGTH('hello'), @b`,
                # result set from statement 2 is `[(1, 5, '2024-02-01')]`.
                #
                # 2nd call to `nextset()` will laod the result set from statement 3,
                # statement 3 is `SELECT @@version`,
                # result set from statement 3 is `[('9.0.0-labs-mrs-8',)]`.
                #
                # 3rd call to `nextset()` will return `None` as there are no more sets,
                # leading to the end of the consumption process of result sets.
                while cur.nextset():
                    result_set, statement = cur.fetchall(), cur.statement
                    # do something with result set
                    ...
            ```

            In case the mapping is disabled (`map_results=False`), all result
            sets get related to the same statement, which is the one provided
            when calling `execute()`. In other words, the property `statement`
            will not change as result sets are consumed, which contrasts with
            the case in which the mapping is enabled. Note that we offer a
            new fetch-related API command which can be leveraged as a shortcut
            for consuming result sets - it is equivalent to the previous
            workflow.

            ```
            sql_operation = '''
            SET @a=1, @b='2024-02-01';
            SELECT @a, LENGTH('hello'), @b;
            SELECT @@version;
            '''
            with cnx.cursor() as cur:
                cur.execute(sql_operation, map_results=True)
                for statement, result_set in cur.fetchsets():
                    # do something with result set
            ```
        """

    @abstractmethod
    def executemany(
        self,
        operation: str,
        seq_params: Sequence[
            Union[Sequence[MySQLConvertibleType], Dict[str, MySQLConvertibleType]]
        ],
    ) -> None:
        """Executes the given operation multiple times.

        The `executemany()` method will execute the operation iterating
        over the list of parameters in `seq_params`.

        `INSERT` statements are optimized by batching the data, that is
        using the MySQL multiple rows syntax.

        Args:
            operation: Operation to be executed.
            seq_params: Parameters to be used when executing the operation.

        Returns:
            Results are discarded. If they are needed, consider looping over data
            using the `execute()` method.

        Examples:
            An optimization is applied for inserts: The data values given by the
            parameter sequences are batched using multiple-row syntax. The following
            example inserts three records:

            ```
            >>> data = [
            >>> ('Jane', date(2005, 2, 12)),
            >>> ('Joe', date(2006, 5, 23)),
            >>> ('John', date(2010, 10, 3)),
            >>> ]
            >>> stmt = "INSERT INTO employees (first_name, hire_date) VALUES (%s, %s)"
            >>> cursor.executemany(stmt, data)
            ```

            For the preceding example, the INSERT statement sent to MySQL is:
            ```
            >>> INSERT INTO employees (first_name, hire_date)
            >>> VALUES ('Jane', '2005-02-12'), ('Joe', '2006-05-23'), ('John', '2010-10-03')
            ```
        """

    @abstractmethod
    def fetchone(self) -> Optional[Union[RowType, Dict[str, RowItemType]]]:
        """Retrieves next row of a query result set

        Returns:
            If the cursor's subclass is `MySQLCursorDict`, a dictionaries is
            returned, otherwise a tuple (RowType). `None` is returned when there aren't
            results to be read.

        Examples:
            ```
            >>> cursor.execute("SELECT * FROM employees")
            >>> row = cursor.fetchone()
            >>> while row is not None:
            >>>     print(row)
            >>>     row = cursor.fetchone()
            ```
        """

    @abstractmethod
    def fetchmany(self, size: int = 1) -> List[Union[RowType, Dict[str, RowItemType]]]:
        """Fetches the next set of rows of a query result.

        Args:
            size: The number of rows returned can be specified using the size
                  argument, which is one by default.

        Returns:
            If the cursor's subclass is `MySQLCursorDict`, a list of dictionaries is
            returned, otherwise a list of tuples (RowType). When no more rows are
            available, it returns an empty list.
        """

    @abstractmethod
    def fetchall(self) -> List[Union[RowType, Dict[str, RowItemType]]]:
        """Fetches all (or all remaining) rows of a query result set.

        Returns:
            If the cursor's subclass is `MySQLCursorDict`, a list of dictionaries is
            returned, otherwise a list of tuples (RowType).

        Examples:
            ```
            >>> cursor.execute("SELECT * FROM employees ORDER BY emp_no")
            >>> head_rows = cursor.fetchmany(size=2)
            >>> remaining_rows = cursor.fetchall()
            ```
        """

    def fetchsets(
        self,
    ) -> Generator[
        tuple[Optional[str], list[Union[RowType, Dict[str, RowItemType]]]], None, None
    ]:
        """Generates the result sets stream caused by the last `execute*()`.

        Returns:
            A 2-tuple; the first element is the statement that caused the
            result set, and the second is the result set itself.

            This method is used as part of the multi statement
            execution workflow - see example below.

        Example:
            Consider the following example where multiple statements are executed in one
            go:

            ```
                sql_operation = '''
                SET @a=1, @b='2024-02-01';
                SELECT @a, LENGTH('hello'), @b;
                SELECT @@version;
                '''
                with cnx.cursor() as cur:
                    cur.execute(sql_operation, map_results=True)

                    result_set, statement = cur.fetchall(), cur.statement
                    # do something with result set
                    ...

                    while cur.nextset():
                        result_set, statement = cur.fetchall(), cur.statement
                        # do something with result set
                        ...
            ```

            In this case, as an alternative to loading the result sets with `nextset()`
            in combination with a `while` loop, you can use `fetchsets()` which is
            equivalent to the previous approach:

            ```
                sql_operation = '''
                SET @a=1, @b='2024-02-01';
                SELECT @a, LENGTH('hello'), @b;
                SELECT @@version;
                '''
                with cnx.cursor() as cur:
                    cur.execute(sql_operation)
                    for statement, result_set in cur.fetchsets():
                        # do something with result set
            ```
        """
        # Some cursor flavor such as `buffered` raise an exception when they don't have
        # result sets to fetch from.
        # Some others, such as `dictionary` or `raw`, return an empty result set
        # under the same circumstances.
        statement_cached = None
        if not self._stmt_map_results:
            statement_cached = self.statement

        try:
            result_set = self.fetchall()
        except InterfaceError:
            result_set = []
        yield (
            self.statement if self._stmt_map_results else statement_cached
        ), result_set
        while self.nextset():
            try:
                result_set = self.fetchall()
            except InterfaceError:
                result_set = []
            yield (
                self.statement if self._stmt_map_results else statement_cached
            ), result_set

    @abstractmethod
    def stored_results(self) -> Iterator[MySQLCursorAbstract]:
        """Returns an iterator (of MySQLCursorAbstract subclass instances) for stored results.

        This method returns an iterator over results which are stored when
        callproc() is called. The iterator will provide `MySQLCursorBuffered`
        instances.

        Examples:
            ```
            >>> cursor.callproc('myproc')
            ()
            >>> for result in cursor.stored_results():
            ...     print result.fetchall()
            ...
            [(1,)]
            [(2,)]
            ```
        """

    @abstractmethod
    def nextset(self) -> Optional[bool]:
        """Makes the cursor skip to the next available set, discarding
        any remaining rows from the current set.

        This method is used as part of the multi statement
        execution workflow - see example below.

        Returns:
            It returns `None` if there are no more sets. Otherwise, it returns
            `True` and subsequent calls to the `fetch*()` methods will return
            rows from the next result set.

        Example:
            The following example runs many single statements in a
            single go and loads the corresponding result sets
            sequentially:

            ```
            sql_operation = '''
            SET @a=1, @b='2024-02-01';
            SELECT @a, LENGTH('hello'), @b;
            SELECT @@version;
            '''
            with cnx.cursor() as cur:
                cur.execute(sql_operation)

                result_set = cur.fetchall()
                # do something with result set
                ...

                while cur.nextset():
                    result_set = cur.fetchall()
                    # do something with result set
                    ...
            ```

            In case the operation is a single statement, you may skip the
            looping section as no more result sets are to be expected.
        """

    def setinputsizes(self, sizes: Any) -> NoReturn:
        """Not Implemented."""

    def setoutputsize(self, size: Any, column: Any = None) -> NoReturn:
        """Not Implemented."""

    def reset(self, free: bool = True) -> None:
        """Resets the cursor to default"""

    @property
    def description(self) -> Optional[List[DescriptionType]]:
        """This read-only property returns a list of tuples describing the columns in a
        result set.

        A tuple is described as follows::
        ```
        (column_name,
            type,
            None,
            None,
            None,
            None,
            null_ok,
            column_flags)  # Addition to PEP-249 specs
        ```

        See [1] for more details and examples.

        Returns:
            A list of tuples.

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/\
                connector-python-api-mysqlcursor-description.html
        """
        return self._description

    @property
    def rowcount(self) -> int:
        """Returns the number of rows produced or affected.

        This property returns the number of rows produced by queries
        such as `SELECT`, or affected rows when executing DML statements
        like `INSERT` or `UPDATE`.

        Note that for non-buffered cursors it is impossible to know the
        number of rows produced before having fetched them all. For those,
        the number of rows will be -1 right after execution, and
        incremented when fetching rows.

        Returns an integer.
        """
        return self._rowcount

    @property
    def lastrowid(self) -> Optional[int]:
        """Returns the value generated for an AUTO_INCREMENT column.

        Returns the value generated for an AUTO_INCREMENT column by
        the previous INSERT or UPDATE statement or `None` when there is
        no such a value available.

        Returns a long value or `None`.
        """
        return self._last_insert_id

    @property
    def warnings(self) -> Optional[List[WarningType]]:
        """Gets a list of tuples (WarningType) containing warnings generated
        by the previously executed operation.

        Examples:
            ```
            >>> cnx.get_warnings = True
            >>> cursor.execute("SELECT 'a'+1")
            >>> cursor.fetchall()
            [(1.0,)]
            >>> cursor.warnings
            [(u'Warning', 1292, u"Truncated incorrect DOUBLE value: 'a'")]
            ```
        """
        return self._warnings

    @property
    def warning_count(self) -> int:
        """Returns the number of warnings.

        This property returns the number of warnings generated by the
        previously executed operation.

        Returns an integer value.
        """
        return self._warning_count

    @property
    def statement(self) -> Optional[str]:
        """Returns the latest executed statement.

        When a multiple statement is executed, the value of `statement`
        corresponds to the one that caused the current result set, provided
        the statement-result mapping was enabled. Otherwise, the value of
        `statement` matches the statement just as provided when calling
        `execute()` and it does not change as result sets are traversed.
        """
        if self._executed is None:
            return None
        try:
            return self._executed.strip().decode("utf-8")
        except (AttributeError, UnicodeDecodeError):
            return cast(str, self._executed.strip())

    @deprecated(DEPRECATED_METHOD_WARNING.format(property_name="warnings"))
    def fetchwarnings(self) -> Optional[List[WarningType]]:
        """Returns a list of tuples (WarningType) containing warnings generated by
        the previously executed operation.

        Examples:
            ```
            >>> cnx.get_warnings = True
            >>> cursor.execute("SELECT 'a'+1")
            >>> cursor.fetchall()
            [(1.0,)]
            >>> cursor.fetchwarnings()
            [(u'Warning', 1292, u"Truncated incorrect DOUBLE value: 'a'")]
            ```
        """
        return self._warnings

    def get_attributes(self) -> Optional[List[Tuple[str, BinaryProtocolType]]]:
        """Gets a list of query attributes from the connector's side.

        Returns:
            List of existing query attributes.
        """
        if hasattr(self, "_connection"):
            return self._connection.query_attrs
        return None

    def add_attribute(self, name: str, value: BinaryProtocolType) -> None:
        """Adds a query attribute and its value into the connector's query attributes list.

        Query attributes must be enabled on the server - they are disabled by default. A
        warning is logged when setting query attributes for a server connection
        that does not support them.

        Args:
            name: Key name used to identify the attribute.
            value: A value converted to the MySQL Binary Protocol.

        Raises:
            ProgrammingError: If the value's conversion fails.
        """
        if not isinstance(name, str):
            raise ProgrammingError("Parameter `name` must be a string type")
        if value is not None and not isinstance(value, MYSQL_PY_TYPES):
            raise ProgrammingError(
                f"Object {value} cannot be converted to a MySQL type"
            )
        if hasattr(self, "_connection"):
            self._connection.query_attrs_append((name, value))

    def remove_attribute(self, name: str) -> BinaryProtocolType:
        """Removes a query attribute by name from the connector's query attributes list.

        If no match, `None` is returned, else the corresponding value is returned.

        Args:
            name: Key name used to identify the attribute.

        Returns:
            value: Attribute's value.
        """
        if not isinstance(name, str):
            raise ProgrammingError("Parameter `name` must be a string type")
        if hasattr(self, "_connection"):
            return self._connection.query_attrs_remove(name)
        return None

    def clear_attributes(self) -> None:
        """Clears the list of query attributes on the connector's side."""
        if hasattr(self, "_connection"):
            self._connection.query_attrs_clear()
