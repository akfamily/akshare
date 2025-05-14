import enum
import reprlib
import sys
from abc import abstractmethod
from array import array
from collections.abc import (
    Callable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    ValuesView,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    NoReturn,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)

from ._abc import MDArg, MultiMapping, MutableMultiMapping, SupportsKeys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class istr(str):
    """Case insensitive str."""

    __is_istr__ = True
    __istr_title__: Optional[str] = None


_V = TypeVar("_V")
_T = TypeVar("_T")

_SENTINEL = enum.Enum("_SENTINEL", "sentinel")
sentinel = _SENTINEL.sentinel

_version = array("Q", [0])


class _Impl(Generic[_V]):
    __slots__ = ("_items", "_version")

    def __init__(self) -> None:
        self._items: list[tuple[str, str, _V]] = []
        self.incr_version()

    def incr_version(self) -> None:
        v = _version
        v[0] += 1
        self._version = v[0]

    if sys.implementation.name != "pypy":

        def __sizeof__(self) -> int:
            return object.__sizeof__(self) + sys.getsizeof(self._items)


class _Iter(Generic[_T]):
    __slots__ = ("_size", "_iter")

    def __init__(self, size: int, iterator: Iterator[_T]):
        self._size = size
        self._iter = iterator

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> _T:
        return next(self._iter)

    def __length_hint__(self) -> int:
        return self._size


class _ViewBase(Generic[_V]):
    def __init__(
        self,
        impl: _Impl[_V],
        identfunc: Callable[[str], str],
        keyfunc: Callable[[str], str],
    ):
        self._impl = impl
        self._identfunc = identfunc
        self._keyfunc = keyfunc

    def __len__(self) -> int:
        return len(self._impl._items)


class _ItemsView(_ViewBase[_V], ItemsView[str, _V]):
    def __contains__(self, item: object) -> bool:
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            return False
        key, value = item
        try:
            ident = self._identfunc(key)
        except TypeError:
            return False
        for i, k, v in self._impl._items:
            if ident == i and value == v:
                return True
        return False

    def __iter__(self) -> _Iter[tuple[str, _V]]:
        return _Iter(len(self), self._iter(self._impl._version))

    def _iter(self, version: int) -> Iterator[tuple[str, _V]]:
        for i, k, v in self._impl._items:
            if version != self._impl._version:
                raise RuntimeError("Dictionary changed during iteration")
            yield self._keyfunc(k), v

    @reprlib.recursive_repr()
    def __repr__(self) -> str:
        lst = []
        for i, k, v in self._impl._items:
            lst.append(f"'{k}': {v!r}")
        body = ", ".join(lst)
        return f"<{self.__class__.__name__}({body})>"

    def _parse_item(
        self, arg: Union[tuple[str, _V], _T]
    ) -> Optional[tuple[str, str, _V]]:
        if not isinstance(arg, tuple):
            return None
        if len(arg) != 2:
            return None
        try:
            return (self._identfunc(arg[0]), arg[0], arg[1])
        except TypeError:
            return None

    def _tmp_set(self, it: Iterable[_T]) -> set[tuple[str, _V]]:
        tmp = set()
        for arg in it:
            item = self._parse_item(arg)
            if item is None:
                continue
            else:
                tmp.add((item[0], item[2]))
        return tmp

    def __and__(self, other: Iterable[Any]) -> set[tuple[str, _V]]:
        ret = set()
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for arg in it:
            item = self._parse_item(arg)
            if item is None:
                continue
            identity, key, value = item
            for i, k, v in self._impl._items:
                if i == identity and v == value:
                    ret.add((k, v))
        return ret

    def __rand__(self, other: Iterable[_T]) -> set[_T]:
        ret = set()
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for arg in it:
            item = self._parse_item(arg)
            if item is None:
                continue
            identity, key, value = item
            for i, k, v in self._impl._items:
                if i == identity and v == value:
                    ret.add(arg)
                    break
        return ret

    def __or__(self, other: Iterable[_T]) -> set[Union[tuple[str, _V], _T]]:
        ret: set[Union[tuple[str, _V], _T]] = set(self)
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for arg in it:
            item: Optional[tuple[str, str, _V]] = self._parse_item(arg)
            if item is None:
                ret.add(arg)
                continue
            identity, key, value = item
            for i, k, v in self._impl._items:
                if i == identity and v == value:
                    break
            else:
                ret.add(arg)
        return ret

    def __ror__(self, other: Iterable[_T]) -> set[Union[tuple[str, _V], _T]]:
        try:
            ret: set[Union[tuple[str, _V], _T]] = set(other)
        except TypeError:
            return NotImplemented
        tmp = self._tmp_set(ret)

        for i, k, v in self._impl._items:
            if (i, v) not in tmp:
                ret.add((k, v))
        return ret

    def __sub__(self, other: Iterable[_T]) -> set[Union[tuple[str, _V], _T]]:
        ret: set[Union[tuple[str, _V], _T]] = set()
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        tmp = self._tmp_set(it)

        for i, k, v in self._impl._items:
            if (i, v) not in tmp:
                ret.add((k, v))

        return ret

    def __rsub__(self, other: Iterable[_T]) -> set[_T]:
        ret: set[_T] = set()
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for arg in it:
            item = self._parse_item(arg)
            if item is None:
                ret.add(arg)
                continue

            identity, key, value = item
            for i, k, v in self._impl._items:
                if i == identity and v == value:
                    break
            else:
                ret.add(arg)
        return ret

    def __xor__(self, other: Iterable[_T]) -> set[Union[tuple[str, _V], _T]]:
        try:
            rgt = set(other)
        except TypeError:
            return NotImplemented
        ret: set[Union[tuple[str, _V], _T]] = self - rgt
        ret |= rgt - self
        return ret

    __rxor__ = __xor__

    def isdisjoint(self, other: Iterable[tuple[str, _V]]) -> bool:
        for arg in other:
            item = self._parse_item(arg)
            if item is None:
                continue

            identity, key, value = item
            for i, k, v in self._impl._items:
                if i == identity and v == value:
                    return False
        return True


