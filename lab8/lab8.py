from __future__ import annotations

import typing

# from collections.abc import MutableSet
from typing import Generic, TypeVar


@typing.runtime_checkable
class SupportsHash(typing.Protocol):
    def __hash__(self) -> int: ...

_T = TypeVar('_T', bound=SupportsHash)

class CustomSet(Generic[_T]): #, MutableSet[_T]):
    _MIN_BUCKETS: int = 8 # We never want to rehash down below this many buckets.
    
    def  __init__(self) -> None:
        self._n_buckets = 8
        self._len = 0
        
        self._L: list[list[_T]] = [[] for _ in range(self._n_buckets)]
    
    def _find_bucket(self, item: SupportsHash) -> int:
        """Return the index of the bucket `item` should go in based on its hash."""
        if not hasattr(item, '__hash__'):
            raise TypeError(
                'CustomSet only supports hashable items, '
                f'but {item} is not hashable'
            )
        
        return hash(item) % self._n_buckets
    
    def _rehash(self, new_buckets: int) -> None:
        """Rehash every item from `n_buckets` into `new_buckets`."""
        new_L: list[list[_T]] = [[] for _ in range(new_buckets)] # noqa: N806
        
        for bucket in self._L:
            for item in bucket:
                item_idx = hash(item) % new_buckets
                new_L[item_idx].append(item)
        
        self._L = new_L # pyright: ignore [reportConstantRedefinition]
        self._n_buckets = new_buckets
    
    def __len__(self) -> int:
        """Get the number of items in the CustomSet."""
        return self._len
    
    def __iter__(self) -> typing.Iterator[_T]:
        """Iterate over the items in the CustomSet."""
        for bucket in self._L:
            yield from bucket
    
    def __contains__(self, item: object) -> bool:
        """Whether the item is in the CustomSet."""
        if not hasattr(item, '__hash__'):
            return False
        
        index = self._find_bucket(item)
        
        return item in self._L[index]
    
    def add(self, item: _T) -> None:
        """Add a new item to CustomSet.
        
        Duplicate adds are ignored.
        """
        index = self._find_bucket(item)
        
        if item not in self._L[index]:
            self._L[index].append(item)
            self._len += 1
            
            if self._len > self._n_buckets // 2:
                self._rehash(2 * self._n_buckets)
    
    def remove(self, item: _T) -> None:
        """Remove item from CustomSet.
        
        Removing an item not in the CustomSet raises a KeyError.
        """
        index = self._find_bucket(item)
        
        if item not in self._L[index]:
            raise KeyError(f'{item} not in CustomSet')
        
        self._L[index].remove(item)
        self._len -= 1
            
        if (
            self._len < self._n_buckets // 4
            and self._n_buckets // 2 >= CustomSet._MIN_BUCKETS
        ):
            self._rehash(self._n_buckets // 2)
