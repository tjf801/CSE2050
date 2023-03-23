from __future__ import annotations

import enum
import typing
from typing import Literal

if typing.TYPE_CHECKING:
    _T_contra = typing.TypeVar('_T_contra', contravariant=True)
    class Sortable(typing.Protocol[_T_contra]):
        def __lt__(self, __other: _T_contra, /) -> bool: ...
        def __le__(self, __other: _T_contra, /) -> bool: ...
    _Sortable = typing.TypeVar('_Sortable', bound=Sortable[typing.Any])
    
    SortingAlgorithm: typing.TypeAlias = Literal[
        "reverse_list",
        "insertionsort",
        "quicksort",
        "mergesort"
    ]


# NOTE: for max performance (that ive tested) MAX_OUT_OF_ORDER would be around 12,
# but its supposed to be 5 for this assignment. Oh well
MAX_OUT_OF_ORDER = 5
SMALL_LIST_THRESHOLD = 16

class EdgeCase(enum.Enum):
    AlreadySorted = 1
    ReverseSorted = 2
    MostlySorted = 3
    # NOTE: this does not necessarily need to be used in this
    # assignment, but I did it for completeness' sake
    MostlyReverseSorted = 4

def linear_scan(__iterator: typing.Iterable[_Sortable]) -> EdgeCase | None:
    """Return an EdgeCase if the iterable matches a certain pattern.
    
    Checks if the iterator is already sorted, sorted in reverse, or has only a few
    elements out of order. If none of these cases apply, returns None.
    """
    # time complexity: O(n)
    num_elements_out_of_order = 0
    total_length = 0
    
    prev_element = None
    
    for element in __iterator:
        total_length += 1
        
        if prev_element is not None and element < prev_element:
            num_elements_out_of_order += 1
        
        prev_element = element
        
        # if we've found too many elements out of order, but at least one IS in order,
        # we know none of these cases apply, and so can exit the iteration early
        max_in_order = total_length - MAX_OUT_OF_ORDER - 1
        if MAX_OUT_OF_ORDER < num_elements_out_of_order < max_in_order:
            break
    
    if num_elements_out_of_order == 0:
        return EdgeCase.AlreadySorted
    if num_elements_out_of_order == total_length - 1:
        return EdgeCase.ReverseSorted
    if num_elements_out_of_order <= MAX_OUT_OF_ORDER:
        return EdgeCase.MostlySorted
    if num_elements_out_of_order >= total_length - MAX_OUT_OF_ORDER - 1:
        return EdgeCase.MostlyReverseSorted
    
    return None

