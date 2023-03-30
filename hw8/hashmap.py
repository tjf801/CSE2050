from __future__ import annotations

import typing
from collections.abc import Iterable, Iterator, MutableMapping
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

if typing.TYPE_CHECKING:
    import types
    # Sadly, since python doesnt have type checkable Sentinel types (see PEP 661 for
    # more info on that), we just have to settle for using ellipsis instead. :(
    _DummyType: typing.TypeAlias = types.EllipsisType

_KT = TypeVar("_KT", bound=typing.Hashable)
_KT_co = TypeVar("_KT_co", bound=typing.Hashable, covariant=True)
_VT = TypeVar("_VT")
_VT_co = TypeVar("_VT_co", covariant=True)

@typing.runtime_checkable
class SupportsKeysAndGetItem(Protocol[_KT, _VT_co]):
    def keys(self) -> Iterable[_KT]: ...
    def __getitem__(self, __key: _KT) -> _VT_co: ...

@dataclass(frozen=True, slots=True)
class _MapEntry(Generic[_KT_co, _VT_co]):
    hash: int # noqa: A003
    key: _KT_co
    value: _VT_co

class CustomHashMap(Generic[_KT, _VT], MutableMapping[_KT, _VT]):
    # NOTE: this takes *heavy* inspiration from python's builtin dict implementation
    
    # class constants
    _INITIAL_SIZE: int = 8
    _PERTURB_SHIFT: int = 5
    _LARGE_DICT_SIZE: int = 50000
    
    # NOTE: this is a sentinel value used to mark deleted entries. The reason it is
    # typed as Ellipsis is because we want to use the type checker to narrow the type
    # of the key using the `is` operator, which it normally only does with `Ellipsis`,
    # `True`, `False`, or `None`, since they're all singletons. This also means, that
    # in order for everything to type check properly, we need to be VERY careful about
    # using the actual `Ellipsis` value and type, because as far as the type checker
    # is concerned, they are the same thing!!
    _DUMMY_VALUE: _DummyType = object() # type: ignore
    
    # instance variables
    _capacity: int
    _used: int
    _table: list[_MapEntry[_KT | _DummyType, _VT] | None]
    
    
    def _lookup(
        self,
        key: typing.Hashable,
        _hash: int | None = None,
    ) -> tuple[int, _MapEntry[_KT, _VT] | None]:
        """Return the index and map entry from the given key and hash.
        
        If the key is not found, return the index where the key should be put and None.
        """
        _hash = _hash or hash(key)
        bit_mask = self._capacity - 1
        
        # used to mark the first free slot
        deleted_slot: int | None = None
        
        table_index = _hash & bit_mask
        perturb = _hash
        
        table_item = self._table[table_index]
        
        while table_item is not None and (
            table_item.hash != _hash
            or table_item.key != key
        ):
            if table_item.key is CustomHashMap._DUMMY_VALUE \
            and deleted_slot is None:
                deleted_slot = table_index
            
            table_index = (5 * table_index + perturb + 1) & bit_mask
            perturb >>= CustomHashMap._PERTURB_SHIFT
            
            table_item = self._table[table_index]
        
        if table_item is None:
            return deleted_slot or table_index, table_item
        
        # TODO: remove these asserts
        # assert entry.key == key and entry.hash == _hash
        # assert entry.key is not CustomHashMap._DUMMY_VALUE
        table_item = typing.cast(
            _MapEntry[_KT, _VT],
            table_item
        )
        
        return table_index, table_item
    
    def _rehash(self) -> None:
        """Resize the table to increase the maximum capacity.
        
        This only gets called when the table is more than 2/3 full.
        Depending on the size of the table, the new capacity will be either
        4x or 2x the old capacity. This is to prevent it from growing too often.
        """
        old_table = self._table
        self._capacity *= 4 if self._capacity <= CustomHashMap._LARGE_DICT_SIZE else 2
        self._table = [None] * self._capacity
        
        for entry in old_table:
            if entry is not None and entry.key is not CustomHashMap._DUMMY_VALUE:
                index, _ = self._lookup(entry.key)
                self._table[index] = entry
        
        del old_table
	
    
    def __init__(
        self,
        __m: SupportsKeysAndGetItem[_KT, _VT]
            | Iterable[tuple[_KT, _VT]]
            | None = None,
        **kwargs: _VT
    ) -> None:
        self._capacity = CustomHashMap._INITIAL_SIZE
        self._used = 0
        self._table = [None] * self._capacity
        
        if __m is not None:
            if isinstance(__m, SupportsKeysAndGetItem):
                for key in __m.keys(): # noqa: SIM118
                    self[key] = __m[key]
            
            elif not hasattr(__m, "__iter__"):
                raise TypeError(f"{type(self).__name__} object is not iterable")
            
            else:
                for key, value in __m:
                    if not hasattr(key, "__hash__"):
                        raise TypeError(f'unhashable type: {type(key).__name__!r}')
                    
                    self[key] = value
        
        if kwargs:
            for key, value in kwargs.items():
                # NOTE: we dont have to check if the key is hashable here because
                # we know its of type str
                
                # mypy doesn't like this at ALL.
                # but the overloads in hashmap.pyi are correct
                self[key] = value # type: ignore
    
    def __len__(self) -> int:
        return self._used
    
    def __contains__(self, key: object) -> bool:
        if not hasattr(key, "__hash__"):
            raise TypeError(f'unhashable type: {type(key).__name__!r}')
        
        _, entry = self._lookup(key)
        
        return entry is not None
    
    def __iter__(self) -> Iterator[_KT]:
        # TODO: maybe preserve insertion order?
        for entry in self._table:
            if entry is not None and entry.key is not CustomHashMap._DUMMY_VALUE:
                yield typing.cast(_KT, entry.key)
    
    def __getitem__(self, key: _KT) -> _VT:
        if not hasattr(key, "__hash__"):
            raise TypeError(f'unhashable type: {type(key).__name__!r}')
        
        _, entry = self._lookup(key)
        
        if entry is None:
            raise KeyError(key)
        
        return entry.value
    
    def __setitem__(self, key: _KT, value: _VT) -> None:
        if not hasattr(key, "__hash__"):
            raise TypeError(f'unhashable type: {type(key).__name__!r}')
        
        # avoid recomputing a potentially slow hash
        _hash = hash(key)
        
        index, entry = self._lookup(key, _hash)
        
        if entry is None:
            self._used += 1
        
        self._table[index] = _MapEntry(_hash, key, value)
        
        # NOTE: the table load factor is 2/3
        if self._capacity * 2 < 3 * self._used:
            self._rehash()
    
    def __delitem__(self, key: _KT) -> None:
        if not hasattr(key, "__hash__"):
            raise TypeError(f'unhashable type: {type(key).__name__!r}')
        
        index, entry = self._lookup(key)
        
        if entry is None:
            raise KeyError(key)
        
        # NOTE: we don't rehash down if the table is less than 1/3 full, since
        # realistically we're not going to be deleting that many items. if you are, at
        # that point you should probably be creating a completely new HashMap anyway
        self._used -= 1
        
        # NOTE: we need to keep the entry in the table so that the lookup algorithm can
        # still find the items with the same hash that are further down the chain. and
        # so we just mark it as deleted by setting the key to `_DUMMY_VALUE`.
        self._table[index] = _MapEntry(
            entry.hash,
            CustomHashMap._DUMMY_VALUE,
            entry.value
        )
