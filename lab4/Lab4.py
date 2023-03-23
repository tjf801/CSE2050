from __future__ import annotations
import typing

_T = typing.TypeVar('_T')

# This class is provided for you - you do not need to change anything
class Node(typing.Generic[_T]):
	'''Node class for linked data structures

		Example:
		--------
			2 Node objects with 1-directional linking
				_____________	  _____________
				| class: Node |	| class: Node |
				|-------------|	|-------------|
				| item = 3	|	| item = 4	|
				| _next = ----|--->| _next = ----|---> None
				|_____________|	|_____________|   
	'''
	
	item: _T
	next: typing.Optional[Node[_T]]
	
	def __init__(self, item: _T, next: typing.Optional[Node[_T]] = None):
		'initialize with data and location of next node'
		self.item = item
		self.next = next
	
	def __iter__(self) -> typing.Iterator[_T]:
		'''recursively yields all items in LL

			iter() is called when we iterate over an object, e.g. `for item in items:`

			Example
			-------
			>>> head_node = Node('a', _next=Node('b', _next=Node('c', _next=Node('d', _next=Node('e')))))
			>>> # head: 'a'-->'b'-->'c'-->'d'-->'e'
			>>> for item in head_node:
			...	 print(item)
			...
			a
			b
			c
			d
			e
		'''
		
		# 1) Yield this item
		yield self.item 
		
		# 2) Yield all other items, starting with the next Node
		if self.next is not None: yield from self.next
	
	def __repr__(self) -> str:
		'Provides a nice string representation of the node'
		return f"Node({self.item})"

class LinkedList(typing.Generic[_T]):
	'''LinkedList supporing O(1) add_first, remove_first, add_last
	
		Diagrams
		--------
			Empty LL: _head and _tail point to None
				ll._head-->None <-+
								  |
				ll._tail----------+
	
			One item: _head and _tail point to the same node
				ll._head-->0-->None
						   ^
				ll._tail---+

			Multiple items: _head and _tail point to different nodes
				ll._head-->0-->1-->2-->...-->n-->None
											 ^
				ll._tail---------------------+
	'''
	
	_head: typing.Optional[Node[_T]]
	_tail: typing.Optional[Node[_T]]
	_len: int
	
	# e.g. DO NOT use an empty list
	def __init__(self, items: typing.Optional[typing.Iterable[_T]] = None):
		'initialize a new LinkedList w/ optional collection items'
		self._head = None
		self._tail = None
		self._len = 0
		if items is not None:
			for item in items:
				self.add_last(item)
	
	def add_first(self, item: _T) -> None:
		'adds item to beginning of linked list'
		
		# create a new node pointed at self._head
		new_node = Node(item, next=self._head)
		
		# update self._head
		self._head = new_node

		# update len
		self._len += 1
	
	def add_last(self, item: _T) -> None:
		'adds item to end of linked list'

		# same as add_first() if this is an empty linked list
		new_node = Node(item, next=None)
		
		# create a new node, update self._tail._next
		if self._tail is not None:
			self._tail.next = new_node
		else:
			self._head = new_node
		
		# update self._tail
		self._tail = new_node
		
		# update len
		self._len += 1
	
	def remove_first(self) -> _T:
		'removes item from beginning of linked list'
		# Edge case - cannot remove from empty
		if self._head is None:
			# NOTE: raising a runtime error here is dumb. prof. clark pls read about basic python error types thx
			raise RuntimeError('Cannot remove from empty linked list')
		
		# Edge case - update tail if this is the last node
		if self._head is self._tail:
			self._tail = None
		
		# store item in temporary variable
		item = self._head.item
		
		# update self._head
		self._head = self._head.next
		
		# update len
		self._len -= 1
		
		# return item from old head
		return item
	
	def __len__(self) -> int:
		'returns number of nodes in Linked list'
		return self._len
	
	def __iter__(self) -> typing.Iterator[_T]:
		'Allows iteration in a for loop'
		if self._head is not None: yield from self._head
	
	def __repr__(self) -> str:
		'''returns a string representation of our linked list
		
			Examples
			--------
			>>> ll1 = LinkedList(range(5))
			>>> print(ll1)
			LinkedList:
				Head: Node(0)
				Tail: Node(4)
				0-->1-->2-->3-->4-->None
			
			>>> ll2 = LinkedList()
			>>> print(ll2)
			LinkedList:
				Head: None
				Tail: None
				None
			
			>>> ll3 = LinkedList(('hello', 'goodbye'))
			>>> print(ll3)
			LinkedList:
				Head: Node(hello)
				Tail: Node(goodbye)
				'hello'-->'goodbye'-->None
		'''
		str_head = f"Head: {self._head}"
		str_tail = f"Tail: {self._tail}"

		L_nodes = []
		# Append string repr of each node
		for node in self:
			L_nodes.append(repr(node)+ '-->')

		# join all the strings together
		return f"LinkedList:\n\t{str_head}\n\t{str_tail}\n\t{''.join(L_nodes)}{None}"