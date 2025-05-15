# Copyright (c) 2009, 2025, Oracle and/or its affiliates.
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

"""Various MySQL constants and character sets."""

import warnings

from abc import ABC, ABCMeta
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, ValuesView

from .charsets import MYSQL_CHARACTER_SETS, MYSQL_CHARACTER_SETS_57
from .errors import ProgrammingError
from .tls_ciphers import APPROVED_TLS_VERSIONS, DEPRECATED_TLS_VERSIONS

NET_BUFFER_LENGTH: int = 8192
MAX_MYSQL_TABLE_COLUMNS: int = 4096
PARAMETER_COUNT_AVAILABLE: int = 8
"""Flag used to send the Query Attributes with 0 (or more) parameters."""
MYSQL_VECTOR_TYPE_CODE = "f"
"""Expected `typecode` when decoding VECTOR values from
MySQL (blob) to Python (array.array).
"""
MYSQL_DEFAULT_CHARSET_ID_57 = 45
MYSQL_DEFAULT_CHARSET_ID_80 = 255

DEFAULT_CONFIGURATION: Dict[str, Optional[Union[str, bool, int]]] = {
    "database": None,
    "user": "",
    "password": "",
    "password1": "",
    "password2": "",
    "password3": "",
    "host": "127.0.0.1",
    "port": 3306,
    "unix_socket": None,
    "use_unicode": True,
    "charset": "utf8mb4",
    "collation": None,
    "converter_class": None,
    "converter_str_fallback": False,
    "autocommit": False,
    "time_zone": None,
    "sql_mode": None,
    "get_warnings": False,
    "raise_on_warnings": False,
    "connection_timeout": None,
    "read_timeout": None,
    "write_timeout": None,
    "client_flags": 0,
    "compress": False,
    "buffered": False,
    "raw": False,
    "ssl_ca": None,
    "ssl_cert": None,
    "ssl_key": None,
    "ssl_verify_cert": False,
    "ssl_verify_identity": False,
    "ssl_cipher": None,
    "tls_ciphersuites": None,
    "ssl_disabled": False,
    "tls_versions": None,
    "passwd": None,
    "db": None,
    "connect_timeout": None,
    "dsn": None,
    "force_ipv6": False,
    "auth_plugin": None,
    "allow_local_infile": False,
    "allow_local_infile_in_path": None,
    "consume_results": False,
    "conn_attrs": None,
    "dns_srv": False,
    "use_pure": False,
    "krb_service_principal": None,
    "oci_config_file": None,
    "oci_config_profile": None,
    "webauthn_callback": None,
    "kerberos_auth_mode": None,
    "init_command": None,
    "openid_token_file": None,
}

CNX_POOL_ARGS: Tuple[str, str, str] = ("pool_name", "pool_size", "pool_reset_session")

CONN_ATTRS_DN: Tuple[str, ...] = (
    "_pid",
    "_platform",
    "_source_host",
    "_client_name",
    "_client_license",
    "_client_version",
    "_os",
    "_connector_name",
    "_connector_license",
    "_connector_version",
)

DEPRECATED_METHOD_WARNING: str = """
    The property counterpart '{property_name}' should be used instead.
"""

TLS_VERSIONS: List[str] = APPROVED_TLS_VERSIONS + DEPRECATED_TLS_VERSIONS
"""Accepted TLS versions. A warning is raised when using a deprecated version."""

