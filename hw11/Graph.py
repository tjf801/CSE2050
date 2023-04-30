from __future__ import annotations

import math
import typing
from collections import deque
from collections.abc import Collection, Hashable, Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

# can you tell I'm a fan of type-driven development?
_T_contra = TypeVar("_T_contra", contravariant=True)
_IT = TypeVar("_IT")
_PT = TypeVar("_PT", bound='Comparable')
_IT_co = TypeVar("_IT_co", covariant=True)
_PT_co = TypeVar("_PT_co", covariant=True, bound='Comparable')
_VT = TypeVar("_VT", bound=Hashable)
_WT = TypeVar("_WT", bound='Comparable')

class Comparable(Protocol):
    def __lt__(self: _T_contra, other: _T_contra, /) -> bool:
        ...

@dataclass(frozen=True)
class _PQEntry(Generic[_IT_co, _PT_co]):
    item: _IT_co
    priority: _PT_co
    
    def __lt__(self, other: _PQEntry[typing.Any, _PT_co], /) -> bool:
        return self.priority < other.priority

# NOTE: this is basically stolen from lab 10
class _PriorityQueue(Collection[_IT], Generic[_IT, _PT]):
    # internally a tree, where for index `i`, the left child is index `2i + 1` and the
    # right child is index `2i + 2`, and the 0th element is the highest priority
    _tree: list[_PQEntry[_IT, _PT]]
    
    def __init__(self, iterable: Iterable[tuple[_IT, _PT]] | None = None, /) -> None:
        """Create a priority queue from an iterable of items."""
        if iterable is None:
            iterable = ()
        self._tree = [_PQEntry(entry[0], entry[1]) for entry in iterable]
        
        for i in range(len(self._tree) // 2):
            self._siftdown(i)
    
    def _siftup(self, i: int) -> None:
        """Bubble up the item at index `i`."""
        # Complexity: O(log n)
        while i > 0:
            parent = (i - 1) // 2
            if self._tree[i] < self._tree[parent]:
                self._tree[i], self._tree[parent] = self._tree[parent], self._tree[i]
            i = parent
    
    def _siftdown(self, i: int) -> None:
        """Bubble down the item at index `i`."""
        # Complexity: O(log n)
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
    
    def __contains__(self, __x: object) -> bool:
        # Complexity: O(n)
        return any(__x == entry.item for entry in self._tree)
    
    def __iter__(self) -> Iterator[_IT]:
        # Complexity: O(1) per item * O(n) items = O(n)
        return iter(entry.item for entry in self._tree)
    
    def __len__(self) -> int:
        # Complexity: O(1)
        return len(self._tree)
    
    def front(self) -> _IT:
        """Get the item with the highest priority."""
        # Complexity: O(1)
        return self._tree[0].item
    
    def pop(self) -> _IT:
        """Remove and return the item with the highest priority."""
        # Complexity: O(log n)
        result = self._tree[0]
        self._tree[0] = self._tree[-1]
        self._tree.pop()
        self._siftdown(0)
        return result.item
    
    def push(self, item: _IT, priority: _PT, /) -> None:
        """Add an item to the priority queue."""
        # Complexity: O(log n)
        self._tree.append(_PQEntry(item, priority))
        self._siftup(len(self._tree) - 1)
    
    def update(self, item: _IT, priority: _PT, /) -> None:
        """Update the priority of an item in the priority queue."""
        # Complexity: O(n)
        for i, entry in enumerate(self._tree):
            if entry.item == item:
                self._tree[i] = _PQEntry(item, priority)
                self._siftup(i)
                self._siftdown(i)
                return
        raise ValueError(f"{item} is not in the priority queue")


class _EdgeWeightDict(dict[frozenset[_VT], _WT], Generic[_VT, _WT]):
    # okay yes i know this class doesn't obey the liskov substitution
    # principle, but given that i dont intend this to be a real dict subtype
    # i dont really care, ESPECIALLY since its a private class
    
    def __contains__( # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        edge: tuple[_VT, _VT]
    ) -> bool:
        """Return whether the edge (u, v) is in the graph."""
        return super().__contains__(frozenset(edge))
    
    def __getitem__( # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        edge: tuple[_VT, _VT]
    ) -> _WT:
        """Return the weight of the edge (u, v)."""
        return super().__getitem__(frozenset(edge))
    
    def __setitem__( # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        edge: tuple[_VT, _VT],
        weight: _WT
    ) -> None:
        """Return the weight of the edge (u, v)."""
        return super().__setitem__(frozenset(edge), weight)
    
    def __delitem__( # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        edge: tuple[_VT, _VT]
    ) -> None:
        """Delete the edge (u, v)."""
        return super().__delitem__(frozenset(edge))

class Graph(Collection[_VT | tuple[_VT, _VT]], Generic[_VT, _WT]):
    # invariant: set(_edges.keys()).issubset(_vertices)
    _vertices: set[_VT]
    _edge_weights: _EdgeWeightDict[_VT, _WT]
    
    def __init__(
        self,
        vertices: Iterable[_VT] | None = None,
        edge_weights: Iterable[tuple[tuple[_VT, _VT], _WT]] | None = None
    ) -> None:
        """Initialize a graph with the given vertices and edges.

        Parameters
        ----------
        vertices : Iterable[_VT] | None
            The vertices of the graph. If None, then the graph is
            initialized with no vertices.
        edge_weights : Iterable[tuple[tuple[_VT, _VT], _WT]] | None
            The edges of the graph, along with their weights. If None,
            then the graph is initialized with no edges.

        Raises
        ------
        ValueError
            If any edge has a node that is not in `vertices`, or if
            any edge has a negative weight.
        """
        self._vertices = set(vertices or ())
        self._edge_weights = _EdgeWeightDict()
        if edge_weights is not None:
            for edge, weight in edge_weights:
                self.add_edge(*edge, weight)
    
    def __contains__(self, value: object | _VT | tuple[_VT, _VT]) -> bool:
        """Return whether the given vertex or edge is in the graph."""
        # i know this is extremely sketchy and probably unsound. i simply do not care.
        # it is currently 3 AM and i am very tired. this is a stupid assignment anyways.
        if isinstance(value, tuple) and len(value) == 2: # pyright: ignore[reportUnknownArgumentType] # noqa: E501
            return value in self._edge_weights
        return value in self._vertices
    
    def __len__(self) -> int:
        """Return the number of vertices in the graph."""
        return len(self._vertices)
    
    def __iter__(self) -> Iterator[_VT]:
        """Return an iterator over all vertices in the graph, in no particular order."""
        return iter(self._vertices)
    
    def add_vertex(self, vertex: _VT) -> None:
        """Add a vertex to the graph."""
        self._vertices.add(vertex)
    
    def remove_vertex(self, v: _VT) -> None:
        """Remove a vertex from the graph.

        Raises
        ------
        ValueError
            If the vertex is not in the graph.
        """
        self._vertices.remove(v)
        for u in self._vertices:
            if (u, v) in self._edge_weights:
                del self._edge_weights[(u, v)]
    
    def add_edge(self, u: _VT, v: _VT, weight: _WT) -> None:
        """Add an edge with the given weight between the given nodes.

        Raises
        ------
        ValueError
            If either node is not in the graph, or if the weight is negative.
        """
        if u not in self._vertices:
            raise ValueError(f"{u} is not in the graph")
        if v not in self._vertices:
            raise ValueError(f"{v} is not in the graph")
        if weight < 0:
            raise ValueError("weight must be nonnegative")
        self._edge_weights[(u, v)] = weight
    
    def remove_edge(self, u: _VT, v: _VT) -> None:
        """Remove the edge between the given nodes.

        Raises
        ------
        ValueError
            If the edge is not in the graph.
        """
        del self._edge_weights[(u, v)]
    
    def weight(self, u: _VT, v: _VT) -> _WT:
        """Return the weight of the edge between the given nodes.

        Raises
        ------
        ValueError
            If the edge is not in the graph.
        """
        if (u, v) not in self._edge_weights:
            raise ValueError(f"({u}, {v}) is not in the graph")
        return self._edge_weights[(u, v)]
    
    def neighbors(self, v: _VT) -> Iterable[tuple[_VT, _WT]]:
        """Return the neighbors of the given node, along with their weights.

        Raises
        ------
        ValueError
            If the vertex is not in the graph.
        """
        if v not in self._vertices:
            raise ValueError(f"{v} is not in the graph")
        for u in self._vertices:
            if (u, v) in self._edge_weights:
                yield (u, self._edge_weights[(u, v)])
    
    def paths_with_fewest_edges(
        self,
        start: _VT
    ) -> tuple[dict[_VT, _VT], dict[_VT, int]]:
        """Return a mapping of vertices to the path with the fewest edges from `start` to that vertex.
        
        It should be noted that this algorithm internally uses a breadth-first search.
        As such, if no path exists to a given vertex from `start`, then that vertex
        will not be in the mapping.

        Returns
        -------
        tuple[dict[_VT, _VT], dict[_VT, int]]
            A tuple of two mappings. The first mapping maps each vertex to the vertex
            that comes before it in the path with the fewest edges from `start` to that
            vertex. The second mapping maps each vertex to the number of edges in the
            path.

        Raises
        ------
        ValueError
            If the `start` vertex is not in the graph.
        """ # noqa: E501
        if start not in self._vertices:
            raise ValueError(f"{start} is not in the graph")
        
        prev: dict[_VT, _VT] = {}
        num_edges: dict[_VT, int] = {}
        node_queue: deque[_VT] = deque()
        
        prev[start] = start
        num_edges[start] = 0
        node_queue.append(start)
        
        while node_queue:
            u = node_queue.popleft()
            for v, _ in self.neighbors(u):
                if v not in prev:
                    prev[v] = u
                    num_edges[v] = num_edges[u] + 1
                    node_queue.append(v)
        
        del prev[start]
        
        return prev, num_edges
    
    def shortest_paths(
        self: Graph[_VT, float] | Graph[_VT, int],
        start: _VT
    ) -> tuple[dict[_VT, _VT], dict[_VT, float]]:
        """Find the shortest paths from `start` to all other vertices in the graph.
        
        This function internally uses Dijkstra's algorithm. As such, if no path exists
        to a given vertex from `start`, then that vertex will not be in the mapping.

        Returns
        -------
        tuple[dict[_VT, _VT], Mapping[_VT, float]]
            A tuple of two dictionaries.
            The first dict maps each vertex to the vertex that comes before it in the
            shortest path from `start` to that vertex.
            The second dict maps each vertex to the minimum distance from `start` to
            that vertex.

        Raises
        ------
        ValueError
            If the `start` vertex is not in the graph.
        """
        if start not in self._vertices:
            raise ValueError(f"{start} is not in the graph")
        
        tree: dict[_VT, _VT] = {}
        
        distances: dict[_VT, float] = {v: math.inf for v in self._vertices}
        distances[start] = 0
        
        to_visit = _PriorityQueue[_VT, float]((v, distances[v]) for v in self._vertices)
        
        while to_visit:
            v = to_visit.pop()
            for u, weight in self.neighbors(v):
                if distances[v] + weight < distances[u]:
                    distances[u] = distances[v] + weight
                    tree[u] = v
                    to_visit.update(u, distances[u])
        
        return tree, distances
    
    def minimum_spanning_tree(
        self,
        start: _VT
    ) -> tuple[dict[_VT, _VT], dict[_VT, _WT]]:
        """Find the minimum spanning tree of the graph, starting from the given vertex.
        
        This algorithm internally uses Prim's algorithm. As such, if the graph is not
        fully connected, then the returned tree will not be a spanning tree.

        Returns
        -------
        tuple[Mapping[_VT, _VT], Mapping[_VT, float]]
            A tuple of two mappings.
            The first mapping maps each vertex to the vertex that comes before it in the
            minimum spanning tree.
            The second mapping maps each vertex to the weight of the edge between it and
            the vertex that comes before it in the minimum spanning tree.

        Raises
        ------
        ValueError
            If the `start` vertex is not in the graph.
        """
        if start not in self._vertices:
            raise ValueError(f"{start} is not in the graph")
        
        tree: dict[_VT, _VT] = {start: start}
        
        edge_queue = _PriorityQueue[tuple[_VT, _VT], _WT]()
        for n, weight in self.neighbors(start):
            edge_queue.push((start, n), weight)
        
        while edge_queue:
            u, v = edge_queue.pop()
            if v not in tree:
                tree[v] = u
                for n, weight in self.neighbors(v):
                    edge_queue.push((v, n), weight)
        
        del tree[start]
        
        return tree, {v: self.weight(v, tree[v]) for v in tree}
    
    # this shit is dumb
    fewest_flights = paths_with_fewest_edges
    shortest_path = shortest_paths
    minimum_salt = minimum_spanning_tree
