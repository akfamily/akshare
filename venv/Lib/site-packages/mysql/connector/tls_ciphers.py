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

"""TLS ciphersuites and versions."""

# Generated from the OSSA cipher list
# version: 3.4
# date: 2024-04-11

from typing import Dict, List

APPROVED_TLS_VERSIONS: List[str] = ["TLSv1.2", "TLSv1.3"]
"""Approved TLS versions."""

DEPRECATED_TLS_VERSIONS: List[str] = []
"""Deprecated TLS versions."""

UNACCEPTABLE_TLS_VERSIONS: List[str] = ["TLSv1", "TLSv1.0", "TLSv1.1"]
"""Unacceptable TLS versions."""

MANDATORY_TLS_CIPHERSUITES: Dict[str, Dict[str, str]] = {
    "TLSv1.2": {
        "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256": "ECDHE-ECDSA-AES128-GCM-SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384": "ECDHE-ECDSA-AES256-GCM-SHA384",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256": "ECDHE-RSA-AES128-GCM-SHA256",
    },
    "TLSv1.3": {},
}
"""Access dictionary by TLS version that translates from cipher suites IANI (key)
 to OpenSSL name (value)."""

APPROVED_TLS_CIPHERSUITES: Dict[str, Dict[str, str]] = {
    "TLSv1.2": {
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384": "ECDHE-RSA-AES256-GCM-SHA384",
        "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-ECDSA-CHACHA20-POLY1305",
        "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-RSA-CHACHA20-POLY1305",
        "TLS_ECDHE_ECDSA_WITH_AES_256_CCM": "ECDHE-ECDSA-AES256-CCM",
        "TLS_ECDHE_ECDSA_WITH_AES_128_CCM": "ECDHE-ECDSA-AES128-CCM",
    },
    "TLSv1.3": {
        "TLS_AES_128_GCM_SHA256": "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384": "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256": "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_CCM_SHA256": "TLS_AES_128_CCM_SHA256",
    },
}
"""Access dictionary by TLS version that translates from cipher suites IANI (key)
 to OpenSSL name (value)."""

DEPRECATED_TLS_CIPHERSUITES: Dict[str, Dict[str, str]] = {
    "TLSv1.2": {
        "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256": "DHE-RSA-AES128-GCM-SHA256",
        "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384": "DHE-RSA-AES256-GCM-SHA384",
        "TLS_DHE_RSA_WITH_AES_256_CCM": "DHE-RSA-AES256-CCM",
        "TLS_DHE_RSA_WITH_AES_128_CCM": "DHE-RSA-AES128-CCM",
        "TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256": "DHE-RSA-CHACHA20-POLY1305",
        "TLS_ECDHE_ECDSA_WITH_AES_256_CCM_8": "ECDHE-ECDSA-AES256-CCM8",
        "TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8": "ECDHE-ECDSA-AES128-CCM8",
        "TLS_DHE_RSA_WITH_AES_256_CCM_8": "DHE-RSA-AES256-CCM8",
        "TLS_DHE_RSA_WITH_AES_128_CCM_8": "DHE-RSA-AES128-CCM8",
        "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256": "ECDHE-ECDSA-AES128-SHA256",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256": "ECDHE-RSA-AES128-SHA256",
        "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384": "ECDHE-ECDSA-AES256-SHA384",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384": "ECDHE-RSA-AES256-SHA384",
        "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384": "DHE-DSS-AES256-GCM-SHA384",
        "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256": "DHE-DSS-AES128-GCM-SHA256",
        "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256": "DHE-DSS-AES128-SHA256",
        "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256": "DHE-DSS-AES256-SHA256",
        "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256": "DHE-RSA-AES256-SHA256",
        "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256": "DHE-RSA-AES128-SHA256",
        "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256": "DHE-RSA-CAMELLIA256-SHA256",
        "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256": "DHE-RSA-CAMELLIA128-SHA256",
        "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA": "ECDHE-RSA-AES128-SHA",
        "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA": "ECDHE-ECDSA-AES128-SHA",
        "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA": "ECDHE-RSA-AES256-SHA",
        "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA": "ECDHE-ECDSA-AES256-SHA",
        "TLS_DHE_DSS_WITH_AES_128_CBC_SHA": "DHE-DSS-AES128-SHA",
        "TLS_DHE_RSA_WITH_AES_128_CBC_SHA": "DHE-RSA-AES128-SHA",
        "TLS_DHE_RSA_WITH_AES_256_CBC_SHA": "DHE-RSA-AES256-SHA",
        "TLS_DHE_DSS_WITH_AES_256_CBC_SHA": "DHE-DSS-AES256-SHA",
        "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA": "DHE-RSA-CAMELLIA256-SHA",
        "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA": "DHE-RSA-CAMELLIA128-SHA",
        "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256": "ECDH-ECDSA-AES128-SHA256",
        "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256": "ECDH-RSA-AES128-SHA256",
        "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384": "ECDH-RSA-AES256-SHA384",
        "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384": "ECDH-ECDSA-AES256-SHA384",
        "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA": "ECDH-ECDSA-AES128-SHA",
        "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA": "ECDH-ECDSA-AES256-SHA",
        "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA": "ECDH-RSA-AES128-SHA",
        "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA": "ECDH-RSA-AES256-SHA",
        "TLS_RSA_WITH_AES_128_GCM_SHA256": "AES128-GCM-SHA256",
        "TLS_RSA_WITH_AES_128_CCM": "AES128-CCM",
        "TLS_RSA_WITH_AES_128_CCM_8": "AES128-CCM8",
        "TLS_RSA_WITH_AES_256_GCM_SHA384": "AES256-GCM-SHA384",
        "TLS_RSA_WITH_AES_256_CCM": "AES256-CCM",
        "TLS_RSA_WITH_AES_256_CCM_8": "AES256-CCM8",
        "TLS_RSA_WITH_AES_128_CBC_SHA256": "AES128-SHA256",
        "TLS_RSA_WITH_AES_256_CBC_SHA256": "AES256-SHA256",
        "TLS_RSA_WITH_AES_128_CBC_SHA": "AES128-SHA",
        "TLS_RSA_WITH_AES_256_CBC_SHA": "AES256-SHA",
        "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA": "CAMELLIA256-SHA",
        "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA": "CAMELLIA128-SHA",
        "TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256": "ECDH-ECDSA-AES128-GCM-SHA256",
        "TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384": "ECDH-ECDSA-AES256-GCM-SHA384",
        "TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256": "ECDH-RSA-AES128-GCM-SHA256",
        "TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384": "ECDH-RSA-AES256-GCM-SHA384",
    },
    "TLSv1.3": {"TLS_AES_128_CCM_8_SHA256": "TLS_AES_128_CCM_8_SHA256"},
}
"""Access dictionary by TLS version that translates from cipher suites IANI (key)
 to OpenSSL name (value)."""

