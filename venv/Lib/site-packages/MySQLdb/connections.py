"""
This module implements connections for MySQLdb. Presently there is
only one class: Connection. Others are unlikely. However, you might
want to make your own subclasses. In most cases, you will probably
override Connection.default_cursor with a non-standard Cursor class.
"""
import re

from . import cursors, _mysql
from ._exceptions import (
    Warning,
    Error,
    InterfaceError,
    DataError,
    DatabaseError,
    OperationalError,
    IntegrityError,
    InternalError,
    NotSupportedError,
    ProgrammingError,
)

# Mapping from MySQL charset name to Python codec name
_charset_to_encoding = {
    "utf8mb4": "utf8",
    "utf8mb3": "utf8",
    "latin1": "cp1252",
    "koi8r": "koi8_r",
    "koi8u": "koi8_u",
}

re_numeric_part = re.compile(r"^(\d+)")


def numeric_part(s):
    """Returns the leading numeric part of a string.

    >>> numeric_part("20-alpha")
    20
    >>> numeric_part("foo")
    >>> numeric_part("16b")
    16
    """

    m = re_numeric_part.match(s)
    if m:
        return int(m.group(1))
    return None


class Connection(_mysql.connection):
    """MySQL Database Connection Object"""

    default_cursor = cursors.Cursor

    def __init__(self, *args, **kwargs):
        """
        Create a connection to the database. It is strongly recommended
        that you only use keyword parameters. Consult the MySQL C API
        documentation for more information.

        :param str host:        host to connect
        :param str user:        user to connect as
        :param str password:    password to use
        :param str passwd:      alias of password (deprecated)
        :param str database:    database to use
        :param str db:          alias of database (deprecated)
        :param int port:        TCP/IP port to connect to
        :param str unix_socket: location of unix_socket to use
        :param dict conv:       conversion dictionary, see MySQLdb.converters
        :param int connect_timeout:
            number of seconds to wait before the connection attempt fails.

        :param bool compress:   if set, compression is enabled
        :param str named_pipe:  if set, a named pipe is used to connect (Windows only)
        :param str init_command:
            command which is run once the connection is created

        :param str read_default_file:
            file from which default client values are read

        :param str read_default_group:
            configuration group to use from the default file

        :param type cursorclass:
            class object, used to create cursors (keyword only)

        :param bool use_unicode:
            If True, text-like columns are returned as unicode objects
            using the connection's character set. Otherwise, text-like
            columns are returned as bytes. Unicode objects will always
            be encoded to the connection's character set regardless of
            this setting.
            Default to True.

        :param str charset:
            If supplied, the connection character set will be changed
            to this character set.

        :param str collation:
            If ``charset`` and ``collation`` are both supplied, the
            character set and collation for the current connection
            will be set.

            If omitted, empty string, or None, the default collation
            for the ``charset`` is implied.

        :param str auth_plugin:
            If supplied, the connection default authentication plugin will be
            changed to this value. Example values:
            `mysql_native_password` or `caching_sha2_password`

        :param str sql_mode:
            If supplied, the session SQL mode will be changed to this
            setting.
            For more details and legal values, see the MySQL documentation.

        :param int client_flag:
            flags to use or 0 (see MySQL docs or constants/CLIENTS.py)

        :param bool multi_statements:
            If True, enable multi statements for clients >= 4.1.
            Defaults to True.

        :param str ssl_mode:
            specify the security settings for connection to the server;
            see the MySQL documentation for more details
            (mysql_option(), MYSQL_OPT_SSL_MODE).
            Only one of 'DISABLED', 'PREFERRED', 'REQUIRED',
            'VERIFY_CA', 'VERIFY_IDENTITY' can be specified.

        :param dict ssl:
            dictionary or mapping contains SSL connection parameters;
            see the MySQL documentation for more details
            (mysql_ssl_set()).  If this is set, and the client does not
            support SSL, NotSupportedError will be raised.
            Since mysqlclient 2.2.4, ssl=True is alias of ssl_mode=REQUIRED
            for better compatibility with PyMySQL and MariaDB.

        :param str server_public_key_path:
            specify the path to a file RSA public key file for caching_sha2_password.
            See https://dev.mysql.com/doc/refman/9.0/en/caching-sha2-pluggable-authentication.html

        :param bool local_infile:
            enables LOAD LOCAL INFILE; zero disables

        :param bool autocommit:
            If False (default), autocommit is disabled.
            If True, autocommit is enabled.
            If None, autocommit isn't set and server default is used.

        :param bool binary_prefix:
            If set, the '_binary' prefix will be used for raw byte query
            arguments (e.g. Binary). This is disabled by default.

        There are a number of undocumented, non-standard methods. See the
        documentation for the MySQL C API for some hints on what they do.
        """
        from MySQLdb.constants import CLIENT, FIELD_TYPE
        from MySQLdb.converters import conversions, _bytes_or_str

        kwargs2 = kwargs.copy()

        if "db" in kwargs2:
            kwargs2["database"] = kwargs2.pop("db")
        if "passwd" in kwargs2:
            kwargs2["password"] = kwargs2.pop("passwd")

        if "conv" in kwargs:
            conv = kwargs["conv"]
        else:
            conv = conversions

        conv2 = {}
        for k, v in conv.items():
            if isinstance(k, int) and isinstance(v, list):
                conv2[k] = v[:]
            else:
                conv2[k] = v
        kwargs2["conv"] = conv2

        cursorclass = kwargs2.pop("cursorclass", self.default_cursor)
        charset = kwargs2.get("charset", "")
        collation = kwargs2.pop("collation", "")
        use_unicode = kwargs2.pop("use_unicode", True)
        sql_mode = kwargs2.pop("sql_mode", "")
        self._binary_prefix = kwargs2.pop("binary_prefix", False)

        client_flag = kwargs.get("client_flag", 0)
        client_flag |= CLIENT.MULTI_RESULTS
        multi_statements = kwargs2.pop("multi_statements", True)
        if multi_statements:
            client_flag |= CLIENT.MULTI_STATEMENTS
        kwargs2["client_flag"] = client_flag

        # PEP-249 requires autocommit to be initially off
        autocommit = kwargs2.pop("autocommit", False)

        self._set_attributes(*args, **kwargs2)
        super().__init__(*args, **kwargs2)

        self.cursorclass = cursorclass
        self.encoders = {
            k: v
            for k, v in conv.items()
            if type(k) is not int  # noqa: E721
        }
        self._server_version = tuple(
            [numeric_part(n) for n in self.get_server_info().split(".")[:2]]
        )
        self.encoding = "ascii"  # overridden in set_character_set()

        if not charset:
            charset = self.character_set_name()
        self.set_character_set(charset, collation)

        if sql_mode:
            self.set_sql_mode(sql_mode)

        if use_unicode:
            for t in (
                FIELD_TYPE.STRING,
                FIELD_TYPE.VAR_STRING,
                FIELD_TYPE.VARCHAR,
                FIELD_TYPE.TINY_BLOB,
                FIELD_TYPE.MEDIUM_BLOB,
                FIELD_TYPE.LONG_BLOB,
                FIELD_TYPE.BLOB,
            ):
                self.converter[t] = _bytes_or_str
            # Unlike other string/blob types, JSON is always text.
            # MySQL may return JSON with charset==binary.
            self.converter[FIELD_TYPE.JSON] = str

        self._transactional = self.server_capabilities & CLIENT.TRANSACTIONS
        if self._transactional:
            if autocommit is not None:
                self.autocommit(autocommit)
        self.messages = []

    def _set_attributes(self, host=None, user=None, password=None, database="", port=3306,
                        unix_socket=None, **kwargs):
        """set some attributes for otel"""
        if unix_socket and not host:
            host = "localhost"
        # support opentelemetry-instrumentation-dbapi
        self.host = host
        # _mysql.Connection provides self.port
        self.user = user
        self.database = database
        # otel-inst-mysqlclient uses db instead of database.
        self.db = database
        # NOTE: We have not supported semantic conventions yet.
        # https://opentelemetry.io/docs/specs/semconv/database/sql/

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def autocommit(self, on):
        on = bool(on)
        if self.get_autocommit() != on:
            _mysql.connection.autocommit(self, on)

    def cursor(self, cursorclass=None):
        """
        Create a cursor on which queries may be performed. The
        optional cursorclass parameter is used to create the
        Cursor. By default, self.cursorclass=cursors.Cursor is
        used.
        """
        return (cursorclass or self.cursorclass)(self)

    def query(self, query):
        # Since _mysql releases GIL while querying, we need immutable buffer.
        if isinstance(query, bytearray):
            query = bytes(query)
        _mysql.connection.query(self, query)

    def _bytes_literal(self, bs):
        assert isinstance(bs, (bytes, bytearray))
        x = self.string_literal(bs)  # x is escaped and quoted bytes
        if self._binary_prefix:
            return b"_binary" + x
        return x

    def _tuple_literal(self, t):
        return b"(%s)" % (b",".join(map(self.literal, t)))

    def literal(self, o):
        """If o is a single object, returns an SQL literal as a string.
        If o is a non-string sequence, the items of the sequence are
        converted and returned as a sequence.

        Non-standard. For internal use; do not use this in your
        applications.
        """
        if isinstance(o, str):
            s = self.string_literal(o.encode(self.encoding))
        elif isinstance(o, bytearray):
            s = self._bytes_literal(o)
        elif isinstance(o, bytes):
            s = self._bytes_literal(o)
        elif isinstance(o, (tuple, list)):
            s = self._tuple_literal(o)
        else:
            s = self.escape(o, self.encoders)
            if isinstance(s, str):
                s = s.encode(self.encoding)
        assert isinstance(s, bytes)
        return s

    def begin(self):
        """Explicitly begin a connection.

        This method is not used when autocommit=False (default).
        """
        self.query(b"BEGIN")

    def set_character_set(self, charset, collation=None):
        """Set the connection character set to charset."""
        super().set_character_set(charset)
        self.encoding = _charset_to_encoding.get(charset, charset)
        if collation:
            self.query(f"SET NAMES {charset} COLLATE {collation}")
            self.store_result()

    def set_sql_mode(self, sql_mode):
        """Set the connection sql_mode. See MySQL documentation for
        legal values."""
        if self._server_version < (4, 1):
            raise NotSupportedError("server is too old to set sql_mode")
        self.query("SET SESSION sql_mode='%s'" % sql_mode)
        self.store_result()

    def show_warnings(self):
        """Return detailed information about warnings as a
        sequence of tuples of (Level, Code, Message). This
        is only supported in MySQL-4.1 and up. If your server
        is an earlier version, an empty sequence is returned."""
        if self._server_version < (4, 1):
            return ()
        self.query("SHOW WARNINGS")
        r = self.store_result()
        warnings = r.fetch_row(0)
        return warnings

    Warning = Warning
    Error = Error
    InterfaceError = InterfaceError
    DatabaseError = DatabaseError
    DataError = DataError
    OperationalError = OperationalError
    IntegrityError = IntegrityError
    InternalError = InternalError
    ProgrammingError = ProgrammingError
    NotSupportedError = NotSupportedError


# vim: colorcolumn=100