class _ValuesView(_ViewBase[_V], ValuesView[_V]):
    def __contains__(self, value: object) -> bool:
        for i, k, v in self._impl._items:
            if v == value:
                return True
        return False

    def __iter__(self) -> _Iter[_V]:
        return _Iter(len(self), self._iter(self._impl._version))

    def _iter(self, version: int) -> Iterator[_V]:
        for i, k, v in self._impl._items:
            if version != self._impl._version:
                raise RuntimeError("Dictionary changed during iteration")
            yield v

    @reprlib.recursive_repr()
    def __repr__(self) -> str:
        lst = []
        for i, k, v in self._impl._items:
            lst.append(repr(v))
        body = ", ".join(lst)
        return f"<{self.__class__.__name__}({body})>"


class _KeysView(_ViewBase[_V], KeysView[str]):
    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        identity = self._identfunc(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return True
        return False

    def __iter__(self) -> _Iter[str]:
        return _Iter(len(self), self._iter(self._impl._version))

    def _iter(self, version: int) -> Iterator[str]:
        for i, k, v in self._impl._items:
            if version != self._impl._version:
                raise RuntimeError("Dictionary changed during iteration")
            yield self._keyfunc(k)

    def __repr__(self) -> str:
        lst = []
        for i, k, v in self._impl._items:
            lst.append(f"'{k}'")
        body = ", ".join(lst)
        return f"<{self.__class__.__name__}({body})>"

    def __and__(self, other: Iterable[object]) -> set[str]:
        ret = set()
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for key in it:
            if not isinstance(key, str):
                continue
            identity = self._identfunc(key)
            for i, k, v in self._impl._items:
                if i == identity:
                    ret.add(k)
        return ret

    def __rand__(self, other: Iterable[_T]) -> set[_T]:
        ret = set()
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for key in it:
            if not isinstance(key, str):
                continue
            identity = self._identfunc(key)
            for i, k, v in self._impl._items:
                if i == identity:
                    ret.add(key)
        return cast(set[_T], ret)

    def __or__(self, other: Iterable[_T]) -> set[Union[str, _T]]:
        ret: set[Union[str, _T]] = set(self)
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for key in it:
            if not isinstance(key, str):
                ret.add(key)
                continue
            identity = self._identfunc(key)
            for i, k, v in self._impl._items:
                if i == identity:
                    break
            else:
                ret.add(key)
        return ret

    def __ror__(self, other: Iterable[_T]) -> set[Union[str, _T]]:
        try:
            ret: set[Union[str, _T]] = set(other)
        except TypeError:
            return NotImplemented

        tmp = set()
        for key in ret:
            if not isinstance(key, str):
                continue
            identity = self._identfunc(key)
            tmp.add(identity)

        for i, k, v in self._impl._items:
            if i not in tmp:
                ret.add(k)
        return ret

    def __sub__(self, other: Iterable[object]) -> set[str]:
        ret = set(self)
        try:
            it = iter(other)
        except TypeError:
            return NotImplemented
        for key in it:
            if not isinstance(key, str):
                continue
            identity = self._identfunc(key)
            for i, k, v in self._impl._items:
                if i == identity:
                    ret.discard(k)
                    break
        return ret

    def __rsub__(self, other: Iterable[_T]) -> set[_T]:
        try:
            ret: set[_T] = set(other)
        except TypeError:
            return NotImplemented
        for key in other:
            if not isinstance(key, str):
                continue
            identity = self._identfunc(key)
            for i, k, v in self._impl._items:
                if i == identity:
                    ret.discard(key)  # type: ignore[arg-type]
                    break
        return ret

    def __xor__(self, other: Iterable[_T]) -> set[Union[str, _T]]:
        try:
            rgt = set(other)
        except TypeError:
            return NotImplemented
        ret: set[Union[str, _T]] = self - rgt  # type: ignore[assignment]
        ret |= rgt - self
        return ret

    __rxor__ = __xor__

    def isdisjoint(self, other: Iterable[object]) -> bool:
        for key in other:
            if not isinstance(key, str):
                continue
            identity = self._identfunc(key)
            for i, k, v in self._impl._items:
                if i == identity:
                    return False
        return True


class _CSMixin:
    def _key(self, key: str) -> str:
        return key

    def _title(self, key: str) -> str:
        if isinstance(key, str):
            return key
        else:
            raise TypeError("MultiDict keys should be either str or subclasses of str")


class _CIMixin:
    _ci: bool = True

    def _key(self, key: str) -> str:
        if type(key) is istr:
            return key
        else:
            return istr(key)

    def _title(self, key: str) -> str:
        if isinstance(key, istr):
            ret = key.__istr_title__
            if ret is None:
                ret = key.title()
                key.__istr_title__ = ret
            return ret
        if isinstance(key, str):
            return key.title()
        else:
            raise TypeError("MultiDict keys should be either str or subclasses of str")


class _Base(MultiMapping[_V]):
    _impl: _Impl[_V]
    _ci: bool = False

    @abstractmethod
    def _key(self, key: str) -> str: ...

    @abstractmethod
    def _title(self, key: str) -> str: ...

    @overload
    def getall(self, key: str) -> list[_V]: ...
    @overload
    def getall(self, key: str, default: _T) -> Union[list[_V], _T]: ...
    def getall(
        self, key: str, default: Union[_T, _SENTINEL] = sentinel
    ) -> Union[list[_V], _T]:
        """Return a list of all values matching the key."""
        identity = self._title(key)
        res = [v for i, k, v in self._impl._items if i == identity]
        if res:
            return res
        if not res and default is not sentinel:
            return default
        raise KeyError("Key not found: %r" % key)

    @overload
    def getone(self, key: str) -> _V: ...
    @overload
    def getone(self, key: str, default: _T) -> Union[_V, _T]: ...
    def getone(
        self, key: str, default: Union[_T, _SENTINEL] = sentinel
    ) -> Union[_V, _T]:
        """Get first value matching the key.

        Raises KeyError if the key is not found and no default is provided.
        """
        identity = self._title(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return v
        if default is not sentinel:
            return default
        raise KeyError("Key not found: %r" % key)

    # Mapping interface #

    def __getitem__(self, key: str) -> _V:
        return self.getone(key)

    @overload
    def get(self, key: str, /) -> Union[_V, None]: ...
    @overload
    def get(self, key: str, /, default: _T) -> Union[_V, _T]: ...
    def get(self, key: str, default: Union[_T, None] = None) -> Union[_V, _T, None]:
        """Get first value matching the key.

        If the key is not found, returns the default (or None if no default is provided)
        """
        return self.getone(key, default)

    def __iter__(self) -> Iterator[str]:
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self._impl._items)

    def keys(self) -> KeysView[str]:
        """Return a new view of the dictionary's keys."""
        return _KeysView(self._impl, self._title, self._key)

    def items(self) -> ItemsView[str, _V]:
        """Return a new view of the dictionary's items *(key, value) pairs)."""
        return _ItemsView(self._impl, self._title, self._key)

    def values(self) -> _ValuesView[_V]:
        """Return a new view of the dictionary's values."""
        return _ValuesView(self._impl, self._title, self._key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mapping):
            return NotImplemented
        if isinstance(other, _Base):
            lft = self._impl._items
            rht = other._impl._items
            if len(lft) != len(rht):
                return False
            for (i1, k2, v1), (i2, k2, v2) in zip(lft, rht):
                if i1 != i2 or v1 != v2:
                    return False
            return True
        if len(self._impl._items) != len(other):
            return False
        for k, v in self.items():
            nv = other.get(k, sentinel)
            if v != nv:
                return False
        return True

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        identity = self._title(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return True
        return False

    @reprlib.recursive_repr()
    def __repr__(self) -> str:
        body = ", ".join(f"'{k}': {v!r}" for i, k, v in self._impl._items)
        return f"<{self.__class__.__name__}({body})>"


class MultiDict(_CSMixin, _Base[_V], MutableMultiMapping[_V]):
    """Dictionary with the support for duplicate keys."""

    def __init__(self, arg: MDArg[_V] = None, /, **kwargs: _V):
        self._impl = _Impl()

        self._extend(arg, kwargs, self.__class__.__name__, self._extend_items)

    if sys.implementation.name != "pypy":

        def __sizeof__(self) -> int:
            return object.__sizeof__(self) + sys.getsizeof(self._impl)

    def __reduce__(self) -> tuple[type[Self], tuple[list[tuple[str, _V]]]]:
        return (self.__class__, (list(self.items()),))

    def add(self, key: str, value: _V) -> None:
        identity = self._title(key)
        self._impl._items.append((identity, key, value))
        self._impl.incr_version()

    def copy(self) -> Self:
        """Return a copy of itself."""
        cls = self.__class__
        return cls(self.items())

    __copy__ = copy

    def extend(self, arg: MDArg[_V] = None, /, **kwargs: _V) -> None:
        """Extend current MultiDict with more values.

        This method must be used instead of update.
        """
        self._extend(arg, kwargs, "extend", self._extend_items)

    def _extend(
        self,
        arg: MDArg[_V],
        kwargs: Mapping[str, _V],
        name: str,
        method: Callable[[list[tuple[str, str, _V]]], None],
    ) -> None:
        if arg:
            if isinstance(arg, (MultiDict, MultiDictProxy)):
                if self._ci is not arg._ci:
                    items = [(self._title(k), k, v) for _, k, v in arg._impl._items]
                else:
                    items = arg._impl._items
                    if kwargs:
                        items = items.copy()
                if kwargs:
                    for key, value in kwargs.items():
                        items.append((self._title(key), key, value))
            else:
                if hasattr(arg, "keys"):
                    arg = cast(SupportsKeys[_V], arg)
                    arg = [(k, arg[k]) for k in arg.keys()]
                if kwargs:
                    arg = list(arg)
                    arg.extend(list(kwargs.items()))
                items = []
                for pos, item in enumerate(arg):
                    if not len(item) == 2:
                        raise ValueError(
                            f"multidict update sequence element #{pos}"
                            f"has length {len(item)}; 2 is required"
                        )
                    items.append((self._title(item[0]), item[0], item[1]))

            method(items)
        else:
            method([(self._title(key), key, value) for key, value in kwargs.items()])

    def _extend_items(self, items: Iterable[tuple[str, str, _V]]) -> None:
        for identity, key, value in items:
            self._impl._items.append((identity, key, value))
        self._impl.incr_version()

    def clear(self) -> None:
        """Remove all items from MultiDict."""
        self._impl._items.clear()
        self._impl.incr_version()

    # Mapping interface #

    def __setitem__(self, key: str, value: _V) -> None:
        self._replace(key, value)

    def __delitem__(self, key: str) -> None:
        identity = self._title(key)
        items = self._impl._items
        found = False
        for i in range(len(items) - 1, -1, -1):
            if items[i][0] == identity:
                del items[i]
                found = True
        if not found:
            raise KeyError(key)
        else:
            self._impl.incr_version()

    @overload
    def setdefault(
        self: "MultiDict[Union[_T, None]]", key: str, default: None = None
    ) -> Union[_T, None]: ...
    @overload
    def setdefault(self, key: str, default: _V) -> _V: ...
    def setdefault(self, key: str, default: Union[_V, None] = None) -> Union[_V, None]:  # type: ignore[misc]
        """Return value for key, set value to default if key is not present."""
        identity = self._title(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return v
        self.add(key, default)  # type: ignore[arg-type]
        return default

    @overload
    def popone(self, key: str) -> _V: ...
    @overload
    def popone(self, key: str, default: _T) -> Union[_V, _T]: ...
    def popone(
        self, key: str, default: Union[_T, _SENTINEL] = sentinel
    ) -> Union[_V, _T]:
        """Remove specified key and return the corresponding value.

        If key is not found, d is returned if given, otherwise
        KeyError is raised.

        """
        identity = self._title(key)
        for i in range(len(self._impl._items)):
            if self._impl._items[i][0] == identity:
                value = self._impl._items[i][2]
                del self._impl._items[i]
                self._impl.incr_version()
                return value
        if default is sentinel:
            raise KeyError(key)
        else:
            return default

    # Type checking will inherit signature for pop() if we don't confuse it here.
    if not TYPE_CHECKING:
        pop = popone

    @overload
    def popall(self, key: str) -> list[_V]: ...
    @overload
    def popall(self, key: str, default: _T) -> Union[list[_V], _T]: ...
    def popall(
        self, key: str, default: Union[_T, _SENTINEL] = sentinel
    ) -> Union[list[_V], _T]:
        """Remove all occurrences of key and return the list of corresponding
        values.

        If key is not found, default is returned if given, otherwise
        KeyError is raised.

        """
        found = False
        identity = self._title(key)
        ret = []
        for i in range(len(self._impl._items) - 1, -1, -1):
            item = self._impl._items[i]
            if item[0] == identity:
                ret.append(item[2])
                del self._impl._items[i]
                self._impl.incr_version()
                found = True
        if not found:
            if default is sentinel:
                raise KeyError(key)
            else:
                return default
        else:
            ret.reverse()
            return ret

    def popitem(self) -> tuple[str, _V]:
        """Remove and return an arbitrary (key, value) pair."""
        if self._impl._items:
            i, k, v = self._impl._items.pop()
            self._impl.incr_version()
            return self._key(k), v
        else:
            raise KeyError("empty multidict")

    def update(self, arg: MDArg[_V] = None, /, **kwargs: _V) -> None:
        """Update the dictionary from *other*, overwriting existing keys."""
        self._extend(arg, kwargs, "update", self._update_items)

    def _update_items(self, items: list[tuple[str, str, _V]]) -> None:
        if not items:
            return
        used_keys: dict[str, int] = {}
        for identity, key, value in items:
            start = used_keys.get(identity, 0)
            for i in range(start, len(self._impl._items)):
                item = self._impl._items[i]
                if item[0] == identity:
                    used_keys[identity] = i + 1
                    self._impl._items[i] = (identity, key, value)
                    break
            else:
                self._impl._items.append((identity, key, value))
                used_keys[identity] = len(self._impl._items)

        # drop tails
        i = 0
        while i < len(self._impl._items):
            item = self._impl._items[i]
            identity = item[0]
            pos = used_keys.get(identity)
            if pos is None:
                i += 1
                continue
            if i >= pos:
                del self._impl._items[i]
            else:
                i += 1

        self._impl.incr_version()

    def _replace(self, key: str, value: _V) -> None:
        identity = self._title(key)
        items = self._impl._items

        for i in range(len(items)):
            item = items[i]
            if item[0] == identity:
                items[i] = (identity, key, value)
                # i points to last found item
                rgt = i
                self._impl.incr_version()
                break
        else:
            self._impl._items.append((identity, key, value))
            self._impl.incr_version()
            return

        # remove all tail items
        # Mypy bug: https://github.com/python/mypy/issues/14209
        i = rgt + 1  # type: ignore[possibly-undefined]
        while i < len(items):
            item = items[i]
            if item[0] == identity:
                del items[i]
            else:
                i += 1


class CIMultiDict(_CIMixin, MultiDict[_V]):
    """Dictionary with the support for duplicate case-insensitive keys."""


class MultiDictProxy(_CSMixin, _Base[_V]):
    """Read-only proxy for MultiDict instance."""

    def __init__(self, arg: Union[MultiDict[_V], "MultiDictProxy[_V]"]):
        if not isinstance(arg, (MultiDict, MultiDictProxy)):
            raise TypeError(
                "ctor requires MultiDict or MultiDictProxy instance"
                f", not {type(arg)}"
            )

        self._impl = arg._impl

    def __reduce__(self) -> NoReturn:
        raise TypeError(f"can't pickle {self.__class__.__name__} objects")

    def copy(self) -> MultiDict[_V]:
        """Return a copy of itself."""
        return MultiDict(self.items())


class CIMultiDictProxy(_CIMixin, MultiDictProxy[_V]):
    """Read-only proxy for CIMultiDict instance."""

    def __init__(self, arg: Union[MultiDict[_V], MultiDictProxy[_V]]):
        if not isinstance(arg, (CIMultiDict, CIMultiDictProxy)):
            raise TypeError(
                "ctor requires CIMultiDict or CIMultiDictProxy instance"
                f", not {type(arg)}"
            )

        self._impl = arg._impl

    def copy(self) -> CIMultiDict[_V]:
        """Return a copy of itself."""
        return CIMultiDict(self.items())


def getversion(md: Union[MultiDict[object], MultiDictProxy[object]]) -> int:
    if not isinstance(md, _Base):
        raise TypeError("Parameter should be multidict or proxy")
    return md._impl._version
