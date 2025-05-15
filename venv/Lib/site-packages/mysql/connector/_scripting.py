# Copyright (c) 2024, 2025, Oracle and/or its affiliates.
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

"""Classes and methods utilized to work with MySQL Scripts."""

import re
import unicodedata

from collections import deque
from typing import Deque, Generator, Optional

from .errors import InterfaceError
from .types import MySQLScriptPartition

DEFAULT_DELIMITER = b";"
"""The default delimiter of MySQL Client and the only one
recognized by the MySQL server protocol."""

DELIMITER_RESERVED_SYMBOLS = {
    "$": rb"\$",
    "^": rb"\^",
    "?": rb"\?",
    "(": rb"\(",
    ")": rb"\)",
    "[": rb"\[",
    "]": rb"\]",
    "{": rb"\{",
    "}": rb"\}",
    ".": rb"\.",
    "|": rb"\|",
    "+": rb"\+",
    "-": rb"\-",
    "*": rb"\*",
}
"""Symbols with a special meaning in regular expression contexts."""

DELIMITER_PATTERN: re.Pattern = re.compile(
    rb"""(delimiter\s+)(?=(?:[^"'`]*(?:"[^"]*"|'[^']*'|`[^`]*`))*[^"'`]*$)""",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""Regular expression pattern recognizing the delimiter command."""


class MySQLScriptSplitter:
    """Breaks a MySQL script into single statements.

    It strips custom delimiters and comments along the way, except for comments
    representing a MySQL extension or optimizer hint.
    """

    _regex_sql_split_stmts = b"""(?=(?:[^"'`]*(?:"[^"]*"|'[^']*'|`[^`]*`))*[^"'`]*$)"""

    def __init__(self, sql_script: bytes) -> None:
        """Constructor."""
        self._code = sql_script
        self._single_stmts: Optional[list[bytes]] = None
        self._mappable_stmts: Optional[list[bytes]] = None
        self._re_sql_split_stmts: dict[bytes, re.Pattern] = {}

    def _split_statement(self, code: bytes, delimiter: bytes) -> list[bytes]:
        """Split code context by delimiter."""
        snippets = []

        if delimiter not in self._re_sql_split_stmts:
            if b"\\" in delimiter:
                raise InterfaceError(
                    "The backslash (\\) character is not a valid delimiter."
                )
            delimiter_pattern = [
                DELIMITER_RESERVED_SYMBOLS.get(char, char.encode())
                for char in delimiter.decode()
            ]
            self._re_sql_split_stmts[delimiter] = re.compile(
                b"".join(delimiter_pattern) + self._regex_sql_split_stmts
            )

        for snippet in self._re_sql_split_stmts[delimiter].split(code):
            snippet_strip = snippet.strip()
            if snippet_strip:
                snippets.append(snippet_strip)

        return snippets

    @staticmethod
    def is_white_space_char(char: int) -> bool:
        """Validates whether `char` is a white-space character or not."""
        return unicodedata.category(chr(char))[0] in {"Z"}

    @staticmethod
    def is_control_char(char: int) -> bool:
        """Validates whether `char` is a control character or not."""
        return unicodedata.category(chr(char))[0] in {"C"}

    @staticmethod
    def split_by_control_char_or_white_space(string: bytes) -> list[bytes]:
        """Split `string` by any control character or whitespace."""
        return re.split(rb"[\s\x00-\x1f\x7f-\x9f]", string)

    @staticmethod
    def has_delimiter(code: bytes) -> bool:
        """Validates whether `code` has the delimiter command pattern or not."""
        return re.search(DELIMITER_PATTERN, code) is not None

    @staticmethod
    def remove_comments(code: bytes) -> bytes:
        """Remove MySQL comments which include `--`-style, `#`-style
        and `C`-style comments.

        A `--`-style comment spans from `--` to the end of the line.
        It requires the second dash to be
        followed by at least one whitespace or control character
        (such as a space, tab, newline, and so on).

        A `#`-style comment spans from `#` to the end of the line.

        A C-style comment spans from a `/*` sequence to the following `*/`
        sequence, as in the C programming language. This syntax enables a
        comment to extend over multiple lines because the beginning and
        closing sequences need not be on the same line.

        **NOTE: Only C-style comments representing MySQL extensions or
        optimizer hints are preserved**. E.g.,

        ```
        /*! MySQL-specific code */

        /*+ MySQL-specific code */
        ```

        *For Reference Manual- MySQL Comments*, see
        https://dev.mysql.com/doc/refman/en/comments.html.
        """

        def is_dash_style(b_str: bytes, b_char: int) -> bool:
            return b_str == b"--" and (
                MySQLScriptSplitter.is_control_char(b_char)
                or MySQLScriptSplitter.is_white_space_char(b_char)
            )

        def is_hash_style(b_str: bytes) -> bool:
            return b_str == b"#"

        def is_c_style(b_str: bytes, b_char: int) -> bool:
            return b_str == b"/*" and b_char not in {ord("!"), ord("+")}

        buf = bytearray(b"")
        i, literal_ctx = 0, None
        line_break, single_quote, double_quote = ord("\n"), ord("'"), ord('"')
        while i < len(code):
            if literal_ctx is None:
                style = None
                if is_dash_style(buf[-2:], code[i]):
                    style = "--"
                elif is_hash_style(buf[-1:]):
                    style = "#"
                elif is_c_style(buf[-2:], code[i]):
                    style = "/*"
                if style is not None:
                    if style in ("--", "#"):
                        while i < len(code) and code[i] != line_break:
                            i += 1
                    else:
                        while i + 1 < len(code) and code[i : i + 2] != b"*/":
                            i += 1
                        i += 2

                    for _ in range(len(style)):
                        buf.pop()

                    while buf and (
                        MySQLScriptSplitter.is_control_char(buf[-1])
                        or MySQLScriptSplitter.is_white_space_char(buf[-1])
                    ):
                        buf.pop()

                    continue

            if literal_ctx is None and code[i] in [single_quote, double_quote]:
                literal_ctx = code[i]
            elif literal_ctx is not None and code[i] in {literal_ctx, line_break}:
                literal_ctx = None

            buf.append(code[i])
            i += 1

        return bytes(buf)

    def split_script(self, remove_comments: bool = True) -> list[bytes]:
        """Splits the given script text into a sequence of individual statements.

        The word DELIMITER and any of its lower and upper case combinations
        such as delimiter, DeLiMiter, etc., are considered reserved words by
        the connector. Users must quote these when included in multi statements
        for other purposes different from declaring an actual statement delimiter;
        e.g., as names for tables, columns, variables, in comments, etc.

        ```
        CREATE TABLE `delimiter` (begin INT, end INT); -- I am a `DELimiTer` comment
        ```

        If they are not quoted, the statement-mapping will not produce the expected
        experience.

        See https://dev.mysql.com/doc/refman/8.0/en/keywords.html to know more
        about quoting a reserved word.

        *Note that comments are always ignored as they are not considered to be
        part of statements, with one exeception; **C-style comments representing
        MySQL extensions or optimizer hints are preserved***.
        """
        # If it was already computed, then skip computation and use the cache
        if self._single_stmts is not None:
            return self._single_stmts

        # initialize variables
        self._single_stmts = []
        delimiter = DEFAULT_DELIMITER
        buf: list[bytes] = []
        prev = b""

        # remove comments
        if remove_comments:
            code = MySQLScriptSplitter.remove_comments(code=self._code)
        else:
            code = self._code

        # let's split the script by `delimiter pattern` - the pattern is also
        # included in the returned list.
        for curr in re.split(pattern=DELIMITER_PATTERN, string=code):
            # Checking if the previous substring is a "switch of context
            # (delimiter)" point.
            if re.search(DELIMITER_PATTERN, prev):
                # The next delimiter must be the sequence of chars until
                # reaching a control char or whitespace
                next_delimiter = self.split_by_control_char_or_white_space(curr)[0]

                # We shall remove the delimiter command from the code
                buf.pop()

                # At this point buf includes all the code where `delimiter` applies.
                self._single_stmts.extend(
                    self._split_statement(code=b" ".join(buf), delimiter=delimiter)
                )

                # From the current substring, let's take everything but the
                # "next delimiter" portion. Also, let's update the delimiter
                delimiter, buf = next_delimiter, [curr[len(next_delimiter) :]]
            else:
                # Let's accumulate
                buf.append(curr)

            # track the previous substring
            prev = curr

        # Ensure there are no loose ends
        if buf:
            self._single_stmts.extend(
                self._split_statement(code=b" ".join(buf), delimiter=delimiter)
            )

        return self._single_stmts

    def __repr__(self) -> str:
        return self._code.decode("utf-8")


def split_multi_statement(
    sql_code: bytes,
    map_results: bool = False,
) -> Generator[MySQLScriptPartition, None, None]:
    """Breaks a MySQL script into sub-scripts.

    If the given script uses `DELIMITER` statements (which are not recognized
    by MySQL Server), the connector will parse such statements to remove them
    from the script and substitute delimiters as needed. This pre-processing
    may cause a performance hit when using long scripts. Note that when enabling
    `map_results`, the script is expected to use `DELIMITER` statements in order
    to split the script into multiple query strings.

    Args:
        sql_code: MySQL script.
        map_results: If True, each sub-script is `statement-result` mappable.

    Returns:
        A generator of typed dictionaries with keys `single_stmts` and `mappable_stmts`.

        If mapping disabled and no delimiters detected, it returns a 1-item generator,
        the field `single_stmts` is an empty list and the `mappable_stmt` field
        corresponds to the unmodified script, that may be mappable.

        If mapping disabled and delimiters detected, it returns a 1-item generator,
        the field `single_stmts` is a list including all the single statements
        found in the script and the `mappable_stmt` field corresponds to the processed
        script (delimiters are stripped) that may be mappable.

        If maping enabled, the script is broken into mappable partitions. It returns
        an N-item generator (as many items as computed partitions), the field
        `single_stmts` is a list including all the single statements of the partition
        and the `mappable_stmt` field corresponds to the sub-script (partition) that
        is guaranteed to be mappable.

    Raises:
        `InterfaceError` if an invalid delimiter string is found.
    """
    if not MySQLScriptSplitter.has_delimiter(sql_code) and not map_results:
        # For those users executing single statements or scripts with no delimiters,
        # they can get a performance boost by bypassing the multi statement splitter.

        # Simply wrap the multi statement up (so it can be processed correctly
        # downstream) and return it as it is.
        yield MySQLScriptPartition(single_stmts=deque([]), mappable_stmt=sql_code)
        return

    tok = MySQLScriptSplitter(sql_script=sql_code)

    # The splitter splits the sql code into many single statements
    # while also getting rid of the delimiters (if any).
    stmts = tok.split_script()

    # if there are not statements to execute
    if not stmts:
        # Simply wrap the multi statement up (so it can be processed correctly
        # downstream).
        yield MySQLScriptPartition(single_stmts=deque([b""]), mappable_stmt=b"")
        return

    if not map_results:
        # group single statements into a unique and possibly no mappable
        # multi statement.
        yield MySQLScriptPartition(
            single_stmts=deque(stmts), mappable_stmt=b";\n".join(stmts)
        )
        return

    # group single statements into one or more mappable multi statements.
    i = 0
    partition_ids = (j for j, stmt in enumerate(stmts) if stmt[:5].upper() == b"CALL ")
    for j in partition_ids:
        if j > i:
            yield (
                MySQLScriptPartition(
                    mappable_stmt=b";\n".join(stmts[i:j]),
                    single_stmts=deque(stmts[i:j]),
                )
            )
        yield MySQLScriptPartition(
            mappable_stmt=stmts[j], single_stmts=deque([stmts[j]])
        )
        i = j + 1

    if i < len(stmts):
        yield (
            MySQLScriptPartition(
                mappable_stmt=b";\n".join(stmts[i : len(stmts)]),
                single_stmts=deque(stmts[i : len(stmts)]),
            )
        )


def get_local_infile_filenames(script: bytes) -> Deque[str]:
    """Scans the MySQL script looking for `filenames` (one for each
    `LOCAL INFILE` statement found).

    Arguments:
        script: a MySQL script that may include one or more `LOCAL INFILE` statements.

    Returns:
        filenames: a list of filenames (one for each `LOCAL INFILE` statement found).
        An empty list is returned if no matches are found.
    """
    matches = re.findall(
        pattern=rb"""LOCAL\s+INFILE\s+(["'])((?:\\\1|(?:(?!\1)).)*)(\1)""",
        string=MySQLScriptSplitter.remove_comments(script),
        flags=re.IGNORECASE,
    )
    if not matches or len(matches[0]) != 3:
        return deque([])

    # If there is a match, we get  ("'", "filename", "'") , that's to say,
    # the 1st and 3rd entries are the quote symbols, and the 2nd the actual filename.
    return deque([match[1].decode("utf-8") for match in matches])
