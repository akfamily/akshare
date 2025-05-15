/*
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version. Alternatively, you may use the original license
reproduced below.

Copyright 1999 by Comstar.net, Inc., Atlanta, GA, US.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Comstar.net, Inc.
or COMSTAR not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior permission.

COMSTAR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL COMSTAR BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
*/
#include <stdbool.h>
#include "mysql.h"
#include "mysqld_error.h"

#if MYSQL_VERSION_ID >= 80000
// https://github.com/mysql/mysql-server/commit/eb821c023cedc029ca0b06456dfae365106bee84
// my_bool was typedef of char before MySQL 8.0.0.
#define my_bool bool
#endif

#if ((MYSQL_VERSION_ID >= 50555 && MYSQL_VERSION_ID <= 50599) || \
     (MYSQL_VERSION_ID >= 50636 && MYSQL_VERSION_ID <= 50699) || \
     (MYSQL_VERSION_ID >= 50711 && MYSQL_VERSION_ID <= 50799) || \
     (MYSQL_VERSION_ID >= 80000)) && \
     !defined(MARIADB_BASE_VERSION) && !defined(MARIADB_VERSION_ID)
#define HAVE_ENUM_MYSQL_OPT_SSL_MODE
#endif

#if defined(MARIADB_VERSION_ID) && MARIADB_VERSION_ID >= 100403 || \
    !defined(MARIADB_VERSION_ID) && MYSQL_VERSION_ID >= 50723
#define HAVE_MYSQL_SERVER_PUBLIC_KEY
#endif

#define PY_SSIZE_T_CLEAN 1
#include "Python.h"

#if PY_MAJOR_VERSION == 2
#error "Python 2 is not supported"
#endif

#include "bytesobject.h"
#include "structmember.h"
#include "errmsg.h"

#define MyAlloc(s,t) (s *) t.tp_alloc(&t,0)
#define MyFree(o) Py_TYPE(o)->tp_free((PyObject*)o)

static PyObject *_mysql_MySQLError;
static PyObject *_mysql_Warning;
static PyObject *_mysql_Error;
static PyObject *_mysql_DatabaseError;
static PyObject *_mysql_InterfaceError;
static PyObject *_mysql_DataError;
static PyObject *_mysql_OperationalError;
static PyObject *_mysql_IntegrityError;
static PyObject *_mysql_InternalError;
static PyObject *_mysql_ProgrammingError;
static PyObject *_mysql_NotSupportedError;

typedef struct {
    PyObject_HEAD
    MYSQL connection;
    bool open;
    bool reconnect;
    PyObject *converter;
} _mysql_ConnectionObject;

#define check_connection(c) \
    if (!(c->open)) { \
        return _mysql_Exception(c); \
    };

#define result_connection(r) ((_mysql_ConnectionObject *)r->conn)
#define check_result_connection(r) check_connection(result_connection(r))

extern PyTypeObject _mysql_ConnectionObject_Type;

typedef struct {
    PyObject_HEAD
    PyObject *conn;
    MYSQL_RES *result;
    int nfields;
    int use;
    char has_next;
    PyObject *converter;
    const char *encoding;
} _mysql_ResultObject;

extern PyTypeObject _mysql_ResultObject_Type;


PyObject *
_mysql_Exception(_mysql_ConnectionObject *c)
{
    PyObject *t, *e;
    int merr;

    if (!(t = PyTuple_New(2))) return NULL;
    if (!(c->open)) {
        /* GH-270: When connection is closed, accessing the c->connection
         * object may cause SEGV.
         */
        merr = CR_SERVER_GONE_ERROR;
    }
    else {
        merr = mysql_errno(&(c->connection));
    }
    switch (merr) {
    case 0:
        e = _mysql_InterfaceError;
        break;
    case CR_COMMANDS_OUT_OF_SYNC:
    case ER_DB_CREATE_EXISTS:
    case ER_SYNTAX_ERROR:
    case ER_PARSE_ERROR:
    case ER_NO_SUCH_TABLE:
    case ER_WRONG_DB_NAME:
    case ER_WRONG_TABLE_NAME:
    case ER_FIELD_SPECIFIED_TWICE:
    case ER_INVALID_GROUP_FUNC_USE:
    case ER_UNSUPPORTED_EXTENSION:
    case ER_TABLE_MUST_HAVE_COLUMNS:
#ifdef ER_CANT_DO_THIS_DURING_AN_TRANSACTION
    case ER_CANT_DO_THIS_DURING_AN_TRANSACTION:
#endif
        e = _mysql_ProgrammingError;
        break;
#ifdef WARN_DATA_TRUNCATED
    case WARN_DATA_TRUNCATED:
#ifdef WARN_NULL_TO_NOTNULL
    case WARN_NULL_TO_NOTNULL:
#endif
#ifdef ER_WARN_DATA_OUT_OF_RANGE
    case ER_WARN_DATA_OUT_OF_RANGE:
#endif
#ifdef ER_NO_DEFAULT
    case ER_NO_DEFAULT:
#endif
#ifdef ER_PRIMARY_CANT_HAVE_NULL
    case ER_PRIMARY_CANT_HAVE_NULL:
#endif
#ifdef ER_DATA_TOO_LONG
    case ER_DATA_TOO_LONG:
#endif
#ifdef ER_DATETIME_FUNCTION_OVERFLOW
    case ER_DATETIME_FUNCTION_OVERFLOW:
#endif
        e = _mysql_DataError;
        break;
#endif
    case ER_DUP_ENTRY:
#ifdef ER_DUP_UNIQUE
    case ER_DUP_UNIQUE:
#endif
#ifdef ER_NO_REFERENCED_ROW
    case ER_NO_REFERENCED_ROW:
#endif
#ifdef ER_NO_REFERENCED_ROW_2
    case ER_NO_REFERENCED_ROW_2:
#endif
#ifdef ER_ROW_IS_REFERENCED
    case ER_ROW_IS_REFERENCED:
#endif
#ifdef ER_ROW_IS_REFERENCED_2
    case ER_ROW_IS_REFERENCED_2:
#endif
#ifdef ER_CANNOT_ADD_FOREIGN
    case ER_CANNOT_ADD_FOREIGN:
#endif
#ifdef ER_NO_DEFAULT_FOR_FIELD
    case ER_NO_DEFAULT_FOR_FIELD:
#endif
    case ER_BAD_NULL_ERROR:
        e = _mysql_IntegrityError;
        break;
#ifdef ER_WARNING_NOT_COMPLETE_ROLLBACK
    case ER_WARNING_NOT_COMPLETE_ROLLBACK:
#endif
#ifdef ER_NOT_SUPPORTED_YET
    case ER_NOT_SUPPORTED_YET:
#endif
#ifdef ER_FEATURE_DISABLED
    case ER_FEATURE_DISABLED:
#endif
#ifdef ER_UNKNOWN_STORAGE_ENGINE
    case ER_UNKNOWN_STORAGE_ENGINE:
#endif
        e = _mysql_NotSupportedError;
        break;
    default:
        if (merr < 1000)
            e = _mysql_InternalError;
        else
            e = _mysql_OperationalError;
        break;
    }
    PyTuple_SET_ITEM(t, 0, PyLong_FromLong((long)merr));
    PyTuple_SET_ITEM(t, 1, PyUnicode_FromString(mysql_error(&(c->connection))));
    PyErr_SetObject(e, t);
    Py_DECREF(t);
    return NULL;
}

static const char *utf8 = "utf8";

static const char*
_get_encoding(MYSQL *mysql)
{
    MY_CHARSET_INFO cs;
    mysql_get_character_set_info(mysql, &cs);
    if (strncmp(utf8, cs.csname, 4) == 0) { // utf8, utf8mb3, utf8mb4
        return utf8;
    }
    else if (strncmp("latin1", cs.csname, 6) == 0) {
        return "cp1252";
    }
    else if (strncmp("koi8r", cs.csname, 5) == 0) {
        return "koi8_r";
    }
    else if (strncmp("koi8u", cs.csname, 5) == 0) {
        return "koi8_u";
    }
    return cs.csname;
}

static char _mysql_ResultObject__doc__[] =
"result(connection, use=0, converter={}) -- Result set from a query.\n\
\n\
Creating instances of this class directly is an excellent way to\n\
shoot yourself in the foot. If using _mysql.connection directly,\n\
use connection.store_result() or connection.use_result() instead.\n\
If using MySQLdb.Connection, this is done by the cursor class.\n\
Just forget you ever saw this. Forget... FOR-GET...";

static int
_mysql_ResultObject_Initialize(
    _mysql_ResultObject *self,
    PyObject *args,
    PyObject *kwargs)
{
    static char *kwlist[] = {"connection", "use", "converter", NULL};
    MYSQL_RES *result;
    _mysql_ConnectionObject *conn=NULL;
    int use=0;
    PyObject *conv=NULL;
    int n, i;
    MYSQL_FIELD *fields;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|iO", kwlist,
                     &_mysql_ConnectionObject_Type, &conn, &use, &conv))
        return -1;

    self->conn = (PyObject *) conn;
    Py_INCREF(conn);
    self->use = use;
    Py_BEGIN_ALLOW_THREADS ;
    if (use)
        result = mysql_use_result(&(conn->connection));
    else
        result = mysql_store_result(&(conn->connection));
    self->result = result;
    self->has_next = (char)mysql_more_results(&(conn->connection));
    Py_END_ALLOW_THREADS ;

    self->encoding = _get_encoding(&(conn->connection));
    //fprintf(stderr, "encoding=%s\n", self->encoding);
    if (!result) {
        if (mysql_errno(&(conn->connection))) {
            _mysql_Exception(conn);
            return -1;
        }
        self->converter = PyTuple_New(0);
        return 0;
    }
    n = mysql_num_fields(result);
    self->nfields = n;
    if (!(self->converter = PyTuple_New(n))) {
        return -1;
    }
    fields = mysql_fetch_fields(result);
    for (i=0; i<n; i++) {
        PyObject *tmp, *fun;
        tmp = PyLong_FromLong((long) fields[i].type);
        if (!tmp) {
            return -1;
        }
        fun = conv ? PyObject_GetItem(conv, tmp) : NULL;
        Py_DECREF(tmp);
        if (!fun) {
            if (PyErr_Occurred()) {
                if (!PyErr_ExceptionMatches(PyExc_KeyError)) {
                    return -1;
                }
                PyErr_Clear();
            }
            fun = Py_None;
            Py_INCREF(Py_None);
        }
        else if (PySequence_Check(fun)) {
            long flags = fields[i].flags;
            PyObject *fun2=NULL;
            int j, n2=PySequence_Size(fun);
            // BINARY_FLAG means ***_bin collation is used.
            // To distinguish text and binary, we should use charsetnr==63 (binary).
            // But we abuse BINARY_FLAG for historical reason.
            if (fields[i].charsetnr == 63) {
                flags |= BINARY_FLAG;
            } else {
                flags &= ~BINARY_FLAG;
            }
            for (j=0; j<n2; j++) {
                PyObject *t = PySequence_GetItem(fun, j);
                if (!t) {
                    Py_DECREF(fun);
                    return -1;
                }
                if (PyTuple_Check(t) && PyTuple_GET_SIZE(t) == 2) {
                    long mask;
                    PyObject *pmask=NULL;
                    pmask = PyTuple_GET_ITEM(t, 0);
                    fun2 = PyTuple_GET_ITEM(t, 1);
                    Py_XINCREF(fun2);
                    if (PyLong_Check(pmask)) {
                        mask = PyLong_AS_LONG(pmask);
                        if (mask & flags) {
                            Py_DECREF(t);
                            break;
                        }
                        else {
                            fun2 = NULL;
                        }
                    } else {
                        Py_DECREF(t);
                        break;
                    }
                }
                Py_DECREF(t);
            }
            if (!fun2) {
                fun2 = Py_None;
                Py_INCREF(fun2);
            }
            Py_DECREF(fun);
            fun = fun2;
        }
        PyTuple_SET_ITEM(self->converter, i, fun);
    }

    return 0;
}

