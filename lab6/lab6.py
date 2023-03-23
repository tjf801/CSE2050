from __future__ import annotations
import typing


_T_contra = typing.TypeVar("_T_contra", contravariant=True)
class SupportsDunderLT(typing.Protocol[_T_contra]):
    def __lt__(self, __other: _T_contra) -> bool: ...
    def __eq__(self, __other: _T_contra) -> bool: ...
_T = typing.TypeVar("_T", bound=SupportsDunderLT)

class OrderedList(typing.Generic[_T]):
    _L: list[_T]
    
    def __init__(self, items: typing.Optional[typing.Iterable[_T]] = None):
        """Initialize an ordered list. If `items` is specified, the OrderedList starts with the items in that collection"""
        self._L = sorted(list(items)) if items is not None else list()
    
    def add(self, item: _T):
        """adds item to the list"""
        self._L.append(item)
        self._L.sort()
    
    def remove(self, item):
        """removes the first occurrence of item from the list. Raises a ValueError if the item is not present."""
        if not item in self:
            # this is my ultimate petty move, since the hw tests for a fucking RUNTIMEERROR.
            class ItemNotInListError(ValueError, RuntimeError): pass
            raise ItemNotInListError(f"{item} not in OrderedList")
        
        self._L.remove(item) # O(log n) to find, then O(n) to remove
    
    def __getitem__(self, index: int) -> _T:
        """returns the item with the given index in the sorted list. This is also known as selection."""
        return self._L[index]
    
    def __iter__(self) -> typing.Iterator[_T]:
        """returns an iterator over the ordered list that yields the items in sorted order. Required for `for` loops."""
        return iter(self._L)
    
    def __len__(self) -> int:
        """returns the length of the ordered list."""
        return len(self._L)
    
    def __contains__(self, item: _T) -> bool:
        """returns true if there is an item of the list equal to item."""
        return self._bs(item, 0, len(self)) # You'll have to implement _bs() for this to work
        
        # The lines below implement contains with different algs.
        # Feel free to try them out, but they are both too slow
        # to pass the tests in gradescope (O(n) instead of O(logn)).
        
        # return self._contains_list(item)  # uses python's default list-search
        # return self._contains_bs_slow(item)    # uses a slow version of binary-search (slicing)
    
    def _contains_list(self, item: _T) -> bool:
        """returns True iff there is an item of the list equal to item."""
        return item in self._L # Works, but slow (O(n))
    
    def _contains_bs_slow(self, item: _T) -> bool:
        return self.__contains_bs_slow(self._L[:], item)
    
    def __contains_bs_slow(self, L: list[_T], item: _T) -> bool:
        """searches L for item. This is slow since it slices L at every level of recursion"""
        # base case - item not in list
        if len(L) == 0: return False
        
        median = len(L) // 2
        
        # base case - we found the item
        if item == L[median]: return True
        
        # item is in smaller half
        elif item < L[median]: return self.__contains_bs_slow(L[:median], item)
        
        # item is in bigger half
        else: return self.__contains_bs_slow(L[median + 1:], item)
    
    def _bs(self, item: _T, lower_idx: int, higher_idx: int) -> bool:
        """searches for item using `left` and `right` indices instead of slicing"""
        # base case - item not in list
        if lower_idx == higher_idx:
            return False
        
        median_idx: int = (lower_idx + higher_idx) // 2
        median: _T = self._L[median_idx]
        
        # base case: found item
        if median == item:
            return True
        
        # item is in smaller half
        elif item < median:
            return self._bs(item, lower_idx, median_idx)
        
        # item is in bigger half
        return self._bs(item, median_idx+1, higher_idx)
