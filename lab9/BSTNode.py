from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from collections.abc import Iterator


class BSTNode:
    key: int
    left: BSTNode | None
    right: BSTNode | None
    
    def __init__(
        self,
        key: int,
        left: BSTNode | None = None,
        right: BSTNode | None = None
    ) -> None:
        """Construct a node. By default, left and right children are None."""
        self.key = key
        self.left = left
        self.right = right
    
    # classical iteration (correct but slow)
    def __iter__(self) -> Iterator[int]:
        """Classical iteration.
        
        Creates a new iterator object, which takes O(n) to construct the in-order list
        then returns items one at a time.
        """
        return BSTNodeIterator(self)
    
    def in_order(self) -> Iterator[int]:
        """Use generator-based iteration.
        
        We can return items as soon as we find them, and the recursive stack we've built
        stays in memory until the next call due to the `yield` keyword.
        """
        if self.left is not None:
            yield from self.left.in_order()   # recursively go left
        yield self.key                        # return this key
        if self.right is not None:
            yield from self.right.in_order()  # recursively go right
    
    def __repr__(self) -> str:
        return f"BSTNode(key={self.key})"
    
    def put(self, key: int) -> None:
        if key == self.key:
            return # key is already in the tree
        
        if key < self.key:
            if self.left is None:
                self.left = BSTNode(key)
            else:
                self.left.put(key)
        
        elif self.right is None:
            self.right = BSTNode(key)
        else:
            self.right.put(key)
    
    def pre_order(self) -> Iterator[int]:
        yield self.key
        if self.left is not None:
            yield from self.left.pre_order()
        if self.right is not None:
            yield from self.right.pre_order()
    
    def post_order(self) -> Iterator[int]:
        if self.left is not None:
            yield from self.left.post_order()
        if self.right is not None:
            yield from self.right.post_order()
        yield self.key

# This technique is slow. We have to queue up the ENTIRE tree before we start
# returning nodes. See above BSTNode.in_order() for an example that yields
# nodes one at a time without queueing up the whole tree.
class BSTNodeIterator:
    queue: list[BSTNode]
    
    def __init__(self, node: BSTNode) -> None:
        self.queue = []
        self.in_order(node) # Queues up the entire tree
        self.counter = 0
    
    # in_order traversal/queueing
    def in_order(self, node: BSTNode) -> None:
        if node.left is not None:
            self.in_order(node.left)
        self.queue.append(node)
        if node.right is not None:
            self.in_order(node.right)
    
    # Update counter, return item, repeat
    def __next__(self) -> int:
        if self.counter < len(self.queue):
            self.counter += 1
            return self.queue[self.counter-1].key
        
        raise StopIteration
    
    def __iter__(self) -> Iterator[int]:
        return self

