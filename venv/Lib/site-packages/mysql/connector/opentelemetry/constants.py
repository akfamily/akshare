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

"""Constants used by the opentelemetry instrumentation implementation."""
# mypy: disable-error-code="no-redef,assignment"

# pylint: disable=unused-import
OTEL_ENABLED = True
try:
    # try to load otel from the system
    from opentelemetry import trace  # check api
    from opentelemetry.sdk.trace import TracerProvider  # check sdk
    from opentelemetry.semconv.trace import SpanAttributes  # check semconv
except ImportError:
    OTEL_ENABLED = False


OPTION_CNX_SPAN = "_span"
"""
Connection option name used to inject the connection span.
This connection option name must not be used, is reserved.
"""

OPTION_CNX_TRACER = "_tracer"
"""
Connection option name used to inject the opentelemetry tracer.
This connection option name must not be used, is reserved.
"""

CONNECTION_SPAN_NAME = "connection"
"""
Connection span name to be used by the instrumentor.
"""

FIRST_SUPPORTED_VERSION = "8.1.0"
"""
First mysql-connector-python version to support opentelemetry instrumentation.
"""

TRACEPARENT_HEADER_NAME = "traceparent"

DB_SYSTEM = "mysql"
DEFAULT_THREAD_NAME = "main"
DEFAULT_THREAD_ID = 0

# Reference: https://github.com/open-telemetry/opentelemetry-specification/blob/main/
# specification/trace/semantic_conventions/span-general.md
NET_SOCK_FAMILY = "net.sock.family"
NET_SOCK_PEER_ADDR = "net.sock.peer.addr"
NET_SOCK_PEER_PORT = "net.sock.peer.port"
NET_SOCK_HOST_ADDR = "net.sock.host.addr"
NET_SOCK_HOST_PORT = "net.sock.host.port"
