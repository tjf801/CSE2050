from __future__ import annotations

import typing

from BSTNode import BSTNode

if typing.TYPE_CHECKING:
    from collections.abc import Iterator

# Public interface: users only interact with the class BSTMap.
# Methods in BSTSet often call BSTNode methods, which do the heavy lifting.
class BSTSet:
    _head: BSTNode | None
    
    def __init__(self) -> None:
        self._head = None
    
    # classic iteration (bad)
    def __iter__(self) -> Iterator[int]:
        if self._head is None:
            raise ValueError("Tree is empty")
        return iter(self._head)
    
    # generator based iteration (good)
    def in_order(self) -> Iterator[int]:
        if self._head is None:
            raise ValueError("Tree is empty")
        yield from self._head.in_order()
    
    # TODO: How should these methods call the BSTNode methods?
    def put(self, key: int) -> None:
        if self._head is None:
            self._head = BSTNode(key)
        else:
            self._head.put(key)
    
    def pre_order(self) -> Iterator[int]:
        if self._head is None:
            return
        yield from self._head.pre_order()
    
    def post_order(self) -> Iterator[int]:
        if self._head is None:
            return
        yield from self._head.post_order()
