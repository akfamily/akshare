"""Exception classes for _mysql and MySQLdb.

These classes are dictated by the DB API v2.0:

    https://www.python.org/dev/peps/pep-0249/
"""


class MySQLError(Exception):
    """Exception related to operation with MySQL."""

    __module__ = "MySQLdb"


class Warning(Warning, MySQLError):
    """Exception raised for important warnings like data truncations
    while inserting, etc."""

    __module__ = "MySQLdb"


class Error(MySQLError):
    """Exception that is the base class of all other error exceptions
    (not Warning)."""

    __module__ = "MySQLdb"


class InterfaceError(Error):
    """Exception raised for errors that are related to the database
    interface rather than the database itself."""

    __module__ = "MySQLdb"


class DatabaseError(Error):
    """Exception raised for errors that are related to the
    database."""

    __module__ = "MySQLdb"


class DataError(DatabaseError):
    """Exception raised for errors that are due to problems with the
    processed data like division by zero, numeric value out of range,
    etc."""

    __module__ = "MySQLdb"


class OperationalError(DatabaseError):
    """Exception raised for errors that are related to the database's
    operation and not necessarily under the control of the programmer,
    e.g. an unexpected disconnect occurs, the data source name is not
    found, a transaction could not be processed, a memory allocation
    error occurred during processing, etc."""

    __module__ = "MySQLdb"


class IntegrityError(DatabaseError):
    """Exception raised when the relational integrity of the database
    is affected, e.g. a foreign key check fails, duplicate key,
    etc."""

    __module__ = "MySQLdb"


class InternalError(DatabaseError):
    """Exception raised when the database encounters an internal
    error, e.g. the cursor is not valid anymore, the transaction is
    out of sync, etc."""

    __module__ = "MySQLdb"


class ProgrammingError(DatabaseError):
    """Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc."""

    __module__ = "MySQLdb"


class NotSupportedError(DatabaseError):
    """Exception raised in case a method or database API was used
    which is not supported by the database, e.g. requesting a
    .rollback() on a connection that does not support transaction or
    has transactions turned off."""

    __module__ = "MySQLdb"