static int _mysql_ResultObject_traverse(
    _mysql_ResultObject *self,
    visitproc visit,
    void *arg)
{
    int r;
    if (self->converter) {
        if (!(r = visit(self->converter, arg))) return r;
    }
    if (self->conn)
        return visit(self->conn, arg);
    return 0;
}

static int _mysql_ResultObject_clear(_mysql_ResultObject *self)
{
    Py_CLEAR(self->converter);
    Py_CLEAR(self->conn);
    return 0;
}

enum {
    SSLMODE_DISABLED = 1,
    SSLMODE_PREFERRED = 2,
    SSLMODE_REQUIRED = 3,
    SSLMODE_VERIFY_CA = 4,
    SSLMODE_VERIFY_IDENTITY = 5
};

static int
_get_ssl_mode_num(const char *ssl_mode)
{
    static const char *ssl_mode_list[] = {
        "DISABLED", "PREFERRED", "REQUIRED", "VERIFY_CA", "VERIFY_IDENTITY" };
    unsigned int i;
    for (i=0; i < sizeof(ssl_mode_list)/sizeof(ssl_mode_list[0]); i++) {
        if (strcmp(ssl_mode, ssl_mode_list[i]) == 0) {
            // SSL_MODE one-based
            return i + 1;
        }
    }
    return -1;
}

static int
_mysql_ConnectionObject_Initialize(
    _mysql_ConnectionObject *self,
    PyObject *args,
    PyObject *kwargs)
{
    MYSQL *conn = NULL;
    PyObject *conv = NULL;
    PyObject *ssl = NULL;
    const char *ssl_mode = NULL;
    const char *key = NULL, *cert = NULL, *ca = NULL,
         *capath = NULL, *cipher = NULL;
    PyObject *ssl_keepref[5] = {NULL};
    int n_ssl_keepref = 0;
    char *host = NULL, *user = NULL, *passwd = NULL,
         *db = NULL, *unix_socket = NULL;
    unsigned int port = 0;
    unsigned int client_flag = 0;
    static char *kwlist[] = { "host", "user", "password", "database", "port",
                  "unix_socket", "conv",
                  "connect_timeout", "compress",
                  "named_pipe", "init_command",
                  "read_default_file", "read_default_group",
                  "client_flag", "ssl", "ssl_mode",
                  "local_infile",
                  "read_timeout", "write_timeout", "charset",
                  "auth_plugin", "server_public_key_path",
                  NULL } ;
    int connect_timeout = 0;
    int read_timeout = 0;
    int write_timeout = 0;
    int compress = -1, named_pipe = -1, local_infile = -1;
    int ssl_mode_num = SSLMODE_PREFERRED;
    char *init_command=NULL,
         *read_default_file=NULL,
         *read_default_group=NULL,
         *charset=NULL,
         *auth_plugin=NULL,
         *server_public_key_path=NULL;

    self->converter = NULL;
    self->open = false;
    self->reconnect = false;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,
                "|ssssisOiiisssiOsiiisss:connect",
                kwlist,
                &host, &user, &passwd, &db,
                &port, &unix_socket, &conv,
                &connect_timeout,
                &compress, &named_pipe,
                &init_command, &read_default_file,
                &read_default_group,
                &client_flag, &ssl, &ssl_mode,
                &local_infile,
                &read_timeout,
                &write_timeout,
                &charset,
                &auth_plugin,
                &server_public_key_path
    ))
        return -1;

#ifndef HAVE_MYSQL_SERVER_PUBLIC_KEY
    if (server_public_key_path) {
        PyErr_SetString(_mysql_NotSupportedError, "server_public_key_path is not supported");
        return -1;
    }
#endif
    // For compatibility with PyPy, we need to keep strong reference
    // to unicode objects until we use UTF8.
#define _stringsuck(d,t,s) {t=PyMapping_GetItemString(s,#d);\
        if(t){d=PyUnicode_AsUTF8(t);ssl_keepref[n_ssl_keepref++]=t;}\
        PyErr_Clear();}

    char ssl_mode_set = 0;
    if (ssl) {
        if (PyMapping_Check(ssl)) {
            PyObject *value = NULL;
            _stringsuck(ca, value, ssl);
            _stringsuck(capath, value, ssl);
            _stringsuck(cert, value, ssl);
            _stringsuck(key, value, ssl);
            _stringsuck(cipher, value, ssl);
        } else if (PyObject_IsTrue(ssl)) {
            // Support ssl=True from mysqlclient 2.2.4.
            // for compatibility with PyMySQL and mysqlclient==2.2.1&libmariadb.
            ssl_mode_num = SSLMODE_REQUIRED;
            ssl_mode_set = 1;
        } else {
            ssl_mode_num = SSLMODE_DISABLED;
            ssl_mode_set = 1;
        }
    }
    if (ssl_mode) {
        if ((ssl_mode_num = _get_ssl_mode_num(ssl_mode)) <= 0) {
            PyErr_SetString(_mysql_NotSupportedError, "Unknown ssl_mode specification");
            return -1;
        }
        ssl_mode_set = 1;
    }

    conn = mysql_init(&(self->connection));
    if (!conn) {
        PyErr_SetNone(PyExc_MemoryError);
        return -1;
    }
    self->open = true;

    if (connect_timeout) {
        unsigned int timeout = connect_timeout;
        mysql_options(&(self->connection), MYSQL_OPT_CONNECT_TIMEOUT,
                (char *)&timeout);
    }
    if (read_timeout) {
        unsigned int timeout = read_timeout;
        mysql_options(&(self->connection), MYSQL_OPT_READ_TIMEOUT,
                (char *)&timeout);
    }
    if (write_timeout) {
        unsigned int timeout = write_timeout;
        mysql_options(&(self->connection), MYSQL_OPT_WRITE_TIMEOUT,
                (char *)&timeout);
    }
    if (compress != -1) {
        mysql_options(&(self->connection), MYSQL_OPT_COMPRESS, 0);
        client_flag |= CLIENT_COMPRESS;
    }
    if (named_pipe != -1)
        mysql_options(&(self->connection), MYSQL_OPT_NAMED_PIPE, 0);
    if (init_command != NULL)
        mysql_options(&(self->connection), MYSQL_INIT_COMMAND, init_command);
    if (read_default_file != NULL)
        mysql_options(&(self->connection), MYSQL_READ_DEFAULT_FILE, read_default_file);
    if (read_default_group != NULL)
        mysql_options(&(self->connection), MYSQL_READ_DEFAULT_GROUP, read_default_group);

    if (local_infile != -1)
        mysql_options(&(self->connection), MYSQL_OPT_LOCAL_INFILE, (char *) &local_infile);

    if (ssl) {
        mysql_options(&(self->connection), MYSQL_OPT_SSL_KEY, key);
        mysql_options(&(self->connection), MYSQL_OPT_SSL_CERT, cert);
        mysql_options(&(self->connection), MYSQL_OPT_SSL_CA, ca);
        mysql_options(&(self->connection), MYSQL_OPT_SSL_CAPATH, capath);
        mysql_options(&(self->connection), MYSQL_OPT_SSL_CIPHER, cipher);
    }
    for (int i=0 ; i<n_ssl_keepref; i++) {
        Py_DECREF(ssl_keepref[i]);
        ssl_keepref[i] = NULL;
    }

#ifdef HAVE_ENUM_MYSQL_OPT_SSL_MODE
    if (ssl_mode_set) {
        mysql_options(&(self->connection), MYSQL_OPT_SSL_MODE, &ssl_mode_num);
    }
#else
    // MariaDB doesn't support MYSQL_OPT_SSL_MODE.
    // See https://github.com/PyMySQL/mysqlclient/issues/474
    // And MariDB 11.4 changed the default value of MYSQL_OPT_SSL_ENFORCE and
    // MYSQL_OPT_SSL_VERIFY_SERVER_CERT to 1.
    // https://github.com/mariadb-corporation/mariadb-connector-c/commit/8dffd56936df3d03eeccf47904773860a0cdeb57
    // We emulate the ssl_mode and old behavior.
    my_bool my_true = 1;
    my_bool my_false = 0;
    if (ssl_mode_num >= SSLMODE_REQUIRED) {
        mysql_options(&(self->connection), MYSQL_OPT_SSL_ENFORCE, (void *)&my_true);
    } else {
        mysql_options(&(self->connection), MYSQL_OPT_SSL_ENFORCE, (void *)&my_false);
    }
    if (ssl_mode_num >= SSLMODE_VERIFY_CA) {
        mysql_options(&(self->connection), MYSQL_OPT_SSL_VERIFY_SERVER_CERT, (void *)&my_true);
    } else {
        mysql_options(&(self->connection), MYSQL_OPT_SSL_VERIFY_SERVER_CERT, (void *)&my_false);
    }
#endif

    if (charset) {
        mysql_options(&(self->connection), MYSQL_SET_CHARSET_NAME, charset);
    }
    if (auth_plugin) {
        mysql_options(&(self->connection), MYSQL_DEFAULT_AUTH, auth_plugin);
    }
#ifdef HAVE_MYSQL_SERVER_PUBLIC_KEY
    if (server_public_key_path) {
        mysql_options(&(self->connection), MYSQL_SERVER_PUBLIC_KEY, server_public_key_path);
    }
#endif

    Py_BEGIN_ALLOW_THREADS
    conn = mysql_real_connect(&(self->connection), host, user, passwd, db,
                  port, unix_socket, client_flag);
    Py_END_ALLOW_THREADS

    if (!conn) {
        _mysql_Exception(self);
        return -1;
    }

    /* Internal references to python-land objects */
    if (!conv)
        conv = PyDict_New();
    else
        Py_INCREF(conv);

    if (!conv)
        return -1;
    self->converter = conv;

    /*
      PyType_GenericAlloc() automatically sets up GC allocation and
      tracking for GC objects, at least in 2.2.1, so it does not need to
      be done here. tp_dealloc still needs to call PyObject_GC_UnTrack(),
      however.
    */
    return 0;
}

