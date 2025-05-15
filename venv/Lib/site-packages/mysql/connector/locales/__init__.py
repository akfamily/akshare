# Copyright (c) 2012, 2024, Oracle and/or its affiliates.
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

"""Translations."""

from typing import List, Optional, Union

__all__: List[str] = ["get_client_error"]

from .. import errorcode


def get_client_error(error: Union[int, str], language: str = "eng") -> Optional[str]:
    """Lookup client error

    This function will lookup the client error message based on the given
    error and return the error message. If the error was not found,
    None will be returned.

    Error can be either an integer or a string. For example:
        error: 2000
        error: CR_UNKNOWN_ERROR

    The language attribute can be used to retrieve a localized message, when
    available.

    Returns a string or None.
    """
    try:
        tmp = __import__(
            f"mysql.connector.locales.{language}",
            globals(),
            locals(),
            ["client_error"],
        )
    except ImportError:
        raise ImportError(
            f"No localization support for language '{language}'"
        ) from None
    client_error = tmp.client_error

    if isinstance(error, int):
        errno = error
        for key, value in errorcode.__dict__.items():
            if value == errno:
                error = key
                break

    if isinstance(error, (str)):
        try:
            return getattr(client_error, error)
        except AttributeError:
            return None

    raise ValueError("error argument needs to be either an integer or string")
