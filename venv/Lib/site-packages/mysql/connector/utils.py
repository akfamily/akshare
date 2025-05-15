# Copyright (c) 2009, 2025, Oracle and/or its affiliates.
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

"""Utilities."""

import importlib
import os
import platform
import struct
import subprocess
import sys
import unicodedata
import warnings

from decimal import Decimal
from functools import lru_cache
from stringprep import (
    in_table_a1,
    in_table_b1,
    in_table_c3,
    in_table_c4,
    in_table_c5,
    in_table_c6,
    in_table_c7,
    in_table_c8,
    in_table_c9,
    in_table_c11,
    in_table_c12,
    in_table_c21_c22,
    in_table_d1,
    in_table_d2,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

if TYPE_CHECKING:
    from mysql.connector.abstracts import MySQLConnectionAbstract

from .custom_types import HexLiteral
from .tls_ciphers import DEPRECATED_TLS_CIPHERSUITES, DEPRECATED_TLS_VERSIONS
from .types import StrOrBytes

__MYSQL_DEBUG__: bool = False

NUMERIC_TYPES: Tuple[Type[int], Type[float], Type[Decimal], Type[HexLiteral]] = (
    int,
    float,
    Decimal,
    HexLiteral,
)


def intread(buf: Union[int, bytes]) -> int:
    """Unpacks the given buffer to an integer"""
    if isinstance(buf, int):
        return buf
    length, tmp = len(buf), bytearray()
    if length == 1:
        return buf[0]
    if length <= 4:
        tmp += buf + b"\x00" * (4 - length)
        return int(struct.unpack("<I", tmp)[0])
    tmp += buf + b"\x00" * (8 - length)
    return int(struct.unpack("<Q", tmp)[0])


def int1store(i: int) -> bytes:
    """
    Takes an unsigned byte (1 byte) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 255:
        raise ValueError("int1store requires 0 <= i <= 255")
    return struct.pack("<B", i)


def int2store(i: int) -> bytes:
    """
    Takes an unsigned short (2 bytes) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 65535:
        raise ValueError("int2store requires 0 <= i <= 65535")
    return struct.pack("<H", i)


def int3store(i: int) -> bytes:
    """
    Takes an unsigned integer (3 bytes) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 16777215:
        raise ValueError("int3store requires 0 <= i <= 16777215")
    return struct.pack("<I", i)[0:3]


def int4store(i: int) -> bytes:
    """
    Takes an unsigned integer (4 bytes) and packs it as a bytes-object.

    Returns string.
    """
    if i < 0 or i > 4294967295:
        raise ValueError("int4store requires 0 <= i <= 4294967295")
    return struct.pack("<I", i)


def int8store(i: int) -> bytes:
    """
    Takes an unsigned integer (8 bytes) and packs it as string.

    Returns string.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError("int8store requires 0 <= i <= 2^64")
    return struct.pack("<Q", i)


def intstore(i: int) -> bytes:
    """
    Takes an unsigned integers and packs it as a bytes-object.

    This function uses int1store, int2store, int3store,
    int4store or int8store depending on the integer value.

    returns string.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError("intstore requires 0 <= i <=  2^64")

    if i <= 255:
        formed_string = int1store
    elif i <= 65535:
        formed_string = int2store
    elif i <= 16777215:
        formed_string = int3store
    elif i <= 4294967295:
        formed_string = int4store
    else:
        formed_string = int8store

    return formed_string(i)


def lc_int(i: int) -> bytes:
    """
    Takes an unsigned integer and packs it as bytes,
    with the information of how much bytes the encoded int takes.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError("Requires 0 <= i <= 2^64")

    if i < 251:
        return struct.pack("<B", i)
    if i <= 65535:
        return b"\xfc" + struct.pack("<H", i)
    if i <= 16777215:
        return b"\xfd" + struct.pack("<I", i)[0:3]

    return b"\xfe" + struct.pack("<Q", i)


def read_bytes(buf: bytes, size: int) -> Tuple[bytes, bytes]:
    """
    Reads bytes from a buffer.

    Returns a tuple with buffer less the read bytes, and the bytes.
    """
    res = buf[0:size]
    return (buf[size:], res)


def read_lc_string(buf: bytes) -> Tuple[bytes, Optional[bytes]]:
    """
    Takes a buffer and reads a length coded string from the start.

    This is how Length coded strings work

    If the string is 250 bytes long or smaller, then it looks like this:

      <-- 1b  -->
      +----------+-------------------------
      |  length  | a string goes here
      +----------+-------------------------

    If the string is bigger than 250, then it looks like this:

      <- 1b -><- 2/3/8 ->
      +------+-----------+-------------------------
      | type |  length   | a string goes here
      +------+-----------+-------------------------

      if type == \xfc:
          length is code in next 2 bytes
      elif type == \xfd:
          length is code in next 3 bytes
      elif type == \xfe:
          length is code in next 8 bytes

    NULL has a special value. If the buffer starts with \xfb then
    it's a NULL and we return None as value.

    Returns a tuple (trucated buffer, bytes).
    """
    if buf[0] == 251:  # \xfb
        # NULL value
        return (buf[1:], None)

    length = lsize = 0
    fst = buf[0]

    if fst <= 250:  # \xFA
        length = fst
        return (buf[1 + length :], buf[1 : length + 1])
    if fst == 252:
        lsize = 2
    elif fst == 253:
        lsize = 3
    elif fst == 254:
        lsize = 8

    length = intread(buf[1 : lsize + 1])
    return (buf[lsize + length + 1 :], buf[lsize + 1 : length + lsize + 1])


def read_lc_string_list(buf: bytes) -> Optional[Tuple[Optional[bytes], ...]]:
    """Reads all length encoded strings from the given buffer

    Returns a list of bytes
    """
    byteslst: List[Optional[bytes]] = []

    sizes = {252: 2, 253: 3, 254: 8}

    buf_len = len(buf)
    pos = 0

    while pos < buf_len:
        first = buf[pos]
        if first == 255:
            # Special case when MySQL error 1317 is returned by MySQL.
            # We simply return None.
            return None
        if first == 251:
            # NULL value
            byteslst.append(None)
            pos += 1
        else:
            if first <= 250:
                length = first
                byteslst.append(buf[(pos + 1) : length + (pos + 1)])
                pos += 1 + length
            else:
                lsize = 0
                try:
                    lsize = sizes[first]
                except KeyError:
                    return None
                length = intread(buf[(pos + 1) : lsize + (pos + 1)])
                byteslst.append(buf[pos + 1 + lsize : length + lsize + (pos + 1)])
                pos += 1 + lsize + length

    return tuple(byteslst)


def read_string(
    buf: bytes,
    end: Optional[bytes] = None,
    size: Optional[int] = None,
) -> Tuple[bytes, bytes]:
    """
    Reads a string up until a character or for a given size.

    Returns a tuple (trucated buffer, string).
    """
    if end is None and size is None:
        raise ValueError("read_string() needs either end or size")

    if end is not None:
        try:
            idx = buf.index(end)
        except ValueError as err:
            raise ValueError("end byte not present in buffer") from err
        return (buf[idx + 1 :], buf[0:idx])
    if size is not None:
        return read_bytes(buf, size)

    raise ValueError("read_string() needs either end or size (weird)")


def read_int(buf: bytes, size: int) -> Tuple[bytes, int]:
    """Read an integer from buffer

    Returns a tuple (truncated buffer, int)
    """
    res = intread(buf[0:size])
    return (buf[size:], res)


def read_lc_int(buf: bytes) -> Tuple[bytes, Optional[int]]:
    """
    Takes a buffer and reads an length code string from the start.

    Returns a tuple with buffer less the integer and the integer read.
    """
    if not buf:
        raise ValueError("Empty buffer.")

    lcbyte = buf[0]
    if lcbyte == 251:
        return (buf[1:], None)
    if lcbyte < 251:
        return (buf[1:], int(lcbyte))
    if lcbyte == 252:
        return (buf[3:], struct.unpack("<xH", buf[0:3])[0])
    if lcbyte == 253:
        return (buf[4:], struct.unpack("<I", buf[1:4] + b"\x00")[0])
    if lcbyte == 254:
        return (buf[9:], struct.unpack("<xQ", buf[0:9])[0])
    raise ValueError("Failed reading length encoded integer")


#
# For debugging
#
def _digest_buffer(buf: StrOrBytes) -> str:
    """Debug function for showing buffers"""
    if not isinstance(buf, str):
        return "".join([f"\\x{c:02x}" for c in buf])
    return "".join([f"\\x{ord(c):02x}" for c in buf])


def print_buffer(
    abuffer: StrOrBytes, prefix: Optional[str] = None, limit: int = 30
) -> None:
    """Debug function printing output of _digest_buffer()"""
    if prefix:
        if limit and limit > 0:
            digest = _digest_buffer(abuffer[0:limit])
        else:
            digest = _digest_buffer(abuffer)
        print(prefix + ": " + digest)
    else:
        print(_digest_buffer(abuffer))


def _parse_os_release() -> Dict[str, str]:
    """Parse the contents of /etc/os-release file.

    Returns:
        A dictionary containing release information.
    """
    distro: Dict[str, str] = {}
    os_release_file = os.path.join("/etc", "os-release")
    if not os.path.exists(os_release_file):
        return distro
    with open(os_release_file, encoding="utf-8") as file_obj:
        for line in file_obj:
            key_value = line.split("=")
            if len(key_value) != 2:
                continue
            key = key_value[0].lower()
            value = key_value[1].rstrip("\n").strip('"')
            distro[key] = value
    return distro


def _parse_lsb_release() -> Dict[str, str]:
    """Parse the contents of /etc/lsb-release file.

    Returns:
        A dictionary containing release information.
    """
    distro = {}
    lsb_release_file = os.path.join("/etc", "lsb-release")
    if os.path.exists(lsb_release_file):
        with open(lsb_release_file, encoding="utf-8") as file_obj:
            for line in file_obj:
                key_value = line.split("=")
                if len(key_value) != 2:
                    continue
                key = key_value[0].lower()
                value = key_value[1].rstrip("\n").strip('"')
                distro[key] = value
    return distro


def _parse_lsb_release_command() -> Optional[Dict[str, str]]:
    """Parse the output of the lsb_release command.

    Returns:
        A dictionary containing release information.
    """
    distro = {}
    with open(os.devnull, "w", encoding="utf-8") as devnull:
        try:
            stdout = subprocess.check_output(("lsb_release", "-a"), stderr=devnull)
        except OSError:
            return None
        lines = stdout.decode(sys.getfilesystemencoding()).splitlines()
        for line in lines:
            key_value = line.split(":")
            if len(key_value) != 2:
                continue
            key = key_value[0].replace(" ", "_").lower()
            value = key_value[1].strip("\t")
            distro[key] = value
    return distro


def linux_distribution() -> Tuple[str, str, str]:
    """Tries to determine the name of the Linux OS distribution name.

    First tries to get information from ``/etc/os-release`` file.
    If fails, tries to get the information of ``/etc/lsb-release`` file.
    And finally the information of ``lsb-release`` command.

    Returns:
        A tuple with (`name`, `version`, `codename`)
    """
    distro: Optional[Dict[str, str]] = _parse_lsb_release()
    if distro:
        return (
            distro.get("distrib_id", ""),
            distro.get("distrib_release", ""),
            distro.get("distrib_codename", ""),
        )

    distro = _parse_lsb_release_command()
    if distro:
        return (
            distro.get("distributor_id", ""),
            distro.get("release", ""),
            distro.get("codename", ""),
        )

    distro = _parse_os_release()
    if distro:
        return (
            distro.get("name", ""),
            distro.get("version_id", ""),
            distro.get("version_codename", ""),
        )

    return ("", "", "")


def _get_unicode_read_direction(unicode_str: str) -> str:
    """Get the readiness direction of the unicode string.

    We assume that the direction is "L-to-R" if the first character does not
    indicate the direction is "R-to-L" or an "AL" (Arabic Letter).
    """
    if unicode_str and unicodedata.bidirectional(unicode_str[0]) in (
        "R",
        "AL",
    ):
        return "R-to-L"
    return "L-to-R"


def _get_unicode_direction_rule(unicode_str: str) -> Dict[str, Callable[[str], bool]]:
    """
    1) The characters in section 5.8 MUST be prohibited.

    2) If a string contains any RandALCat character, the string MUST NOT
       contain any LCat character.

    3) If a string contains any RandALCat character, a RandALCat
       character MUST be the first character of the string, and a
       RandALCat character MUST be the last character of the string.
    """
    read_dir = _get_unicode_read_direction(unicode_str)

    # point 3)
    if read_dir == "R-to-L":
        if not (in_table_d1(unicode_str[0]) and in_table_d1(unicode_str[-1])):
            raise ValueError(
                "Invalid unicode Bidirectional sequence, if the "
                "first character is RandALCat, the final character"
                "must be RandALCat too."
            )
        # characters from in_table_d2 are prohibited.
        return {"Bidirectional Characters requirement 2 [StringPrep, d2]": in_table_d2}

    # characters from in_table_d1 are prohibited.
    return {"Bidirectional Characters requirement 2 [StringPrep, d2]": in_table_d1}


def validate_normalized_unicode_string(
    normalized_str: str,
) -> Optional[Tuple[str, str]]:
    """Check for Prohibited Output according to rfc4013 profile.

    This profile specifies the following characters as prohibited input:

       - Non-ASCII space characters [StringPrep, C.1.2]
       - ASCII control characters [StringPrep, C.2.1]
       - Non-ASCII control characters [StringPrep, C.2.2]
       - Private Use characters [StringPrep, C.3]
       - Non-character code points [StringPrep, C.4]
       - Surrogate code points [StringPrep, C.5]
       - Inappropriate for plain text characters [StringPrep, C.6]
       - Inappropriate for canonical representation characters [StringPrep, C.7]
       - Change display properties or deprecated characters [StringPrep, C.8]
       - Tagging characters [StringPrep, C.9]

    In addition of checking of Bidirectional Characters [StringPrep, Section 6]
    and the Unassigned Code Points [StringPrep, A.1].

    Returns:
        A tuple with ("probited character", "breaked_rule")
    """
    rules = {
        "Space characters that contains the ASCII code points": in_table_c11,
        "Space characters non-ASCII code points": in_table_c12,
        "Unassigned Code Points [StringPrep, A.1]": in_table_a1,
        "Non-ASCII space characters [StringPrep, C.1.2]": in_table_c12,
        "ASCII control characters [StringPrep, C.2.1]": in_table_c21_c22,
        "Private Use characters [StringPrep, C.3]": in_table_c3,
        "Non-character code points [StringPrep, C.4]": in_table_c4,
        "Surrogate code points [StringPrep, C.5]": in_table_c5,
        "Inappropriate for plain text characters [StringPrep, C.6]": in_table_c6,
        "Inappropriate for canonical representation characters [StringPrep, C.7]": in_table_c7,
        "Change display properties or deprecated characters [StringPrep, C.8]": in_table_c8,
        "Tagging characters [StringPrep, C.9]": in_table_c9,
    }

    try:
        rules.update(_get_unicode_direction_rule(normalized_str))
    except ValueError as err:
        return normalized_str, str(err)

    for char in normalized_str:
        for rule, func in rules.items():
            if func(char) and char != " ":
                return char, rule

    return None


def normalize_unicode_string(a_string: str) -> str:
    """normalizes a unicode string according to rfc4013

    Normalization of a unicode string according to rfc4013: The SASLprep profile
    of the "stringprep" algorithm.

    Normalization Unicode equivalence is the specification by the Unicode
    character encoding standard that some sequences of code points represent
    essentially the same character.

    This method normalizes using the Normalization Form Compatibility
    Composition (NFKC), as described in rfc4013 2.2.

    Returns:
        Normalized unicode string according to rfc4013.
    """
    # Per rfc4013 2.1. Mapping
    # non-ASCII space characters [StringPrep, C.1.2] are mapped to ' ' (U+0020)
    # "commonly mapped to nothing" characters [StringPrep, B.1] are mapped to ''
    nstr_list = [
        " " if in_table_c12(char) else "" if in_table_b1(char) else char
        for char in a_string
    ]

    nstr = "".join(nstr_list)

    # Per rfc4013 2.2. Use NFKC Normalization Form Compatibility Composition
    # Characters are decomposed by compatibility, then recomposed by canonical
    # equivalence.
    nstr = unicodedata.normalize("NFKC", nstr)
    if not nstr:
        # Normilization results in empty string.
        return ""

    return nstr


def init_bytearray(
    payload: Union[int, StrOrBytes] = b"", encoding: str = "utf-8"
) -> bytearray:
    """Initialize a bytearray from the payload."""
    if isinstance(payload, bytearray):
        return payload
    if isinstance(payload, int):
        return bytearray(payload)
    if not isinstance(payload, bytes):
        try:
            return bytearray(payload.encode(encoding=encoding))
        except AttributeError as err:
            raise ValueError("payload must be a str or bytes") from err

    return bytearray(payload)


@lru_cache()
def get_platform() -> Dict[str, Union[str, Tuple[str, str]]]:
    """Return a dict with the platform arch and OS version."""
    plat: Dict[str, Union[str, Tuple[str, str]]] = {"arch": "", "version": ""}
    if os.name == "nt":
        if "64" in platform.architecture()[0]:
            plat["arch"] = "x86_64"
        elif "32" in platform.architecture()[0]:
            plat["arch"] = "i386"
        else:
            plat["arch"] = platform.architecture()
        plat["version"] = f"Windows-{platform.win32_ver()[1]}"
    else:
        plat["arch"] = platform.machine()
        if platform.system() == "Darwin":
            plat["version"] = f"macOS-{platform.mac_ver()[0]}"
        else:
            plat["version"] = "-".join(linux_distribution()[0:2])

    return plat


def import_object(fullpath: str) -> Any:
    """Import an object from a fully qualified module path.

    Args:
        obj (str): A string representing the fully qualified name of the object.

    Returns:
        Object: The imported object.

    Raises:
        ValueError: If the object can't be imported.

    .. versionadded:: 8.0.33
    """
    if not isinstance(fullpath, str):
        raise ValueError(
            "'fullpath' should be a str representing the fully qualified name of the "
            "object to be imported"
        )
    try:
        module_str, callable_str = fullpath.rsplit(".", 1)
        module = importlib.import_module(module_str)
        obj = getattr(module, callable_str)
    except ValueError:
        raise ValueError(f"No callable named '{fullpath}'") from None
    except (AttributeError, ModuleNotFoundError) as err:
        raise ValueError(f"{err}") from err

    return obj


def warn_ciphersuites_deprecated(cipher_as_ossl: str, tls_version: str) -> None:
    """Emits a warning if a deprecated cipher is being utilized.

    Args:
        cipher: Must be ingested as OpenSSL name.
        tls_versions: TLS version to check the cipher against.

    Raises:
        DeprecationWarning: If the cipher is flagged as deprecated
                            according to the OSSA cipher list.
    """
    if cipher_as_ossl in DEPRECATED_TLS_CIPHERSUITES.get(tls_version, {}).values():
        warn_msg = (
            f"This connection is using TLS cipher {cipher_as_ossl} which is now "
            "deprecated and will be removed in a future release of "
            "MySQL Connector/Python."
        )
        warnings.warn(warn_msg, DeprecationWarning)


def warn_tls_version_deprecated(tls_version: str) -> None:
    """Emits a warning if a deprecated TLS version is being utilized.

    Args:
        tls_versions: TLS version to check.

    Raises:
        DeprecationWarning: If the TLS version is flagged as deprecated
                            according to the OSSA cipher list.
    """
    if tls_version in DEPRECATED_TLS_VERSIONS:
        warn_msg = (
            f"This connection is using TLS version {tls_version} which is now "
            "deprecated and will be removed in a future release of "
            "MySQL Connector/Python."
        )
        warnings.warn(warn_msg, DeprecationWarning)


class GenericWrapper:
    """Base class that provides basic object wrapper functionality."""

    def __init__(self, wrapped: Any) -> None:
        """Constructor."""
        self._wrapped: Any = wrapped

    def __getattr__(self, attr: str) -> Any:
        """Gets an attribute.

        Attributes defined in the wrapper object have higher precedence
        than those wrapped object equivalent. Attributes not found in
        the wrapper are then searched in the wrapped object.
        """
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._wrapped, attr)

    def __setattr__(self, name: str, value: Any) -> None:
        """Sets an attribute."""
        if "_wrapped" not in self.__dict__:
            self.__dict__["_wrapped"] = value
            return

        if name in self.__dict__:
            # this object has it
            super().__setattr__(name, value)
            return
        # proxy to the wrapped object
        self._wrapped.__setattr__(name, value)

    def get_wrapped_class(self) -> str:
        """Gets the wrapped class name."""
        return self._wrapped.__class__.__name__