UNACCEPTABLE_TLS_CIPHERSUITES: Dict[str, Dict[str, str]] = {
    "TLSv1.2": {
        "TLS_DH_RSA_WITH_AES_128_CBC_SHA256": "DH-RSA-AES128-SHA256",
        "TLS_DH_RSA_WITH_AES_256_CBC_SHA256": "DH-RSA-AES256-SHA256",
        "TLS_DH_DSS_WITH_AES_128_CBC_SHA256": "DH-DSS-AES128-SHA256",
        "TLS_DH_DSS_WITH_AES_128_CBC_SHA": "DH-DSS-AES128-SHA",
        "TLS_DH_DSS_WITH_AES_256_CBC_SHA": "DH-DSS-AES256-SHA",
        "TLS_DH_DSS_WITH_AES_256_CBC_SHA256": "DH-DSS-AES256-SHA256",
        "TLS_DH_RSA_WITH_AES_128_CBC_SHA": "DH-RSA-AES128-SHA",
        "TLS_DH_RSA_WITH_AES_256_CBC_SHA": "DH-RSA-AES256-SHA",
        "TLS_DH_DSS_WITH_AES_128_GCM_SHA256": "DH-DSS-AES128-GCM-SHA256",
        "TLS_DH_DSS_WITH_AES_256_GCM_SHA384": "DH-DSS-AES256-GCM-SHA384",
        "TLS_DH_RSA_WITH_AES_128_GCM_SHA256": "DH-RSA-AES128-GCM-SHA256",
        "TLS_DH_RSA_WITH_AES_256_GCM_SHA384": "DH-RSA-AES256-GCM-SHA384",
        "TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA": "DH-DSS-DES-CBC3-SHA",
        "TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA": "DH-RSA-DES-CBC3-SHA",
        "TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA": "EDH-DSS-DES-CBC3-SHA",
        "TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA": "EDH-RSA-DES-CBC3-SHA",
        "TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA": "ECDH-RSA-DES-CBC3-SHA",
        "TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA": "ECDH-ECDSA-DES-CBC3-SHA",
        "TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA": "ECDHE-RSA-DES-CBC3-SHA",
        "TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA": "ECDHE-ECDSA-DES-CBC3-SHA",
        "TLS_RSA_WITH_3DES_EDE_CBC_SHA": "DES-CBC3-SHA",
        "TLS_KRB5_WITH_3DES_EDE_CBC_SHA": "KRB5-DES-CBC3-SHA",
        "TLS_KRB5_WITH_3DES_EDE_CBC_MD5": "KRB5-DES-CBC3-MD5",
        "TLS_KRB5_WITH_IDEA_CBC_SHA": "KRB5-IDEA-CBC-SHA",
    },
    "TLSv1.3": {},
}
"""Access dictionary by TLS version that translates from cipher suites IANI (key)
 to OpenSSL name (value)."""