static char _mysql_connect__doc__[] =
"Returns a MYSQL connection object. Exclusive use of\n\
keyword parameters strongly recommended. Consult the\n\
MySQL C API documentation for more details.\n\
\n\
host\n\
  string, host to connect\n\
\n\
user\n\
  string, user to connect as\n\
\n\
password\n\
  string, password to use\n\
\n\
database\n\
  string, database to use\n\
\n\
port\n\
  integer, TCP/IP port to connect to\n\
\n\
unix_socket\n\
  string, location of unix_socket (UNIX-ish only)\n\
\n\
conv\n\
  mapping, maps MySQL FIELD_TYPE.* to Python functions which\n\
  convert a string to the appropriate Python type\n\
\n\
connect_timeout\n\
  number of seconds to wait before the connection\n\
  attempt fails.\n\
\n\
compress\n\
  if set, gzip compression is enabled\n\
\n\
named_pipe\n\
  if set, connect to server via named pipe (Windows only)\n\
\n\
init_command\n\
  command which is run once the connection is created\n\
\n\
read_default_file\n\
  see the MySQL documentation for mysql_options()\n\
\n\
read_default_group\n\
  see the MySQL documentation for mysql_options()\n\
\n\
client_flag\n\
  client flags from MySQLdb.constants.CLIENT\n\
\n\
load_infile\n\
  int, non-zero enables LOAD LOCAL INFILE, zero disables\n\
\n\
";

static PyObject *
_mysql_connect(
    PyObject *self,
    PyObject *args,
    PyObject *kwargs)
{
    _mysql_ConnectionObject *c=NULL;

    c = MyAlloc(_mysql_ConnectionObject, _mysql_ConnectionObject_Type);
    if (c == NULL) return NULL;
    if (_mysql_ConnectionObject_Initialize(c, args, kwargs)) {
        Py_DECREF(c);
        c = NULL;
    }
    return (PyObject *) c;
}

static int _mysql_ConnectionObject_traverse(
    _mysql_ConnectionObject *self,
    visitproc visit,
    void *arg)
{
    if (self->converter)
        return visit(self->converter, arg);
    return 0;
}

static int _mysql_ConnectionObject_clear(
    _mysql_ConnectionObject *self)
{
    Py_XDECREF(self->converter);
    self->converter = NULL;
    return 0;
}

static char _mysql_ConnectionObject_close__doc__[] =
"Close the connection. No further activity possible.";

