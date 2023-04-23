from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Collection, Hashable, Iterable, Iterator
from typing import TypeVar

Vertex = TypeVar("Vertex", bound=Hashable)

class AbstractGraph(ABC, Collection[Vertex]):
    @abstractmethod
    def __init__(
        self,
        vertices: Iterable[Vertex] | None = None,
        edges: Iterable[tuple[Vertex, Vertex]] | None = None,
    ) -> None:
        """Initialize a graph with the given vertices and edges.
        
        If no vertices or edges are given, the graph is empty.

        Parameters
        ----------
        vertices : Iterable[Vertex], optional
            The vertices to add to the graph. If None, no vertices are added.
        edges : Iterable[tuple[Vertex, Vertex]], optional
            The edges to add to the graph. If None, no edges are added.
            The vertices in the edges must already be in the graph.

        Raises
        ------
        ValueError
            If an edge is given whose vertices are not in the graph.
        """
    
    @abstractmethod
    def __len__(self) -> int:
        """Return the number of vertices in the graph."""
    @abstractmethod
    def __iter__(self) -> Iterator[Vertex]:
        """Return an iterator over all the vertices in the graph."""
    @abstractmethod
    def __contains__(self, v: object) -> bool:
        """Return True if the given vertex is in the graph."""
    
    @abstractmethod
    def add_vertex(self, v: Vertex) -> None:
        """Add a vertex to the graph.

        Raises
        ------
        ValueError
            If the vertex is already in the graph.
        """
    @abstractmethod
    def remove_vertex(self, v: Vertex) -> None:
        """Remove a vertex from the graph.

        Raises
        ------
        ValueError
            If the vertex is not in the graph.
        """
    
    @abstractmethod
    def add_edge(self, e: tuple[Vertex, Vertex]) -> None:
        """Add an edge to the graph.

        Raises
        ------
        ValueError
            If the edge is already in the graph.
        """
    @abstractmethod
    def remove_edge(self, e: tuple[Vertex, Vertex]) -> None:
        """Remove an edge from the graph.

        Raises
        ------
        ValueError
            If the edge is not in the graph.
        """
    
    @abstractmethod
    def _neighbors(self, v: Vertex) -> set[Vertex]:
        """Return the neighbors of the given vertex."""


class Graph_ES(AbstractGraph[Vertex]): # noqa: N801
    _vertices: set[Vertex]
    _edges: set[tuple[Vertex, Vertex]]
    
    def __init__(
        self,
        vertices: Iterable[Vertex] | None = None,
        edges: Iterable[tuple[Vertex, Vertex]] | None = None,
    ) -> None:
        self._vertices = set(vertices) if vertices is not None else set()
        self._edges = set(edges) if edges is not None else set()
        
        for u, v in self._edges:
            if u not in self._vertices or v not in self._vertices:
                raise ValueError("Edge vertices must be in the graph.")
    
    def __len__(self) -> int:
        return len(self._vertices)
    
    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._vertices)
    
    def __contains__(self, v: object) -> bool:
        return v in self._vertices
    
    def add_vertex(self, v: Vertex) -> None:
        if v in self._vertices:
            raise ValueError("Vertex already in the graph.")
        self._vertices.add(v)
    
    def remove_vertex(self, v: Vertex) -> None:
        if v not in self._vertices:
            raise ValueError("Vertex not in the graph.")
        self._vertices.remove(v)
        self._edges = {(u, w) for u, w in self._edges if u != v and w != v}
    
    def add_edge(self, e: tuple[Vertex, Vertex]) -> None:
        if e in self._edges:
            raise ValueError("Edge already in the graph.")
        if e[0] not in self._vertices or e[1] not in self._vertices:
            raise ValueError("Edge vertices must be in the graph.")
        self._edges.add(e)
    
    def remove_edge(self, e: tuple[Vertex, Vertex]) -> None:
        if e not in self._edges:
            raise ValueError("Edge not in the graph.")
        self._edges.remove(e)
    
    def _neighbors(self, v: Vertex) -> set[Vertex]:
        return {w for u, w in self._edges if u == v}

class Graph_AS(AbstractGraph[Vertex]): # noqa: N801
    _vertices: set[Vertex]
    _neighbor_dict: dict[Vertex, set[Vertex]]
    
    def __init__(
        self,
        vertices: Iterable[Vertex] | None = None,
        edges: Iterable[tuple[Vertex, Vertex]] | None = None,
    ) -> None:
        self._vertices = set(vertices) if vertices is not None else set()
        self._neighbor_dict = {v: set() for v in self._vertices}
        
        for u, v in edges or []:
            if u not in self._vertices or v not in self._vertices:
                raise ValueError("Edge vertices must be in the graph.")
            self._neighbor_dict[u].add(v)
            self._neighbor_dict[v].add(u)
    
    def __len__(self) -> int:
        return len(self._vertices)
    
    def __iter__(self) -> Iterator[Vertex]:
        return iter(self._vertices)
    
    def __contains__(self, v: object) -> bool:
        return v in self._vertices
    
    def add_vertex(self, v: Vertex) -> None:
        if v in self._vertices:
            raise ValueError("Vertex already in the graph.")
        self._vertices.add(v)
        self._neighbor_dict[v] = set()
    
    def remove_vertex(self, v: Vertex) -> None:
        if v not in self._vertices:
            raise ValueError("Vertex not in the graph.")
        self._vertices.remove(v)
        del self._neighbor_dict[v]
        for u in self._neighbor_dict:
            self._neighbor_dict[u].discard(v)
    
    def add_edge(self, e: tuple[Vertex, Vertex]) -> None:
        if e[0] not in self._vertices or e[1] not in self._vertices:
            raise ValueError("Edge vertices must be in the graph.")
        self._neighbor_dict[e[0]].add(e[1])
        self._neighbor_dict[e[1]].add(e[0])
    
    def remove_edge(self, e: tuple[Vertex, Vertex]) -> None:
        self._neighbor_dict[e[0]].discard(e[1])
        self._neighbor_dict[e[1]].discard(e[0])
    
    def _neighbors(self, v: Vertex) -> set[Vertex]:
        return self._neighbor_dict[v]
