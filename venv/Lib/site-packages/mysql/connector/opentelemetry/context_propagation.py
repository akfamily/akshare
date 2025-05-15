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

"""Trace context propagation utilities."""
# mypy: disable-error-code="no-redef"
# pylint: disable=invalid-name

from typing import TYPE_CHECKING, Any, Callable

from .constants import OTEL_ENABLED, TRACEPARENT_HEADER_NAME

if OTEL_ENABLED:
    # pylint: disable=import-error
    # load otel from the system
    from opentelemetry import trace
    from opentelemetry.trace.span import format_span_id, format_trace_id


if TYPE_CHECKING:
    from ..abstracts import MySQLConnectionAbstract


def build_traceparent_header(span: Any) -> str:
    """Build a traceparent header according to the provided span.

    The context information from the provided span is used to build the traceparent
    header that will be propagated to the MySQL server. For particulars regarding
    the header creation, refer to [1].

    This method assumes version 0 of the W3C specification.

    Args:
        span (opentelemetry.trace.span.Span): current span in trace.

    Returns:
        traceparent_header (str): HTTP header field that identifies requests in a
        tracing system.

    References:
        [1]: https://www.w3.org/TR/trace-context/#traceparent-header
    """
    # pylint: disable=possibly-used-before-assignment
    ctx = span.get_span_context()

    version = "00"  # version 0 of the W3C specification
    trace_id = format_trace_id(ctx.trace_id)
    span_id = format_span_id(ctx.span_id)
    trace_flags = "00"  # sampled flag is off

    return "-".join([version, trace_id, span_id, trace_flags])


def with_context_propagation(method: Callable) -> Callable:
    """Perform trace context propagation.

    The trace context is propagated via query attributes. The `traceparent` header
    from W3C specification [1] is used, in this sense, the attribute name is
    `traceparent` (is RESERVED, avoid using it), and its value is built as per
    instructed in [1].

    If opentelemetry API/SDK is unavailable or there is no recording span,
    trace context propagation is skipped.

    References:
        [1]: https://www.w3.org/TR/trace-context/#traceparent-header
    """

    def wrapper(cnx: "MySQLConnectionAbstract", *args: Any, **kwargs: Any) -> Any:
        """Context propagation decorator."""
        # pylint: disable=possibly-used-before-assignment
        if not OTEL_ENABLED or not cnx.otel_context_propagation:
            return method(cnx, *args, **kwargs)

        current_span = trace.get_current_span()
        tp_header = None
        if current_span.is_recording():
            tp_header = build_traceparent_header(current_span)
            cnx.query_attrs_append(value=(TRACEPARENT_HEADER_NAME, tp_header))

        try:
            result = method(cnx, *args, **kwargs)
        finally:
            if tp_header is not None:
                cnx.query_attrs_remove(name=TRACEPARENT_HEADER_NAME)
        return result

    return wrapper
