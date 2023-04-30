import unittest

from Graph import Graph


class test_Graph(unittest.TestCase): # noqa: N801
    def setUp(self) -> None:
        """Create a graph `self.g` to use in other unittests."""
        self.g = Graph[int, int]( # pyright: ignore[reportUninitializedInstanceVariable]
            vertices = [1, 2, 3, 4, 5],
            edge_weights = {
                ((1, 2), 1),
                ((2, 3), 1),
                ((1, 3), 2),
                ((3, 4), 1),
                ((3, 5), 3),
                ((4, 5), 2),
            }
        )
    
    def test_len(self) -> None:
        """Test the `__len__` method of the `Graph` class."""
        self.assertEqual(len(self.g), 5)
        self.assertEqual(len(Graph[int, int]()), 0)
    
    def test_contains(self) -> None:
        """Test the `__contains__` method of the `Graph` class."""
        self.assertIn(1, self.g)
        self.assertIn(2, self.g)
        self.assertIn(3, self.g)
        self.assertIn(4, self.g)
        self.assertIn(5, self.g)
        self.assertNotIn(6, self.g)
        self.assertNotIn(None, self.g)
        self.assertNotIn(False, self.g) # noqa: FBT003
        self.assertNotIn(object(), self.g)
    
    def test_contains_edge(self) -> None:
        """Test the `__contains__` method of the `Graph` class with edges."""
        self.assertIn((1, 2), self.g)
        self.assertIn((2, 1), self.g)
        self.assertIn((2, 3), self.g)
        self.assertIn((3, 5), self.g)
        self.assertNotIn((1, 5), self.g)
        self.assertNotIn((5, 1), self.g)
        self.assertNotIn((6, 9), self.g)
        self.assertNotIn((0, 1), self.g)
    
    def test_iter(self) -> None:
        """Test the `__iter__` method of the `Graph` class."""
        self.assertEqual(set(self.g), {1, 2, 3, 4, 5})
        self.assertEqual(set(Graph[int, int]()), set())
    
    def test_add_vertex(self) -> None:
        """Test the `add_vertex` method of the `Graph` class."""
        self.g.add_vertex(6)
        self.assertIn(6, self.g)
        self.assertEqual(len(self.g), 6)
    
    def test_remove_vertex(self) -> None:
        """Test the `remove_vertex` method of the `Graph` class."""
        self.g.remove_vertex(3)
        self.assertNotIn(3, self.g)
        self.assertEqual(len(self.g), 4)
        self.assertNotIn((3, 4), self.g)
    
    def test_add_edge(self) -> None:
        """Test the `add_edge` method of the `Graph` class."""
        self.assertNotIn((1, 5), self.g)
        self.g.add_edge(1, 5, 0)
        self.assertIn((1, 5), self.g)
        self.assertIn((5, 1), self.g)
    
    def test_remove_edge(self) -> None:
        """Test the `remove_edge` method of the `Graph` class."""
        self.assertIn((3, 4), self.g)
        self.g.remove_edge(3, 4)
        self.assertNotIn((3, 4), self.g)
        self.assertNotIn((4, 3), self.g)
    
    def test_weight(self) -> None:
        """Test the `weight` method of the `Graph` class."""
        self.assertEqual(self.g.weight(1, 2), 1)
        self.assertEqual(self.g.weight(2, 1), 1)
        self.assertEqual(self.g.weight(2, 3), 1)
        self.assertEqual(self.g.weight(3, 5), 3)
        with self.assertRaises(ValueError):
            self.g.weight(1, 5)
    
    def test_neighbors(self) -> None:
        """Test the `neighbors` method of the `Graph` class."""
        self.assertEqual({n for n, _ in self.g.neighbors(1)}, {2, 3})
        self.assertEqual({n for n, _ in self.g.neighbors(2)}, {1, 3})
        self.assertEqual({n for n, _ in self.g.neighbors(3)}, {1, 2, 4, 5})
        self.assertEqual({n for n, _ in self.g.neighbors(4)}, {3, 5})
        self.assertEqual({n for n, _ in self.g.neighbors(5)}, {3, 4})
        with self.assertRaises(ValueError):
            set(self.g.neighbors(6))

