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

"""
Type hint aliases hub.
"""
import os

from datetime import date, datetime, time, timedelta
from decimal import Decimal
from time import struct_time
from typing import (
    TYPE_CHECKING,
    Any,
    Deque,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypedDict,
    Union,
)

if TYPE_CHECKING:
    from .custom_types import HexLiteral


class MySQLScriptPartition(TypedDict):
    """Represents a partition or sub-script."""

    mappable_stmt: bytes
    single_stmts: Deque[bytes]


StrOrBytes = Union[str, bytes]
"""Shortcut to for `String or Bytes`."""

StrOrBytesAny = Union[StrOrBytes, Any]
"""Shortcut to for `String or Bytes or Any`."""

StrOrBytesPath = Union[StrOrBytes, os.PathLike]
"""Shortcut to for `String or Bytes or os.PathLike` - this shortcut
may come in handy as a hint for path-like variables."""

PythonProducedType = Union[
    Decimal,
    bytes,
    date,
    datetime,
    float,
    int,
    Set[str],
    str,
    timedelta,
    None,
]
"""
Python producible types in converter - Types produced after processing a MySQL text
result using the built-in converter.
"""

BinaryProtocolType = Union[
    Decimal,
    bytes,
    date,
    datetime,
    float,
    int,
    str,
    time,
    timedelta,
    None,
]
"""
Supported MySQL Binary Protocol Types - Python type that can be
converted to a MySQL type. It's a subset of `MySQLConvertibleType`.
"""

# pylint: disable=invalid-name
MySQLConvertibleType = Union[BinaryProtocolType, bool, struct_time]
"""
MySQL convertible Python types - Python types consumed by the built-in converter that
can be converted to MySQL. It's a superset of `BinaryProtocolType`.
"""

MySQLProducedType = Optional[Union[int, float, bytes, "HexLiteral"]]
"""
Types produced after processing MySQL convertible Python types.
"""

HandShakeType = Dict[str, Optional[Union[int, str, bytes]]]
"""Dictionary representing the parsed `handshake response`
sent at `connection` time by the server."""

OkPacketType = Dict[str, Optional[Union[int, str]]]
"""Dictionary representing the parsed `OK response`
produced by the server to signal successful completion of a command."""

EofPacketType = OkPacketType
"""Dictionary representing the parsed `EOF response`
produced by the server to signal successful completion of a command.
In the MySQL client/server protocol, the EOF and OK responses serve
the same purpose, to mark the end of a query execution resul.
"""

DescriptionType = Tuple[
    str,  # field name
    int,  # field type
    None,  # you can ignore it or take a look at protocol.parse_column()
    None,
    None,
    None,
    Union[bool, int],  # null ok
    int,  # field flags
    int,  # MySQL charset ID
]
"""
Tuple representing column information.

Sometimes it can be represented as a 2-Tuple of the form:
`Tuple[str, int]` <-> field name, field type.

However, let's stick with the 9-Tuple format produced by the protocol module.
```
DescriptionType = Tuple[
    str,  # field name
    int,  # field type
    None,  # you can ignore it or take a look at protocol.parse_column()
    None,
    None,
    None,
    Union[bool, int],  # null ok
    int,  # field flags
    int,  # MySQL charset ID
]
```
"""

StatsPacketType = Dict[str, Union[int, Decimal]]
"""Dictionary representing the parsed `Stats response`
produced by the server after completing a `COM_STATISTICS` command."""

ResultType = Mapping[
    str, Optional[Union[int, str, EofPacketType, List[DescriptionType]]]
]
"""
Represents the returned type by `MySQLConnection._handle_result()`.

This method can return a dictionary of the form:
- columns -> column information
- EOF_response -> end-of-file response

Or, it can return an `OkPacketType`/`EofPacketType`.
"""

RowItemType = Union[PythonProducedType, BinaryProtocolType]
"""Item type found in `RowType`."""

RowType = Tuple[RowItemType, ...]
"""Row returned by the MySQL server after sending a query command."""

CextEofPacketType = Dict[str, int]
"""Similar to `EofPacketType` but for the C-EXT."""

CextResultType = Dict[str, Union[CextEofPacketType, List[DescriptionType]]]
"""Similar to `ResultType` but for the C-EXT.

Represents the returned type by `CMySQLConnection.fetch_eof_columns()`.

This method returns a dictionary of the form:
- columns -> column information
- EOF_response -> end-of-file response
"""

ParamsSequenceType = Sequence[MySQLConvertibleType]
"""Sequence type expected by `cursor.execute()`."""

ParamsDictType = Dict[str, MySQLConvertibleType]
"""Dictionary type expected by `cursor.execute()`."""

ParamsSequenceOrDictType = Union[ParamsDictType, ParamsSequenceType]
"""Shortcut for `ParamsSequenceType or ParamsDictType`."""

WarningType = Tuple[str, int, str]
"""Warning generated by the previously executed operation."""
