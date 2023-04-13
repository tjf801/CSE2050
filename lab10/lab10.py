from __future__ import annotations

import typing
from abc import abstractmethod, abstractproperty
from collections.abc import Collection, Iterator
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

# me when static typing ._.
_T_contra = TypeVar("_T_contra", contravariant=True)

class Comparable(Protocol):
    def __lt__(self: _T_contra, other: _T_contra, /) -> bool:
        ...

_IT = TypeVar("_IT")
_PT = TypeVar("_PT", bound=Comparable)
_IT_co = TypeVar("_IT_co", covariant=True)
_PT_co = TypeVar("_PT_co", covariant=True, bound=Comparable)

@dataclass(frozen=True)
class Entry(Generic[_IT_co, _PT_co]):
    item: _IT_co
    priority: _PT_co
    
    def __lt__(self, other: Entry[typing.Any, _PT_co], /) -> bool:
        return self.priority < other.priority

class AbstractListPriorityQueue(Generic[_IT, _PT], Collection[Entry[_IT, _PT]]):
    @abstractproperty
    def _entries(self) -> list[Entry[_IT, _PT]]: ...
    
    @abstractmethod
    def __init__(self, iterable: Iterator[Entry[_IT, _PT]] | None = None, /) -> None:
        raise NotImplementedError
    
    def __len__(self) -> int:
        """Get the number of items in the priority queue.
        
        Complexity: O(1)
        """
        return len(self._entries)
    
    def __iter__(self) -> Iterator[Entry[_IT, _PT]]:
        """Iterate over the items in the priority queue.
        
        The first item returned is the one with the highest priority.
        """
        return iter(self._entries)
    
    def __contains__(self, __x: object) -> bool:
        """Check if the priority queue contains an item.
        
        Complexity: O(n)
        """
        return any(__x == entry.item for entry in self._entries)
    
    @abstractmethod
    def find_min(self) -> Entry[_IT, _PT]:
        """Get the item with the highest priority.
        
        This returns the item by reference, and so does not remove it from the queue.
        
        Complexity: O(1)
        """
        raise NotImplementedError
    
    @abstractmethod
    def insert(self, item: _IT, priority: _PT) -> None:
        """Insert an item into the priority queue."""
        raise NotImplementedError
    
    @abstractmethod
    def remove_min(self) -> Entry[_IT, _PT]:
        """Remove and return the item with the highest priority."""
        raise NotImplementedError

class PriorityQueueUnorderedList(AbstractListPriorityQueue[_IT, _PT]):
    # internally a tree, where for index `i`, the left child is index `2i + 1` and the
    # right child is index `2i + 2`, and the 0th element is the highest priority
    _tree: list[Entry[_IT, _PT]]
    
    @property
    def _entries(self) -> list[Entry[_IT, _PT]]:
        return self._tree
    
    def __init__(self, iterable: Iterator[Entry[_IT, _PT]] | None = None, /) -> None:
        """Create a priority queue from an iterable of items.
        
        Complexity: O(n log n)
        """
        self._tree = list(iterable) if iterable is not None else []
        
        for i in range(len(self._tree) // 2):
            self._siftdown(i)
    
    
    def _siftup(self, i: int) -> None:
        """Bubble up the item at index `i`. Complexity is O(log n)."""
        # TODO: make this more pythonic?
        while i > 0:
            parent = (i - 1) // 2
            if self._tree[i] < self._tree[parent]:
                self._tree[i], self._tree[parent] = self._tree[parent], self._tree[i]
            i = parent
    
    def _siftdown(self, i: int) -> None:
        """Bubble down the item at index `i`. Complexity is O(log n)."""
        while 2*i+1 < len(self._tree):
            left = 2*i+1
            right = 2*i+2
            
            if right < len(self._tree) and self._tree[right] < self._tree[left]:
                child = right
            else:
                child = left
            
            if self._tree[child] < self._tree[i]:
                self._tree[i], self._tree[child] = self._tree[child], self._tree[i]
            
            i = child
    
    
    def find_min(self) -> Entry[_IT, _PT]:
        """Get the item with the highest priority.
        
        This returns the item by reference, and so does not remove it from the queue.
        
        Complexity: O(1)

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        return self._tree[0]
    
    def insert(self, item: _IT, priority: _PT) -> None:
        """Insert an item into the priority queue.
        
        Complexity: O(log n)
        """
        self._tree.append(Entry(item, priority))
        self._siftup(len(self._tree) - 1)
    
    def remove_min(self) -> Entry[_IT, _PT]:
        """Remove and return the item with the highest priority.
        
        Complexity: O(log n)

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        result = self._tree[0]
        self._tree[0] = self._tree[-1]
        self._tree.pop()
        self._siftdown(0)
        return result

class PriorityQueueOrderedList(AbstractListPriorityQueue[_IT, _PT]):
    # internally just a list with highest priority at the end
    _list: list[Entry[_IT, _PT]]
    
    @property
    def _entries(self) -> list[Entry[_IT, _PT]]:
        return self._list
    
    def __init__(self, iterable: Iterator[Entry[_IT, _PT]] | None = None, /) -> None:
        """Create a priority queue from an iterable of items.
        
        Complexity: O(n log n)
        """
        self._list = list(iterable) if iterable is not None else []
        self._list.sort(reverse=True)
    
    def find_min(self) -> Entry[_IT, _PT]:
        """Get the item with the highest priority.
        
        This returns the item by reference, and so does not remove it from the queue.
        
        Complexity: O(1)

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        return self._list[-1]
    
    def insert(self, item: _IT, priority: _PT) -> None:
        """Insert an item into the priority queue.
        
        Complexity: O(n)
        """
        # find where to insert (Complexity: O(n))
        # TODO: maybe use binary search?
        for i, entry in enumerate(self._list): # noqa: B007
            if entry.priority < priority:
                break
        else:
            i = len(self._list)
        
        # insert (Complexity: O(n))
        self._list.insert(i, Entry(item, priority))
    
    def remove_min(self) -> Entry[_IT, _PT]:
        """Remove and return the item with the highest priority.
        
        Complexity: O(1)

        Raises
        ------
        IndexError
            If the priority queue is empty.
        """
        return self._list.pop()

# these are just here to get the dumb autograder to shut up
PQ_OL: typing.TypeAlias = PriorityQueueOrderedList[_IT, _PT]
PQ_UL: typing.TypeAlias = PriorityQueueUnorderedList[_IT, _PT]
