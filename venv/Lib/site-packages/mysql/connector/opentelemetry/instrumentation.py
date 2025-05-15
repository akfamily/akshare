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

"""MySQL instrumentation supporting mysql-connector."""
# mypy: disable-error-code="no-redef"
# pylint: disable=protected-access,global-statement,invalid-name,unused-argument

from __future__ import annotations

import functools
import re

from abc import ABC, abstractmethod
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any, Callable, Collection, Dict, Optional, Union

# pylint: disable=cyclic-import
if TYPE_CHECKING:
    # `TYPE_CHECKING` is always False at run time, hence circular import
    # will not happen at run time (no error happens whatsoever).
    # Since pylint is a static checker it happens that `TYPE_CHECKING`
    # is True when analyzing the code which makes pylint believe there
    # is a circular import issue when there isn't.

    from ..abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
    from ..pooling import PooledMySQLConnection

from ... import connector
from ..constants import CNX_POOL_ARGS, DEFAULT_CONFIGURATION
from ..logger import logger
from ..version import VERSION_TEXT

try:
    # pylint: disable=unused-import
    # try to load otel from the system
    from opentelemetry import trace  # check api
    from opentelemetry.sdk.trace import TracerProvider  # check sdk
    from opentelemetry.semconv.trace import SpanAttributes  # check semconv
except ImportError as missing_dependencies_err:
    raise connector.errors.ProgrammingError(
        "OpenTelemetry installation not found. You must install the API and SDK."
    ) from missing_dependencies_err


from .constants import (
    CONNECTION_SPAN_NAME,
    DB_SYSTEM,
    DEFAULT_THREAD_ID,
    DEFAULT_THREAD_NAME,
    FIRST_SUPPORTED_VERSION,
    NET_SOCK_FAMILY,
    NET_SOCK_HOST_ADDR,
    NET_SOCK_HOST_PORT,
    NET_SOCK_PEER_ADDR,
    NET_SOCK_PEER_PORT,
    OPTION_CNX_SPAN,
    OPTION_CNX_TRACER,
)

leading_comment_remover: re.Pattern = re.compile(r"^/\*.*?\*/")


def record_exception_event(span: trace.Span, exc: Optional[Exception]) -> None:
    """Records an exeception event."""
    if not span or not span.is_recording() or not exc:
        return

    span.set_status(trace.Status(trace.StatusCode.ERROR))
    span.record_exception(exc)


def end_span(span: trace.Span) -> None:
    """Ends span."""
    if not span or not span.is_recording():
        return

    span.end()


def get_operation_name(operation: str) -> str:
    """Parse query to extract operation name."""
    if operation and isinstance(operation, str):
        # Strip leading comments so we get the operation name.
        return leading_comment_remover.sub("", operation).split()[0]
    return ""