# TLS v1.2 cipher suites IANI to OpenSSL name translation
TLSV1_2_CIPHER_SUITES: Dict[str, str] = {
    "TLS_RSA_WITH_NULL_SHA256": "NULL-SHA256",
    "TLS_RSA_WITH_AES_128_CBC_SHA256": "AES128-SHA256",
    "TLS_RSA_WITH_AES_256_CBC_SHA256": "AES256-SHA256",
    "TLS_RSA_WITH_AES_128_GCM_SHA256": "AES128-GCM-SHA256",
    "TLS_RSA_WITH_AES_256_GCM_SHA384": "AES256-GCM-SHA384",
    "TLS_DH_RSA_WITH_AES_128_CBC_SHA256": "DH-RSA-AES128-SHA256",
    "TLS_DH_RSA_WITH_AES_256_CBC_SHA256": "DH-RSA-AES256-SHA256",
    "TLS_DH_RSA_WITH_AES_128_GCM_SHA256": "DH-RSA-AES128-GCM-SHA256",
    "TLS_DH_RSA_WITH_AES_256_GCM_SHA384": "DH-RSA-AES256-GCM-SHA384",
    "TLS_DH_DSS_WITH_AES_128_CBC_SHA256": "DH-DSS-AES128-SHA256",
    "TLS_DH_DSS_WITH_AES_256_CBC_SHA256": "DH-DSS-AES256-SHA256",
    "TLS_DH_DSS_WITH_AES_128_GCM_SHA256": "DH-DSS-AES128-GCM-SHA256",
    "TLS_DH_DSS_WITH_AES_256_GCM_SHA384": "DH-DSS-AES256-GCM-SHA384",
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256": "DHE-RSA-AES128-SHA256",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256": "DHE-RSA-AES256-SHA256",
    "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256": "DHE-RSA-AES128-GCM-SHA256",
    "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384": "DHE-RSA-AES256-GCM-SHA384",
    "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256": "DHE-DSS-AES128-SHA256",
    "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256": "DHE-DSS-AES256-SHA256",
    "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256": "DHE-DSS-AES128-GCM-SHA256",
    "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384": "DHE-DSS-AES256-GCM-SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256": "ECDHE-RSA-AES128-SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384": "ECDHE-RSA-AES256-SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256": "ECDHE-RSA-AES128-GCM-SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384": "ECDHE-RSA-AES256-GCM-SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256": "ECDHE-ECDSA-AES128-SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384": "ECDHE-ECDSA-AES256-SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256": "ECDHE-ECDSA-AES128-GCM-SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384": "ECDHE-ECDSA-AES256-GCM-SHA384",
    "TLS_DH_anon_WITH_AES_128_CBC_SHA256": "ADH-AES128-SHA256",
    "TLS_DH_anon_WITH_AES_256_CBC_SHA256": "ADH-AES256-SHA256",
    "TLS_DH_anon_WITH_AES_128_GCM_SHA256": "ADH-AES128-GCM-SHA256",
    "TLS_DH_anon_WITH_AES_256_GCM_SHA384": "ADH-AES256-GCM-SHA384",
    "RSA_WITH_AES_128_CCM": "AES128-CCM",
    "RSA_WITH_AES_256_CCM": "AES256-CCM",
    "DHE_RSA_WITH_AES_128_CCM": "DHE-RSA-AES128-CCM",
    "DHE_RSA_WITH_AES_256_CCM": "DHE-RSA-AES256-CCM",
    "RSA_WITH_AES_128_CCM_8": "AES128-CCM8",
    "RSA_WITH_AES_256_CCM_8": "AES256-CCM8",
    "DHE_RSA_WITH_AES_128_CCM_8": "DHE-RSA-AES128-CCM8",
    "DHE_RSA_WITH_AES_256_CCM_8": "DHE-RSA-AES256-CCM8",
    "ECDHE_ECDSA_WITH_AES_128_CCM": "ECDHE-ECDSA-AES128-CCM",
    "ECDHE_ECDSA_WITH_AES_256_CCM": "ECDHE-ECDSA-AES256-CCM",
    "ECDHE_ECDSA_WITH_AES_128_CCM_8": "ECDHE-ECDSA-AES128-CCM8",
    "ECDHE_ECDSA_WITH_AES_256_CCM_8": "ECDHE-ECDSA-AES256-CCM8",
    # ARIA cipher suites from RFC6209, extending TLS v1.2
    "TLS_RSA_WITH_ARIA_128_GCM_SHA256": "ARIA128-GCM-SHA256",
    "TLS_RSA_WITH_ARIA_256_GCM_SHA384": "ARIA256-GCM-SHA384",
    "TLS_DHE_RSA_WITH_ARIA_128_GCM_SHA256": "DHE-RSA-ARIA128-GCM-SHA256",
    "TLS_DHE_RSA_WITH_ARIA_256_GCM_SHA384": "DHE-RSA-ARIA256-GCM-SHA384",
    "TLS_DHE_DSS_WITH_ARIA_128_GCM_SHA256": "DHE-DSS-ARIA128-GCM-SHA256",
    "TLS_DHE_DSS_WITH_ARIA_256_GCM_SHA384": "DHE-DSS-ARIA256-GCM-SHA384",
    "TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256": "ECDHE-ECDSA-ARIA128-GCM-SHA256",
    "TLS_ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384": "ECDHE-ECDSA-ARIA256-GCM-SHA384",
    "TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256": "ECDHE-ARIA128-GCM-SHA256",
    "TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384": "ECDHE-ARIA256-GCM-SHA384",
    "TLS_PSK_WITH_ARIA_128_GCM_SHA256": "PSK-ARIA128-GCM-SHA256",
    "TLS_PSK_WITH_ARIA_256_GCM_SHA384": "PSK-ARIA256-GCM-SHA384",
    "TLS_DHE_PSK_WITH_ARIA_128_GCM_SHA256": "DHE-PSK-ARIA128-GCM-SHA256",
    "TLS_DHE_PSK_WITH_ARIA_256_GCM_SHA384": "DHE-PSK-ARIA256-GCM-SHA384",
    "TLS_RSA_PSK_WITH_ARIA_128_GCM_SHA256": "RSA-PSK-ARIA128-GCM-SHA256",
    "TLS_RSA_PSK_WITH_ARIA_256_GCM_SHA384": "RSA-PSK-ARIA256-GCM-SHA384",
    # Camellia HMAC-Based cipher suites from RFC6367, extending TLS v1.2
    "TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256": "ECDHE-ECDSA-CAMELLIA128-SHA256",
    "TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384": "ECDHE-ECDSA-CAMELLIA256-SHA384",
    "TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256": "ECDHE-RSA-CAMELLIA128-SHA256",
    "TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384": "ECDHE-RSA-CAMELLIA256-SHA384",
    # Pre-shared keying (PSK) cipher suites",
    "PSK_WITH_NULL_SHA": "PSK-NULL-SHA",
    "DHE_PSK_WITH_NULL_SHA": "DHE-PSK-NULL-SHA",
    "RSA_PSK_WITH_NULL_SHA": "RSA-PSK-NULL-SHA",
    "PSK_WITH_RC4_128_SHA": "PSK-RC4-SHA",
    "PSK_WITH_3DES_EDE_CBC_SHA": "PSK-3DES-EDE-CBC-SHA",
    "PSK_WITH_AES_128_CBC_SHA": "PSK-AES128-CBC-SHA",
    "PSK_WITH_AES_256_CBC_SHA": "PSK-AES256-CBC-SHA",
    "DHE_PSK_WITH_RC4_128_SHA": "DHE-PSK-RC4-SHA",
    "DHE_PSK_WITH_3DES_EDE_CBC_SHA": "DHE-PSK-3DES-EDE-CBC-SHA",
    "DHE_PSK_WITH_AES_128_CBC_SHA": "DHE-PSK-AES128-CBC-SHA",
    "DHE_PSK_WITH_AES_256_CBC_SHA": "DHE-PSK-AES256-CBC-SHA",
    "RSA_PSK_WITH_RC4_128_SHA": "RSA-PSK-RC4-SHA",
    "RSA_PSK_WITH_3DES_EDE_CBC_SHA": "RSA-PSK-3DES-EDE-CBC-SHA",
    "RSA_PSK_WITH_AES_128_CBC_SHA": "RSA-PSK-AES128-CBC-SHA",
    "RSA_PSK_WITH_AES_256_CBC_SHA": "RSA-PSK-AES256-CBC-SHA",
    "PSK_WITH_AES_128_GCM_SHA256": "PSK-AES128-GCM-SHA256",
    "PSK_WITH_AES_256_GCM_SHA384": "PSK-AES256-GCM-SHA384",
    "DHE_PSK_WITH_AES_128_GCM_SHA256": "DHE-PSK-AES128-GCM-SHA256",
    "DHE_PSK_WITH_AES_256_GCM_SHA384": "DHE-PSK-AES256-GCM-SHA384",
    "RSA_PSK_WITH_AES_128_GCM_SHA256": "RSA-PSK-AES128-GCM-SHA256",
    "RSA_PSK_WITH_AES_256_GCM_SHA384": "RSA-PSK-AES256-GCM-SHA384",
    "PSK_WITH_AES_128_CBC_SHA256": "PSK-AES128-CBC-SHA256",
    "PSK_WITH_AES_256_CBC_SHA384": "PSK-AES256-CBC-SHA384",
    "PSK_WITH_NULL_SHA256": "PSK-NULL-SHA256",
    "PSK_WITH_NULL_SHA384": "PSK-NULL-SHA384",
    "DHE_PSK_WITH_AES_128_CBC_SHA256": "DHE-PSK-AES128-CBC-SHA256",
    "DHE_PSK_WITH_AES_256_CBC_SHA384": "DHE-PSK-AES256-CBC-SHA384",
    "DHE_PSK_WITH_NULL_SHA256": "DHE-PSK-NULL-SHA256",
    "DHE_PSK_WITH_NULL_SHA384": "DHE-PSK-NULL-SHA384",
    "RSA_PSK_WITH_AES_128_CBC_SHA256": "RSA-PSK-AES128-CBC-SHA256",
    "RSA_PSK_WITH_AES_256_CBC_SHA384": "RSA-PSK-AES256-CBC-SHA384",
    "RSA_PSK_WITH_NULL_SHA256": "RSA-PSK-NULL-SHA256",
    "RSA_PSK_WITH_NULL_SHA384": "RSA-PSK-NULL-SHA384",
    "ECDHE_PSK_WITH_RC4_128_SHA": "ECDHE-PSK-RC4-SHA",
    "ECDHE_PSK_WITH_3DES_EDE_CBC_SHA": "ECDHE-PSK-3DES-EDE-CBC-SHA",
    "ECDHE_PSK_WITH_AES_128_CBC_SHA": "ECDHE-PSK-AES128-CBC-SHA",
    "ECDHE_PSK_WITH_AES_256_CBC_SHA": "ECDHE-PSK-AES256-CBC-SHA",
    "ECDHE_PSK_WITH_AES_128_CBC_SHA256": "ECDHE-PSK-AES128-CBC-SHA256",
    "ECDHE_PSK_WITH_AES_256_CBC_SHA384": "ECDHE-PSK-AES256-CBC-SHA384",
    "ECDHE_PSK_WITH_NULL_SHA": "ECDHE-PSK-NULL-SHA",
    "ECDHE_PSK_WITH_NULL_SHA256": "ECDHE-PSK-NULL-SHA256",
    "ECDHE_PSK_WITH_NULL_SHA384": "ECDHE-PSK-NULL-SHA384",
    "PSK_WITH_CAMELLIA_128_CBC_SHA256": "PSK-CAMELLIA128-SHA256",
    "PSK_WITH_CAMELLIA_256_CBC_SHA384": "PSK-CAMELLIA256-SHA384",
    "DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256": "DHE-PSK-CAMELLIA128-SHA256",
    "DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384": "DHE-PSK-CAMELLIA256-SHA384",
    "RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256": "RSA-PSK-CAMELLIA128-SHA256",
    "RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384": "RSA-PSK-CAMELLIA256-SHA384",
    "ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256": "ECDHE-PSK-CAMELLIA128-SHA256",
    "ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384": "ECDHE-PSK-CAMELLIA256-SHA384",
    "PSK_WITH_AES_128_CCM": "PSK-AES128-CCM",
    "PSK_WITH_AES_256_CCM": "PSK-AES256-CCM",
    "DHE_PSK_WITH_AES_128_CCM": "DHE-PSK-AES128-CCM",
    "DHE_PSK_WITH_AES_256_CCM": "DHE-PSK-AES256-CCM",
    "PSK_WITH_AES_128_CCM_8": "PSK-AES128-CCM8",
    "PSK_WITH_AES_256_CCM_8": "PSK-AES256-CCM8",
    "DHE_PSK_WITH_AES_128_CCM_8": "DHE-PSK-AES128-CCM8",
    "DHE_PSK_WITH_AES_256_CCM_8": "DHE-PSK-AES256-CCM8",
    # ChaCha20-Poly1305 cipher suites, extending TLS v1.2
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-RSA-CHACHA20-POLY1305",
    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-ECDSA-CHACHA20-POLY1305",
    "TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256": "DHE-RSA-CHACHA20-POLY1305",
    "TLS_PSK_WITH_CHACHA20_POLY1305_SHA256": "PSK-CHACHA20-POLY1305",
    "TLS_ECDHE_PSK_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-PSK-CHACHA20-POLY1305",
    "TLS_DHE_PSK_WITH_CHACHA20_POLY1305_SHA256": "DHE-PSK-CHACHA20-POLY1305",
    "TLS_RSA_PSK_WITH_CHACHA20_POLY1305_SHA256": "RSA-PSK-CHACHA20-POLY1305",
}