static PyObject *
_mysql_ConnectionObject_close(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    mysql_close(&(self->connection));
    Py_END_ALLOW_THREADS
    self->open = false;
    _mysql_ConnectionObject_clear(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_affected_rows__doc__ [] =
"Return number of rows affected by the last query.\n\
Non-standard. Use Cursor.rowcount.\n\
";

static PyObject *
_mysql_ConnectionObject_affected_rows(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    my_ulonglong ret;
    check_connection(self);
    ret = mysql_affected_rows(&(self->connection));
    if (ret == (my_ulonglong)-1)
        return PyLong_FromLong(-1);
    return PyLong_FromUnsignedLongLong(ret);
}

static char _mysql_debug__doc__[] =
"Does a DBUG_PUSH with the given string.\n\
mysql_debug() uses the Fred Fish debug library.\n\
To use this function, you must compile the client library to\n\
support debugging.\n\
";
static PyObject *
_mysql_debug(
    PyObject *self,
    PyObject *args)
{
    char *debug;
    if (!PyArg_ParseTuple(args, "s", &debug)) return NULL;
    mysql_debug(debug);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_dump_debug_info__doc__[] =
"Instructs the server to write some debug information to the\n\
log. The connected user must have the process privilege for\n\
this to work. Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_dump_debug_info(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    int err;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    err = mysql_dump_debug_info(&(self->connection));
    Py_END_ALLOW_THREADS
    if (err) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_autocommit__doc__[] =
"Set the autocommit mode. True values enable; False value disable.\n\
";
static PyObject *
_mysql_ConnectionObject_autocommit(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    int flag, err;
    if (!PyArg_ParseTuple(args, "i", &flag)) return NULL;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    err = mysql_autocommit(&(self->connection), flag);
    Py_END_ALLOW_THREADS
    if (err) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_get_autocommit__doc__[] =
"Get the autocommit mode. True when enable; False when disable.\n";

static PyObject *
_mysql_ConnectionObject_get_autocommit(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    check_connection(self);
    if (self->connection.server_status & SERVER_STATUS_AUTOCOMMIT) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static char _mysql_ConnectionObject_commit__doc__[] =
"Commits the current transaction\n\
";
static PyObject *
_mysql_ConnectionObject_commit(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    int err;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    err = mysql_commit(&(self->connection));
    Py_END_ALLOW_THREADS
    if (err) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_rollback__doc__[] =
"Rolls back the current transaction\n\
";
static PyObject *
_mysql_ConnectionObject_rollback(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    int err;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    err = mysql_rollback(&(self->connection));
    Py_END_ALLOW_THREADS
    if (err) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_next_result__doc__[] =
"If more query results exist, next_result() reads the next query\n\
results and returns the status back to application.\n\
\n\
After calling next_result() the state of the connection is as if\n\
you had called query() for the next query. This means that you can\n\
now call store_result(), warning_count(), affected_rows()\n\
, and so forth. \n\
\n\
Returns 0 if there are more results; -1 if there are no more results\n\
\n\
Non-standard.\n\
";
static PyObject *
_mysql_ConnectionObject_next_result(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    int err;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    err = mysql_next_result(&(self->connection));
    Py_END_ALLOW_THREADS
    if (err > 0) return _mysql_Exception(self);
    return PyLong_FromLong(err);
}


static char _mysql_ConnectionObject_set_server_option__doc__[] =
"set_server_option(option) -- Enables or disables an option\n\
for the connection.\n\
\n\
Non-standard.\n\
";
static PyObject *
_mysql_ConnectionObject_set_server_option(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    int err, flags=0;
    if (!PyArg_ParseTuple(args, "i", &flags))
        return NULL;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    err = mysql_set_server_option(&(self->connection), flags);
    Py_END_ALLOW_THREADS
    if (err) return _mysql_Exception(self);
    return PyLong_FromLong(err);
}

static char _mysql_ConnectionObject_sqlstate__doc__[] =
"Returns a string containing the SQLSTATE error code\n\
for the last error. The error code consists of five characters.\n\
'00000' means \"no error.\" The values are specified by ANSI SQL\n\
and ODBC. For a list of possible values, see section 23\n\
Error Handling in MySQL in the MySQL Manual.\n\
\n\
Note that not all MySQL errors are yet mapped to SQLSTATE's.\n\
The value 'HY000' (general error) is used for unmapped errors.\n\
\n\
Non-standard.\n\
";
static PyObject *
_mysql_ConnectionObject_sqlstate(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyUnicode_FromString(mysql_sqlstate(&(self->connection)));
}

static char _mysql_ConnectionObject_warning_count__doc__[] =
"Returns the number of warnings generated during execution\n\
of the previous SQL statement.\n\
\n\
Non-standard.\n\
";
static PyObject *
_mysql_ConnectionObject_warning_count(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyLong_FromLong(mysql_warning_count(&(self->connection)));
}

static char _mysql_ConnectionObject_errno__doc__[] =
"Returns the error code for the most recently invoked API function\n\
that can succeed or fail. A return value of zero means that no error\n\
occurred.\n\
";

static PyObject *
_mysql_ConnectionObject_errno(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyLong_FromLong((long)mysql_errno(&(self->connection)));
}

static char _mysql_ConnectionObject_error__doc__[] =
"Returns the error message for the most recently invoked API function\n\
that can succeed or fail. An empty string ("") is returned if no error\n\
occurred.\n\
";

static PyObject *
_mysql_ConnectionObject_error(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyUnicode_FromString(mysql_error(&(self->connection)));
}

static char _mysql_escape_string__doc__[] =
"escape_string(s) -- quote any SQL-interpreted characters in string s.\n\
\n\
Use connection.escape_string(s), if you use it at all.\n\
_mysql.escape_string(s) cannot handle character sets. You are\n\
probably better off using connection.escape(o) instead, since\n\
it will escape entire sequences as well as strings.";

static PyObject *
_mysql_escape_string(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    PyObject *str;
    char *in, *out;
    unsigned long len;
    Py_ssize_t size;
    if (!PyArg_ParseTuple(args, "s#:escape_string", &in, &size)) return NULL;
    str = PyBytes_FromStringAndSize((char *) NULL, size*2+1);
    if (!str) return PyErr_NoMemory();
    out = PyBytes_AS_STRING(str);

    if (self && PyModule_Check((PyObject*)self))
        self = NULL;
    if (self && self->open) {
#if MYSQL_VERSION_ID >= 50707 && !defined(MARIADB_BASE_VERSION) && !defined(MARIADB_VERSION_ID)
        len = mysql_real_escape_string_quote(&(self->connection), out, in, size, '\'');
#else
        len = mysql_real_escape_string(&(self->connection), out, in, size);
#endif
    } else {
        len = mysql_escape_string(out, in, size);
    }
    if (_PyBytes_Resize(&str, len) < 0) return NULL;
    return (str);
}

static char _mysql_string_literal__doc__[] =
"string_literal(obj) -- converts object obj into a SQL string literal.\n\
This means, any special SQL characters are escaped, and it is enclosed\n\
within single quotes. In other words, it performs:\n\
\n\
\"'%s'\" % escape_string(str(obj))\n\
\n\
Use connection.string_literal(obj), if you use it at all.\n\
_mysql.string_literal(obj) cannot handle character sets.";

static PyObject *
_mysql_string_literal(
    _mysql_ConnectionObject *self,
    PyObject *o)
{
    PyObject *s; // input string or bytes. need to decref.

    if (self && PyModule_Check((PyObject*)self))
        self = NULL;

    if (PyBytes_Check(o)) {
        s = o;
        Py_INCREF(s);
    }
    else {
        PyObject *t = PyObject_Str(o);
        if (!t) return NULL;

        const char *encoding = (self && self->open) ?
            _get_encoding(&self->connection) : utf8;
        if (encoding == utf8) {
            s = t;
        }
        else {
            s = PyUnicode_AsEncodedString(t, encoding, "strict");
            Py_DECREF(t);
            if (!s) return NULL;
        }
    }

    // Prepare input string (in, size)
    const char *in;
    Py_ssize_t size;
    if (PyUnicode_Check(s)) {
        in = PyUnicode_AsUTF8AndSize(s, &size);
    } else {
        assert(PyBytes_Check(s));
        in = PyBytes_AsString(s);
        size = PyBytes_GET_SIZE(s);
    }

    // Prepare output buffer (str, out)
    PyObject *str = PyBytes_FromStringAndSize((char *) NULL, size*2+3);
    if (!str) {
        Py_DECREF(s);
        return PyErr_NoMemory();
    }
    char *out = PyBytes_AS_STRING(str);

    // escape
    unsigned long len;
    if (self && self->open) {
#if MYSQL_VERSION_ID >= 50707 && !defined(MARIADB_BASE_VERSION) && !defined(MARIADB_VERSION_ID)
        len = mysql_real_escape_string_quote(&(self->connection), out+1, in, size, '\'');
#else
        len = mysql_real_escape_string(&(self->connection), out+1, in, size);
#endif
    } else {
        len = mysql_escape_string(out+1, in, size);
    }

    Py_DECREF(s);
    *out = *(out+len+1) = '\'';
    if (_PyBytes_Resize(&str, len+2) < 0) {
        Py_DECREF(str);
        return NULL;
    }
    return str;
}

static PyObject *
_escape_item(
    PyObject *self,
    PyObject *item,
    PyObject *d)
{
    PyObject *quoted=NULL, *itemtype, *itemconv;
    if (!(itemtype = PyObject_Type(item))) {
        return NULL;
    }
    itemconv = PyObject_GetItem(d, itemtype);
    Py_DECREF(itemtype);
    if (!itemconv) {
        PyErr_Clear();
        return _mysql_string_literal((_mysql_ConnectionObject*)self, item);
    }
    Py_INCREF(d);
    quoted = PyObject_CallFunction(itemconv, "OO", item, d);
    Py_DECREF(d);
    Py_DECREF(itemconv);

    return quoted;
}

static char _mysql_escape__doc__[] =
"escape(obj, dict) -- escape any special characters in object obj\n\
using mapping dict to provide quoting functions for each type.\n\
Returns a SQL literal string.";
static PyObject *
_mysql_escape(
    PyObject *self,
    PyObject *args)
{
    PyObject *o=NULL, *d=NULL;
    if (!PyArg_ParseTuple(args, "O|O:escape", &o, &d))
        return NULL;
    if (d) {
        if (!PyMapping_Check(d)) {
            PyErr_SetString(PyExc_TypeError,
                    "argument 2 must be a mapping");
            return NULL;
        }
        return _escape_item(self, o, d);
    } else {
        if (!self) {
            PyErr_SetString(PyExc_TypeError,
                    "argument 2 must be a mapping");
            return NULL;
        }
        return _escape_item(self, o,
               ((_mysql_ConnectionObject *) self)->converter);
    }
}

static char _mysql_ResultObject_describe__doc__[] =
"Returns the sequence of 7-tuples required by the DB-API for\n\
the Cursor.description attribute.\n\
";

static PyObject *
_mysql_ResultObject_describe(
    _mysql_ResultObject *self,
    PyObject *noargs)
{
    PyObject *d;
    MYSQL_FIELD *fields;
    unsigned int i, n;

    check_result_connection(self);

    n = mysql_num_fields(self->result);
    fields = mysql_fetch_fields(self->result);
    if (!(d = PyTuple_New(n))) return NULL;
    for (i=0; i<n; i++) {
        PyObject *t;
        PyObject *name;
        if (self->encoding == utf8) {
            name = PyUnicode_DecodeUTF8(fields[i].name, fields[i].name_length, "replace");
        } else {
            name = PyUnicode_Decode(fields[i].name, fields[i].name_length, self->encoding, "replace");
        }
        if (name == NULL) {
            goto error;
        }

        t = Py_BuildValue("(Niiiiii)",
                  name,
                  (long) fields[i].type,
                  (long) fields[i].max_length,
                  (long) fields[i].length,
                  (long) fields[i].length,
                  (long) fields[i].decimals,
                  (long) !(IS_NOT_NULL(fields[i].flags)));
        if (!t) goto error;
        PyTuple_SET_ITEM(d, i, t);
    }
    return d;
  error:
    Py_XDECREF(d);
    return NULL;
}

static char _mysql_ResultObject_field_flags__doc__[] =
"Returns a tuple of field flags, one for each column in the result.\n\
" ;

static PyObject *
_mysql_ResultObject_field_flags(
    _mysql_ResultObject *self,
    PyObject *noargs)
{
    PyObject *d;
    MYSQL_FIELD *fields;
    unsigned int i, n;
    check_result_connection(self);
    n = mysql_num_fields(self->result);
    fields = mysql_fetch_fields(self->result);
    if (!(d = PyTuple_New(n))) return NULL;
    for (i=0; i<n; i++) {
        PyObject *f;
        if (!(f = PyLong_FromLong((long)fields[i].flags))) goto error;
        PyTuple_SET_ITEM(d, i, f);
    }
    return d;
  error:
    Py_XDECREF(d);
    return NULL;
}

static PyObject *
_mysql_field_to_python(
    PyObject *converter,
    const char *rowitem,
    Py_ssize_t length,
    MYSQL_FIELD *field,
    const char *encoding)
{
    if (rowitem == NULL) {
        Py_RETURN_NONE;
    }

    // Fast paths for int, string and binary.
    if (converter == (PyObject*)&PyUnicode_Type) {
        if (encoding == utf8) {
            //fprintf(stderr, "decoding with utf8!\n");
            return PyUnicode_DecodeUTF8(rowitem, length, NULL);
        } else {
            //fprintf(stderr, "decoding with %s\n", encoding);
            return PyUnicode_Decode(rowitem, length, encoding, NULL);
        }
    }
    if (converter == (PyObject*)&PyBytes_Type || converter == Py_None) {
        //fprintf(stderr, "decoding with bytes\n", encoding);
        return PyBytes_FromStringAndSize(rowitem, length);
    }
    if (converter == (PyObject*)&PyLong_Type) {
        //fprintf(stderr, "decoding with int\n", encoding);
        return PyLong_FromString(rowitem, NULL, 10);
    }

    //fprintf(stderr, "decoding with callback\n");
    //PyObject_Print(converter, stderr, 0);
    //fprintf(stderr, "\n");
    int binary;
    switch (field->type) {
    case FIELD_TYPE_DECIMAL:
    case FIELD_TYPE_NEWDECIMAL:
    case FIELD_TYPE_TIMESTAMP:
    case FIELD_TYPE_DATETIME:
    case FIELD_TYPE_TIME:
    case FIELD_TYPE_DATE:
        binary = 0;  // pass str, because these converters expect it
        break;
    default: // Default to just passing bytes
        binary = 1;
    }
    return PyObject_CallFunction(converter,
            binary ? "y#" : "s#",
            rowitem, (Py_ssize_t)length);
}

static PyObject *
_mysql_row_to_tuple(
    _mysql_ResultObject *self,
    MYSQL_ROW row,
    PyObject *unused)
{
    unsigned int n, i;
    unsigned long *length;
    PyObject *r, *c;
    MYSQL_FIELD *fields;

    n = mysql_num_fields(self->result);
    if (!(r = PyTuple_New(n))) return NULL;
    length = mysql_fetch_lengths(self->result);
    fields = mysql_fetch_fields(self->result);
    for (i=0; i<n; i++) {
        PyObject *v;
        c = PyTuple_GET_ITEM(self->converter, i);
        v = _mysql_field_to_python(c, row[i], length[i], &fields[i], self->encoding);
        if (!v) goto error;
        PyTuple_SET_ITEM(r, i, v);
    }
    return r;
  error:
    Py_XDECREF(r);
    return NULL;
}

static PyObject *
_mysql_row_to_dict(
    _mysql_ResultObject *self,
    MYSQL_ROW row,
    PyObject *cache)
{
    unsigned int n, i;
    unsigned long *length;
    PyObject *r, *c;
    MYSQL_FIELD *fields;

    n = mysql_num_fields(self->result);
    if (!(r = PyDict_New())) return NULL;
    length = mysql_fetch_lengths(self->result);
    fields = mysql_fetch_fields(self->result);
    for (i=0; i<n; i++) {
        PyObject *v;
        c = PyTuple_GET_ITEM(self->converter, i);
        v = _mysql_field_to_python(c, row[i], length[i], &fields[i], self->encoding);
        if (!v) goto error;

        PyObject *pyname = PyUnicode_FromString(fields[i].name);
        if (pyname == NULL) {
            Py_DECREF(v);
            goto error;
        }
        int err = PyDict_Contains(r, pyname);
        if (err < 0) { // error
            Py_DECREF(v);
            goto error;
        }
        if (err) { // duplicate
            Py_DECREF(pyname);
            pyname = PyUnicode_FromFormat("%s.%s", fields[i].table, fields[i].name);
            if (pyname == NULL) {
                Py_DECREF(v);
                goto error;
            }
        }

        err = PyDict_SetItem(r, pyname, v);
        if (cache) {
            PyTuple_SET_ITEM(cache, i, pyname);
        } else {
            Py_DECREF(pyname);
        }
        Py_DECREF(v);
        if (err) {
            goto error;
        }
    }
    return r;
error:
    Py_DECREF(r);
    return NULL;
}

static PyObject *
_mysql_row_to_dict_old(
    _mysql_ResultObject *self,
    MYSQL_ROW row,
    PyObject *cache)
{
    unsigned int n, i;
    unsigned long *length;
    PyObject *r, *c;
    MYSQL_FIELD *fields;

    n = mysql_num_fields(self->result);
    if (!(r = PyDict_New())) return NULL;
    length = mysql_fetch_lengths(self->result);
    fields = mysql_fetch_fields(self->result);
    for (i=0; i<n; i++) {
        PyObject *v;
        c = PyTuple_GET_ITEM(self->converter, i);
        v = _mysql_field_to_python(c, row[i], length[i], &fields[i], self->encoding);
        if (!v) {
            goto error;
        }

        PyObject *pyname;
        if (strlen(fields[i].table)) {
            pyname = PyUnicode_FromFormat("%s.%s", fields[i].table, fields[i].name);
        } else {
            pyname = PyUnicode_FromString(fields[i].name);
        }
        int err = PyDict_SetItem(r, pyname, v);
        Py_DECREF(v);
        if (cache) {
            PyTuple_SET_ITEM(cache, i, pyname);
        } else {
            Py_DECREF(pyname);
        }
        if (err) {
            goto error;
        }
    }
    return r;
  error:
    Py_XDECREF(r);
    return NULL;
}

static PyObject *
_mysql_row_to_dict_cached(
    _mysql_ResultObject *self,
    MYSQL_ROW row,
    PyObject *cache)
{
    PyObject *r = PyDict_New();
    if (!r) {
        return NULL;
    }

    unsigned int n = mysql_num_fields(self->result);
    unsigned long *length = mysql_fetch_lengths(self->result);
    MYSQL_FIELD *fields = mysql_fetch_fields(self->result);

    for (unsigned int i=0; i<n; i++) {
        PyObject *c = PyTuple_GET_ITEM(self->converter, i);
        PyObject *v = _mysql_field_to_python(c, row[i], length[i], &fields[i], self->encoding);
        if (!v) {
            goto error;
        }

        PyObject *pyname = PyTuple_GET_ITEM(cache, i); // borrowed
        int err = PyDict_SetItem(r, pyname, v);
        Py_DECREF(v);
        if (err) {
            goto error;
        }
    }
    return r;
  error:
    Py_XDECREF(r);
    return NULL;
}


typedef PyObject *_convertfunc(_mysql_ResultObject *, MYSQL_ROW, PyObject *);
static _convertfunc * const row_converters[] = {
    _mysql_row_to_tuple,
    _mysql_row_to_dict,
    _mysql_row_to_dict_old
};

Py_ssize_t
_mysql__fetch_row(
    _mysql_ResultObject *self,
    PyObject *r, /* list object */
    Py_ssize_t maxrows,
    int how)
{
    _convertfunc *convert_row = row_converters[how];

    PyObject *cache = NULL;
    if (maxrows > 0 && how > 0) {
        cache = PyTuple_New(mysql_num_fields(self->result));
        if (!cache) {
            return -1;
        }
    }

    Py_ssize_t i;
    for (i = 0; i < maxrows; i++) {
        MYSQL_ROW row;
        if (!self->use)
            row = mysql_fetch_row(self->result);
        else {
            Py_BEGIN_ALLOW_THREADS
            row = mysql_fetch_row(self->result);
            Py_END_ALLOW_THREADS
        }
        if (!row && mysql_errno(&(((_mysql_ConnectionObject *)(self->conn))->connection))) {
            _mysql_Exception((_mysql_ConnectionObject *)self->conn);
            goto error;
        }
        if (!row) {
            break;
        }
        PyObject *v = convert_row(self, row, cache);
        if (!v) {
            goto error;
        }
        if (cache) {
            convert_row = _mysql_row_to_dict_cached;
        }
        if (PyList_Append(r, v)) {
            Py_DECREF(v);
            goto error;
        }
        Py_DECREF(v);
    }
    Py_XDECREF(cache);
    return i;
error:
    Py_XDECREF(cache);
    return -1;
}

static char _mysql_ResultObject_fetch_row__doc__[] =
"fetch_row([maxrows, how]) -- Fetches up to maxrows as a tuple.\n\
The rows are formatted according to how:\n\
\n\
    0 -- tuples (default)\n\
    1 -- dictionaries, key=column or table.column if duplicated\n\
    2 -- dictionaries, key=table.column\n\
";

static PyObject *
_mysql_ResultObject_fetch_row(
    _mysql_ResultObject *self,
    PyObject *args,
    PyObject *kwargs)
{
    static char *kwlist[] = {"maxrows", "how", NULL };
    int maxrows=1, how=0;
    PyObject *r=NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|ii:fetch_row", kwlist,
                     &maxrows, &how))
        return NULL;
    check_result_connection(self);
    if (how >= (int)(sizeof(row_converters) / sizeof(row_converters[0]))) {
        PyErr_SetString(PyExc_ValueError, "how out of range");
        return NULL;
    }
    if (!maxrows) {
        if (self->use) {
            maxrows = INT_MAX;
        } else {
            // todo: preallocate.
            maxrows = (Py_ssize_t) mysql_num_rows(self->result);
        }
    }
    if (!(r = PyList_New(0))) goto error;
    Py_ssize_t rowsadded = _mysql__fetch_row(self, r, maxrows, how);
    if (rowsadded == -1) goto error;

    /* DB-API allows return rows as list.
     * But we need to return list because Django expecting tuple.
     */
    PyObject *t = PyList_AsTuple(r);
    Py_DECREF(r);
    return t;
  error:
    Py_XDECREF(r);
    return NULL;
}

static const char _mysql_ResultObject_discard__doc__[] =
"discard() -- Discard remaining rows in the resultset.";

static PyObject *
_mysql_ResultObject_discard(
    _mysql_ResultObject *self,
    PyObject *noargs)
{
    check_result_connection(self);

    MYSQL_ROW row;
    Py_BEGIN_ALLOW_THREADS
    while (NULL != (row = mysql_fetch_row(self->result))) {
        // do nothing
    }
    Py_END_ALLOW_THREADS
    _mysql_ConnectionObject *conn = (_mysql_ConnectionObject *)self->conn;
    if (mysql_errno(&conn->connection)) {
        return _mysql_Exception(conn);
    }
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_change_user__doc__[] =
"Changes the user and causes the database specified by db to\n\
become the default (current) database on the connection\n\
specified by mysql. In subsequent queries, this database is\n\
the default for table references that do not include an\n\
explicit database specifier.\n\
\n\
This function was introduced in MySQL Version 3.23.3.\n\
\n\
Fails unless the connected user can be authenticated or if he\n\
doesn't have permission to use the database. In this case the\n\
user and database are not changed.\n\
\n\
The db parameter may be set to None if you don't want to have\n\
a default database.\n\
";

static PyObject *
_mysql_ConnectionObject_change_user(
    _mysql_ConnectionObject *self,
    PyObject *args,
    PyObject *kwargs)
{
    char *user, *pwd=NULL, *db=NULL;
    int r;
    static char *kwlist[] = { "user", "passwd", "db", NULL } ;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|ss:change_user",
                     kwlist, &user, &pwd, &db))
        return NULL;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
        r = mysql_change_user(&(self->connection), user, pwd, db);
    Py_END_ALLOW_THREADS
    if (r)     return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_character_set_name__doc__[] =
"Returns the default character set for the current connection.\n\
Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_character_set_name(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    const char *s;
    check_connection(self);
    s = mysql_character_set_name(&(self->connection));
    return PyUnicode_FromString(s);
}

static char _mysql_ConnectionObject_set_character_set__doc__[] =
"Sets the default character set for the current connection.\n\
Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_set_character_set(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    const char *s;
    int err;
    if (!PyArg_ParseTuple(args, "s", &s)) return NULL;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    err = mysql_set_character_set(&(self->connection), s);
    Py_END_ALLOW_THREADS
    if (err) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

#if MYSQL_VERSION_ID >= 50010
static char _mysql_ConnectionObject_get_character_set_info__doc__[] =
"Returns a dict with information about the current character set:\n\
\n\
collation\n\
    collation name\n\
name\n\
    character set name\n\
comment\n\
    comment or descriptive name\n\
dir\n\
    character set directory\n\
mbminlen\n\
    min. length for multibyte string\n\
mbmaxlen\n\
    max. length for multibyte string\n\
\n\
Not all keys may be present, particularly dir.\n\
\n\
Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_get_character_set_info(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    PyObject *result;
    MY_CHARSET_INFO cs;

    check_connection(self);
    mysql_get_character_set_info(&(self->connection), &cs);
    if (!(result = PyDict_New())) return NULL;
    if (cs.csname)
        PyDict_SetItemString(result, "name", PyUnicode_FromString(cs.csname));
    if (cs.name)
        PyDict_SetItemString(result, "collation", PyUnicode_FromString(cs.name));
    if (cs.comment)
        PyDict_SetItemString(result, "comment", PyUnicode_FromString(cs.comment));
    if (cs.dir)
        PyDict_SetItemString(result, "dir", PyUnicode_FromString(cs.dir));
    PyDict_SetItemString(result, "mbminlen", PyLong_FromLong(cs.mbminlen));
    PyDict_SetItemString(result, "mbmaxlen", PyLong_FromLong(cs.mbmaxlen));
    return result;
}
#endif

static char _mysql_ConnectionObject_get_native_connection__doc__[] =
"Return the internal MYSQL* wrapped in a PyCapsule object.\n\
NOTE: this is a private API introduced ONLY for XTA integration,\n\
      don't use it for different use cases.\n\
      This method is supported only for XTA integration and support must\n\
      be asked to LIXA project: http://www.tiian.org/lixa/\n\
      Please DO NOT ask support to PyMySQL/mysqlclient-python project.\n\
";

static PyObject *
_mysql_ConnectionObject_get_native_connection(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    PyObject *result;
    check_connection(self);
    result = PyCapsule_New(&(self->connection),
        "_mysql.connection.native_connection", NULL);
    return result;
}


static char _mysql_get_client_info__doc__[] =
"get_client_info() -- Returns a string that represents\n\
the client library version.";
static PyObject *
_mysql_get_client_info(
    PyObject *self,
    PyObject *noargs)
{
    return PyUnicode_FromString(mysql_get_client_info());
}

static char _mysql_ConnectionObject_get_host_info__doc__[] =
"Returns a string that represents the MySQL client library\n\
version. Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_get_host_info(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyUnicode_FromString(mysql_get_host_info(&(self->connection)));
}

static char _mysql_ConnectionObject_get_proto_info__doc__[] =
"Returns an unsigned integer representing the protocol version\n\
used by the current connection. Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_get_proto_info(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyLong_FromLong((long)mysql_get_proto_info(&(self->connection)));
}

static char _mysql_ConnectionObject_get_server_info__doc__[] =
"Returns a string that represents the server version number.\n\
Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_get_server_info(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyUnicode_FromString(mysql_get_server_info(&(self->connection)));
}

