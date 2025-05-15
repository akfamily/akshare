# Copyright (c) 2009, 2024, Oracle and/or its affiliates.
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

"""MySQL Connector/Python - MySQL driver written in Python."""

try:
    from .connection_cext import CMySQLConnection
except ImportError:
    HAVE_CEXT = False
else:
    HAVE_CEXT = True


from . import version
from .connection import MySQLConnection
from .constants import CharacterSet, ClientFlag, FieldFlag, FieldType, RefreshOption
from .dbapi import (
    BINARY,
    DATETIME,
    NUMBER,
    ROWID,
    STRING,
    Binary,
    Date,
    DateFromTicks,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
    apilevel,
    paramstyle,
    threadsafety,
)
from .errors import (  # pylint: disable=redefined-builtin
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    PoolError,
    ProgrammingError,
    Warning,
    custom_error_exception,
)
from .pooling import connect

Connect = connect

__version_info__ = version.VERSION
"""This attribute indicates the Connector/Python version as an array
of version components."""

__version__ = version.VERSION_TEXT
"""This attribute indicates the Connector/Python version as a string."""

__all__ = [
    "MySQLConnection",
    "Connect",
    "custom_error_exception",
    # Some useful constants
    "FieldType",
    "FieldFlag",
    "ClientFlag",
    "CharacterSet",
    "RefreshOption",
    "HAVE_CEXT",
    # Error handling
    "Error",
    "Warning",
    "InterfaceError",
    "DatabaseError",
    "NotSupportedError",
    "DataError",
    "IntegrityError",
    "PoolError",
    "ProgrammingError",
    "OperationalError",
    "InternalError",
    # DBAPI PEP 249 required exports
    "connect",
    "apilevel",
    "threadsafety",
    "paramstyle",
    "Date",
    "Time",
    "Timestamp",
    "Binary",
    "DateFromTicks",
    "DateFromTicks",
    "TimestampFromTicks",
    "TimeFromTicks",
    "STRING",
    "BINARY",
    "NUMBER",
    "DATETIME",
    "ROWID",
    # C Extension
    "CMySQLConnection",
]