# TLS v1.3 cipher suites IANI to OpenSSL name translation
TLSV1_3_CIPHER_SUITES: Dict[str, str] = {
    "TLS_AES_128_GCM_SHA256": "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384": "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256": "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_128_CCM_SHA256": "TLS_AES_128_CCM_SHA256",
    "TLS_AES_128_CCM_8_SHA256": "TLS_AES_128_CCM_8_SHA256",
}

TLS_CIPHER_SUITES: Dict[str, Dict[str, str]] = {
    "TLSv1.2": TLSV1_2_CIPHER_SUITES,
    "TLSv1.3": TLSV1_3_CIPHER_SUITES,
}

OPENSSL_CS_NAMES: Dict[str, ValuesView[str]] = {
    "TLSv1.2": TLSV1_2_CIPHER_SUITES.values(),
    "TLSv1.3": TLSV1_3_CIPHER_SUITES.values(),
}


def flag_is_set(flag: int, flags: int) -> bool:
    """Checks if the flag is set

    Returns boolean"""
    if (flags & flag) > 0:
        return True
    return False


def _obsolete_option(name: str, new_name: str, value: int) -> int:
    """Raise a deprecation warning and advise a new option name.

    Args:
        name (str): The name of the option.
        new_name (str): The new option name.
        value (int): The value of the option.

    Returns:
        int: The value of the option.
    """
    warnings.warn(
        f"The option '{name}' has been deprecated, use '{new_name}' instead.",
        category=DeprecationWarning,
    )
    return value


class _Constants(ABC):
    """Base class for constants."""

    prefix: str = ""
    desc: Dict[str, Tuple[int, str]] = {}

    @classmethod
    def get_desc(cls, name: str) -> Optional[str]:
        """Get description of given constant"""
        try:
            return cls.desc[name][1]
        except (IndexError, KeyError):
            return None

    @classmethod
    def get_info(cls, setid: int) -> Union[Optional[str], Tuple[str, str]]:
        """Get information about given constant"""
        for name, info in cls.desc.items():
            if info[0] == setid:
                return name
        return None

    @classmethod
    def get_full_info(cls) -> Union[str, Sequence[str]]:
        """get full information about given constant"""
        res: Union[str, List[str]] = []
        try:
            res = [f"{k} : {v[1]}" for k, v in cls.desc.items()]
        except (AttributeError, IndexError) as err:
            res = f"No information found in constant class. {err}"

        return res