class test_GraphTraversal(unittest.TestCase): # noqa: N801
    def setUp(self) -> None:
        """Create a graph `self.g` to use in other unittests."""
        # my house ------------ ur moms house
        #             2.0       ____/   |
        #                  ____/        |
        #             ____/ 1.0         | 1.0
        #        ____/                  |
        # the divorce court ----- a cheap motel
        #            \       1.5    /
        #        0.5  \            / 2.5
        #              \          /
        #             ur dads office
        self.g = Graph[str, float]( # pyright: ignore[reportUninitializedInstanceVariable] # noqa: E501
            vertices = [
                'ur moms house',
                'my house',
                'a cheap motel',
                'ur dads office',
                'the divorce court'
            ],
            edge_weights=[
                (('my house', 'ur moms house'), 2.0),
                (('ur moms house', 'a cheap motel'), 1.0),
                (('ur moms house', 'the divorce court'), 1.0),
                (('a cheap motel', 'the divorce court'), 1.5),
                (('the divorce court', 'ur dads office'), 0.5),
                (('ur dads office', 'a cheap motel'), 2.5),
            ]
        )
    
    def test_prims_algorithm(self) -> None:
        textbook_example = Graph(
            {1,2,3,4,5},
            {
                ((1, 2), 1),
                ((2, 3), 1),
                ((1, 3), 2),
                ((3, 4), 1),
                ((3, 5), 3),
                ((4, 5), 2),
            }
        )
        self.assertEqual(
            textbook_example.minimum_spanning_tree(1)[0],
            {2: 1, 3: 2, 4: 3, 5: 4},
        )
    
    def test_dijkstras_algorithm(self) -> None:
        stolen_wikipedia_example = Graph(
            vertices = [1, 2, 3, 4, 5, 6],
            edge_weights = [
                ((1, 2), 7),
                ((1, 3), 9),
                ((1, 6), 14),
                ((2, 3), 10),
                ((2, 4), 15),
                ((3, 4), 11),
                ((3, 6), 2),
                ((4, 5), 6),
                ((5, 6), 9),
            ]
        )
        self.assertEqual(
            stolen_wikipedia_example.shortest_paths(1),
            (
                {2: 1, 3: 1, 4: 3, 5: 6, 6: 3},
                {1: 0, 2: 7, 3: 9, 4: 20, 5: 20, 6: 11}
            )
        )
    
    # TODO: Which alg do you use here, and why?
    # Alg: Breadth-first search
    # Why: Simple unweighted graph traversal algorithm
    def test_fewest_flights(self) -> None:
        """Test the `fewest_flights` method of the `Graph` class."""
        _, num_flights = self.g.fewest_flights('ur moms house')
        self.assertEqual(num_flights['my house'], 1)
        self.assertEqual(num_flights['a cheap motel'], 1)
        self.assertEqual(num_flights['ur dads office'], 2)
        self.assertEqual(num_flights['the divorce court'], 1)
    
    # TODO: Which alg do you use here, and why?
    # Alg: Dijkstra's algorithm
    # Why: Because it finds the shortest path between nodes in a weighted graph
    def test_shortest_path(self) -> None:
        """Test the `shortest_path` method of the `Graph` class."""
        shortest_paths, _ = self.g.shortest_path('ur moms house')
        self.assertEqual(shortest_paths['my house'], 'ur moms house')
        self.assertEqual(shortest_paths['a cheap motel'], 'ur moms house')
        self.assertEqual(shortest_paths['ur dads office'], 'the divorce court')
        self.assertEqual(shortest_paths['the divorce court'], 'ur moms house')
    
    # TODO: Which alg do you use here, and why?
    # Alg: Prim's algorithm
    # Why: Because it finds the minimum spanning tree of a weighted graph
    def test_minimum_salt(self) -> None:
        """Test the `minimum_salt` method of the `Graph` class."""
        spanning_tree, _ = self.g.minimum_salt('ur moms house')
        self.assertEqual(spanning_tree['my house'], 'ur moms house')
        self.assertEqual(spanning_tree['a cheap motel'], 'ur moms house')
        self.assertEqual(spanning_tree['the divorce court'], 'ur moms house')
        self.assertEqual(spanning_tree['ur dads office'], 'the divorce court')

if __name__ == '__main__':
    unittest.main()
