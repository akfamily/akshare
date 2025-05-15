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

"""Database Client."""

import os
import subprocess

from typing import Any, Dict, Iterable, List, Optional, Tuple

from django.db.backends.base.client import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    """Encapsulate backend-specific methods for opening a client shell."""

    executable_name = "mysql"

    @classmethod
    def settings_to_cmd_args_env(
        cls, settings_dict: Dict[str, Any], parameters: Optional[Iterable[str]] = None
    ) -> Tuple[List[str], Optional[Dict[str, Any]]]:
        args = [cls.executable_name]

        db = settings_dict["OPTIONS"].get("database", settings_dict["NAME"])
        user = settings_dict["OPTIONS"].get("user", settings_dict["USER"])
        passwd = settings_dict["OPTIONS"].get("password", settings_dict["PASSWORD"])
        host = settings_dict["OPTIONS"].get("host", settings_dict["HOST"])
        port = settings_dict["OPTIONS"].get("port", settings_dict["PORT"])
        ssl_ca = settings_dict["OPTIONS"].get("ssl_ca")
        ssl_cert = settings_dict["OPTIONS"].get("ssl_cert")
        ssl_key = settings_dict["OPTIONS"].get("ssl_key")
        defaults_file = settings_dict["OPTIONS"].get("read_default_file")
        charset = settings_dict["OPTIONS"].get("charset")

        # --defaults-file should always be the first option
        if defaults_file:
            args.append(f"--defaults-file={defaults_file}")

        # Load any custom init_commands. We always force SQL_MODE to TRADITIONAL
        init_command = settings_dict["OPTIONS"].get("init_command", "")
        args.append(f"--init-command=SET @@session.SQL_MODE=TRADITIONAL;{init_command}")

        if user:
            args.append(f"--user={user}")
        if passwd:
            args.append(f"--password={passwd}")

        if host:
            if "/" in host:
                args.append(f"--socket={host}")
            else:
                args.append(f"--host={host}")

        if port:
            args.append(f"--port={port}")

        if db:
            args.append(f"--database={db}")

        if ssl_ca:
            args.append(f"--ssl-ca={ssl_ca}")
        if ssl_cert:
            args.append(f"--ssl-cert={ssl_cert}")
        if ssl_key:
            args.append(f"--ssl-key={ssl_key}")

        if charset:
            args.append(f"--default-character-set={charset}")

        if parameters:
            args.extend(parameters)

        return args, None

    def runshell(self, parameters: Optional[Iterable[str]] = None) -> None:
        args, env = self.settings_to_cmd_args_env(
            self.connection.settings_dict, parameters
        )
        env = {**os.environ, **env} if env else None
        subprocess.run(args, env=env, check=True)