static char _mysql_ConnectionObject_info__doc__[] =
"Retrieves a string providing information about the most\n\
recently executed query. Non-standard. Use messages or\n\
Cursor.messages.\n\
";

static PyObject *
_mysql_ConnectionObject_info(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    const char *s;
    check_connection(self);
    s = mysql_info(&(self->connection));
    if (s) return PyUnicode_FromString(s);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_insert_id__doc__[] =
"Returns the ID generated for an AUTO_INCREMENT column by the previous\n\
query. Use this function after you have performed an INSERT query into a\n\
table that contains an AUTO_INCREMENT field.\n\
\n\
Note that this returns 0 if the previous query does not\n\
generate an AUTO_INCREMENT value. If you need to save the value for\n\
later, be sure to call this immediately after the query\n\
that generates the value.\n\
\n\
The ID is updated after INSERT and UPDATE statements that generate\n\
an AUTO_INCREMENT value or that set a column value to\n\
LAST_INSERT_ID(expr). See section 6.3.5.2 Miscellaneous Functions\n\
in the MySQL documentation.\n\
\n\
Also note that the value of the SQL LAST_INSERT_ID() function always\n\
contains the most recently generated AUTO_INCREMENT value, and is not\n\
reset between queries because the value of that function is maintained\n\
in the server.\n\
" ;

static PyObject *
_mysql_ConnectionObject_insert_id(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    my_ulonglong r;
    check_connection(self);
    r = mysql_insert_id(&(self->connection));
    return PyLong_FromUnsignedLongLong(r);
}

static char _mysql_ConnectionObject_kill__doc__[] =
"Asks the server to kill the thread specified by pid.\n\
Non-standard. Deprecated.";

static PyObject *
_mysql_ConnectionObject_kill(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    unsigned long pid;
    int r;
    char query[50];
    if (!PyArg_ParseTuple(args, "k:kill", &pid)) return NULL;
    check_connection(self);
    snprintf(query, 50, "KILL %lu", pid);
    Py_BEGIN_ALLOW_THREADS
    r = mysql_query(&(self->connection), query);
    Py_END_ALLOW_THREADS
    if (r) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_field_count__doc__[] =
"Returns the number of columns for the most recent query on the\n\
connection. Non-standard. Will probably give you bogus results\n\
on most cursor classes. Use Cursor.rowcount.\n\
";

static PyObject *
_mysql_ConnectionObject_field_count(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyLong_FromLong((long)mysql_field_count(&(self->connection)));
}

static char _mysql_ConnectionObject_fileno__doc__[] =
"Return file descriptor of the underlying libmysqlclient connection.\n\
This provides raw access to the underlying network connection.\n\
";

static PyObject *
_mysql_ConnectionObject_fileno(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    return PyLong_FromLong(self->connection.net.fd);
}

static char _mysql_ResultObject_num_fields__doc__[] =
"Returns the number of fields (column) in the result." ;

static PyObject *
_mysql_ResultObject_num_fields(
    _mysql_ResultObject *self,
    PyObject *noargs)
{
    check_result_connection(self);
    return PyLong_FromLong((long)mysql_num_fields(self->result));
}

static char _mysql_ResultObject_num_rows__doc__[] =
"Returns the number of rows in the result set. Note that if\n\
use=1, this will not return a valid value until the entire result\n\
set has been read.\n\
";

static PyObject *
_mysql_ResultObject_num_rows(
    _mysql_ResultObject *self,
    PyObject *noargs)
{
    check_result_connection(self);
    return PyLong_FromUnsignedLongLong(mysql_num_rows(self->result));
}

static char _mysql_ConnectionObject_ping__doc__[] =
"Checks whether or not the connection to the server is working.\n\
\n\
This function can be used by clients that remain idle for a\n\
long while, to check whether or not the server has closed the\n\
connection.\n\
\n\
New in 1.2.2: Accepts an optional reconnect parameter. If True,\n\
then the client will attempt reconnection. Note that this setting\n\
is persistent. By default, this is on in MySQL<5.0.3, and off\n\
thereafter.\n\
MySQL 8.0.33 deprecated the MYSQL_OPT_RECONNECT option so reconnect\n\
parameter is also deprecated in mysqlclient 2.2.1.\n\
\n\
Non-standard. You should assume that ping() performs an\n\
implicit rollback; use only when starting a new transaction.\n\
You have been warned.\n\
";

static PyObject *
_mysql_ConnectionObject_ping(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    int reconnect = 0;
    if (!PyArg_ParseTuple(args, "|p", &reconnect)) return NULL;
    check_connection(self);
    if (reconnect != (self->reconnect == true)) {
        // libmysqlclient show warning to stderr when MYSQL_OPT_RECONNECT is used.
        // so we avoid using it as possible for now.
        // TODO: Warn when reconnect is true.
        // MySQL 8.0.33 show warning to stderr already.
        // We will emit Pytohn warning in future.
        my_bool recon = (my_bool)reconnect;
        mysql_options(&self->connection, MYSQL_OPT_RECONNECT, &recon);
        self->reconnect = (bool)reconnect;
    }
    int r;
    Py_BEGIN_ALLOW_THREADS
    r = mysql_ping(&(self->connection));
    Py_END_ALLOW_THREADS
    if (r) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_query__doc__[] =
"Execute a query. store_result() or use_result() will get the\n\
result set, if any. Non-standard. Use cursor() to create a cursor,\n\
then cursor.execute().\n\
" ;

static PyObject *
_mysql_ConnectionObject_query(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    char *query;
    Py_ssize_t len;
    int r;
    if (!PyArg_ParseTuple(args, "s#:query", &query, &len)) return NULL;
    check_connection(self);

    Py_BEGIN_ALLOW_THREADS
    r = mysql_real_query(&(self->connection), query, len);
    Py_END_ALLOW_THREADS
    if (r) return _mysql_Exception(self);
    Py_RETURN_NONE;
}


static char _mysql_ConnectionObject_send_query__doc__[] =
"Send a query. Same to query() except not wait response.\n\n\
Use read_query_result() before calling store_result() or use_result()\n";

static PyObject *
_mysql_ConnectionObject_send_query(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    char *query;
    Py_ssize_t len;
    int r;
    MYSQL *mysql = &(self->connection);
    if (!PyArg_ParseTuple(args, "s#:query", &query, &len)) return NULL;
    check_connection(self);

    Py_BEGIN_ALLOW_THREADS
    r = mysql_send_query(mysql, query, len);
    Py_END_ALLOW_THREADS
    if (r) return _mysql_Exception(self);
    Py_RETURN_NONE;
}


static char _mysql_ConnectionObject_read_query_result__doc__[] =
"Read result of query sent by send_query().\n";

static PyObject *
_mysql_ConnectionObject_read_query_result(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    int r;
    MYSQL *mysql = &(self->connection);
    check_connection(self);

    Py_BEGIN_ALLOW_THREADS
    r = (int)mysql_read_query_result(mysql);
    Py_END_ALLOW_THREADS
    if (r) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_select_db__doc__[] =
"Causes the database specified by db to become the default\n\
(current) database on the connection specified by mysql. In subsequent\n\
queries, this database is the default for table references that do not\n\
include an explicit database specifier.\n\
\n\
Fails unless the connected user can be authenticated as having\n\
permission to use the database.\n\
\n\
Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_select_db(
    _mysql_ConnectionObject *self,
    PyObject *args)
{
    char *db;
    int r;
    if (!PyArg_ParseTuple(args, "s:select_db", &db)) return NULL;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    r = mysql_select_db(&(self->connection), db);
    Py_END_ALLOW_THREADS
    if (r)     return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_shutdown__doc__[] =
"Asks the database server to shut down. The connected user must\n\
have shutdown privileges. Non-standard. Deprecated.\n\
";

static PyObject *
_mysql_ConnectionObject_shutdown(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    int r;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    r = mysql_query(&(self->connection), "SHUTDOWN");
    Py_END_ALLOW_THREADS
    if (r) return _mysql_Exception(self);
    Py_RETURN_NONE;
}

static char _mysql_ConnectionObject_stat__doc__[] =
"Returns a character string containing information similar to\n\
that provided by the mysqladmin status command. This includes\n\
uptime in seconds and the number of running threads,\n\
questions, reloads, and open tables. Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_stat(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    const char *s;
    check_connection(self);
    Py_BEGIN_ALLOW_THREADS
    s = mysql_stat(&(self->connection));
    Py_END_ALLOW_THREADS
    if (!s) return _mysql_Exception(self);
    return PyUnicode_FromString(s);
}

static char _mysql_ConnectionObject_store_result__doc__[] =
"Returns a result object acquired by mysql_store_result\n\
(results stored in the client). If no results are available,\n\
None is returned. Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_store_result(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    PyObject *arglist=NULL, *kwarglist=NULL, *result=NULL;
    _mysql_ResultObject *r=NULL;

    check_connection(self);
    arglist = Py_BuildValue("(OiO)", self, 0, self->converter);
    if (!arglist) goto error;
    kwarglist = PyDict_New();
    if (!kwarglist) goto error;
    r = MyAlloc(_mysql_ResultObject, _mysql_ResultObject_Type);
    if (!r) goto error;
    if (_mysql_ResultObject_Initialize(r, arglist, kwarglist)) {
        Py_DECREF(r);
        goto error;
    }
    result = (PyObject *) r;
    if (!(r->result)) {
        Py_DECREF(result);
        Py_INCREF(Py_None);
        result = Py_None;
    }
  error:
    Py_XDECREF(arglist);
    Py_XDECREF(kwarglist);
    return result;
}

static char _mysql_ConnectionObject_thread_id__doc__[] =
"Returns the thread ID of the current connection. This value\n\
can be used as an argument to kill() to kill the thread.\n\
\n\
If the connection is lost and you reconnect with ping(), the\n\
thread ID will change. This means you should not get the\n\
thread ID and store it for later. You should get it when you\n\
need it.\n\
\n\
Non-standard.";

static PyObject *
_mysql_ConnectionObject_thread_id(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    unsigned long pid;
    check_connection(self);
    pid = mysql_thread_id(&(self->connection));
    return PyLong_FromLong((long)pid);
}

static char _mysql_ConnectionObject_use_result__doc__[] =
"Returns a result object acquired by mysql_use_result\n\
(results stored in the server). If no results are available,\n\
None is returned. Non-standard.\n\
";

static PyObject *
_mysql_ConnectionObject_use_result(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    PyObject *arglist=NULL, *kwarglist=NULL, *result=NULL;
    _mysql_ResultObject *r=NULL;

    check_connection(self);
    arglist = Py_BuildValue("(OiO)", self, 1, self->converter);
    if (!arglist) return NULL;
    kwarglist = PyDict_New();
    if (!kwarglist) goto error;
    r = MyAlloc(_mysql_ResultObject, _mysql_ResultObject_Type);
    if (!r) goto error;
    if (_mysql_ResultObject_Initialize(r, arglist, kwarglist)) {
        Py_DECREF(r);
        goto error;
    }
    result = (PyObject *) r;
    if (!(r->result)) {
        Py_DECREF(result);
        Py_INCREF(Py_None);
        result = Py_None;
    }
  error:
    Py_DECREF(arglist);
    Py_XDECREF(kwarglist);
    return result;
}

static const char _mysql_ConnectionObject_discard_result__doc__[] =
"Discard current result set.\n\n"
"This function can be called instead of use_result() or store_result(). Non-standard.";

static PyObject *
_mysql_ConnectionObject_discard_result(
    _mysql_ConnectionObject *self,
    PyObject *noargs)
{
    check_connection(self);
    MYSQL *conn = &(self->connection);

    Py_BEGIN_ALLOW_THREADS;

    MYSQL_RES *res = mysql_use_result(conn);
    if (res == NULL) {
        Py_BLOCK_THREADS;
        if (mysql_errno(conn) != 0) {
            // fprintf(stderr, "mysql_use_result failed: %s\n", mysql_error(conn));
            return _mysql_Exception(self);
        }
        Py_RETURN_NONE;
    }

    MYSQL_ROW row;
    while (NULL != (row = mysql_fetch_row(res))) {
        // do nothing.
    }
    mysql_free_result(res);
    Py_END_ALLOW_THREADS;
    if (mysql_errno(conn)) {
        // fprintf(stderr, "mysql_free_result failed: %s\n", mysql_error(conn));
        return _mysql_Exception(self);
    }
    Py_RETURN_NONE;
}

static void
_mysql_ConnectionObject_dealloc(
    _mysql_ConnectionObject *self)
{
    PyObject_GC_UnTrack(self);
    if (self->open) {
        mysql_close(&(self->connection));
        self->open = false;
    }
    Py_CLEAR(self->converter);
    MyFree(self);
}

static PyObject *
_mysql_ConnectionObject_repr(
    _mysql_ConnectionObject *self)
{
    char buf[300];
    if (self->open)
        snprintf(buf, 300, "<_mysql.connection open to '%.256s' at %p>",
            self->connection.host, self);
    else
        snprintf(buf, 300, "<_mysql.connection closed at %p>", self);
    return PyUnicode_FromString(buf);
}

static char _mysql_ResultObject_data_seek__doc__[] =
"data_seek(n) -- seek to row n of result set";
static PyObject *
_mysql_ResultObject_data_seek(
     _mysql_ResultObject *self,
     PyObject *args)
{
    unsigned int row;
    if (!PyArg_ParseTuple(args, "i:data_seek", &row)) return NULL;
    check_result_connection(self);
    mysql_data_seek(self->result, row);
    Py_RETURN_NONE;
}

static void
_mysql_ResultObject_dealloc(
    _mysql_ResultObject *self)
{
    PyObject_GC_UnTrack((PyObject *)self);
    mysql_free_result(self->result);
    _mysql_ResultObject_clear(self);
    MyFree(self);
}

static PyObject *
_mysql_ResultObject_repr(
    _mysql_ResultObject *self)
{
    char buf[300];
    snprintf(buf, 300, "<_mysql.result object at %p>", self);
    return PyUnicode_FromString(buf);
}

static PyMethodDef _mysql_ConnectionObject_methods[] = {
    {
        "affected_rows",
        (PyCFunction)_mysql_ConnectionObject_affected_rows,
        METH_NOARGS,
        _mysql_ConnectionObject_affected_rows__doc__
    },
    {
        "autocommit",
        (PyCFunction)_mysql_ConnectionObject_autocommit,
        METH_VARARGS,
        _mysql_ConnectionObject_autocommit__doc__
    },
    {
        "get_autocommit",
        (PyCFunction)_mysql_ConnectionObject_get_autocommit,
        METH_NOARGS,
        _mysql_ConnectionObject_get_autocommit__doc__
    },
    {
        "commit",
        (PyCFunction)_mysql_ConnectionObject_commit,
        METH_NOARGS,
        _mysql_ConnectionObject_commit__doc__
    },
    {
        "rollback",
        (PyCFunction)_mysql_ConnectionObject_rollback,
        METH_NOARGS,
        _mysql_ConnectionObject_rollback__doc__
    },
    {
        "next_result",
        (PyCFunction)_mysql_ConnectionObject_next_result,
        METH_NOARGS,
        _mysql_ConnectionObject_next_result__doc__
    },
    {
        "set_server_option",
        (PyCFunction)_mysql_ConnectionObject_set_server_option,
        METH_VARARGS,
        _mysql_ConnectionObject_set_server_option__doc__
    },
    {
        "sqlstate",
        (PyCFunction)_mysql_ConnectionObject_sqlstate,
        METH_NOARGS,
        _mysql_ConnectionObject_sqlstate__doc__
    },
    {
        "warning_count",
        (PyCFunction)_mysql_ConnectionObject_warning_count,
        METH_NOARGS,
        _mysql_ConnectionObject_warning_count__doc__
    },
    {
        "change_user",
        (PyCFunction)_mysql_ConnectionObject_change_user,
        METH_VARARGS | METH_KEYWORDS,
        _mysql_ConnectionObject_change_user__doc__
    },
    {
        "character_set_name",
        (PyCFunction)_mysql_ConnectionObject_character_set_name,
        METH_NOARGS,
        _mysql_ConnectionObject_character_set_name__doc__
    },
    {
        "set_character_set",
        (PyCFunction)_mysql_ConnectionObject_set_character_set,
        METH_VARARGS,
        _mysql_ConnectionObject_set_character_set__doc__
    },
#if MYSQL_VERSION_ID >= 50010
    {
        "get_character_set_info",
        (PyCFunction)_mysql_ConnectionObject_get_character_set_info,
        METH_NOARGS,
        _mysql_ConnectionObject_get_character_set_info__doc__
    },
#endif
    {
        "_get_native_connection",
        (PyCFunction)_mysql_ConnectionObject_get_native_connection,
        METH_NOARGS,
        _mysql_ConnectionObject_get_native_connection__doc__
    },
    {
        "close",
        (PyCFunction)_mysql_ConnectionObject_close,
        METH_NOARGS,
        _mysql_ConnectionObject_close__doc__
    },
    {
        "dump_debug_info",
        (PyCFunction)_mysql_ConnectionObject_dump_debug_info,
        METH_NOARGS,
        _mysql_ConnectionObject_dump_debug_info__doc__
    },
    {
        "escape",
        (PyCFunction)_mysql_escape,
        METH_VARARGS,
        _mysql_escape__doc__
    },
    {
        "escape_string",
        (PyCFunction)_mysql_escape_string,
        METH_VARARGS,
        _mysql_escape_string__doc__
    },
    {
        "error",
        (PyCFunction)_mysql_ConnectionObject_error,
        METH_NOARGS,
        _mysql_ConnectionObject_error__doc__
    },
    {
        "errno",
        (PyCFunction)_mysql_ConnectionObject_errno,
        METH_NOARGS,
        _mysql_ConnectionObject_errno__doc__
    },
    {
        "field_count",
        (PyCFunction)_mysql_ConnectionObject_field_count,
        METH_NOARGS,
        _mysql_ConnectionObject_field_count__doc__
    },
    {
        "fileno",
        (PyCFunction)_mysql_ConnectionObject_fileno,
        METH_NOARGS,
        _mysql_ConnectionObject_fileno__doc__
    },
    {
        "get_host_info",
        (PyCFunction)_mysql_ConnectionObject_get_host_info,
        METH_NOARGS,
        _mysql_ConnectionObject_get_host_info__doc__
    },
    {
        "get_proto_info",
        (PyCFunction)_mysql_ConnectionObject_get_proto_info,
        METH_NOARGS,
        _mysql_ConnectionObject_get_proto_info__doc__
    },
    {
        "get_server_info",
        (PyCFunction)_mysql_ConnectionObject_get_server_info,
        METH_NOARGS,
        _mysql_ConnectionObject_get_server_info__doc__
    },
    {
        "info",
        (PyCFunction)_mysql_ConnectionObject_info,
        METH_NOARGS,
        _mysql_ConnectionObject_info__doc__
    },
    {
        "insert_id",
        (PyCFunction)_mysql_ConnectionObject_insert_id,
        METH_NOARGS,
        _mysql_ConnectionObject_insert_id__doc__
    },
    {
        "kill",
        (PyCFunction)_mysql_ConnectionObject_kill,
        METH_VARARGS,
        _mysql_ConnectionObject_kill__doc__
    },
    {
        "ping",
        (PyCFunction)_mysql_ConnectionObject_ping,
        METH_VARARGS,
        _mysql_ConnectionObject_ping__doc__
    },
    {
        "query",
        (PyCFunction)_mysql_ConnectionObject_query,
        METH_VARARGS,
        _mysql_ConnectionObject_query__doc__
    },
    {
        "send_query",
        (PyCFunction)_mysql_ConnectionObject_send_query,
        METH_VARARGS,
        _mysql_ConnectionObject_send_query__doc__,
    },
    {
        "read_query_result",
        (PyCFunction)_mysql_ConnectionObject_read_query_result,
        METH_NOARGS,
        _mysql_ConnectionObject_read_query_result__doc__,
    },
    {
        "select_db",
        (PyCFunction)_mysql_ConnectionObject_select_db,
        METH_VARARGS,
        _mysql_ConnectionObject_select_db__doc__
    },
    {
        "shutdown",
        (PyCFunction)_mysql_ConnectionObject_shutdown,
        METH_NOARGS,
        _mysql_ConnectionObject_shutdown__doc__
    },
    {
        "stat",
        (PyCFunction)_mysql_ConnectionObject_stat,
        METH_NOARGS,
        _mysql_ConnectionObject_stat__doc__
    },
    {
        "store_result",
        (PyCFunction)_mysql_ConnectionObject_store_result,
        METH_NOARGS,
        _mysql_ConnectionObject_store_result__doc__
    },
    {
        "string_literal",
        (PyCFunction)_mysql_string_literal,
        METH_O,
        _mysql_string_literal__doc__},
    {
        "thread_id",
        (PyCFunction)_mysql_ConnectionObject_thread_id,
        METH_NOARGS,
        _mysql_ConnectionObject_thread_id__doc__
    },
    {
        "use_result",
        (PyCFunction)_mysql_ConnectionObject_use_result,
        METH_NOARGS,
        _mysql_ConnectionObject_use_result__doc__
    },
    {
        "discard_result",
        (PyCFunction)_mysql_ConnectionObject_discard_result,
        METH_NOARGS,
        _mysql_ConnectionObject_discard_result__doc__
    },
    {NULL,              NULL} /* sentinel */
};

static struct PyMemberDef _mysql_ConnectionObject_memberlist[] = {
    {
        "open",
        T_INT,
        offsetof(_mysql_ConnectionObject,open),
        READONLY,
        "True if connection is open"
    },
    {
        "converter",
        T_OBJECT,
        offsetof(_mysql_ConnectionObject,converter),
        0,
        "Type conversion mapping"
    },
    {
        "server_capabilities",
        T_ULONG,
        offsetof(_mysql_ConnectionObject,connection.server_capabilities),
        READONLY,
        "Capabilities of server; consult MySQLdb.constants.CLIENT"
    },
    {
        "port",
        T_UINT,
        offsetof(_mysql_ConnectionObject,connection.port),
        READONLY,
        "TCP/IP port of the server connection"
    },
    {
        "client_flag",
        T_ULONG,
        offsetof(_mysql_ConnectionObject,connection.client_flag),
        READONLY,
        "Client flags; refer to MySQLdb.constants.CLIENT"
    },
    {NULL} /* Sentinel */
};

static PyMethodDef _mysql_ResultObject_methods[] = {
    {
        "data_seek",
        (PyCFunction)_mysql_ResultObject_data_seek,
        METH_VARARGS,
        _mysql_ResultObject_data_seek__doc__
    },
    {
        "describe",
        (PyCFunction)_mysql_ResultObject_describe,
        METH_NOARGS,
        _mysql_ResultObject_describe__doc__
    },
    {
        "fetch_row",
        (PyCFunction)_mysql_ResultObject_fetch_row,
        METH_VARARGS | METH_KEYWORDS,
        _mysql_ResultObject_fetch_row__doc__
    },
    {
        "discard",
        (PyCFunction)_mysql_ResultObject_discard,
        METH_NOARGS,
        _mysql_ResultObject_discard__doc__
    },
    {
        "field_flags",
        (PyCFunction)_mysql_ResultObject_field_flags,
        METH_NOARGS,
        _mysql_ResultObject_field_flags__doc__
    },
    {
        "num_fields",
        (PyCFunction)_mysql_ResultObject_num_fields,
        METH_NOARGS,
        _mysql_ResultObject_num_fields__doc__
    },
    {
        "num_rows",
        (PyCFunction)_mysql_ResultObject_num_rows,
        METH_NOARGS,
        _mysql_ResultObject_num_rows__doc__
    },
    {NULL,              NULL} /* sentinel */
};

static struct PyMemberDef _mysql_ResultObject_memberlist[] = {
    {
        "converter",
        T_OBJECT,
        offsetof(_mysql_ResultObject,converter),
        READONLY,
        "Type conversion mapping"
    },
    {
        "has_next",
        T_BOOL,
        offsetof(_mysql_ResultObject, has_next),
        READONLY,
        "Has next result"
    },
    {NULL} /* Sentinel */
};

static PyObject *
_mysql_ConnectionObject_getattro(
    _mysql_ConnectionObject *self,
    PyObject *name)
{
    const char *cname;
    cname = PyUnicode_AsUTF8(name);
    if (strcmp(cname, "closed") == 0)
        return PyLong_FromLong((long)!(self->open));

    return PyObject_GenericGetAttr((PyObject *)self, name);
}

static int
_mysql_ConnectionObject_setattro(
    _mysql_ConnectionObject *self,
    PyObject *name,
    PyObject *v)
{
    if (v == NULL) {
        PyErr_SetString(PyExc_AttributeError,
                "can't delete connection attributes");
        return -1;
    }
    return PyObject_GenericSetAttr((PyObject *)self, name, v);
}

static int
_mysql_ResultObject_setattro(
    _mysql_ResultObject *self,
    PyObject *name,
    PyObject *v)
{
    if (v == NULL) {
        PyErr_SetString(PyExc_AttributeError,
                "can't delete connection attributes");
        return -1;
    }
    return PyObject_GenericSetAttr((PyObject *)self, name, v);
}

PyTypeObject _mysql_ConnectionObject_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_mysql.connection", /* (char *)tp_name For printing */
    sizeof(_mysql_ConnectionObject),
    0,
    (destructor)_mysql_ConnectionObject_dealloc, /* tp_dealloc */
    0, /*tp_print*/
    0, /* tp_getattr */
    0, /* tp_setattr */
    0, /*tp_compare*/
    (reprfunc)_mysql_ConnectionObject_repr, /* tp_repr */

    /* Method suites for standard classes */

    0, /* (PyNumberMethods *) tp_as_number */
    0, /* (PySequenceMethods *) tp_as_sequence */
    0, /* (PyMappingMethods *) tp_as_mapping */

    /* More standard operations (here for binary compatibility) */

    0, /* (hashfunc) tp_hash */
    0, /* (ternaryfunc) tp_call */
    0, /* (reprfunc) tp_str */
    (getattrofunc)_mysql_ConnectionObject_getattro, /* tp_getattro */
    (setattrofunc)_mysql_ConnectionObject_setattro, /* tp_setattro */

    /* Functions to access object as input/output buffer */
    0, /* (PyBufferProcs *) tp_as_buffer */

    /* (tp_flags) Flags to define presence of optional/expanded features */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE,
    _mysql_connect__doc__, /* (char *) tp_doc Documentation string */

    /* call function for all accessible objects */
    (traverseproc) _mysql_ConnectionObject_traverse, /* tp_traverse */

    /* delete references to contained objects */
    (inquiry) _mysql_ConnectionObject_clear, /* tp_clear */

    /* rich comparisons */
    0, /* (richcmpfunc) tp_richcompare */

    /* weak reference enabler */
    0, /* (long) tp_weaklistoffset */

    /* Iterators */
    0, /* (getiterfunc) tp_iter */
    0, /* (iternextfunc) tp_iternext */

    /* Attribute descriptor and subclassing stuff */
    (struct PyMethodDef *)_mysql_ConnectionObject_methods, /* tp_methods */
    (struct PyMemberDef *)_mysql_ConnectionObject_memberlist, /* tp_members */
    0, /* (struct getsetlist *) tp_getset; */
    0, /* (struct _typeobject *) tp_base; */
    0, /* (PyObject *) tp_dict */
    0, /* (descrgetfunc) tp_descr_get */
    0, /* (descrsetfunc) tp_descr_set */
    0, /* (long) tp_dictoffset */
    (initproc)_mysql_ConnectionObject_Initialize, /* tp_init */
    NULL, /* tp_alloc */
    PyType_GenericNew, /* tp_new */
    NULL, /* tp_free Low-level free-memory routine */
    0, /* (PyObject *) tp_bases */
    0, /* (PyObject *) tp_mro method resolution order */
    0, /* (PyObject *) tp_defined */
} ;

PyTypeObject _mysql_ResultObject_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_mysql.result",
    sizeof(_mysql_ResultObject),
    0,
    (destructor)_mysql_ResultObject_dealloc, /* tp_dealloc */
    0, /*tp_print*/
    0, /* tp_getattr */
    0, /* tp_setattr */
    0, /*tp_compare*/
    (reprfunc)_mysql_ResultObject_repr, /* tp_repr */

    /* Method suites for standard classes */

    0, /* (PyNumberMethods *) tp_as_number */
    0, /* (PySequenceMethods *) tp_as_sequence */
    0, /* (PyMappingMethods *) tp_as_mapping */

    /* More standard operations (here for binary compatibility) */

    0, /* (hashfunc) tp_hash */
    0, /* (ternaryfunc) tp_call */
    0, /* (reprfunc) tp_str */
    (getattrofunc)PyObject_GenericGetAttr, /* tp_getattro */
    (setattrofunc)_mysql_ResultObject_setattro, /* tp_setattr */

    /* Functions to access object as input/output buffer */
    0, /* (PyBufferProcs *) tp_as_buffer */

    /* Flags to define presence of optional/expanded features */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE,

    _mysql_ResultObject__doc__, /* (char *) tp_doc Documentation string */

    /* call function for all accessible objects */
    (traverseproc) _mysql_ResultObject_traverse, /* tp_traverse */

    /* delete references to contained objects */
    (inquiry) _mysql_ResultObject_clear, /* tp_clear */

    /* rich comparisons */
    0, /* (richcmpfunc) tp_richcompare */

    /* weak reference enabler */
    0, /* (long) tp_weaklistoffset */

    /* Iterators */
    0, /* (getiterfunc) tp_iter */
    0, /* (iternextfunc) tp_iternext */

    /* Attribute descriptor and subclassing stuff */
    (struct PyMethodDef *) _mysql_ResultObject_methods, /* tp_methods */
    (struct PyMemberDef *) _mysql_ResultObject_memberlist, /*tp_members */
    0, /* (struct getsetlist *) tp_getset; */
    0, /* (struct _typeobject *) tp_base; */
    0, /* (PyObject *) tp_dict */
    0, /* (descrgetfunc) tp_descr_get */
    0, /* (descrsetfunc) tp_descr_set */
    0, /* (long) tp_dictoffset */
    (initproc)_mysql_ResultObject_Initialize, /* tp_init */
    NULL, /* tp_alloc */
    PyType_GenericNew, /* tp_new */
    NULL, /* tp_free Low-level free-memory routine */
    0, /* (PyObject *) tp_bases */
    0, /* (PyObject *) tp_mro method resolution order */
    0, /* (PyObject *) tp_defined */
};

