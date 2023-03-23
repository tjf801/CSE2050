from __future__ import annotations
import typing
from typing import Sequence, Optional

_T_contra = typing.TypeVar("_T_contra", contravariant=True)
class Sortable(typing.Protocol[_T_contra]):
    def __lt__(self, __other: _T_contra) -> bool: ...
_Sortable = typing.TypeVar("_Sortable", bound=Sortable)

def find_zero(L: Sequence[_Sortable]) -> Optional[int]:
    """
    Finds the index of a zero element in a list containing negative items, zeros, and positive items (in that order).
    Returns `None` if no zero was found.
    
    Calling this function on a list not in the above order results in undefined behavior.
    
    Examples:
        >>> find_zero([-1, -2, -69, 0, 2, 3])
        3
        >>> find_zero([0, 1, 2, 3, 4, 5])
        0
        >>> find_zero([-1, -1, -2, 7])
        None
    """
    low_index = 0
    high_index = len(L)
    
    # yes, im using an iterative algorithm. deal with it 😎
    while True:
        # split sub-list down the middle
        median_index = (low_index + high_index) // 2
        
        if L[median_index] == 0:
            # zero was found
            return median_index
        elif median_index == high_index:
            # no zero in the list
            return None
        elif L[median_index] < 0:
            # Zero is to the right
            low_index = median_index + 1
        else:
            # Zero is to the left
            high_index = median_index

def bubble(L: typing.MutableSequence[_Sortable], left: int, right: int):
    if not left <= right:
        raise ValueError("left index must be less than right index")
    
    if right - left in (0, 1):
        # sub-list has length 0 or 1, and so is trivially sorted
        return
    
    # NOTE: the assignment says it should be adaptive, so thats why it has the extra `swapped` variable
    
    for i in range(left, right):
        # at the end of each iteration, L[i:right] is sorted
        swapped = False
        for j in range(left, right-(i-left)-1):
            if L[j] > L[j + 1]:
                L[j], L[j + 1] = L[j + 1], L[j]
                swapped = True
        if not swapped:
            continue # no swaps were made, so the list is sorted

def selection(L: typing.MutableSequence[_Sortable], left: int, right: int):
    if not left <= right:
        raise ValueError("left index must be less than right index")
    
    if right - left in (0, 1): return
    
    for i in range(left, right):
        # NOTE: at the end of each iteration, L[left:i+1] is sorted
        
        # i love python
        min_index = min(range(i, right), key=L.__getitem__)
        L[i], L[min_index] = L[min_index], L[i]

def insertion(L: typing.MutableSequence[_Sortable], left: int, right: int):
    if not left <= right:
        raise ValueError("left index must be less than right index")
    
    if right - left in (0, 1): return
    
    for i in range(left, right):
        # at the end of each iteration, L[left:i+1] has to be sorted
        # this makes the algorithm adaptive :)
        if L[i-1] < L[i]:
            continue
        
        # find the index where L[i] should be inserted
        insert_index = next((j for j in range(left, i) if L[i] < L[j]), i)
        
        # insert L[i] into the correct position
        # NOTE: this has the same time complexity as swapping all the elements between i and insert_index
        L.insert(insert_index, L.pop(i))

def sort_halfsorted(
        L: typing.MutableSequence[_Sortable], 
        sort: typing.Callable[[typing.MutableSequence[_Sortable], int, int], None]
):
    '''Efficiently sorts a list comprising a series of negative items, a single 0, and a series of positive items
    
        Input
        -----
            * L:list
                a half sorted list, e.g. [-2, -1, -3, 0, 4, 3, 7, 9, 14]
                                         <---neg--->     <----pos----->

            * sort: func(L:list, left:int, right:int)
                a function that sorts the sublist L[left:right] in-place
                note that we use python convention here: L[left:right] includes left but not right

        Output
        ------
            * None
                this algorithm sorts `L` in-place, so it does not need a return statement

        Examples
        --------
            >>> L = [-1, -2, -3, 0, 3, 2, 1]
            >>> sort_halfsorted(L, bubble)
            >>> print(L)
            [-3, -2, -1, 0, 1, 2, 3]
    '''
    
    idx_zero = find_zero(L)     # find the 0 index 
    assert idx_zero is not None
    sort(L, 0, idx_zero)        # sort left half
    # LOL the provided code has a bug.
    # this fails when idx_zero is the last index in the list.
    sort(L, idx_zero+1, len(L)) # sort right half

if __name__ == "__main__":
    L = [-31, -13, -31, -5, -24, -12, -23, -23, -21, -32, -17, -34, -7, -20, -13, -34, -24, -3, -34, -17, 
-25, -27, -36, -17, -18, -4, -35, -2, 0, 14, 23, 5, 27, 20, 12, 35, 24, 33]
    sort_halfsorted(L, insertion)
    print(L)