class _Flags(_Constants):
    """Base class for classes describing flags"""

    @classmethod
    def get_bit_info(cls, value: int) -> List[str]:
        """Get the name of all bits set

        Returns a list of strings."""
        res = []
        for name, info in cls.desc.items():
            if value & info[0]:
                res.append(name)
        return res


class FieldType(_Constants):
    """MySQL Field Types.

    This class provides all supported MySQL field or data types. They can be useful
    when dealing with raw data or defining your own converters. The field type is
    stored with every cursor in the description for each column.

    The `FieldType` class shouldn't be instantiated.

    Examples:
        The following example shows how to print the name of the data type for
        each column in a result set.

        ```
        from __future__ import print_function
        import mysql.connector
        from mysql.connector import FieldType

        cnx = mysql.connector.connect(user='scott', database='test')
        cursor = cnx.cursor()

        cursor.execute(
        "SELECT DATE(NOW()) AS `c1`, TIME(NOW()) AS `c2`, "
        "NOW() AS `c3`, 'a string' AS `c4`, 42 AS `c5`")
        rows = cursor.fetchall()

        for desc in cursor.description:
            colname = desc[0]
            coltype = desc[1]
            print("Column {} has type {}".format(
                colname, FieldType.get_info(coltype)))

        cursor.close()
        cnx.close()
        ```
    """

    prefix: str = "FIELD_TYPE_"
    DECIMAL: int = 0x00
    TINY: int = 0x01
    SHORT: int = 0x02
    LONG: int = 0x03
    FLOAT: int = 0x04
    DOUBLE: int = 0x05
    NULL: int = 0x06
    TIMESTAMP: int = 0x07
    LONGLONG: int = 0x08
    INT24: int = 0x09
    DATE: int = 0x0A
    TIME: int = 0x0B
    DATETIME: int = 0x0C
    YEAR: int = 0x0D
    NEWDATE: int = 0x0E
    VARCHAR: int = 0x0F
    BIT: int = 0x10
    VECTOR: int = 0xF2
    JSON: int = 0xF5
    NEWDECIMAL: int = 0xF6
    ENUM: int = 0xF7
    SET: int = 0xF8
    TINY_BLOB: int = 0xF9
    MEDIUM_BLOB: int = 0xFA
    LONG_BLOB: int = 0xFB
    BLOB: int = 0xFC
    VAR_STRING: int = 0xFD
    STRING: int = 0xFE
    GEOMETRY: int = 0xFF

    desc: Dict[str, Tuple[int, str]] = {
        "DECIMAL": (DECIMAL, "DECIMAL"),
        "TINY": (TINY, "TINY"),
        "SHORT": (SHORT, "SHORT"),
        "LONG": (LONG, "LONG"),
        "FLOAT": (FLOAT, "FLOAT"),
        "DOUBLE": (DOUBLE, "DOUBLE"),
        "NULL": (NULL, "NULL"),
        "TIMESTAMP": (TIMESTAMP, "TIMESTAMP"),
        "LONGLONG": (LONGLONG, "LONGLONG"),
        "INT24": (INT24, "INT24"),
        "DATE": (DATE, "DATE"),
        "TIME": (TIME, "TIME"),
        "DATETIME": (DATETIME, "DATETIME"),
        "YEAR": (YEAR, "YEAR"),
        "NEWDATE": (NEWDATE, "NEWDATE"),
        "VARCHAR": (VARCHAR, "VARCHAR"),
        "BIT": (BIT, "BIT"),
        "VECTOR": (VECTOR, "VECTOR"),
        "JSON": (JSON, "JSON"),
        "NEWDECIMAL": (NEWDECIMAL, "NEWDECIMAL"),
        "ENUM": (ENUM, "ENUM"),
        "SET": (SET, "SET"),
        "TINY_BLOB": (TINY_BLOB, "TINY_BLOB"),
        "MEDIUM_BLOB": (MEDIUM_BLOB, "MEDIUM_BLOB"),
        "LONG_BLOB": (LONG_BLOB, "LONG_BLOB"),
        "BLOB": (BLOB, "BLOB"),
        "VAR_STRING": (VAR_STRING, "VAR_STRING"),
        "STRING": (STRING, "STRING"),
        "GEOMETRY": (GEOMETRY, "GEOMETRY"),
    }

    @classmethod
    def get_string_types(cls) -> List[int]:
        """Get the list of all string types"""
        return [
            cls.VARCHAR,
            cls.ENUM,
            cls.VAR_STRING,
            cls.STRING,
        ]

    @classmethod
    def get_binary_types(cls) -> List[int]:
        """Get the list of all binary types"""
        return [
            cls.TINY_BLOB,
            cls.MEDIUM_BLOB,
            cls.LONG_BLOB,
            cls.BLOB,
        ]

    @classmethod
    def get_number_types(cls) -> List[int]:
        """Get the list of all number types"""
        return [
            cls.DECIMAL,
            cls.NEWDECIMAL,
            cls.TINY,
            cls.SHORT,
            cls.LONG,
            cls.FLOAT,
            cls.DOUBLE,
            cls.LONGLONG,
            cls.INT24,
            cls.BIT,
            cls.YEAR,
        ]

    @classmethod
    def get_timestamp_types(cls) -> List[int]:
        """Get the list of all timestamp types"""
        return [
            cls.DATETIME,
            cls.TIMESTAMP,
        ]


