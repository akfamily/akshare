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

"""Python exceptions."""
from typing import Dict, Mapping, Optional, Tuple, Type, Union

from .locales import get_client_error
from .types import StrOrBytes
from .utils import read_bytes, read_int


class Error(Exception):
    """Exception that is base class for all other error exceptions.

    See [1] for more details.

    References:
        [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html
    """

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        values: Optional[Tuple[Union[int, str], ...]] = None,
        sqlstate: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.msg = msg
        self._full_msg = self.msg
        self.errno = errno or -1
        self.sqlstate = sqlstate

        if not self.msg and (2000 <= self.errno < 3000):
            self.msg = get_client_error(self.errno)
            if values is not None:
                try:
                    self.msg = self.msg % values
                except TypeError as err:
                    self.msg = f"{self.msg} (Warning: {err})"
        elif not self.msg:
            self._full_msg = self.msg = "Unknown error"

        if self.msg and self.errno != -1:
            fields = {"errno": self.errno, "msg": self.msg}
            if self.sqlstate:
                fmt = "{errno} ({state}): {msg}"
                fields["state"] = self.sqlstate
            else:
                fmt = "{errno}: {msg}"
            self._full_msg = fmt.format(**fields)

        self.args = (self.errno, self._full_msg, self.sqlstate)

    def __str__(self) -> str:
        return self._full_msg


class Warning(Exception):  # pylint: disable=redefined-builtin
    """Exception for important warnings"""


class InterfaceError(Error):
    """Exception for errors related to the interface"""


class DatabaseError(Error):
    """Exception for errors related to the database"""


class InternalError(DatabaseError):
    """Exception for errors internal database errors"""


class OperationalError(DatabaseError):
    """Exception for errors related to the database's operation"""


class ProgrammingError(DatabaseError):
    """Exception for errors programming errors"""


class IntegrityError(DatabaseError):
    """Exception for errors regarding relational integrity"""


class DataError(DatabaseError):
    """Exception for errors reporting problems with processed data"""


class NotSupportedError(DatabaseError):
    """Exception for errors when an unsupported database feature was used"""


class PoolError(Error):
    """Exception for errors relating to connection pooling"""


class ConnectionTimeoutError(Error):
    """
    Exception for errors related to the socket connection timing out while connecting with
    the server
    """


class ReadTimeoutError(Error):
    """Exception for errors relating to socket timing out while receiving data from the server"""

    DEFAULT_READ_TIMEOUT_ERROR_MSG: str = """
    The Read Operation timed out. As a consequence the current connection has been closed to avoid
    any unstable behaviour, consider using the reconnect() option and continue with the current
    session's workflow.
    """

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        values: Optional[Tuple[str, int]] = None,
        sqlstate: Optional[str] = None,
    ) -> None:
        super().__init__(self.DEFAULT_READ_TIMEOUT_ERROR_MSG, errno, values, sqlstate)


class WriteTimeoutError(Error):
    """Exception for errors relating to socket timing out while sending data to the server"""

    DEFAULT_WRITE_TIMEOUT_ERROR_MSG: str = """
    The Write Operation timed out. As a consequence the current connection has been closed to avoid
    any unstable behaviour, consider using the reconnect() option to continue with the current
    session's workflow.
    """

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        values: Optional[Tuple[str, int]] = None,
        sqlstate: Optional[str] = None,
    ) -> None:
        super().__init__(self.DEFAULT_WRITE_TIMEOUT_ERROR_MSG, errno, values, sqlstate)


ErrorClassTypes = Union[
    Type[Error],
    Type[InterfaceError],
    Type[DatabaseError],
    Type[InternalError],
    Type[OperationalError],
    Type[ProgrammingError],
    Type[IntegrityError],
    Type[DataError],
    Type[NotSupportedError],
    Type[PoolError],
    Type[ConnectionTimeoutError],
    Type[ReadTimeoutError],
    Type[WriteTimeoutError],
]
ErrorTypes = Union[
    Error,
    InterfaceError,
    DatabaseError,
    InternalError,
    OperationalError,
    ProgrammingError,
    IntegrityError,
    DataError,
    NotSupportedError,
    PoolError,
    Warning,
    ConnectionTimeoutError,
    ReadTimeoutError,
    WriteTimeoutError,
]
# _CUSTOM_ERROR_EXCEPTIONS holds custom exceptions and is used by the
# function custom_error_exception. _ERROR_EXCEPTIONS (at bottom of module)
# is similar, but hardcoded exceptions.
_CUSTOM_ERROR_EXCEPTIONS: Dict[int, ErrorClassTypes] = {}


