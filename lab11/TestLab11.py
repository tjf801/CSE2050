# pyright: reportPrivateUsage=false, reportUninitializedInstanceVariable=false
# ruff: noqa: N801
import typing
import unittest

if typing.TYPE_CHECKING:
    from .lab11 import Graph_AS, Graph_ES
else:
    from lab11 import Graph_AS, Graph_ES


class test_GraphES(unittest.TestCase):
    def setUp(self) -> None:
        """Initialize a Graph with a few vertices and edges."""
        # 1 <--> 2 <--> 3
        vs = {1, 2, 3}
        es = {(1,2), (2,1), (2,3), (3,2)}
        self.g = Graph_ES(vs, es) # self.g available in all unittests
    
    def test_addremove_vertices(self) -> None:
        """Tests that we can add and remove vertices from graph."""
        self.assertEqual(len(self.g), 3) # should have 3 vertices
        
        self.g.remove_vertex(2)
        self.assertEqual(len(self.g), 2) # should have 2 vertices
        
        self.g.add_vertex(4)
        self.assertEqual(len(self.g), 3)
    
    def test_addremove_edges(self) -> None:
        """Test that we can add and remove edges from graph."""
        # Initially, 1 is connected to 2
        n1 = set(self.g._neighbors(1)) # normally we wouldn't test private attributes
                                    # we do so here since it's part of the assignment.
        self.assertEqual(n1, {2})
        
        # add connection from 1-3
        self.g.add_edge((1, 3))
        n1 = set(self.g._neighbors(1))
        self.assertEqual(n1, {2,3})
        
        # remove connection 1-2
        self.g.remove_edge((1, 2))
        n1 = set(self.g._neighbors(1))
        self.assertEqual(n1, {3})
    
    def test_iter(self) -> None:
        """Test that iter() goes over vertices correctly."""
        vs = set(self.g)
        self.assertEqual(vs, {1, 2, 3})

        # Note that order does not matter when comparing sets
        self.g.add_vertex(7)
        vs = set(self.g)
        self.assertEqual(vs, {7, 1, 2, 3})

class test_GraphAS(unittest.TestCase):
    def setUp(self) -> None:
        """Initialize a Graph with a few vertices and edges."""
        # 1 <--> 2 <--> 3
        vs = {1, 2, 3}
        es = {(1,2), (2,1), (2,3), (3,2)}
        self.g = Graph_AS(vs, es) # self.g available in all unittests
    
    def test_addremove_vertices(self) -> None:
        """Test that we can add and remove vertices from graph."""
        self.assertEqual(len(self.g), 3) # should have 3 vertices
        
        self.g.remove_vertex(2)
        self.assertEqual(len(self.g), 2) # should have 2 vertices
        
        self.g.add_vertex(4)
        self.assertEqual(len(self.g), 3)
    
    def test_addremove_edges(self) -> None:
        """Test that we can add and remove edges from graph."""
        # Initialliy, 1 is connected to 2
        n1 = set(self.g._neighbors(1))# normally we wouldn't test private attributes
                                      # we do so here since it's part of the assignment.
        self.assertEqual(n1, {2})
        
        # add connection from 1-3
        self.g.add_edge((1, 3))
        n1 = set(self.g._neighbors(1))
        self.assertEqual(n1, {2,3})
        
        # remove connection 1-2
        self.g.remove_edge((1, 2))
        n1 = set(self.g._neighbors(1))
        self.assertEqual(n1, {3})
    
    def test_iter(self) -> None:
        """Test that iter() goes over vertices correctly."""
        vs = set(self.g)
        self.assertEqual(vs, {1, 2, 3})
        
        # Note that order does not matter when comparing sets
        self.g.add_vertex(7)
        vs = set(self.g)
        self.assertEqual(vs, {7, 1, 2, 3})

if __name__=="__main__":
    unittest.main()