class FieldFlag(_Flags):
    """MySQL Field Flags

    Field flags as found in MySQL sources mysql-src/include/mysql_com.h
    """

    _prefix: str = ""
    NOT_NULL: int = 1 << 0
    PRI_KEY: int = 1 << 1
    UNIQUE_KEY: int = 1 << 2
    MULTIPLE_KEY: int = 1 << 3
    BLOB: int = 1 << 4
    UNSIGNED: int = 1 << 5
    ZEROFILL: int = 1 << 6
    BINARY: int = 1 << 7

    ENUM: int = 1 << 8
    AUTO_INCREMENT: int = 1 << 9
    TIMESTAMP: int = 1 << 10
    SET: int = 1 << 11

    NO_DEFAULT_VALUE: int = 1 << 12
    ON_UPDATE_NOW: int = 1 << 13
    NUM: int = 1 << 14
    PART_KEY: int = 1 << 15
    GROUP: int = 1 << 14  # SAME AS NUM !!!!!!!????
    UNIQUE: int = 1 << 16
    BINCMP: int = 1 << 17

    GET_FIXED_FIELDS: int = 1 << 18
    FIELD_IN_PART_FUNC: int = 1 << 19
    FIELD_IN_ADD_INDEX: int = 1 << 20
    FIELD_IS_RENAMED: int = 1 << 21

    desc: Dict[str, Tuple[int, str]] = {
        "NOT_NULL": (1 << 0, "Field can't be NULL"),
        "PRI_KEY": (1 << 1, "Field is part of a primary key"),
        "UNIQUE_KEY": (1 << 2, "Field is part of a unique key"),
        "MULTIPLE_KEY": (1 << 3, "Field is part of a key"),
        "BLOB": (1 << 4, "Field is a blob"),
        "UNSIGNED": (1 << 5, "Field is unsigned"),
        "ZEROFILL": (1 << 6, "Field is zerofill"),
        "BINARY": (1 << 7, "Field is binary  "),
        "ENUM": (1 << 8, "field is an enum"),
        "AUTO_INCREMENT": (1 << 9, "field is a autoincrement field"),
        "TIMESTAMP": (1 << 10, "Field is a timestamp"),
        "SET": (1 << 11, "field is a set"),
        "NO_DEFAULT_VALUE": (1 << 12, "Field doesn't have default value"),
        "ON_UPDATE_NOW": (1 << 13, "Field is set to NOW on UPDATE"),
        "NUM": (1 << 14, "Field is num (for clients)"),
        "PART_KEY": (1 << 15, "Intern; Part of some key"),
        "GROUP": (1 << 14, "Intern: Group field"),  # Same as NUM
        "UNIQUE": (1 << 16, "Intern: Used by sql_yacc"),
        "BINCMP": (1 << 17, "Intern: Used by sql_yacc"),
        "GET_FIXED_FIELDS": (1 << 18, "Used to get fields in item tree"),
        "FIELD_IN_PART_FUNC": (1 << 19, "Field part of partition func"),
        "FIELD_IN_ADD_INDEX": (1 << 20, "Intern: Field used in ADD INDEX"),
        "FIELD_IS_RENAMED": (1 << 21, "Intern: Field is being renamed"),
    }


class ServerCmdMeta(ABCMeta):
    """ClientFlag Metaclass."""

    def __getattribute__(cls, name: str) -> Any:
        deprecated_options = (
            "FIELD_LIST",
            "REFRESH",
            "SHUTDOWN",
            "PROCESS_INFO",
            "PROCESS_KILL",
        )
        if name in deprecated_options:
            warnings.warn(
                f"The option 'ServerCmd.{name}' is deprecated and will be removed in "
                "a future release.",
                category=DeprecationWarning,
            )
        return super().__getattribute__(name)


class ServerCmd(_Constants, metaclass=ServerCmdMeta):
    """MySQL Server Commands"""

    _prefix: str = "COM_"
    SLEEP: int = 0
    QUIT: int = 1
    INIT_DB: int = 2
    QUERY: int = 3
    FIELD_LIST: int = 4
    CREATE_DB: int = 5
    DROP_DB: int = 6
    REFRESH: int = 7
    SHUTDOWN: int = 8
    STATISTICS: int = 9
    PROCESS_INFO: int = 10
    CONNECT: int = 11
    PROCESS_KILL: int = 12
    DEBUG: int = 13
    PING: int = 14
    TIME: int = 15
    DELAYED_INSERT: int = 16
    CHANGE_USER: int = 17
    BINLOG_DUMP: int = 18
    TABLE_DUMP: int = 19
    CONNECT_OUT: int = 20
    REGISTER_REPLICA: int = 21
    STMT_PREPARE: int = 22
    STMT_EXECUTE: int = 23
    STMT_SEND_LONG_DATA: int = 24
    STMT_CLOSE: int = 25
    STMT_RESET: int = 26
    SET_OPTION: int = 27
    STMT_FETCH: int = 28
    DAEMON: int = 29
    BINLOG_DUMP_GTID: int = 30
    RESET_CONNECTION: int = 31

    desc: Dict[str, Tuple[int, str]] = {
        "SLEEP": (0, "SLEEP"),
        "QUIT": (1, "QUIT"),
        "INIT_DB": (2, "INIT_DB"),
        "QUERY": (3, "QUERY"),
        "FIELD_LIST": (4, "FIELD_LIST"),
        "CREATE_DB": (5, "CREATE_DB"),
        "DROP_DB": (6, "DROP_DB"),
        "REFRESH": (7, "REFRESH"),
        "SHUTDOWN": (8, "SHUTDOWN"),
        "STATISTICS": (9, "STATISTICS"),
        "PROCESS_INFO": (10, "PROCESS_INFO"),
        "CONNECT": (11, "CONNECT"),
        "PROCESS_KILL": (12, "PROCESS_KILL"),
        "DEBUG": (13, "DEBUG"),
        "PING": (14, "PING"),
        "TIME": (15, "TIME"),
        "DELAYED_INSERT": (16, "DELAYED_INSERT"),
        "CHANGE_USER": (17, "CHANGE_USER"),
        "BINLOG_DUMP": (18, "BINLOG_DUMP"),
        "TABLE_DUMP": (19, "TABLE_DUMP"),
        "CONNECT_OUT": (20, "CONNECT_OUT"),
        "REGISTER_REPLICA": (21, "REGISTER_REPLICA"),
        "STMT_PREPARE": (22, "STMT_PREPARE"),
        "STMT_EXECUTE": (23, "STMT_EXECUTE"),
        "STMT_SEND_LONG_DATA": (24, "STMT_SEND_LONG_DATA"),
        "STMT_CLOSE": (25, "STMT_CLOSE"),
        "STMT_RESET": (26, "STMT_RESET"),
        "SET_OPTION": (27, "SET_OPTION"),
        "STMT_FETCH": (28, "STMT_FETCH"),
        "DAEMON": (29, "DAEMON"),
        "BINLOG_DUMP_GTID": (30, "BINLOG_DUMP_GTID"),
        "RESET_CONNECTION": (31, "RESET_CONNECTION"),
    }