static PyMethodDef
_mysql_methods[] = {
    {
        "connect",
        (PyCFunction)_mysql_connect,
        METH_VARARGS | METH_KEYWORDS,
        _mysql_connect__doc__
    },
    {
        "debug",
        (PyCFunction)_mysql_debug,
        METH_VARARGS,
        _mysql_debug__doc__
    },
    {
        "escape",
        (PyCFunction)_mysql_escape,
        METH_VARARGS,
        _mysql_escape__doc__
    },
    {
        "escape_string",
        (PyCFunction)_mysql_escape_string,
        METH_VARARGS,
        _mysql_escape_string__doc__
    },
    {
        "string_literal",
        (PyCFunction)_mysql_string_literal,
        METH_O,
        _mysql_string_literal__doc__
    },
    {
        "get_client_info",
        (PyCFunction)_mysql_get_client_info,
        METH_NOARGS,
        _mysql_get_client_info__doc__
    },
    {NULL, NULL} /* sentinel */
};

static PyObject *
_mysql_NewException(
    PyObject *dict,
    PyObject *edict,
    char *name)
{
    PyObject *e;
    if (!(e = PyDict_GetItemString(edict, name)))
        return NULL;
    if (PyDict_SetItemString(dict, name, e))
        return NULL;
    Py_INCREF(e);
    return e;
}

