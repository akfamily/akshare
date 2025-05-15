# Copyright (c) 2012, 2025, Oracle and/or its affiliates.
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

"""MySQL Connector/Python version information

The file version.py gets installed and is available after installation
as mysql.connector.version.
"""

VERSION = (9, 3, 0, "", 1)

# pylint: disable=consider-using-f-string
if VERSION[3] and VERSION[4]:
    VERSION_TEXT = "{0}.{1}.{2}{3}{4}".format(*VERSION)
else:
    VERSION_TEXT = "{0}.{1}.{2}".format(*VERSION[0:3])
# pylint: enable=consider-using-f-string

VERSION_EXTRA = ""
LICENSE = "GPLv2 with FOSS License Exception"
EDITION = ""  # Added in package names, after the version