class ClientFlag(_Flags):
    """MySQL Client Flags.

    Client options as found in the MySQL sources mysql-src/include/mysql_com.h.

    This class provides constants defining MySQL client flags that can be used
    when the connection is established to configure the session. The `ClientFlag`
    class is available when importing mysql.connector.

    The `ClientFlag` class shouldn't be instantiated.

    Examples:
        ```
        >>> import mysql.connector
        >>> mysql.connector.ClientFlag.FOUND_ROWS
        2
        ```
    """

    LONG_PASSWD: int = 1 << 0
    FOUND_ROWS: int = 1 << 1
    LONG_FLAG: int = 1 << 2
    CONNECT_WITH_DB: int = 1 << 3
    NO_SCHEMA: int = 1 << 4
    COMPRESS: int = 1 << 5
    ODBC: int = 1 << 6
    LOCAL_FILES: int = 1 << 7
    IGNORE_SPACE: int = 1 << 8
    PROTOCOL_41: int = 1 << 9
    INTERACTIVE: int = 1 << 10
    SSL: int = 1 << 11
    IGNORE_SIGPIPE: int = 1 << 12
    TRANSACTIONS: int = 1 << 13
    RESERVED: int = 1 << 14
    SECURE_CONNECTION: int = 1 << 15
    MULTI_STATEMENTS: int = 1 << 16
    MULTI_RESULTS: int = 1 << 17
    PS_MULTI_RESULTS: int = 1 << 18
    PLUGIN_AUTH: int = 1 << 19
    CONNECT_ARGS: int = 1 << 20
    PLUGIN_AUTH_LENENC_CLIENT_DATA: int = 1 << 21
    CAN_HANDLE_EXPIRED_PASSWORDS: int = 1 << 22
    SESION_TRACK: int = 1 << 23  # deprecated
    SESSION_TRACK: int = 1 << 23
    DEPRECATE_EOF: int = 1 << 24
    CLIENT_QUERY_ATTRIBUTES: int = 1 << 27
    SSL_VERIFY_SERVER_CERT: int = 1 << 30
    REMEMBER_OPTIONS: int = 1 << 31
    MULTI_FACTOR_AUTHENTICATION: int = 1 << 28

    desc: Dict[str, Tuple[int, str]] = {
        "LONG_PASSWD": (1 << 0, "New more secure passwords"),
        "FOUND_ROWS": (1 << 1, "Found instead of affected rows"),
        "LONG_FLAG": (1 << 2, "Get all column flags"),
        "CONNECT_WITH_DB": (1 << 3, "One can specify db on connect"),
        "NO_SCHEMA": (1 << 4, "Don't allow database.table.column"),
        "COMPRESS": (1 << 5, "Can use compression protocol"),
        "ODBC": (1 << 6, "ODBC client"),
        "LOCAL_FILES": (1 << 7, "Can use LOAD DATA LOCAL"),
        "IGNORE_SPACE": (1 << 8, "Ignore spaces before ''"),
        "PROTOCOL_41": (1 << 9, "New 4.1 protocol"),
        "INTERACTIVE": (1 << 10, "This is an interactive client"),
        "SSL": (1 << 11, "Switch to SSL after handshake"),
        "IGNORE_SIGPIPE": (1 << 12, "IGNORE sigpipes"),
        "TRANSACTIONS": (1 << 13, "Client knows about transactions"),
        "RESERVED": (1 << 14, "Old flag for 4.1 protocol"),
        "SECURE_CONNECTION": (1 << 15, "New 4.1 authentication"),
        "MULTI_STATEMENTS": (1 << 16, "Enable/disable multi-stmt support"),
        "MULTI_RESULTS": (1 << 17, "Enable/disable multi-results"),
        "PS_MULTI_RESULTS": (1 << 18, "Multi-results in PS-protocol"),
        "PLUGIN_AUTH": (1 << 19, "Client supports plugin authentication"),
        "CONNECT_ARGS": (1 << 20, "Client supports connection attributes"),
        "PLUGIN_AUTH_LENENC_CLIENT_DATA": (
            1 << 21,
            "Enable authentication response packet to be larger than 255 bytes",
        ),
        "CAN_HANDLE_EXPIRED_PASSWORDS": (
            1 << 22,
            "Don't close the connection for a connection with expired password",
        ),
        "SESION_TRACK": (  # deprecated
            1 << 23,
            "Capable of handling server state change information",
        ),
        "SESSION_TRACK": (
            1 << 23,
            "Capable of handling server state change information",
        ),
        "DEPRECATE_EOF": (1 << 24, "Client no longer needs EOF packet"),
        "CLIENT_QUERY_ATTRIBUTES": (
            1 << 27,
            "Support optional extension for query parameters",
        ),
        "SSL_VERIFY_SERVER_CERT": (1 << 30, ""),
        "REMEMBER_OPTIONS": (1 << 31, ""),
    }

    default: List[int] = [
        LONG_PASSWD,
        LONG_FLAG,
        CONNECT_WITH_DB,
        PROTOCOL_41,
        TRANSACTIONS,
        SECURE_CONNECTION,
        MULTI_STATEMENTS,
        MULTI_RESULTS,
        CONNECT_ARGS,
        PLUGIN_AUTH_LENENC_CLIENT_DATA,
    ]

    @classmethod
    def get_default(cls) -> int:
        """Get the default client options set

        Returns a flag with all the default client options set"""
        flags = 0
        for option in cls.default:
            flags |= option
        return flags


