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

# mypy: disable-error-code="override,attr-defined"

"""Database Operations."""

from datetime import datetime, time, timezone
from typing import Optional

from django.conf import settings
from django.db.backends.mysql.operations import (
    DatabaseOperations as MySQLDatabaseOperations,
)
from django.utils import timezone as django_timezone

try:
    from _mysql_connector import datetime_to_mysql, time_to_mysql
except ImportError:
    HAVE_CEXT = False
else:
    HAVE_CEXT = True


class DatabaseOperations(MySQLDatabaseOperations):
    """Database Operations class."""

    compiler_module = "mysql.connector.django.compiler"

    def regex_lookup(self, lookup_type: str) -> str:
        """Return the string to use in a query when performing regular
        expression lookup."""
        if self.connection.mysql_version < (8, 0, 0):
            if lookup_type == "regex":
                return "%s REGEXP BINARY %s"
            return "%s REGEXP %s"

        match_option = "c" if lookup_type == "regex" else "i"
        return f"REGEXP_LIKE(%s, %s, '{match_option}')"

    def adapt_datetimefield_value(self, value: Optional[datetime]) -> Optional[bytes]:
        """Transform a datetime value to an object compatible with what is
        expected by the backend driver for datetime columns."""
        return self.value_to_db_datetime(value)

    def value_to_db_datetime(self, value: Optional[datetime]) -> Optional[bytes]:
        """Convert value to MySQL DATETIME."""
        ans: Optional[bytes] = None
        if value is None:
            return ans
        # MySQL doesn't support tz-aware times
        if django_timezone.is_aware(value):
            if settings.USE_TZ:
                value = value.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                raise ValueError("MySQL backend does not support timezone-aware times")
        if not self.connection.features.supports_microsecond_precision:
            value = value.replace(microsecond=0)
        if not self.connection.use_pure:
            return datetime_to_mysql(value)
        return self.connection.converter.to_mysql(value)

    def adapt_timefield_value(self, value: Optional[time]) -> Optional[bytes]:
        """Transform a time value to an object compatible with what is expected
        by the backend driver for time columns."""
        return self.value_to_db_time(value)

    def value_to_db_time(self, value: Optional[time]) -> Optional[bytes]:
        """Convert value to MySQL TIME."""
        if value is None:
            return None

        # MySQL doesn't support tz-aware times
        if django_timezone.is_aware(value):
            raise ValueError("MySQL backend does not support timezone-aware times")

        if not self.connection.use_pure:
            return time_to_mysql(value)
        return self.connection.converter.to_mysql(value)
