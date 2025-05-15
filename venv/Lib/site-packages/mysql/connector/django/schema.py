# Copyright (c) 2020, 2024, Oracle and/or its affiliates.
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

# mypy: disable-error-code="override"

"""Database schema editor."""
from typing import Any

from django.db.backends.mysql.schema import (
    DatabaseSchemaEditor as MySQLDatabaseSchemaEditor,
)


class DatabaseSchemaEditor(MySQLDatabaseSchemaEditor):
    """This class is responsible for emitting schema-changing statements to the
    databases.
    """

    def quote_value(self, value: Any) -> Any:
        """Quote value."""
        self.connection.ensure_connection()
        if isinstance(value, str):
            value = value.replace("%", "%%")
        quoted = self.connection.connection.converter.escape(value)
        if isinstance(value, str) and isinstance(quoted, bytes):
            quoted = quoted.decode()
        return quoted

    def prepare_default(self, value: Any) -> Any:
        """Implement the required abstract method.

        MySQL has requires_literal_defaults=False, therefore return the value.
        """
        return value
