from __future__ import annotations

import typing
from collections.abc import Iterable, Iterator, MutableMapping
from typing import Generic, Protocol, TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_VT_co = TypeVar("_VT_co", covariant=True)

class SupportsKeysAndGetItem(Protocol[_KT, _VT_co]):
    def keys(self) -> Iterable[_KT]: ...
    def __getitem__(self, __key: _KT) -> _VT_co: ...

DictParamType: typing.TypeAlias = (
      SupportsKeysAndGetItem[_KT, _VT]
    | Iterable[tuple[_KT, _VT]]
    | Iterable[list[str]]
)

class CustomHashMap(Generic[_KT, _VT], MutableMapping[_KT, _VT]):
    # shamelessly stolen from the python typeshed
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self: CustomHashMap[str, _VT], **kwargs: _VT) -> None: ...
    @typing.overload
    def __init__(self, __map: SupportsKeysAndGetItem[_KT, _VT], /) -> None: ...
    @typing.overload
    def __init__(
        self: CustomHashMap[str, _VT],
        __map: SupportsKeysAndGetItem[str, _VT],
        /,
        **kwargs: _VT
    ) -> None: ...
    @typing.overload
    def __init__(self, __iterable: Iterable[tuple[_KT, _VT]], /) -> None: ...
    @typing.overload
    def __init__(
        self: CustomHashMap[str, _VT],
        __iterable: Iterable[tuple[str, _VT]],
        /,
        **kwargs: _VT
    ) -> None: ...
    @typing.overload
    def __init__(
        self: CustomHashMap[str, str],
        __iterable: Iterable[list[str]],
    ) -> None: ...
    # MutableMapping abstract methods
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_KT]: ...
    def __getitem__(self, key: _KT) -> _VT: ...
    def __setitem__(self, key: _KT, value: _VT) -> None: ...
    def __delitem__(self, key: _KT) -> None: ...
