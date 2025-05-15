"""MySQL CLIENT constants

These constants are used when creating the connection. Use bitwise-OR
(|) to combine options together, and pass them as the client_flags
parameter to MySQLdb.Connection. For more information on these flags,
see the MySQL C API documentation for mysql_real_connect().

"""

LONG_PASSWORD = 1
FOUND_ROWS = 2
LONG_FLAG = 4
CONNECT_WITH_DB = 8
NO_SCHEMA = 16
COMPRESS = 32
ODBC = 64
LOCAL_FILES = 128
IGNORE_SPACE = 256
CHANGE_USER = 512
INTERACTIVE = 1024
SSL = 2048
IGNORE_SIGPIPE = 4096
TRANSACTIONS = 8192  # mysql_com.h was WRONG prior to 3.23.35
RESERVED = 16384
SECURE_CONNECTION = 32768
MULTI_STATEMENTS = 65536
MULTI_RESULTS = 131072
