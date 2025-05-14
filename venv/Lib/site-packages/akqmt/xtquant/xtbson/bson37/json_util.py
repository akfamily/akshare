# Copyright 2009-present MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for using Python's :mod:`json` module with BSON documents.

This module provides two helper methods `dumps` and `loads` that wrap the
native :mod:`json` methods and provide explicit BSON conversion to and from
JSON. :class:`~bson.json_util.JSONOptions` provides a way to control how JSON
is emitted and parsed, with the default being the Relaxed Extended JSON format.
:mod:`~bson.json_util` can also generate Canonical or legacy `Extended JSON`_
when :const:`CANONICAL_JSON_OPTIONS` or :const:`LEGACY_JSON_OPTIONS` is
provided, respectively.

.. _Extended JSON: https://github.com/mongodb/specifications/blob/master/source/extended-json.rst

Example usage (deserialization):

.. doctest::

   >>> from .json_util import loads
   >>> loads('[{"foo": [1, 2]}, {"bar": {"hello": "world"}}, {"code": {"$scope": {}, "$code": "function x() { return 1; }"}}, {"bin": {"$type": "80", "$binary": "AQIDBA=="}}]')
   [{'foo': [1, 2]}, {'bar': {'hello': 'world'}}, {'code': Code('function x() { return 1; }', {})}, {'bin': Binary(b'...', 128)}]

Example usage with :const:`RELAXED_JSON_OPTIONS` (the default):

.. doctest::

   >>> from . import Binary, Code
   >>> from .json_util import dumps
   >>> dumps([{'foo': [1, 2]},
   ...        {'bar': {'hello': 'world'}},
   ...        {'code': Code("function x() { return 1; }")},
   ...        {'bin': Binary(b"\x01\x02\x03\x04")}])
   '[{"foo": [1, 2]}, {"bar": {"hello": "world"}}, {"code": {"$code": "function x() { return 1; }"}}, {"bin": {"$binary": {"base64": "AQIDBA==", "subType": "00"}}}]'

Example usage (with :const:`CANONICAL_JSON_OPTIONS`):

.. doctest::

   >>> from . import Binary, Code
   >>> from .json_util import dumps, CANONICAL_JSON_OPTIONS
   >>> dumps([{'foo': [1, 2]},
   ...        {'bar': {'hello': 'world'}},
   ...        {'code': Code("function x() { return 1; }")},
   ...        {'bin': Binary(b"\x01\x02\x03\x04")}],
   ...       json_options=CANONICAL_JSON_OPTIONS)
   '[{"foo": [{"$numberInt": "1"}, {"$numberInt": "2"}]}, {"bar": {"hello": "world"}}, {"code": {"$code": "function x() { return 1; }"}}, {"bin": {"$binary": {"base64": "AQIDBA==", "subType": "00"}}}]'

Example usage (with :const:`LEGACY_JSON_OPTIONS`):

.. doctest::

   >>> from . import Binary, Code
   >>> from .json_util import dumps, LEGACY_JSON_OPTIONS
   >>> dumps([{'foo': [1, 2]},
   ...        {'bar': {'hello': 'world'}},
   ...        {'code': Code("function x() { return 1; }", {})},
   ...        {'bin': Binary(b"\x01\x02\x03\x04")}],
   ...       json_options=LEGACY_JSON_OPTIONS)
   '[{"foo": [1, 2]}, {"bar": {"hello": "world"}}, {"code": {"$code": "function x() { return 1; }", "$scope": {}}}, {"bin": {"$binary": "AQIDBA==", "$type": "00"}}]'