def custom_error_exception(
    error: Optional[Union[int, Dict[int, Optional[ErrorClassTypes]]]] = None,
    exception: Optional[ErrorClassTypes] = None,
) -> Mapping[int, Optional[ErrorClassTypes]]:
    """Defines custom exceptions for MySQL server errors.

    This function defines custom exceptions for MySQL server errors and
    returns the current set customizations.

    To reset the customizations, simply supply an empty dictionary.

    Args:
        error: Can be a MySQL Server error number or a dictionary in which case the
               key is the server error number and the value is the exception to be raised.
        exception: If `error` is a MySQL Server error number then you have to pass
                   also the exception class, otherwise you don't.

    Returns:
        dictionary: Current set customizations.

    Examples:
        ```
        import mysql.connector
        from mysql.connector import errorcode

        # Server error 1028 should raise a DatabaseError
        mysql.connector.custom_error_exception(
            1028, mysql.connector.DatabaseError)

        # Or using a dictionary:
        mysql.connector.custom_error_exception({
            1028: mysql.connector.DatabaseError,
            1029: mysql.connector.OperationalError,
            })

        # Reset
        mysql.connector.custom_error_exception({})
        ```
    """
    global _CUSTOM_ERROR_EXCEPTIONS  # pylint: disable=global-statement

    if isinstance(error, dict) and not error:
        _CUSTOM_ERROR_EXCEPTIONS = {}
        return _CUSTOM_ERROR_EXCEPTIONS

    if not error and not exception:
        return _CUSTOM_ERROR_EXCEPTIONS

    if not isinstance(error, (int, dict)):
        raise ValueError("The error argument should be either an integer or dictionary")

    if isinstance(error, int):
        error = {error: exception}

    for errno, _exception in error.items():
        if not isinstance(errno, int):
            raise ValueError("Error number should be an integer")
        try:
            if _exception is None or not issubclass(_exception, Exception):
                raise TypeError
        except TypeError as err:
            raise ValueError("Exception should be subclass of Exception") from err
        _CUSTOM_ERROR_EXCEPTIONS[errno] = _exception

    return _CUSTOM_ERROR_EXCEPTIONS


def get_mysql_exception(
    errno: int,
    msg: Optional[str] = None,
    sqlstate: Optional[str] = None,
    warning: Optional[bool] = False,
) -> ErrorTypes:
    """Get the exception matching the MySQL error

    This function will return an exception based on the SQLState. The given
    message will be passed on in the returned exception.

    The exception returned can be customized using the
    mysql.connector.custom_error_exception() function.

    Returns an Exception
    """
    try:
        return _CUSTOM_ERROR_EXCEPTIONS[errno](msg=msg, errno=errno, sqlstate=sqlstate)
    except KeyError:
        # Error was not mapped to particular exception
        pass

    try:
        return _ERROR_EXCEPTIONS[errno](msg=msg, errno=errno, sqlstate=sqlstate)
    except KeyError:
        # Error was not mapped to particular exception
        pass

    if not sqlstate:
        if warning:
            return Warning(errno, msg)
        return DatabaseError(msg=msg, errno=errno)

    try:
        return _SQLSTATE_CLASS_EXCEPTION[sqlstate[0:2]](
            msg=msg, errno=errno, sqlstate=sqlstate
        )
    except KeyError:
        # Return default InterfaceError
        return DatabaseError(msg=msg, errno=errno, sqlstate=sqlstate)


def get_exception(packet: bytes) -> ErrorTypes:
    """Returns an exception object based on the MySQL error

    Returns an exception object based on the MySQL error in the given
    packet.

    Returns an Error-Object.
    """
    errno = errmsg = None

    try:
        if packet[4] != 255:
            raise ValueError("Packet is not an error packet")
    except IndexError as err:
        return InterfaceError(f"Failed getting Error information ({err})")

    sqlstate: Optional[StrOrBytes] = None
    try:
        packet = packet[5:]
        packet, errno = read_int(packet, 2)
        if packet[0] != 35:
            # Error without SQLState
            if isinstance(packet, (bytes, bytearray)):
                errmsg = packet.decode("utf8")
            else:
                errmsg = packet
        else:
            packet, sqlstate = read_bytes(packet[1:], 5)
            sqlstate = sqlstate.decode("utf8")
            errmsg = packet.decode("utf8")
    except (IndexError, UnicodeError) as err:
        return InterfaceError(f"Failed getting Error information ({err})")
    return get_mysql_exception(errno, errmsg, sqlstate)  # type: ignore[arg-type]


_SQLSTATE_CLASS_EXCEPTION: Dict[str, ErrorClassTypes] = {
    "02": DataError,  # no data
    "07": DatabaseError,  # dynamic SQL error
    "08": OperationalError,  # connection exception
    "0A": NotSupportedError,  # feature not supported
    "21": DataError,  # cardinality violation
    "22": DataError,  # data exception
    "23": IntegrityError,  # integrity constraint violation
    "24": ProgrammingError,  # invalid cursor state
    "25": ProgrammingError,  # invalid transaction state
    "26": ProgrammingError,  # invalid SQL statement name
    "27": ProgrammingError,  # triggered data change violation
    "28": ProgrammingError,  # invalid authorization specification
    "2A": ProgrammingError,  # direct SQL syntax error or access rule violation
    "2B": DatabaseError,  # dependent privilege descriptors still exist
    "2C": ProgrammingError,  # invalid character set name
    "2D": DatabaseError,  # invalid transaction termination
    "2E": DatabaseError,  # invalid connection name
    "33": DatabaseError,  # invalid SQL descriptor name
    "34": ProgrammingError,  # invalid cursor name
    "35": ProgrammingError,  # invalid condition number
    "37": ProgrammingError,  # dynamic SQL syntax error or access rule violation
    "3C": ProgrammingError,  # ambiguous cursor name
    "3D": ProgrammingError,  # invalid catalog name
    "3F": ProgrammingError,  # invalid schema name
    "40": InternalError,  # transaction rollback
    "42": ProgrammingError,  # syntax error or access rule violation
    "44": InternalError,  # with check option violation
    "HZ": OperationalError,  # remote database access
    "XA": IntegrityError,
    "0K": OperationalError,
    "HY": DatabaseError,  # default when no SQLState provided by MySQL server
}

_ERROR_EXCEPTIONS: Dict[int, ErrorClassTypes] = {
    1243: ProgrammingError,
    1210: ProgrammingError,
    2002: InterfaceError,
    2013: OperationalError,
    2049: NotSupportedError,
    2055: OperationalError,
    2061: InterfaceError,
    2026: InterfaceError,
}