def set_connection_span_attrs(
    cnx: Optional["MySQLConnectionAbstract"],
    cnx_span: trace.Span,
    cnx_kwargs: Optional[Dict[str, Any]] = None,
) -> None:
    """Defines connection span attributes. If `cnx` is None then we use `cnx_kwargs`
    to get basic net information. Basic net attributes are defined such as:

    * DB_SYSTEM
    * NET_TRANSPORT
    * NET_SOCK_FAMILY

    Socket-level attributes [*] are also defined [**].

    [*]: Socket-level attributes identify peer and host that are directly connected to
    each other. Since instrumentations may have limited knowledge on network
    information, instrumentations SHOULD populate such attributes to the best of
    their knowledge when populate them at all.

    [**]: `CMySQLConnection` connections have no access to socket-level
    details so socket-level attributes aren't included. `MySQLConnection`
    connections, on the other hand, do include socket-level attributes.

    References:
        [1]: https://github.com/open-telemetry/opentelemetry-specification/blob/main/\
            specification/trace/semantic_conventions/span-general.md
    """
    # pylint: disable=broad-exception-caught
    if not cnx_span or not cnx_span.is_recording():
        return

    if cnx_kwargs is None:
        cnx_kwargs = {}

    is_tcp = not cnx._unix_socket if cnx else "unix_socket" not in cnx_kwargs

    attrs: Dict[str, Any] = {
        SpanAttributes.DB_SYSTEM: DB_SYSTEM,
        SpanAttributes.NET_TRANSPORT: "ip_tcp" if is_tcp else "inproc",
        NET_SOCK_FAMILY: "inet" if is_tcp else "unix",
    }

    # Only socket and tcp connections are supported.
    if is_tcp:
        attrs[SpanAttributes.NET_PEER_NAME] = (
            cnx._host if cnx else cnx_kwargs.get("host", DEFAULT_CONFIGURATION["host"])
        )
        attrs[SpanAttributes.NET_PEER_PORT] = (
            cnx._port if cnx else cnx_kwargs.get("port", DEFAULT_CONFIGURATION["port"])
        )

        if hasattr(cnx, "_socket") and cnx._socket:
            try:
                (
                    attrs[NET_SOCK_PEER_ADDR],
                    sock_peer_port,
                ) = cnx._socket.sock.getpeername()

                (
                    attrs[NET_SOCK_HOST_ADDR],
                    attrs[NET_SOCK_HOST_PORT],
                ) = cnx._socket.sock.getsockname()
            except Exception as sock_err:
                logger.warning("Connection socket is down %s", sock_err)
            else:
                if attrs[SpanAttributes.NET_PEER_PORT] != sock_peer_port:
                    # NET_SOCK_PEER_PORT is recommended if different than net.peer.port
                    # and if net.sock.peer.addr is set.
                    attrs[NET_SOCK_PEER_PORT] = sock_peer_port
    else:
        # For Unix domain socket, net.sock.peer.addr attribute represents
        # destination name and net.peer.name SHOULD NOT be set.
        attrs[NET_SOCK_PEER_ADDR] = (
            cnx._unix_socket if cnx else cnx_kwargs.get("unix_socket")
        )

        if hasattr(cnx, "_socket") and cnx._socket:
            try:
                attrs[NET_SOCK_HOST_ADDR] = cnx._socket.sock.getsockname()
            except Exception as sock_err:
                logger.warning("Connection socket is down %s", sock_err)

    cnx_span.set_attributes(attrs)


def with_cnx_span_attached(method: Callable) -> Callable:
    """Attach the connection span while executing the connection method."""

    def wrapper(cnx: "MySQLConnectionAbstract", *args: Any, **kwargs: Any) -> Any:
        """Connection span attacher decorator."""
        with trace.use_span(
            cnx._span, end_on_exit=False
        ) if cnx._span and cnx._span.is_recording() else nullcontext():
            return method(cnx, *args, **kwargs)

    return wrapper


def with_cnx_query_span(method: Callable) -> Callable:
    """Create a query span while executing the connection method."""

    def wrapper(cnx: TracedMySQLConnection, *args: Any, **kwargs: Any) -> Any:
        """Query span creator decorator."""
        logger.info("Creating query span for connection.%s", method.__name__)

        query_span_attributes: Dict = {
            SpanAttributes.DB_SYSTEM: DB_SYSTEM,
            SpanAttributes.DB_USER: cnx._user,
            SpanAttributes.THREAD_ID: DEFAULT_THREAD_ID,
            SpanAttributes.THREAD_NAME: DEFAULT_THREAD_NAME,
            "connection_type": cnx.get_wrapped_class(),
        }

        with cnx._tracer.start_as_current_span(
            name=method.__name__.upper(),
            kind=trace.SpanKind.CLIENT,
            links=[trace.Link(cnx._span.get_span_context())],
            attributes=query_span_attributes,
        ) if cnx._span and cnx._span.is_recording() else nullcontext():
            return method(cnx, *args, **kwargs)

    return wrapper