Alternatively, you can manually pass the `default` to :func:`json.dumps`.
It won't handle :class:`~bson.binary.Binary` and :class:`~bson.code.Code`
instances (as they are extended strings you can't provide custom defaults),
but it will be faster as there is less recursion.

.. note::
   If your application does not need the flexibility offered by
   :class:`JSONOptions` and spends a large amount of time in the `json_util`
   module, look to
   `python-bsonjs <https://pypi.python.org/pypi/python-bsonjs>`_ for a nice
   performance improvement. `python-bsonjs` is a fast BSON to MongoDB
   Extended JSON converter for Python built on top of
   `libbson <https://github.com/mongodb/libbson>`_. `python-bsonjs` works best
   with PyMongo when using :class:`~bson.raw_bson.RawBSONDocument`.
"""

import base64
import datetime
import json
import math
import re
import uuid
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Type, Union, cast

from .binary import ALL_UUID_SUBTYPES, UUID_SUBTYPE, Binary, UuidRepresentation
from .code import Code
from .codec_options import CodecOptions, DatetimeConversion
from .datetime_ms import (
    EPOCH_AWARE,
    DatetimeMS,
    _datetime_to_millis,
    _max_datetime_ms,
    _millis_to_datetime,
)
from .dbref import DBRef
from .decimal128 import Decimal128
from .int64 import Int64
from .max_key import MaxKey
from .min_key import MinKey
from .objectid import ObjectId
from .regex import Regex
from .son import RE_TYPE, SON
from .timestamp import Timestamp
from .tz_util import utc

_RE_OPT_TABLE = {
    "i": re.I,
    "l": re.L,
    "m": re.M,
    "s": re.S,
    "u": re.U,
    "x": re.X,
}


class DatetimeRepresentation:
    LEGACY = 0
    """Legacy MongoDB Extended JSON datetime representation.

    :class:`datetime.datetime` instances will be encoded to JSON in the
    format `{"$date": <dateAsMilliseconds>}`, where `dateAsMilliseconds` is
    a 64-bit signed integer giving the number of milliseconds since the Unix
    epoch UTC. This was the default encoding before PyMongo version 3.4.

    .. versionadded:: 3.4
    """

    NUMBERLONG = 1
    """NumberLong datetime representation.

    :class:`datetime.datetime` instances will be encoded to JSON in the
    format `{"$date": {"$numberLong": "<dateAsMilliseconds>"}}`,
    where `dateAsMilliseconds` is the string representation of a 64-bit signed
    integer giving the number of milliseconds since the Unix epoch UTC.

    .. versionadded:: 3.4
    """

    ISO8601 = 2
    """ISO-8601 datetime representation.

    :class:`datetime.datetime` instances greater than or equal to the Unix
    epoch UTC will be encoded to JSON in the format `{"$date": "<ISO-8601>"}`.
    :class:`datetime.datetime` instances before the Unix epoch UTC will be
    encoded as if the datetime representation is
    :const:`~DatetimeRepresentation.NUMBERLONG`.

    .. versionadded:: 3.4
    """


class JSONMode:
    LEGACY = 0
    """Legacy Extended JSON representation.

    In this mode, :func:`~bson.json_util.dumps` produces PyMongo's legacy
    non-standard JSON output. Consider using
    :const:`~bson.json_util.JSONMode.RELAXED` or
    :const:`~bson.json_util.JSONMode.CANONICAL` instead.

    .. versionadded:: 3.5
    """

    RELAXED = 1
    """Relaxed Extended JSON representation.

    In this mode, :func:`~bson.json_util.dumps` produces Relaxed Extended JSON,
    a mostly JSON-like format. Consider using this for things like a web API,
    where one is sending a document (or a projection of a document) that only
    uses ordinary JSON type primitives. In particular, the ``int``,
    :class:`~bson.int64.Int64`, and ``float`` numeric types are represented in
    the native JSON number format. This output is also the most human readable
    and is useful for debugging and documentation.

    .. seealso:: The specification for Relaxed `Extended JSON`_.

    .. versionadded:: 3.5
    """

    CANONICAL = 2
    """Canonical Extended JSON representation.

    In this mode, :func:`~bson.json_util.dumps` produces Canonical Extended
    JSON, a type preserving format. Consider using this for things like
    testing, where one has to precisely specify expected types in JSON. In
    particular, the ``int``, :class:`~bson.int64.Int64`, and ``float`` numeric
    types are encoded with type wrappers.

    .. seealso:: The specification for Canonical `Extended JSON`_.

    .. versionadded:: 3.5
    """


class JSONOptions(CodecOptions):
    """Encapsulates JSON options for :func:`dumps` and :func:`loads`.

    :Parameters:
      - `strict_number_long`: If ``True``, :class:`~bson.int64.Int64` objects
        are encoded to MongoDB Extended JSON's *Strict mode* type
        `NumberLong`, ie ``'{"$numberLong": "<number>" }'``. Otherwise they
        will be encoded as an `int`. Defaults to ``False``.
      - `datetime_representation`: The representation to use when encoding
        instances of :class:`datetime.datetime`. Defaults to
        :const:`~DatetimeRepresentation.LEGACY`.
      - `strict_uuid`: If ``True``, :class:`uuid.UUID` object are encoded to
        MongoDB Extended JSON's *Strict mode* type `Binary`. Otherwise it
        will be encoded as ``'{"$uuid": "<hex>" }'``. Defaults to ``False``.
      - `json_mode`: The :class:`JSONMode` to use when encoding BSON types to
        Extended JSON. Defaults to :const:`~JSONMode.LEGACY`.
      - `document_class`: BSON documents returned by :func:`loads` will be
        decoded to an instance of this class. Must be a subclass of
        :class:`collections.MutableMapping`. Defaults to :class:`dict`.
      - `uuid_representation`: The :class:`~bson.binary.UuidRepresentation`
        to use when encoding and decoding instances of :class:`uuid.UUID`.
        Defaults to :const:`~bson.binary.UuidRepresentation.UNSPECIFIED`.
      - `tz_aware`: If ``True``, MongoDB Extended JSON's *Strict mode* type
        `Date` will be decoded to timezone aware instances of
        :class:`datetime.datetime`. Otherwise they will be naive. Defaults
        to ``False``.
      - `tzinfo`: A :class:`datetime.tzinfo` subclass that specifies the
        timezone from which :class:`~datetime.datetime` objects should be
        decoded. Defaults to :const:`~bson.tz_util.utc`.
      - `datetime_conversion`: Specifies how UTC datetimes should be decoded
        within BSON. Valid options include 'datetime_ms' to return as a
        DatetimeMS, 'datetime' to return as a datetime.datetime and
        raising a ValueError for out-of-range values, 'datetime_auto' to
        return DatetimeMS objects when the underlying datetime is
        out-of-range and 'datetime_clamp' to clamp to the minimum and
        maximum possible datetimes. Defaults to 'datetime'. See
        :ref:`handling-out-of-range-datetimes` for details.
      - `args`: arguments to :class:`~bson.codec_options.CodecOptions`
      - `kwargs`: arguments to :class:`~bson.codec_options.CodecOptions`

    .. seealso:: The specification for Relaxed and Canonical `Extended JSON`_.

    .. versionchanged:: 4.0
       The default for `json_mode` was changed from :const:`JSONMode.LEGACY`
       to :const:`JSONMode.RELAXED`.
       The default for `uuid_representation` was changed from
       :const:`~bson.binary.UuidRepresentation.PYTHON_LEGACY` to
       :const:`~bson.binary.UuidRepresentation.UNSPECIFIED`.

    .. versionchanged:: 3.5
       Accepts the optional parameter `json_mode`.

    .. versionchanged:: 4.0
       Changed default value of `tz_aware` to False.
    """

    json_mode: int
    strict_number_long: bool
    datetime_representation: int
    strict_uuid: bool

    def __new__(
        cls: Type["JSONOptions"],
        strict_number_long: Optional[bool] = None,
        datetime_representation: Optional[int] = None,
        strict_uuid: Optional[bool] = None,
        json_mode: int = JSONMode.RELAXED,
        *args: Any,
        **kwargs: Any
    ) -> "JSONOptions":
        kwargs["tz_aware"] = kwargs.get("tz_aware", False)
        if kwargs["tz_aware"]:
            kwargs["tzinfo"] = kwargs.get("tzinfo", utc)
        if datetime_representation not in (
            DatetimeRepresentation.LEGACY,
            DatetimeRepresentation.NUMBERLONG,
            DatetimeRepresentation.ISO8601,
            None,
        ):
            raise ValueError(
                "JSONOptions.datetime_representation must be one of LEGACY, "
                "NUMBERLONG, or ISO8601 from DatetimeRepresentation."
            )
        self = cast(JSONOptions, super(JSONOptions, cls).__new__(cls, *args, **kwargs))
        if json_mode not in (JSONMode.LEGACY, JSONMode.RELAXED, JSONMode.CANONICAL):
            raise ValueError(
                "JSONOptions.json_mode must be one of LEGACY, RELAXED, "
                "or CANONICAL from JSONMode."
            )
        self.json_mode = json_mode
        if self.json_mode == JSONMode.RELAXED:
            if strict_number_long:
                raise ValueError("Cannot specify strict_number_long=True with JSONMode.RELAXED")
            if datetime_representation not in (None, DatetimeRepresentation.ISO8601):
                raise ValueError(
                    "datetime_representation must be DatetimeRepresentation."
                    "ISO8601 or omitted with JSONMode.RELAXED"
                )
            if strict_uuid not in (None, True):
                raise ValueError("Cannot specify strict_uuid=False with JSONMode.RELAXED")
            self.strict_number_long = False
            self.datetime_representation = DatetimeRepresentation.ISO8601
            self.strict_uuid = True
        elif self.json_mode == JSONMode.CANONICAL:
            if strict_number_long not in (None, True):
                raise ValueError("Cannot specify strict_number_long=False with JSONMode.RELAXED")
            if datetime_representation not in (None, DatetimeRepresentation.NUMBERLONG):
                raise ValueError(
                    "datetime_representation must be DatetimeRepresentation."
                    "NUMBERLONG or omitted with JSONMode.RELAXED"
                )
            if strict_uuid not in (None, True):
                raise ValueError("Cannot specify strict_uuid=False with JSONMode.RELAXED")
            self.strict_number_long = True
            self.datetime_representation = DatetimeRepresentation.NUMBERLONG
            self.strict_uuid = True
        else:  # JSONMode.LEGACY
            self.strict_number_long = False
            self.datetime_representation = DatetimeRepresentation.LEGACY
            self.strict_uuid = False
            if strict_number_long is not None:
                self.strict_number_long = strict_number_long
            if datetime_representation is not None:
                self.datetime_representation = datetime_representation
            if strict_uuid is not None:
                self.strict_uuid = strict_uuid
        return self

    def _arguments_repr(self) -> str:
        return (
            "strict_number_long=%r, "
            "datetime_representation=%r, "
            "strict_uuid=%r, json_mode=%r, %s"
            % (
                self.strict_number_long,
                self.datetime_representation,
                self.strict_uuid,
                self.json_mode,
                super(JSONOptions, self)._arguments_repr(),
            )
        )

    def _options_dict(self) -> Dict[Any, Any]:
        # TODO: PYTHON-2442 use _asdict() instead
        options_dict = super(JSONOptions, self)._options_dict()
        options_dict.update(
            {
                "strict_number_long": self.strict_number_long,
                "datetime_representation": self.datetime_representation,
                "strict_uuid": self.strict_uuid,
                "json_mode": self.json_mode,
            }
        )
        return options_dict

    def with_options(self, **kwargs: Any) -> "JSONOptions":
        """
        Make a copy of this JSONOptions, overriding some options::

            >>> from .json_util import CANONICAL_JSON_OPTIONS
            >>> CANONICAL_JSON_OPTIONS.tz_aware
            True
            >>> json_options = CANONICAL_JSON_OPTIONS.with_options(tz_aware=False, tzinfo=None)
            >>> json_options.tz_aware
            False

        .. versionadded:: 3.12
        """
        opts = self._options_dict()
        for opt in ("strict_number_long", "datetime_representation", "strict_uuid", "json_mode"):
            opts[opt] = kwargs.get(opt, getattr(self, opt))
        opts.update(kwargs)
        return JSONOptions(**opts)


LEGACY_JSON_OPTIONS: JSONOptions = JSONOptions(json_mode=JSONMode.LEGACY)
""":class:`JSONOptions` for encoding to PyMongo's legacy JSON format.

.. seealso:: The documentation for :const:`bson.json_util.JSONMode.LEGACY`.

.. versionadded:: 3.5
"""

CANONICAL_JSON_OPTIONS: JSONOptions = JSONOptions(json_mode=JSONMode.CANONICAL)
""":class:`JSONOptions` for Canonical Extended JSON.

.. seealso:: The documentation for :const:`bson.json_util.JSONMode.CANONICAL`.

.. versionadded:: 3.5
"""

RELAXED_JSON_OPTIONS: JSONOptions = JSONOptions(json_mode=JSONMode.RELAXED)
""":class:`JSONOptions` for Relaxed Extended JSON.

.. seealso:: The documentation for :const:`bson.json_util.JSONMode.RELAXED`.

.. versionadded:: 3.5
"""

DEFAULT_JSON_OPTIONS: JSONOptions = RELAXED_JSON_OPTIONS
"""The default :class:`JSONOptions` for JSON encoding/decoding.

The same as :const:`RELAXED_JSON_OPTIONS`.

.. versionchanged:: 4.0
   Changed from :const:`LEGACY_JSON_OPTIONS` to
   :const:`RELAXED_JSON_OPTIONS`.

.. versionadded:: 3.4
"""


def dumps(obj: Any, *args: Any, **kwargs: Any) -> str:
    """Helper function that wraps :func:`json.dumps`.

    Recursive function that handles all BSON types including
    :class:`~bson.binary.Binary` and :class:`~bson.code.Code`.

    :Parameters:
      - `json_options`: A :class:`JSONOptions` instance used to modify the
        encoding of MongoDB Extended JSON types. Defaults to
        :const:`DEFAULT_JSON_OPTIONS`.

    .. versionchanged:: 4.0
       Now outputs MongoDB Relaxed Extended JSON by default (using
       :const:`DEFAULT_JSON_OPTIONS`).

    .. versionchanged:: 3.4
       Accepts optional parameter `json_options`. See :class:`JSONOptions`.
    """
    json_options = kwargs.pop("json_options", DEFAULT_JSON_OPTIONS)
    return json.dumps(_json_convert(obj, json_options), *args, **kwargs)


def loads(s: str, *args: Any, **kwargs: Any) -> Any:
    """Helper function that wraps :func:`json.loads`.

    Automatically passes the object_hook for BSON type conversion.

    Raises ``TypeError``, ``ValueError``, ``KeyError``, or
    :exc:`~bson.errors.InvalidId` on invalid MongoDB Extended JSON.

    :Parameters:
      - `json_options`: A :class:`JSONOptions` instance used to modify the
        decoding of MongoDB Extended JSON types. Defaults to
        :const:`DEFAULT_JSON_OPTIONS`.

    .. versionchanged:: 4.0
       Now loads :class:`datetime.datetime` instances as naive by default. To
       load timezone aware instances utilize the `json_options` parameter.
       See :ref:`tz_aware_default_change` for an example.

    .. versionchanged:: 3.5
       Parses Relaxed and Canonical Extended JSON as well as PyMongo's legacy
       format. Now raises ``TypeError`` or ``ValueError`` when parsing JSON
       type wrappers with values of the wrong type or any extra keys.

    .. versionchanged:: 3.4
       Accepts optional parameter `json_options`. See :class:`JSONOptions`.
    """
    json_options = kwargs.pop("json_options", DEFAULT_JSON_OPTIONS)
    kwargs["object_pairs_hook"] = lambda pairs: object_pairs_hook(pairs, json_options)
    return json.loads(s, *args, **kwargs)


def _json_convert(obj: Any, json_options: JSONOptions = DEFAULT_JSON_OPTIONS) -> Any:
    """Recursive helper method that converts BSON types so they can be
    converted into json.
    """
    if hasattr(obj, "items"):
        return SON(((k, _json_convert(v, json_options)) for k, v in obj.items()))
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes)):
        return list((_json_convert(v, json_options) for v in obj))
    try:
        return default(obj, json_options)
    except TypeError:
        return obj


def object_pairs_hook(
    pairs: Sequence[Tuple[str, Any]], json_options: JSONOptions = DEFAULT_JSON_OPTIONS
) -> Any:
    return object_hook(json_options.document_class(pairs), json_options)


def object_hook(dct: Mapping[str, Any], json_options: JSONOptions = DEFAULT_JSON_OPTIONS) -> Any:
    if "$oid" in dct:
        return _parse_canonical_oid(dct)
    if (
        isinstance(dct.get("$ref"), str)
        and "$id" in dct
        and isinstance(dct.get("$db"), (str, type(None)))
    ):
        return _parse_canonical_dbref(dct)
    if "$date" in dct:
        return _parse_canonical_datetime(dct, json_options)
    if "$regex" in dct:
        return _parse_legacy_regex(dct)
    if "$minKey" in dct:
        return _parse_canonical_minkey(dct)
    if "$maxKey" in dct:
        return _parse_canonical_maxkey(dct)
    if "$binary" in dct:
        if "$type" in dct:
            return _parse_legacy_binary(dct, json_options)
        else:
            return _parse_canonical_binary(dct, json_options)
    if "$code" in dct:
        return _parse_canonical_code(dct)
    if "$uuid" in dct:
        return _parse_legacy_uuid(dct, json_options)
    if "$undefined" in dct:
        return None
    if "$numberLong" in dct:
        return _parse_canonical_int64(dct)
    if "$timestamp" in dct:
        tsp = dct["$timestamp"]
        return Timestamp(tsp["t"], tsp["i"])
    if "$numberDecimal" in dct:
        return _parse_canonical_decimal128(dct)
    if "$dbPointer" in dct:
        return _parse_canonical_dbpointer(dct)
    if "$regularExpression" in dct:
        return _parse_canonical_regex(dct)
    if "$symbol" in dct:
        return _parse_canonical_symbol(dct)
    if "$numberInt" in dct:
        return _parse_canonical_int32(dct)
    if "$numberDouble" in dct:
        return _parse_canonical_double(dct)
    return dct


def _parse_legacy_regex(doc: Any) -> Any:
    pattern = doc["$regex"]
    # Check if this is the $regex query operator.
    if not isinstance(pattern, (str, bytes)):
        return doc
    flags = 0
    # PyMongo always adds $options but some other tools may not.
    for opt in doc.get("$options", ""):
        flags |= _RE_OPT_TABLE.get(opt, 0)
    return Regex(pattern, flags)


def _parse_legacy_uuid(doc: Any, json_options: JSONOptions) -> Union[Binary, uuid.UUID]:
    """Decode a JSON legacy $uuid to Python UUID."""
    if len(doc) != 1:
        raise TypeError("Bad $uuid, extra field(s): %s" % (doc,))
    if not isinstance(doc["$uuid"], str):
        raise TypeError("$uuid must be a string: %s" % (doc,))
    if json_options.uuid_representation == UuidRepresentation.UNSPECIFIED:
        return Binary.from_uuid(uuid.UUID(doc["$uuid"]))
    else:
        return uuid.UUID(doc["$uuid"])


def _binary_or_uuid(data: Any, subtype: int, json_options: JSONOptions) -> Union[Binary, uuid.UUID]:
    # special handling for UUID
    if subtype in ALL_UUID_SUBTYPES:
        uuid_representation = json_options.uuid_representation
        binary_value = Binary(data, subtype)
        if uuid_representation == UuidRepresentation.UNSPECIFIED:
            return binary_value
        if subtype == UUID_SUBTYPE:
            # Legacy behavior: use STANDARD with binary subtype 4.
            uuid_representation = UuidRepresentation.STANDARD
        elif uuid_representation == UuidRepresentation.STANDARD:
            # subtype == OLD_UUID_SUBTYPE
            # Legacy behavior: STANDARD is the same as PYTHON_LEGACY.
            uuid_representation = UuidRepresentation.PYTHON_LEGACY
        return binary_value.as_uuid(uuid_representation)

    if subtype == 0:
        return cast(uuid.UUID, data)
    return Binary(data, subtype)


def _parse_legacy_binary(doc: Any, json_options: JSONOptions) -> Union[Binary, uuid.UUID]:
    if isinstance(doc["$type"], int):
        doc["$type"] = "%02x" % doc["$type"]
    subtype = int(doc["$type"], 16)
    if subtype >= 0xFFFFFF80:  # Handle mongoexport values
        subtype = int(doc["$type"][6:], 16)
    data = base64.b64decode(doc["$binary"].encode())
    return _binary_or_uuid(data, subtype, json_options)


def _parse_canonical_binary(doc: Any, json_options: JSONOptions) -> Union[Binary, uuid.UUID]:
    binary = doc["$binary"]
    b64 = binary["base64"]
    subtype = binary["subType"]
    if not isinstance(b64, str):
        raise TypeError("$binary base64 must be a string: %s" % (doc,))
    if not isinstance(subtype, str) or len(subtype) > 2:
        raise TypeError("$binary subType must be a string at most 2 characters: %s" % (doc,))
    if len(binary) != 2:
        raise TypeError('$binary must include only "base64" and "subType" components: %s' % (doc,))

    data = base64.b64decode(b64.encode())
    return _binary_or_uuid(data, int(subtype, 16), json_options)


def _parse_canonical_datetime(
    doc: Any, json_options: JSONOptions
) -> Union[datetime.datetime, DatetimeMS]:
    """Decode a JSON datetime to python datetime.datetime."""
    dtm = doc["$date"]
    if len(doc) != 1:
        raise TypeError("Bad $date, extra field(s): %s" % (doc,))
    # mongoexport 2.6 and newer
    if isinstance(dtm, str):
        # Parse offset
        if dtm[-1] == "Z":
            dt = dtm[:-1]
            offset = "Z"
        elif dtm[-6] in ("+", "-") and dtm[-3] == ":":
            # (+|-)HH:MM
            dt = dtm[:-6]
            offset = dtm[-6:]
        elif dtm[-5] in ("+", "-"):
            # (+|-)HHMM
            dt = dtm[:-5]
            offset = dtm[-5:]
        elif dtm[-3] in ("+", "-"):
            # (+|-)HH
            dt = dtm[:-3]
            offset = dtm[-3:]
        else:
            dt = dtm
            offset = ""

        # Parse the optional factional seconds portion.
        dot_index = dt.rfind(".")
        microsecond = 0
        if dot_index != -1:
            microsecond = int(float(dt[dot_index:]) * 1000000)
            dt = dt[:dot_index]

        aware = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S").replace(
            microsecond=microsecond, tzinfo=utc
        )

        if offset and offset != "Z":
            if len(offset) == 6:
                hours, minutes = offset[1:].split(":")
                secs = int(hours) * 3600 + int(minutes) * 60
            elif len(offset) == 5:
                secs = int(offset[1:3]) * 3600 + int(offset[3:]) * 60
            elif len(offset) == 3:
                secs = int(offset[1:3]) * 3600
            if offset[0] == "-":
                secs *= -1
            aware = aware - datetime.timedelta(seconds=secs)

        if json_options.tz_aware:
            if json_options.tzinfo:
                aware = aware.astimezone(json_options.tzinfo)
            if json_options.datetime_conversion == DatetimeConversion.DATETIME_MS:
                return DatetimeMS(aware)
            return aware
        else:
            aware_tzinfo_none = aware.replace(tzinfo=None)
            if json_options.datetime_conversion == DatetimeConversion.DATETIME_MS:
                return DatetimeMS(aware_tzinfo_none)
            return aware_tzinfo_none
    return _millis_to_datetime(int(dtm), json_options)


def _parse_canonical_oid(doc: Any) -> ObjectId:
    """Decode a JSON ObjectId to bson.objectid.ObjectId."""
    if len(doc) != 1:
        raise TypeError("Bad $oid, extra field(s): %s" % (doc,))
    return ObjectId(doc["$oid"])


def _parse_canonical_symbol(doc: Any) -> str:
    """Decode a JSON symbol to Python string."""
    symbol = doc["$symbol"]
    if len(doc) != 1:
        raise TypeError("Bad $symbol, extra field(s): %s" % (doc,))
    return str(symbol)


def _parse_canonical_code(doc: Any) -> Code:
    """Decode a JSON code to bson.code.Code."""
    for key in doc:
        if key not in ("$code", "$scope"):
            raise TypeError("Bad $code, extra field(s): %s" % (doc,))
    return Code(doc["$code"], scope=doc.get("$scope"))


def _parse_canonical_regex(doc: Any) -> Regex:
    """Decode a JSON regex to bson.regex.Regex."""
    regex = doc["$regularExpression"]
    if len(doc) != 1:
        raise TypeError("Bad $regularExpression, extra field(s): %s" % (doc,))
    if len(regex) != 2:
        raise TypeError(
            'Bad $regularExpression must include only "pattern"'
            'and "options" components: %s' % (doc,)
        )
    opts = regex["options"]
    if not isinstance(opts, str):
        raise TypeError(
            "Bad $regularExpression options, options must be string, was type %s" % (type(opts))
        )
    return Regex(regex["pattern"], opts)


def _parse_canonical_dbref(doc: Any) -> DBRef:
    """Decode a JSON DBRef to bson.dbref.DBRef."""
    return DBRef(doc.pop("$ref"), doc.pop("$id"), database=doc.pop("$db", None), **doc)


def _parse_canonical_dbpointer(doc: Any) -> Any:
    """Decode a JSON (deprecated) DBPointer to bson.dbref.DBRef."""
    dbref = doc["$dbPointer"]
    if len(doc) != 1:
        raise TypeError("Bad $dbPointer, extra field(s): %s" % (doc,))
    if isinstance(dbref, DBRef):
        dbref_doc = dbref.as_doc()
        # DBPointer must not contain $db in its value.
        if dbref.database is not None:
            raise TypeError("Bad $dbPointer, extra field $db: %s" % (dbref_doc,))
        if not isinstance(dbref.id, ObjectId):
            raise TypeError("Bad $dbPointer, $id must be an ObjectId: %s" % (dbref_doc,))
        if len(dbref_doc) != 2:
            raise TypeError("Bad $dbPointer, extra field(s) in DBRef: %s" % (dbref_doc,))
        return dbref
    else:
        raise TypeError("Bad $dbPointer, expected a DBRef: %s" % (doc,))


def _parse_canonical_int32(doc: Any) -> int:
    """Decode a JSON int32 to python int."""
    i_str = doc["$numberInt"]
    if len(doc) != 1:
        raise TypeError("Bad $numberInt, extra field(s): %s" % (doc,))
    if not isinstance(i_str, str):
        raise TypeError("$numberInt must be string: %s" % (doc,))
    return int(i_str)


def _parse_canonical_int64(doc: Any) -> Int64:
    """Decode a JSON int64 to bson.int64.Int64."""
    l_str = doc["$numberLong"]
    if len(doc) != 1:
        raise TypeError("Bad $numberLong, extra field(s): %s" % (doc,))
    return Int64(l_str)


def _parse_canonical_double(doc: Any) -> float:
    """Decode a JSON double to python float."""
    d_str = doc["$numberDouble"]
    if len(doc) != 1:
        raise TypeError("Bad $numberDouble, extra field(s): %s" % (doc,))
    if not isinstance(d_str, str):
        raise TypeError("$numberDouble must be string: %s" % (doc,))
    return float(d_str)


def _parse_canonical_decimal128(doc: Any) -> Decimal128:
    """Decode a JSON decimal128 to bson.decimal128.Decimal128."""
    d_str = doc["$numberDecimal"]
    if len(doc) != 1:
        raise TypeError("Bad $numberDecimal, extra field(s): %s" % (doc,))
    if not isinstance(d_str, str):
        raise TypeError("$numberDecimal must be string: %s" % (doc,))
    return Decimal128(d_str)


def _parse_canonical_minkey(doc: Any) -> MinKey:
    """Decode a JSON MinKey to bson.min_key.MinKey."""
    if type(doc["$minKey"]) is not int or doc["$minKey"] != 1:
        raise TypeError("$minKey value must be 1: %s" % (doc,))
    if len(doc) != 1:
        raise TypeError("Bad $minKey, extra field(s): %s" % (doc,))
    return MinKey()


def _parse_canonical_maxkey(doc: Any) -> MaxKey:
    """Decode a JSON MaxKey to bson.max_key.MaxKey."""
    if type(doc["$maxKey"]) is not int or doc["$maxKey"] != 1:
        raise TypeError("$maxKey value must be 1: %s", (doc,))
    if len(doc) != 1:
        raise TypeError("Bad $minKey, extra field(s): %s" % (doc,))
    return MaxKey()


def _encode_binary(data: bytes, subtype: int, json_options: JSONOptions) -> Any:
    if json_options.json_mode == JSONMode.LEGACY:
        return SON([("$binary", base64.b64encode(data).decode()), ("$type", "%02x" % subtype)])
    return {
        "$binary": SON([("base64", base64.b64encode(data).decode()), ("subType", "%02x" % subtype)])
    }


def default(obj: Any, json_options: JSONOptions = DEFAULT_JSON_OPTIONS) -> Any:
    # We preserve key order when rendering SON, DBRef, etc. as JSON by
    # returning a SON for those types instead of a dict.
    if isinstance(obj, ObjectId):
        return {"$oid": str(obj)}
    if isinstance(obj, DBRef):
        return _json_convert(obj.as_doc(), json_options=json_options)
    if isinstance(obj, datetime.datetime):
        if json_options.datetime_representation == DatetimeRepresentation.ISO8601:
            if not obj.tzinfo:
                obj = obj.replace(tzinfo=utc)
                assert obj.tzinfo is not None
            if obj >= EPOCH_AWARE:
                off = obj.tzinfo.utcoffset(obj)
                if (off.days, off.seconds, off.microseconds) == (0, 0, 0):  # type: ignore
                    tz_string = "Z"
                else:
                    tz_string = obj.strftime("%z")
                millis = int(obj.microsecond / 1000)
                fracsecs = ".%03d" % (millis,) if millis else ""
                return {
                    "$date": "%s%s%s" % (obj.strftime("%Y-%m-%dT%H:%M:%S"), fracsecs, tz_string)
                }

        millis = _datetime_to_millis(obj)
        if json_options.datetime_representation == DatetimeRepresentation.LEGACY:
            return {"$date": millis}
        return {"$date": {"$numberLong": str(millis)}}
    if isinstance(obj, DatetimeMS):
        if (
            json_options.datetime_representation == DatetimeRepresentation.ISO8601
            and 0 <= int(obj) <= _max_datetime_ms()
        ):
            return default(obj.as_datetime(), json_options)
        elif json_options.datetime_representation == DatetimeRepresentation.LEGACY:
            return {"$date": str(int(obj))}
        return {"$date": {"$numberLong": str(int(obj))}}
    if json_options.strict_number_long and isinstance(obj, Int64):
        return {"$numberLong": str(obj)}
    if isinstance(obj, (RE_TYPE, Regex)):
        flags = ""
        if obj.flags & re.IGNORECASE:
            flags += "i"
        if obj.flags & re.LOCALE:
            flags += "l"
        if obj.flags & re.MULTILINE:
            flags += "m"
        if obj.flags & re.DOTALL:
            flags += "s"
        if obj.flags & re.UNICODE:
            flags += "u"
        if obj.flags & re.VERBOSE:
            flags += "x"
        if isinstance(obj.pattern, str):
            pattern = obj.pattern
        else:
            pattern = obj.pattern.decode("utf-8")
        if json_options.json_mode == JSONMode.LEGACY:
            return SON([("$regex", pattern), ("$options", flags)])
        return {"$regularExpression": SON([("pattern", pattern), ("options", flags)])}
    if isinstance(obj, MinKey):
        return {"$minKey": 1}
    if isinstance(obj, MaxKey):
        return {"$maxKey": 1}
    if isinstance(obj, Timestamp):
        return {"$timestamp": SON([("t", obj.time), ("i", obj.inc)])}
    if isinstance(obj, Code):
        if obj.scope is None:
            return {"$code": str(obj)}
        return SON([("$code", str(obj)), ("$scope", _json_convert(obj.scope, json_options))])
    if isinstance(obj, Binary):
        return _encode_binary(obj, obj.subtype, json_options)
    if isinstance(obj, bytes):
        return _encode_binary(obj, 0, json_options)
    if isinstance(obj, uuid.UUID):
        if json_options.strict_uuid:
            binval = Binary.from_uuid(obj, uuid_representation=json_options.uuid_representation)
            return _encode_binary(binval, binval.subtype, json_options)
        else:
            return {"$uuid": obj.hex}
    if isinstance(obj, Decimal128):
        return {"$numberDecimal": str(obj)}
    if isinstance(obj, bool):
        return obj
    if json_options.json_mode == JSONMode.CANONICAL and isinstance(obj, int):
        if -(2**31) <= obj < 2**31:
            return {"$numberInt": str(obj)}
        return {"$numberLong": str(obj)}
    if json_options.json_mode != JSONMode.LEGACY and isinstance(obj, float):
        if math.isnan(obj):
            return {"$numberDouble": "NaN"}
        elif math.isinf(obj):
            representation = "Infinity" if obj > 0 else "-Infinity"
            return {"$numberDouble": representation}
        elif json_options.json_mode == JSONMode.CANONICAL:
            # repr() will return the shortest string guaranteed to produce the
            # original value, when float() is called on it.
            return {"$numberDouble": str(repr(obj))}
    raise TypeError("%r is not JSON serializable" % obj)
