# Copyright (c) 2014, 2024, Oracle and/or its affiliates.
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

# mypy: disable-error-code="attr-defined"

"""Implements parser to parse MySQL option files."""

import ast
import codecs
import io
import os
import re

from configparser import ConfigParser as SafeConfigParser, MissingSectionHeaderError
from typing import Any, Dict, List, Optional, Tuple, Union

from .constants import CNX_POOL_ARGS, DEFAULT_CONFIGURATION

DEFAULT_EXTENSIONS: Dict[str, Tuple[str, ...]] = {
    "nt": ("ini", "cnf"),
    "posix": ("cnf",),
}


def read_option_files(**config: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Read option files for connection parameters.

    Checks if connection arguments contain option file arguments, and then
    reads option files accordingly.
    """
    if "option_files" in config:
        try:
            if isinstance(config["option_groups"], str):
                config["option_groups"] = [config["option_groups"]]
            groups = config["option_groups"]
            del config["option_groups"]
        except KeyError:
            groups = ["client", "connector_python"]

        if isinstance(config["option_files"], str):
            config["option_files"] = [config["option_files"]]
        option_parser = MySQLOptionsParser(
            list(config["option_files"]), keep_dashes=False
        )
        del config["option_files"]

        config_from_file: Dict[str, Any] = (
            option_parser.get_groups_as_dict_with_priority(*groups)
        )
        config_options: Dict[str, Tuple[str, int, str]] = {}
        for group in groups:
            try:
                for option, value in config_from_file[group].items():
                    value += (group,)
                    try:
                        if option == "socket":
                            option = "unix_socket"
                            option_parser.set(group, "unix_socket", value[0])

                        if option not in CNX_POOL_ARGS and option != "failover":
                            _ = DEFAULT_CONFIGURATION[option]

                        if (
                            option not in config_options
                            or config_options[option][1] <= value[1]
                        ):
                            config_options[option] = value
                    except KeyError:
                        if group == "connector_python":
                            raise AttributeError(
                                f"Unsupported argument '{option}'"
                            ) from None
            except KeyError:
                continue

        for option, values in config_options.items():
            value, _, section = values
            if (
                option not in config
                and option_parser.has_section(section)
                and option_parser.has_option(section, option)
            ):
                if option in ("password", "passwd"):  # keep the value as string
                    config[option] = str(value)
                else:
                    try:
                        config[option] = ast.literal_eval(value)
                    except (ValueError, TypeError, SyntaxError):
                        config[option] = value
        if "socket" in config:
            config["unix_socket"] = config.pop("socket")
    return config


class MySQLOptionsParser(SafeConfigParser):
    """This class implements methods to parse MySQL option files"""

    def __init__(
        self, files: Optional[Union[List[str], str]] = None, keep_dashes: bool = True
    ) -> None:
        """Initialize

        If defaults is True, default option files are read first

        Raises ValueError if defaults is set to True but defaults files
        cannot be found.
        """

        # Regular expression to allow options with no value(For Python v2.6)
        self.optcre: re.Pattern = re.compile(
            r"(?P<option>[^:=\s][^:=]*)"
            r"\s*(?:"
            r"(?P<vi>[:=])\s*"
            r"(?P<value>.*))?$"
        )

        self._options_dict: Dict[str, Dict[str, Tuple[str, int]]] = {}

        SafeConfigParser.__init__(self, strict=False)

        self.default_extension: Tuple[str, ...] = DEFAULT_EXTENSIONS[os.name]
        self.keep_dashes: bool = keep_dashes

        if not files:
            raise ValueError("files argument should be given")
        self.files: List[str] = [files] if isinstance(files, str) else files

        self._parse_options(list(self.files))
        self._sections: Dict[str, Dict[str, str]] = self.get_groups_as_dict()

    def optionxform(self, optionstr: str) -> str:
        """Converts option strings

        Converts option strings to lower case and replaces dashes(-) with
        underscores(_) if keep_dashes variable is set.
        """
        if not self.keep_dashes:
            optionstr = optionstr.replace("-", "_")
        return optionstr.lower()

    def _parse_options(self, files: List[str]) -> None:
        """Parse options from files given as arguments.
         This method checks for !include or !inculdedir directives and if there
         is any, those files included by these directives are also parsed
         for options.

        Raises ValueError if any of the included or file given in arguments
        is not readable.
        """
        initial_files = files[:]
        files = []
        index = 0
        err_msg = "Option file '{0}' being included again in file '{1}'"

        for file_ in initial_files:
            try:
                if file_ in initial_files[index + 1 :]:
                    raise ValueError(
                        f"Same option file '{file_}' occurring more "
                        "than once in the list"
                    )
                with open(file_, "r", encoding="utf-8") as op_file:
                    for line in op_file.readlines():
                        if line.startswith("!includedir"):
                            _, dir_path = line.split(None, 1)
                            dir_path = dir_path.strip()
                            for entry in os.listdir(dir_path):
                                entry = os.path.join(dir_path, entry)
                                if entry in files:
                                    raise ValueError(err_msg.format(entry, file_))
                                if os.path.isfile(entry) and entry.endswith(
                                    self.default_extension
                                ):
                                    files.append(entry)

                        elif line.startswith("!include"):
                            _, filename = line.split(None, 1)
                            filename = filename.strip()
                            if filename in files:
                                raise ValueError(err_msg.format(filename, file_))
                            files.append(filename)

                    index += 1
                    files.append(file_)
            except IOError as err:
                raise ValueError(f"Failed reading file '{file_}': {err}") from err

        read_files = self.read(files)
        not_read_files = set(files) - set(read_files)
        if not_read_files:
            raise ValueError(f"File(s) {', '.join(not_read_files)} could not be read.")

    def read(  # type: ignore[override]
        self, filenames: Union[str, List[str]], encoding: Optional[str] = None
    ) -> List[str]:
        """Read and parse a filename or a list of filenames.

        Overridden from ConfigParser and modified so as to allow options
        which are not inside any section header

        Return list of successfully read files.
        """
        if isinstance(filenames, str):
            filenames = [filenames]
        read_ok = []
        for priority, filename in enumerate(filenames):
            try:
                out_file = io.StringIO()
                with codecs.open(filename, encoding="utf-8") as in_file:
                    for line in in_file:
                        line = line.strip()
                        # Skip lines that begin with "!includedir" or "!include"
                        if line.startswith("!include"):
                            continue

                        match_obj = self.optcre.match(line)
                        if not self.SECTCRE.match(line) and match_obj:
                            optname, delimiter, optval = match_obj.group(
                                "option", "vi", "value"
                            )
                            if optname and not optval and not delimiter:
                                out_file.write(f"{line}=\n")
                            else:
                                out_file.write(f"{line}\n")
                        else:
                            out_file.write(f"{line}\n")
                out_file.seek(0)
            except IOError:
                continue
            try:
                self._read(out_file, filename)
                for group in self._sections.keys():
                    try:
                        self._options_dict[group]
                    except KeyError:
                        self._options_dict[group] = {}
                    for option, value in self._sections[group].items():
                        self._options_dict[group][option] = (value, priority)

                self._sections = self._dict()

            except MissingSectionHeaderError:
                self._read(out_file, filename)
            out_file.close()
            read_ok.append(filename)
        return read_ok

    def get_groups(self, *args: str) -> Dict[str, str]:
        """Returns options as a dictionary.

        Returns options from all the groups specified as arguments, returns
        the options from all groups if no argument provided. Options are
        overridden when they are found in the next group.

        Returns a dictionary
        """
        if not args:
            args = tuple(self._options_dict.keys())

        options = {}
        priority: Dict[str, int] = {}
        for group in args:
            try:
                for option, value in [
                    (
                        key,
                        value,
                    )
                    for key, value in self._options_dict[group].items()
                    if key != "__name__" and not key.startswith("!")
                ]:
                    if option not in options or priority[option] <= value[1]:
                        priority[option] = value[1]
                        options[option] = value[0]
            except KeyError:
                pass

        return options

    def get_groups_as_dict_with_priority(
        self, *args: str
    ) -> Dict[str, Dict[str, Tuple[str, int]]]:
        """Returns options as dictionary of dictionaries.

        Returns options from all the groups specified as arguments. For each
        group the option are contained in a dictionary. The order in which
        the groups are specified is unimportant. Also options are not
        overridden in between the groups.

        The value is a tuple with two elements, first being the actual value
        and second is the priority of the value which is higher for a value
        read from a higher priority file.

        Returns an dictionary of dictionaries
        """
        if not args:
            args = tuple(self._options_dict.keys())

        options = {}
        for group in args:
            try:
                options[group] = dict(
                    (
                        key,
                        value,
                    )
                    for key, value in self._options_dict[group].items()
                    if key != "__name__" and not key.startswith("!")
                )
            except KeyError:
                pass
        return options

    def get_groups_as_dict(self, *args: str) -> Dict[str, Dict[str, str]]:
        """Returns options as dictionary of dictionaries.

        Returns options from all the groups specified as arguments. For each
        group the option are contained in a dictionary. The order in which
        the groups are specified is unimportant. Also options are not
        overridden in between the groups.

        Returns an dictionary of dictionaries
        """
        if not args:
            args = tuple(self._options_dict.keys())

        options = {}
        for group in args:
            try:
                options[group] = dict(
                    (
                        key,
                        value[0],
                    )
                    for key, value in self._options_dict[group].items()
                    if key != "__name__" and not key.startswith("!")
                )
            except KeyError:
                pass

        return options
