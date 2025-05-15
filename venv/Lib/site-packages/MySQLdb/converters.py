"""MySQLdb type conversion module

This module handles all the type conversions for MySQL. If the default
type conversions aren't what you need, you can make your own. The
dictionary conversions maps some kind of type to a conversion function
which returns the corresponding value:

Key: FIELD_TYPE.* (from MySQLdb.constants)

Conversion function:

    Arguments: string

    Returns: Python object

Key: Python type object (from types) or class

Conversion function:

    Arguments: Python object of indicated type or class AND
               conversion dictionary

    Returns: SQL literal value

    Notes: Most conversion functions can ignore the dictionary, but
           it is a required parameter. It is necessary for converting
           things like sequences and instances.

Don't modify conversions if you can avoid it. Instead, make copies
(with the copy() method), modify the copies, and then pass them to
MySQL.connect().
"""
from decimal import Decimal

from MySQLdb._mysql import string_literal
from MySQLdb.constants import FIELD_TYPE, FLAG
from MySQLdb.times import (
    Date,
    DateTimeType,
    DateTime2literal,
    DateTimeDeltaType,
    DateTimeDelta2literal,
    DateTime_or_None,
    TimeDelta_or_None,
    Date_or_None,
)
from MySQLdb._exceptions import ProgrammingError

import array

NoneType = type(None)

try:
    ArrayType = array.ArrayType
except AttributeError:
    ArrayType = array.array


def Bool2Str(s, d):
    return b"1" if s else b"0"


def Set2Str(s, d):
    # Only support ascii string.  Not tested.
    return string_literal(",".join(s))


def Thing2Str(s, d):
    """Convert something into a string via str()."""
    return str(s)


def Float2Str(o, d):
    s = repr(o)
    if s in ("inf", "-inf", "nan"):
        raise ProgrammingError("%s can not be used with MySQL" % s)
    if "e" not in s:
        s += "e0"
    return s


def None2NULL(o, d):
    """Convert None to NULL."""
    return b"NULL"


def Thing2Literal(o, d):
    """Convert something into a SQL string literal.  If using
    MySQL-3.23 or newer, string_literal() is a method of the
    _mysql.MYSQL object, and this function will be overridden with
    that method when the connection is created."""
    return string_literal(o)


def Decimal2Literal(o, d):
    return format(o, "f")


def array2Str(o, d):
    return Thing2Literal(o.tostring(), d)


# bytes or str regarding to BINARY_FLAG.
_bytes_or_str = ((FLAG.BINARY, bytes), (None, str))

conversions = {
    int: Thing2Str,
    float: Float2Str,
    NoneType: None2NULL,
    ArrayType: array2Str,
    bool: Bool2Str,
    Date: Thing2Literal,
    DateTimeType: DateTime2literal,
    DateTimeDeltaType: DateTimeDelta2literal,
    set: Set2Str,
    Decimal: Decimal2Literal,
    FIELD_TYPE.TINY: int,
    FIELD_TYPE.SHORT: int,
    FIELD_TYPE.LONG: int,
    FIELD_TYPE.FLOAT: float,
    FIELD_TYPE.DOUBLE: float,
    FIELD_TYPE.DECIMAL: Decimal,
    FIELD_TYPE.NEWDECIMAL: Decimal,
    FIELD_TYPE.LONGLONG: int,
    FIELD_TYPE.INT24: int,
    FIELD_TYPE.YEAR: int,
    FIELD_TYPE.TIMESTAMP: DateTime_or_None,
    FIELD_TYPE.DATETIME: DateTime_or_None,
    FIELD_TYPE.TIME: TimeDelta_or_None,
    FIELD_TYPE.DATE: Date_or_None,
    FIELD_TYPE.TINY_BLOB: bytes,
    FIELD_TYPE.MEDIUM_BLOB: bytes,
    FIELD_TYPE.LONG_BLOB: bytes,
    FIELD_TYPE.BLOB: bytes,
    FIELD_TYPE.STRING: bytes,
    FIELD_TYPE.VAR_STRING: bytes,
    FIELD_TYPE.VARCHAR: bytes,
    FIELD_TYPE.JSON: bytes,
}
