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

"""
This module implements some constructors and singletons as required by the
DB API v2.0 (PEP-249).
"""

# Python Db API v2
# pylint: disable=invalid-name
apilevel: str = "2.0"
"""This attribute is a string that indicates the supported DB API level."""

threadsafety: int = 1
"""This attribute is an integer that indicates the supported level of thread safety
provided by Connector/Python."""

paramstyle: str = "pyformat"
"""This attribute is a string that indicates the Connector/Python default
parameter style."""

import datetime
import time

from typing import Tuple

from . import constants


class _DBAPITypeObject:
    def __init__(self, *values: int) -> None:
        self.values: Tuple[int, ...] = values

    def __eq__(self, other: object) -> bool:
        return other in self.values

    def __ne__(self, other: object) -> bool:
        return other not in self.values


Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime


def DateFromTicks(ticks: int) -> datetime.date:
    """Construct an object holding a date value from the given ticks value."""
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks: int) -> datetime.time:
    """Construct an object holding a time value from the given ticks value."""
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks: int) -> datetime.datetime:
    """Construct an object holding a time stamp from the given ticks value."""
    return Timestamp(*time.localtime(ticks)[:6])


Binary = bytes

STRING = _DBAPITypeObject(*constants.FieldType.get_string_types())
BINARY = _DBAPITypeObject(*constants.FieldType.get_binary_types())
NUMBER = _DBAPITypeObject(*constants.FieldType.get_number_types())
DATETIME = _DBAPITypeObject(*constants.FieldType.get_timestamp_types())
ROWID = _DBAPITypeObject()