class ServerFlag(_Flags):
    """MySQL Server Flags

    Server flags as found in the MySQL sources mysql-src/include/mysql_com.h
    """

    _prefix: str = "SERVER_"
    STATUS_IN_TRANS: int = 1 << 0
    STATUS_AUTOCOMMIT: int = 1 << 1
    MORE_RESULTS_EXISTS: int = 1 << 3
    QUERY_NO_GOOD_INDEX_USED: int = 1 << 4
    QUERY_NO_INDEX_USED: int = 1 << 5
    STATUS_CURSOR_EXISTS: int = 1 << 6
    STATUS_LAST_ROW_SENT: int = 1 << 7
    STATUS_DB_DROPPED: int = 1 << 8
    STATUS_NO_BACKSLASH_ESCAPES: int = 1 << 9
    SERVER_STATUS_METADATA_CHANGED: int = 1 << 10
    SERVER_QUERY_WAS_SLOW: int = 1 << 11
    SERVER_PS_OUT_PARAMS: int = 1 << 12
    SERVER_STATUS_IN_TRANS_READONLY: int = 1 << 13
    SERVER_SESSION_STATE_CHANGED: int = 1 << 14

    desc: Dict[str, Tuple[int, str]] = {
        "SERVER_STATUS_IN_TRANS": (1 << 0, "Transaction has started"),
        "SERVER_STATUS_AUTOCOMMIT": (1 << 1, "Server in auto_commit mode"),
        "SERVER_MORE_RESULTS_EXISTS": (
            1 << 3,
            "Multi query - next query exists",
        ),
        "SERVER_QUERY_NO_GOOD_INDEX_USED": (1 << 4, ""),
        "SERVER_QUERY_NO_INDEX_USED": (1 << 5, ""),
        "SERVER_STATUS_CURSOR_EXISTS": (
            1 << 6,
            "Set when server opened a read-only non-scrollable cursor for a query.",
        ),
        "SERVER_STATUS_LAST_ROW_SENT": (
            1 << 7,
            "Set when a read-only cursor is exhausted",
        ),
        "SERVER_STATUS_DB_DROPPED": (1 << 8, "A database was dropped"),
        "SERVER_STATUS_NO_BACKSLASH_ESCAPES": (1 << 9, ""),
        "SERVER_STATUS_METADATA_CHANGED": (
            1024,
            "Set if after a prepared statement "
            "reprepare we discovered that the "
            "new statement returns a different "
            "number of result set columns.",
        ),
        "SERVER_QUERY_WAS_SLOW": (2048, ""),
        "SERVER_PS_OUT_PARAMS": (
            4096,
            "To mark ResultSet containing output parameter values.",
        ),
        "SERVER_STATUS_IN_TRANS_READONLY": (
            8192,
            "Set if multi-statement transaction is a read-only transaction.",
        ),
        "SERVER_SESSION_STATE_CHANGED": (
            1 << 14,
            "Session state has changed on the "
            "server because of the execution of "
            "the last statement",
        ),
    }


class RefreshOptionMeta(ABCMeta):
    """RefreshOption Metaclass."""

    @property
    def SLAVE(self) -> int:  # pylint: disable=bad-mcs-method-argument,invalid-name
        """Return the deprecated alias of RefreshOption.REPLICA.

        Raises a warning about this attribute deprecation.
        """
        return _obsolete_option(
            "RefreshOption.SLAVE",
            "RefreshOption.REPLICA",
            RefreshOption.REPLICA,
        )


class RefreshOption(_Constants, metaclass=RefreshOptionMeta):
    """MySQL Refresh command options.

    Options used when sending the COM_REFRESH server command.
    """

    _prefix: str = "REFRESH_"
    GRANT: int = 1 << 0
    LOG: int = 1 << 1
    TABLES: int = 1 << 2
    HOST: int = 1 << 3
    STATUS: int = 1 << 4
    REPLICA: int = 1 << 6

    desc: Dict[str, Tuple[int, str]] = {
        "GRANT": (1 << 0, "Refresh grant tables"),
        "LOG": (1 << 1, "Start on new log file"),
        "TABLES": (1 << 2, "close all tables"),
        "HOST": (1 << 3, "Flush host cache"),
        "STATUS": (1 << 4, "Flush status variables"),
        "REPLICA": (1 << 6, "Reset source info and restart replica thread"),
        "SLAVE": (1 << 6, "Deprecated option; use REPLICA instead."),
    }


class ShutdownType(_Constants):
    """MySQL Shutdown types

    Shutdown types used by the COM_SHUTDOWN server command.
    """

    _prefix: str = ""
    SHUTDOWN_DEFAULT: int = 0
    SHUTDOWN_WAIT_CONNECTIONS: int = 1
    SHUTDOWN_WAIT_TRANSACTIONS: int = 2
    SHUTDOWN_WAIT_UPDATES: int = 8
    SHUTDOWN_WAIT_ALL_BUFFERS: int = 16
    SHUTDOWN_WAIT_CRITICAL_BUFFERS: int = 17
    KILL_QUERY: int = 254
    KILL_CONNECTION: int = 255

    desc: Dict[str, Tuple[int, str]] = {
        "SHUTDOWN_DEFAULT": (
            SHUTDOWN_DEFAULT,
            "defaults to SHUTDOWN_WAIT_ALL_BUFFERS",
        ),
        "SHUTDOWN_WAIT_CONNECTIONS": (
            SHUTDOWN_WAIT_CONNECTIONS,
            "wait for existing connections to finish",
        ),
        "SHUTDOWN_WAIT_TRANSACTIONS": (
            SHUTDOWN_WAIT_TRANSACTIONS,
            "wait for existing trans to finish",
        ),
        "SHUTDOWN_WAIT_UPDATES": (
            SHUTDOWN_WAIT_UPDATES,
            "wait for existing updates to finish",
        ),
        "SHUTDOWN_WAIT_ALL_BUFFERS": (
            SHUTDOWN_WAIT_ALL_BUFFERS,
            "flush InnoDB and other storage engine buffers",
        ),
        "SHUTDOWN_WAIT_CRITICAL_BUFFERS": (
            SHUTDOWN_WAIT_CRITICAL_BUFFERS,
            "don't flush InnoDB buffers, flush other storage engines' buffers",
        ),
        "KILL_QUERY": (KILL_QUERY, "(no description)"),
        "KILL_CONNECTION": (KILL_CONNECTION, "(no description)"),
    }