def with_cursor_query_span(method: Callable) -> Callable:
    """Create a query span while executing the cursor method."""

    def wrapper(cur: TracedMySQLCursor, *args: Any, **kwargs: Any) -> Any:
        """Query span creator decorator."""
        logger.info("Creating query span for cursor.%s", method.__name__)

        connection: "MySQLConnectionAbstract" = (
            getattr(cur._wrapped, "_connection")
            if hasattr(cur._wrapped, "_connection")
            else getattr(cur._wrapped, "_cnx")
        )

        query_span_attributes: Dict = {
            SpanAttributes.DB_SYSTEM: DB_SYSTEM,
            SpanAttributes.DB_USER: connection._user,
            SpanAttributes.THREAD_ID: DEFAULT_THREAD_ID,
            SpanAttributes.THREAD_NAME: DEFAULT_THREAD_NAME,
            "cursor_type": cur.get_wrapped_class(),
        }

        with cur._tracer.start_as_current_span(
            name=get_operation_name(args[0]) or "SQL statement",
            kind=trace.SpanKind.CLIENT,
            links=[cur._connection_span_link],
            attributes=query_span_attributes,
        ):
            return method(cur, *args, **kwargs)

    return wrapper


class BaseMySQLTracer(ABC):
    """Base class that provides basic object wrapper functionality."""

    @abstractmethod
    def __init__(self) -> None:
        """Must be implemented by subclasses."""

    def __getattr__(self, attr: str) -> Any:
        """Gets an attribute.

        Attributes defined in the wrapper object have higher precedence
        than those wrapped object equivalent. Attributes not found in
        the wrapper are then searched in the wrapped object.
        """
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._wrapped, attr)

    def __setattr__(self, name: str, value: Any) -> None:
        if "_wrapped" not in self.__dict__:
            self.__dict__["_wrapped"] = value
            return

        if name in self.__dict__ or name == "autocommit":
            # this object has it
            super().__setattr__(name, value)
            return
        # proxy to the wrapped object
        self._wrapped.__setattr__(name, value)

    def __enter__(self) -> Any:
        """Magic method."""
        self._wrapped.__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Magic method."""
        self._wrapped.__exit__(*args, **kwargs)

    def get_wrapped_class(self) -> str:
        """Gets the wrapped class name."""
        return self._wrapped.__class__.__name__


class TracedMySQLCursor(BaseMySQLTracer):
    """Wrapper class for a `MySQLCursor` or `CMySQLCursor` object."""

    def __init__(
        self,
        wrapped: "MySQLCursorAbstract",
        tracer: trace.Tracer,
        connection_span: trace.Span,
    ):
        """Constructor."""
        self._wrapped: "MySQLCursorAbstract" = wrapped
        self._tracer: trace.Tracer = tracer
        self._connection_span_link: trace.Link = trace.Link(
            connection_span.get_span_context()
        )

    @with_cursor_query_span
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.execute(*args, **kwargs)

    @with_cursor_query_span
    def executemany(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.executemany(*args, **kwargs)

    @with_cursor_query_span
    def callproc(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.callproc(*args, **kwargs)


class TracedMySQLConnection(BaseMySQLTracer):
    """Wrapper class for a `MySQLConnection` or `CMySQLConnection` object."""

    def __init__(self, wrapped: "MySQLConnectionAbstract") -> None:
        """Constructor."""
        self._wrapped: "MySQLConnectionAbstract" = wrapped

        # call `sql_mode` so its value is cached internally and querying it does not
        # interfere when recording query span events later.
        _ = self._wrapped.sql_mode

    def cursor(self, *args: Any, **kwargs: Any) -> TracedMySQLCursor:
        """Wraps the object method."""
        return TracedMySQLCursor(
            wrapped=self._wrapped.cursor(*args, **kwargs),
            tracer=self._tracer,
            connection_span=self._span,
        )

    @with_cnx_query_span
    def cmd_change_user(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_change_user(*args, **kwargs)

    @with_cnx_query_span
    def commit(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.commit(*args, **kwargs)

    @with_cnx_query_span
    def rollback(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.rollback(*args, **kwargs)

    @with_cnx_query_span
    def cmd_query(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_query(*args, **kwargs)

    @with_cnx_query_span
    def cmd_init_db(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_init_db(*args, **kwargs)

    @with_cnx_query_span
    def cmd_refresh(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_refresh(*args, **kwargs)

    @with_cnx_query_span
    def cmd_quit(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_quit(*args, **kwargs)

    @with_cnx_query_span
    def cmd_shutdown(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_shutdown(*args, **kwargs)

    @with_cnx_query_span
    def cmd_statistics(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_statistics(*args, **kwargs)

    @with_cnx_query_span
    def cmd_process_kill(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_process_kill(*args, **kwargs)

    @with_cnx_query_span
    def cmd_debug(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_debug(*args, **kwargs)

    @with_cnx_query_span
    def cmd_ping(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_ping(*args, **kwargs)

    @property
    @with_cnx_query_span
    def database(self) -> str:
        """Instrument method."""
        return self._wrapped.database

    @with_cnx_query_span
    def is_connected(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.is_connected(*args, **kwargs)

    @with_cnx_query_span
    def reset_session(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.reset_session(*args, **kwargs)

    @with_cnx_query_span
    def ping(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.ping(*args, **kwargs)

    @with_cnx_query_span
    def info_query(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.info_query(*args, **kwargs)

    @with_cnx_query_span
    def cmd_stmt_prepare(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_stmt_prepare(*args, **kwargs)

    @with_cnx_query_span
    def cmd_stmt_execute(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_stmt_execute(*args, **kwargs)

    @with_cnx_query_span
    def cmd_stmt_close(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_stmt_close(*args, **kwargs)

    @with_cnx_query_span
    def cmd_stmt_send_long_data(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_stmt_send_long_data(*args, **kwargs)

    @with_cnx_query_span
    def cmd_stmt_reset(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_stmt_reset(*args, **kwargs)

    @with_cnx_query_span
    def cmd_reset_connection(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.cmd_reset_connection(*args, **kwargs)

    @property
    @with_cnx_query_span
    def time_zone(self) -> str:
        """Instrument method."""
        return self._wrapped.time_zone

    @property
    @with_cnx_query_span
    def sql_mode(self) -> str:
        """Instrument method."""
        return self._wrapped.sql_mode

    @property
    @with_cnx_query_span
    def autocommit(self) -> bool:
        """Instrument method."""
        return self._wrapped.autocommit

    @autocommit.setter
    @with_cnx_query_span
    def autocommit(self, value: bool) -> None:
        """Instrument method."""
        self._wrapped.autocommit = value

    @with_cnx_query_span
    def set_charset_collation(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.set_charset_collation(*args, **kwargs)

    @with_cnx_query_span
    def start_transaction(self, *args: Any, **kwargs: Any) -> Any:
        """Instrument method."""
        return self._wrapped.start_transaction(*args, **kwargs)


def _instrument_connect(
    connect: Callable[..., Union["MySQLConnectionAbstract", "PooledMySQLConnection"]],
    tracer_provider: Optional[trace.TracerProvider] = None,
) -> Callable[..., Union["MySQLConnectionAbstract", "PooledMySQLConnection"]]:
    """Retrurn the instrumented version of `connect`."""

    # let's preserve `connect` identity.
    @functools.wraps(connect)
    def wrapper(
        *args: Any, **kwargs: Any
    ) -> Union["MySQLConnectionAbstract", "PooledMySQLConnection"]:
        """Wraps the connection object returned by the method `connect`.

        Instrumentation for PooledConnections is not supported.
        """
        if any(key in kwargs for key in CNX_POOL_ARGS):
            logger.warning("Instrumentation for pooled connections not supported")
            return connect(*args, **kwargs)

        tracer = trace.get_tracer(
            instrumenting_module_name="MySQL Connector/Python",
            instrumenting_library_version=VERSION_TEXT,
            tracer_provider=tracer_provider,
        )

        # The connection span is passed in as an argument so the connection object can
        # keep a pointer to it.
        kwargs[OPTION_CNX_SPAN] = tracer.start_span(
            name=CONNECTION_SPAN_NAME, kind=trace.SpanKind.CLIENT
        )
        kwargs[OPTION_CNX_TRACER] = tracer

        # attach connection span
        with trace.use_span(kwargs[OPTION_CNX_SPAN], end_on_exit=False) as cnx_span:
            # Add basic net information.
            set_connection_span_attrs(None, cnx_span, kwargs)

            # Connection may fail at this point, in case it does, basic net info is already
            # included so the user can check the net configuration she/he provided.
            cnx = connect(*args, **kwargs)

            # connection went ok, let's refine the net information.
            set_connection_span_attrs(cnx, cnx_span, kwargs)  # type: ignore[arg-type]

            return TracedMySQLConnection(
                wrapped=cnx,  # type: ignore[return-value, arg-type]
            )

    return wrapper


class MySQLInstrumentor:
    """MySQL instrumentation supporting mysql-connector-python."""

    _instance: Optional[MySQLInstrumentor] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> MySQLInstrumentor:
        """Singlenton.

        Restricts the instantiation to a singular instance.
        """
        if cls._instance is None:
            # create instance
            cls._instance = object.__new__(cls, *args, **kwargs)
            # keep a pointer to the uninstrumented connect method
            setattr(cls._instance, "_original_connect", connector.connect)
        return cls._instance

    def instrumentation_dependencies(self) -> Collection[str]:
        """Return a list of python packages with versions
        that the will be instrumented (e.g., versions >= 8.1.0)."""
        return [f"mysql-connector-python >= {FIRST_SUPPORTED_VERSION}"]

    def instrument(self, **kwargs: Any) -> None:
        """Instrument the library.

        Args:
            trace_module: reference to the 'trace' module from opentelemetry.
            tracer_provider (optional): TracerProvider instance.

        NOTE: Instrumentation for pooled connections not supported.
        """
        if connector.connect != getattr(self, "_original_connect"):
            logger.warning("MySQL Connector/Python module already instrumented.")
            return
        connector.connect = _instrument_connect(
            connect=getattr(self, "_original_connect"),
            tracer_provider=kwargs.get("tracer_provider"),
        )

    def instrument_connection(
        self,
        connection: "MySQLConnectionAbstract",
        tracer_provider: Optional[trace.TracerProvider] = None,
    ) -> "MySQLConnectionAbstract":
        """Enable instrumentation in a MySQL connection.

        Args:
            connection: uninstrumented connection instance.
            trace_module: reference to the 'trace' module from opentelemetry.
            tracer_provider (optional): TracerProvider instance.

        Returns:
            connection: instrumented connection instace.

        NOTE: Instrumentation for pooled connections not supported.
        """
        if isinstance(connection, TracedMySQLConnection):
            logger.warning("Connection already instrumented.")
            return connection

        if not hasattr(connection, "_span") or not hasattr(connection, "_tracer"):
            logger.warning(
                "Instrumentation for class %s not supported.",
                connection.__class__.__name__,
            )
            return connection

        tracer = trace.get_tracer(
            instrumenting_module_name="MySQL Connector/Python",
            instrumenting_library_version=VERSION_TEXT,
            tracer_provider=tracer_provider,
        )
        connection._span = tracer.start_span(
            name=CONNECTION_SPAN_NAME, kind=trace.SpanKind.CLIENT
        )
        connection._tracer = tracer

        set_connection_span_attrs(connection, connection._span)

        return TracedMySQLConnection(wrapped=connection)  # type: ignore[return-value]

    def uninstrument(self, **kwargs: Any) -> None:
        """Uninstrument the library."""
        # pylint: disable=unused-argument
        if connector.connect == getattr(self, "_original_connect"):
            logger.warning("MySQL Connector/Python module already uninstrumented.")
            return
        connector.connect = getattr(self, "_original_connect")

    def uninstrument_connection(
        self, connection: "MySQLConnectionAbstract"
    ) -> "MySQLConnectionAbstract":
        """Disable instrumentation in a MySQL connection.

        Args:
            connection: instrumented connection instance.

        Returns:
            connection: uninstrumented connection instace.

        NOTE: Instrumentation for pooled connections not supported.
        """
        if not hasattr(connection, "_span"):
            logger.warning(
                "Uninstrumentation for class %s not supported.",
                connection.__class__.__name__,
            )
            return connection

        if not isinstance(connection, TracedMySQLConnection):
            logger.warning("Connection already uninstrumented.")
            return connection

        # stop connection span recording
        if connection._span and connection._span.is_recording():
            connection._span.end()
            connection._span = None

        return connection._wrapped
