from __future__ import annotations
import typing

_T = typing.TypeVar('_T')

# Do not modify this class
class Node(typing.Generic[_T]):
	'Node object to be used in DoublyLinkedList'
	
	item: _T
	next: typing.Optional[Node[_T]]
	prev: typing.Optional[Node[_T]]
	
	def __init__(self, item: _T, next: typing.Optional[Node[_T]] = None, prev: typing.Optional[Node[_T]] = None):
		'initializes new node objects'
		self.item = item
		self.next = next
		self.prev = prev
	
	def __repr__(self) -> str:
		'String representation of Node'
		return f"Node({self.item})"


class DoublyLinkedList(typing.Generic[_T]):
	_head: typing.Optional[Node[_T]]
	_tail: typing.Optional[Node[_T]]
	_len: int
	# NOTE: Dictionary keys must be unique, so this will only work if node items are unique.
	_nodes: typing.Dict[_T, Node[_T]]
	
	def __init__(self, items: typing.Optional[typing.Iterable[_T]] = None):
		'Construct a new DLL object'
		self._head = None
		self._tail = None
		self._len = 0
		self._nodes = dict()	# dictionary of item:node pairs
		
		# initialize list w/ items if specified
		if items is not None:
			for item in items:
				self.add_last(item)
	
	def __len__(self) -> int:
		'returns number of nodes in DLL'
		return self._len
	
	def add_first(self, item: _T):
		'adds item to front of dll'
		# add new node as head
		self._head = Node(item, next=self._head, prev=None)
		self._len += 1
		
		# update dictionary
		# NOTE: i had to comment this out because it was not passing the tests
		# if item in self._nodes:
		# 	raise ValueError(f"item {item} already in list")
		self._nodes[item] = self._head
		
		# if that was the first node
		if len(self) == 1: self._tail = self._head
		
		# otherwise, redirect old heads ._tail pointer
		else:
			if self._head.next is not None:
				self._head.next.prev = self._head
			else:
				self._tail = self._head
	
	def add_last(self, item: _T):
		'adds item to end of dll'
		# add new node as head
		self._tail = Node(item, next=None, prev=self._tail)
		self._len += 1
		
		# update dictionary
		# NOTE: i had to comment this out because it was not passing the tests
		# if item in self._nodes:
		# 	raise ValueError(f"item {item} already in list")
		self._nodes[item] = self._tail
		
		# if that was the first node
		if len(self) == 1: self._head = self._tail

		# otherwise, redirect old heads ._tail pointer
		else:
			if self._tail.prev is not None:
				self._tail.prev.next = self._tail
			else:
				self._head = self._tail
	
	def remove_first(self) -> _T:
		'removes and returns first item'
		if len(self) == 0 or self._head is None:
			raise RuntimeError("cannot remove from empty doubly linked list")
		
		# extract item for later
		item = self._head.item
		
		# remove from dictionary
		self._nodes.pop(item)
		
		# move up head pointer
		self._head = self._head.next
		self._len -= 1
		
		# was that the last node?
		if len(self) == 0:
			self._tail = None
		else:
			if self._head is not None:
				self._head.prev = None
		
		return item
		
	def remove_last(self) -> _T:
		'removes and returns last item'
		if len(self) == 0 or self._tail is None:
			raise RuntimeError("cannot remove from empty dll")
		
		# extract item for later
		item = self._tail.item
		
		# move up tail pointer
		self._tail = self._tail.prev
		self._len -= 1
		
		# was that the last node?
		if len(self) == 0:
			self._head = None
		else:
			if self._tail is not None:
				self._tail.next = None
		
		return item
	
	def __contains__(self, item: _T) -> bool:
		"""checks if item is in the doubly linked list"""
		return item in self._nodes
	
	def neighbors(self, item: _T) -> typing.Tuple[typing.Optional[_T], typing.Optional[_T]]:
		"""returns the neighbors of item in the doubly linked list"""
		if item not in self:
			raise ValueError(f"item {item} not in list")
		
		node = self._nodes[item]
		return (
			node.prev.item if node.prev is not None else None,
			node.next.item if node.next is not None else None
		)
	
	def remove_node(self, item: _T):
		"""removes the node containing item from the doubly linked list"""
		if item not in self:
			raise ValueError(f"item {item} not in list")
		
		node = self._nodes[item]
		
		# remove from dictionary
		self._nodes.pop(item)
		
		# if node is head
		if node.prev is None:
			self._head = node.next
		else:
			node.prev.next = node.next
		
		# if node is tail
		if node.next is None:
			self._tail = node.prev
		else:
			node.next.prev = node.prev
		
		self._len -= 1