class CharacterSet:
    """MySQL supported character sets and collations

    List of character sets with their collations supported by MySQL. This
    maps to the character set we get from the server within the handshake
    packet.

    The list is hardcode so we avoid a database query when getting the
    name of the used character set or collation.
    """

    # Multi-byte character sets which use 5c (backslash) in characters
    slash_charsets: Tuple[int, ...] = (1, 13, 28, 84, 87, 88)

    def __init__(self) -> None:
        # Use LTS character set as default
        self._desc: List[Optional[Tuple[str, str, bool]]] = MYSQL_CHARACTER_SETS_57
        self._mysql_version: Tuple[int, ...] = (5, 7)

    def set_mysql_version(self, version: Tuple[int, ...]) -> None:
        """Set the MySQL major version and change the charset mapping if is 5.7.

        Args:
            version (tuple): MySQL version tuple.
        """
        self._mysql_version = version[:2]
        if self._mysql_version >= (8, 0):
            self._desc = MYSQL_CHARACTER_SETS

    def get_info(self, setid: int) -> Tuple[str, str]:
        """Retrieves character set information as tuple using an ID

        Retrieves character set and collation information based on the
        given MySQL ID.

        Raises ProgrammingError when character set is not supported.

        Returns a tuple.
        """
        try:
            return self._desc[setid][0:2]
        except IndexError:
            raise ProgrammingError(f"Character set '{setid}' unsupported") from None

    def get_desc(self, name: int) -> str:
        """Retrieves character set information as string using an ID

        Retrieves character set and collation information based on the
        given MySQL ID.

        Returns a tuple.
        """
        charset, collation = self.get_info(name)
        return f"{charset}/{collation}"

    def get_default_collation(self, charset: Union[int, str]) -> Tuple[str, str, int]:
        """Retrieves the default collation for given character set

        Raises ProgrammingError when character set is not supported.

        Returns list (collation, charset, index)
        """
        if isinstance(charset, int):
            try:
                info = self._desc[charset]
                return info[1], info[0], charset
            except (IndexError, KeyError) as err:
                raise ProgrammingError(
                    f"Character set ID '{charset}' unsupported"
                ) from err

        for cid, info in enumerate(self._desc):
            if info is None:
                continue
            if info[0] == charset and info[2] is True:
                return info[1], info[0], cid

        raise ProgrammingError(f"Character set '{charset}' unsupported")

    def get_charset_info(
        self, charset: Optional[Union[int, str]] = None, collation: Optional[str] = None
    ) -> Tuple[int, str, str]:
        """Get character set information using charset name and/or collation

        Retrieves character set and collation information given character
        set name and/or a collation name.
        If charset is an integer, it will look up the character set based
        on the MySQL's ID.
        For example:
            get_charset_info('utf8',None)
            get_charset_info(collation='utf8_general_ci')
            get_charset_info(47)

        Raises ProgrammingError when character set is not supported.

        Returns a tuple with (id, characterset name, collation)
        """
        info: Optional[Union[Tuple[str, str, bool], Tuple[str, str, int]]] = None
        if isinstance(charset, int):
            try:
                info = self._desc[charset]
                return (charset, info[0], info[1])
            except IndexError as err:
                raise ProgrammingError(f"Character set ID {charset} unknown") from err

        if charset in ("utf8", "utf-8") and self._mysql_version >= (8, 0):
            charset = "utf8mb4"
        if charset is not None and collation is None:
            info = self.get_default_collation(charset)
            return (info[2], info[1], info[0])
        if charset is None and collation is not None:
            for cid, info in enumerate(self._desc):
                if info is None:
                    continue
                if collation == info[1]:
                    return (cid, info[0], info[1])
            raise ProgrammingError(f"Collation '{collation}' unknown")
        for cid, info in enumerate(self._desc):
            if info is None:
                continue
            if info[0] == charset and info[1] == collation:
                return (cid, info[0], info[1])
        _ = self.get_default_collation(charset)
        raise ProgrammingError(f"Collation '{collation}' unknown")

    def get_supported(self) -> Tuple[str, ...]:
        """Retrieves a list with names of all supproted character sets

        Returns a tuple.
        """
        res = []
        for info in self._desc:
            if info and info[0] not in res:
                res.append(info[0])
        return tuple(res)


class SQLMode(_Constants):
    """MySQL SQL Modes

    The numeric values of SQL Modes are not interesting, only the names
    are used when setting the SQL_MODE system variable using the MySQL
    SET command.

    The `SQLMode` class shouldn't be instantiated.

    See http://dev.mysql.com/doc/refman/5.6/en/server-sql-mode.html
    """

    _prefix: str = "MODE_"
    REAL_AS_FLOAT: str = "REAL_AS_FLOAT"
    PIPES_AS_CONCAT: str = "PIPES_AS_CONCAT"
    ANSI_QUOTES: str = "ANSI_QUOTES"
    IGNORE_SPACE: str = "IGNORE_SPACE"
    NOT_USED: str = "NOT_USED"
    ONLY_FULL_GROUP_BY: str = "ONLY_FULL_GROUP_BY"
    NO_UNSIGNED_SUBTRACTION: str = "NO_UNSIGNED_SUBTRACTION"
    NO_DIR_IN_CREATE: str = "NO_DIR_IN_CREATE"
    POSTGRESQL: str = "POSTGRESQL"
    ORACLE: str = "ORACLE"
    MSSQL: str = "MSSQL"
    DB2: str = "DB2"
    MAXDB: str = "MAXDB"
    NO_KEY_OPTIONS: str = "NO_KEY_OPTIONS"
    NO_TABLE_OPTIONS: str = "NO_TABLE_OPTIONS"
    NO_FIELD_OPTIONS: str = "NO_FIELD_OPTIONS"
    MYSQL323: str = "MYSQL323"
    MYSQL40: str = "MYSQL40"
    ANSI: str = "ANSI"
    NO_AUTO_VALUE_ON_ZERO: str = "NO_AUTO_VALUE_ON_ZERO"
    NO_BACKSLASH_ESCAPES: str = "NO_BACKSLASH_ESCAPES"
    STRICT_TRANS_TABLES: str = "STRICT_TRANS_TABLES"
    STRICT_ALL_TABLES: str = "STRICT_ALL_TABLES"
    NO_ZERO_IN_DATE: str = "NO_ZERO_IN_DATE"
    NO_ZERO_DATE: str = "NO_ZERO_DATE"
    INVALID_DATES: str = "INVALID_DATES"
    ERROR_FOR_DIVISION_BY_ZERO: str = "ERROR_FOR_DIVISION_BY_ZERO"
    TRADITIONAL: str = "TRADITIONAL"
    NO_AUTO_CREATE_USER: str = "NO_AUTO_CREATE_USER"
    HIGH_NOT_PRECEDENCE: str = "HIGH_NOT_PRECEDENCE"
    NO_ENGINE_SUBSTITUTION: str = "NO_ENGINE_SUBSTITUTION"
    PAD_CHAR_TO_FULL_LENGTH: str = "PAD_CHAR_TO_FULL_LENGTH"

    @classmethod
    def get_desc(cls, name: str) -> Optional[str]:
        raise NotImplementedError

    @classmethod
    def get_info(cls, setid: int) -> Optional[str]:
        raise NotImplementedError

    @classmethod
    def get_full_info(cls) -> Tuple[str, ...]:
        """Returns a sequence of all available SQL Modes

        This class method returns a tuple containing all SQL Mode names. The
        names will be alphabetically sorted.

        Returns a tuple.
        """
        res = []
        for key in vars(cls).keys():
            if not key.startswith("_") and not hasattr(getattr(cls, key), "__call__"):
                res.append(key)
        return tuple(sorted(res))