#define QUOTE(X) _QUOTE(X)
#define _QUOTE(X) #X

static char _mysql___doc__[] =
"an adaptation of the MySQL C API (mostly)\n\
\n\
You probably are better off using MySQLdb instead of using this\n\
module directly.\n\
\n\
In general, renaming goes from mysql_* to _mysql.*. _mysql.connect()\n\
returns a connection object (MYSQL). Functions which expect MYSQL * as\n\
an argument are now methods of the connection object. A number of things\n\
return result objects (MYSQL_RES). Functions which expect MYSQL_RES * as\n\
an argument are now methods of the result object. Deprecated functions\n\
(as of 3.23) are NOT implemented.\n\
";

static struct PyModuleDef _mysqlmodule = {
   PyModuleDef_HEAD_INIT,
   "_mysql",   /* name of module */
   _mysql___doc__, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   _mysql_methods
};

PyMODINIT_FUNC
PyInit__mysql(void)
{
    PyObject *dict, *module, *emod, *edict;

    if (mysql_library_init(0, NULL, NULL)) {
        PyErr_SetString(PyExc_ImportError, "_mysql: mysql_library_init failed");
        return NULL;
    }

    if (PyType_Ready(&_mysql_ConnectionObject_Type) < 0)
        return NULL;
    if (PyType_Ready(&_mysql_ResultObject_Type) < 0)
        return NULL;

    module = PyModule_Create(&_mysqlmodule);
    if (!module) return module; /* this really should never happen */

    if (!(dict = PyModule_GetDict(module))) goto error;
    if (PyDict_SetItemString(dict, "version_info",
                   PyRun_String(QUOTE(version_info), Py_eval_input,
                       dict, dict)))
        goto error;
    if (PyDict_SetItemString(dict, "__version__",
                   PyUnicode_FromString(QUOTE(__version__))))
        goto error;
    if (PyDict_SetItemString(dict, "connection",
                   (PyObject *)&_mysql_ConnectionObject_Type))
        goto error;
    Py_INCREF(&_mysql_ConnectionObject_Type);
    if (PyDict_SetItemString(dict, "result",
                   (PyObject *)&_mysql_ResultObject_Type))
        goto error;
    Py_INCREF(&_mysql_ResultObject_Type);
    if (!(emod = PyImport_ImportModule("MySQLdb._exceptions"))) {
        PyErr_Print();
        goto error;
    }
    if (!(edict = PyModule_GetDict(emod))) goto error;
    if (!(_mysql_MySQLError =
          _mysql_NewException(dict, edict, "MySQLError")))
        goto error;
    if (!(_mysql_Warning =
          _mysql_NewException(dict, edict, "Warning")))
        goto error;
    if (!(_mysql_Error =
          _mysql_NewException(dict, edict, "Error")))
        goto error;
    if (!(_mysql_InterfaceError =
          _mysql_NewException(dict, edict, "InterfaceError")))
        goto error;
    if (!(_mysql_DatabaseError =
          _mysql_NewException(dict, edict, "DatabaseError")))
        goto error;
    if (!(_mysql_DataError =
          _mysql_NewException(dict, edict, "DataError")))
        goto error;
    if (!(_mysql_OperationalError =
          _mysql_NewException(dict, edict, "OperationalError")))
        goto error;
    if (!(_mysql_IntegrityError =
          _mysql_NewException(dict, edict, "IntegrityError")))
        goto error;
    if (!(_mysql_InternalError =
          _mysql_NewException(dict, edict, "InternalError")))
        goto error;
    if (!(_mysql_ProgrammingError =
          _mysql_NewException(dict, edict, "ProgrammingError")))
        goto error;
    if (!(_mysql_NotSupportedError =
          _mysql_NewException(dict, edict, "NotSupportedError")))
        goto error;
    Py_DECREF(emod);
  error:
    if (PyErr_Occurred()) {
        PyErr_SetString(PyExc_ImportError, "_mysql: init failed");
        module = NULL;
    }
    return module;
}

/* vim: set ts=4 sts=4 sw=4 expandtab : */