def reverse_list(__list: typing.MutableSequence[typing.Any]) -> None:
    """Reverse a list in-place."""
    # time complexity: O(n)
    for i in range(len(__list) // 2):
        __list[i], __list[-i - 1] = __list[-i - 1], __list[i]

def insertionsort(
    __list: typing.MutableSequence[_Sortable], /,
    left: int = 0, right: int = ...
) -> None:
    """Sort a list in-place using the insertion sort algorithm.
    
    This algorithm is adaptive and stable, with a time complexity of O(n^2).
    """
    if right is ...:
        right = len(__list)
    
    if not left <= right:
        raise ValueError("left index must be less than or equal to right index")
    
    if right - left in (0, 1):
        # sub-list has length 0 or 1, and so is trivially sorted
        return
    
    for i in range(left, right):
        # make the algorithm adaptive by skipping elements that are already in order
        if __list[i - 1] < __list[i]:
            continue
        
        # find the index where __list[i] should be inserted
        # TODO: binary search could easily be used here
        insert_index = next((j for j in range(left, i) if __list[i] <= __list[j]), i)
        
        # insert L[i] into the correct position
        # NOTE: this has the same time complexity as swapping
        #       all the elements between i and insert_index
        # TODO: implement a more efficient algorithm, maybe using memcpy?
        __list.insert(insert_index, __list.pop(i))

def quicksort(
    __list: typing.MutableSequence[_Sortable], /,
    left: int = 0, right: int = ...,
    *, current_depth: int = 0, best_max_depth: int = ...
) -> set[SortingAlgorithm]:
    if right is ...:
        right = len(__list)
    
    if not left <= right:
        raise ValueError("left index must be less than or equal to right index")
    
    if right - left <= 1:
        return set()
    
    if right - left <= SMALL_LIST_THRESHOLD:
        insertionsort(__list, left, right)
        return {"insertionsort"}
    
    if best_max_depth is ...:
        # NOTE: instead of using math.log2()+1, im gonna use int.bit_length()
        best_max_depth = int.bit_length(len(__list))
    
    # if the current depth is too deep, use a different algorithm instead
    if current_depth >= best_max_depth * 2:
        return mergesort(__list, left, right)
    
    # the main quicksort algorithm
    
    # partition the list
    middle = _quicksort_partition(__list, left, right)
    
    # recursively sort the sub-lists
    sublist1_algs = quicksort(
        __list, left, middle,
        current_depth = current_depth + 1,
        best_max_depth=best_max_depth
    )
    sublist_2_algs = quicksort(
        __list, middle, right,
        current_depth = current_depth + 1,
        best_max_depth=best_max_depth
    )
    
    # NOTE: if this wasnt a mandatory part of the assignment, i would use
    # an enum like a sane person would in this situation. but no. this class
    # is made by the average python programmer (dumbasses) so i have to use
    # a fucking set of strings. i hate this class. kill me.
    # TODO: i hate mypy why does it think that {"quicksort"} is not a
    # set[SortingAlgorithm] or at the very least a set[Literal["quicksort"]]
    _: set[Literal["quicksort"]] = {"quicksort"}
    
    return sublist1_algs | sublist_2_algs | _

def _quicksort_get_pivot(
    __list: typing.MutableSequence[_Sortable], /,
    _left: int, right: int,
) -> tuple[int, _Sortable]:
    """Get the pivot element for the quicksort algorithm."""
    # NOTE: the pivot is the last element in the list for this assignment
    return right-1, __list[right-1]

def _quicksort_partition(
    __list: typing.MutableSequence[_Sortable], /,
    left: int, right: int,
) -> int:
    """Partition a list in-place using the quicksort algorithm.
    
    This algorithm is not stable, but it is in-place and has a time complexity of O(n).
    """
    # get the pivot element
    pivot_idx, pivot = _quicksort_get_pivot(__list, left, right)
    
    # make the two sub-lists
    left_idx = left
    right_idx = right - 2
    
    while left_idx <= right_idx:
        # find the next element that is out of order
        while left_idx <= right_idx and __list[left_idx] < pivot:
            left_idx += 1
        while left_idx <= right_idx and pivot <= __list[right_idx]:
            right_idx -= 1
        
        # swap the elements at left_idx and right_idx
        if left_idx <= right_idx:
            __list[left_idx], __list[right_idx] = __list[right_idx], __list[left_idx]
            left_idx += 1
            right_idx -= 1
    
    # swap the pivot into the correct position
    __list[left_idx], __list[pivot_idx] = __list[pivot_idx], __list[left_idx]
    
    return left_idx

def mergesort(
    __list: typing.MutableSequence[_Sortable], /,
    left: int = 0, right: int = ...,
) -> set[SortingAlgorithm]:
    """Sort a list using the mergesort algorithm."""
    if right is ...:
        right = len(__list)
    
    if not left <= right:
        raise ValueError("left index must be less than or equal to right index")
    
    if right - left <= 1:
        return set() # trivially sorted
    
    if right - left <= SMALL_LIST_THRESHOLD:
        insertionsort(__list, left, right)
        return {"insertionsort"}
    
    # the main mergesort algorithm
    
    # split the list into two sub-lists
    middle = (left + right) // 2
    
    # recursively sort the sub-lists
    sublist1_algs = mergesort(__list, left, middle)
    sublist_2_algs = mergesort(__list, middle, right)
    
    # merge the sub-lists
    _mergesort_merge(__list, left, middle, right)
    
    # TODO: if i never submit another assignment for this class, it is because i have
    # decided to fake my own death, move to the midwest, and become a cabbage farmer,
    # where i will remain until the day i die, having lived a happy life.
    # (or at least until you stop making me use strings as enums in my assignments.)
    _: set[Literal["mergesort"]] = {"mergesort"}
    
    return sublist1_algs | sublist_2_algs | _

def _mergesort_merge(
    __list: typing.MutableSequence[_Sortable], /,
    left: int, middle: int, right: int,
) -> None:
    """Merge two sorted sub-lists into a single sorted list.
    
    This algorithm is stable, adaptive, and has a time complexity of O(n).
    However, it is not in-place, and requires O(n) extra space.
    
    NOTE: the middle index is the first index of the second sub-list.
    """
    assert left <= middle <= right
    
    # if the sub-lists are already sorted, dont do anything
    # NOTE: this makes the algorithm adaptive
    if __list[middle-1] <= __list[middle]:
        return
    
    # create an empty list to store the merged sub-lists
    merged: list[_Sortable] = []
    
    # merge the sub-lists
    left_idx = left
    right_idx = middle
    
    while left_idx < middle and right_idx < right:
        if __list[left_idx] <= __list[right_idx]:
            merged.append(__list[left_idx])
            left_idx += 1
        else:
            merged.append(__list[right_idx])
            right_idx += 1
    
    # copy the remaining elements from the first sub-list
    if left_idx < middle:
        merged.extend(__list[left_idx:middle])
    
    # copy the remaining elements from the second sub-list
    elif right_idx < right:
        merged.extend(__list[right_idx:right])
    
    # copy the merged sub-lists back into the original list
    __list[left:right] = merged

def magic_sort(__list: typing.MutableSequence[_Sortable]) -> set[SortingAlgorithm]:
    """Sort a list in-place using the best algorithm for the given data."""
    # i like how pyright does the exhastive pattern matching that rust does 😳
    match linear_scan(__list):
        case EdgeCase.AlreadySorted:
            return set()
        case EdgeCase.ReverseSorted:
            reverse_list(__list)
            return {"reverse_list"}
        case EdgeCase.MostlySorted:
            insertionsort(__list)
            return {"insertionsort"}
        case EdgeCase.MostlyReverseSorted:
            reverse_list(__list)
            insertionsort(__list)
            return {"reverse_list", "insertionsort"}
        case None:
            return quicksort(__list)
