# Copyright 2022-present MongoDB, Inc.
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

"""Workaround for https://bugs.python.org/issue43923.
Ideally we would have done this with a single class, but
generic subclasses *must* take a parameter, and prior to Python 3.9
or in Python 3.7 and 3.8 with `from __future__ import annotations`,
you get the error: "TypeError: 'type' object is not subscriptable".
"""

import datetime
import abc
import enum
from typing import Tuple, Generic, Optional, Mapping, Any, TypeVar, Type, Dict, Iterable, Tuple, MutableMapping, Callable, Union


class TypeEncoder(abc.ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def python_type(self) -> Any: ...
    @abc.abstractmethod
    def transform_python(self, value: Any) -> Any: ...

class TypeDecoder(abc.ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def bson_type(self) -> Any: ...
    @abc.abstractmethod
    def transform_bson(self, value: Any) -> Any: ...

class TypeCodec(TypeEncoder, TypeDecoder, metaclass=abc.ABCMeta): ...

Codec = Union[TypeEncoder, TypeDecoder, TypeCodec]
Fallback = Callable[[Any], Any]

class TypeRegistry:
    _decoder_map: Dict[Any, Any]
    _encoder_map: Dict[Any, Any]
    _fallback_encoder: Optional[Fallback]

    def __init__(self, type_codecs: Optional[Iterable[Codec]] = ..., fallback_encoder: Optional[Fallback] = ...) -> None: ...
    def __eq__(self, other: Any) -> Any: ...


_DocumentType = TypeVar("_DocumentType", bound=Mapping[str, Any])

class DatetimeConversion(int, enum.Enum):
    DATETIME = ...
    DATETIME_CLAMP = ...
    DATETIME_MS = ...
    DATETIME_AUTO = ...

class CodecOptions(Tuple, Generic[_DocumentType]):
    document_class: Type[_DocumentType]
    tz_aware: bool
    uuid_representation: int
    unicode_decode_error_handler: Optional[str]
    tzinfo: Optional[datetime.tzinfo]
    type_registry: TypeRegistry
    datetime_conversion: Optional[int]

    def __new__(
        cls: Type[CodecOptions],
        document_class: Optional[Type[_DocumentType]] = ...,
        tz_aware: bool = ...,
        uuid_representation: Optional[int] = ...,
        unicode_decode_error_handler: Optional[str] = ...,
        tzinfo: Optional[datetime.tzinfo] = ...,
        type_registry: Optional[TypeRegistry] = ...,
        datetime_conversion: Optional[int] = ...,
    ) -> CodecOptions[_DocumentType]: ...

    # CodecOptions API
    def with_options(self, **kwargs: Any) -> CodecOptions[_DocumentType]: ...

    def _arguments_repr(self) -> str: ...

    def _options_dict(self) -> Dict[Any, Any]: ...

    # NamedTuple API
    @classmethod
    def _make(cls, obj: Iterable) -> CodecOptions[_DocumentType]: ...

    def _asdict(self) -> Dict[str, Any]: ...

    def _replace(self, **kwargs: Any) -> CodecOptions[_DocumentType]: ...

    _source: str
    _fields: Tuple[str]


DEFAULT_CODEC_OPTIONS: CodecOptions[MutableMapping[str, Any]]
_RAW_BSON_DOCUMENT_MARKER: int

def _raw_document_class(document_class: Any) -> bool: ...

def _parse_codec_options(options: Any) -> CodecOptions: ...
