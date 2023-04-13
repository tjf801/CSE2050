# ruff: noqa: E501, ANN201, S311, N801
import random
import typing
import unittest

if typing.TYPE_CHECKING:
    from .lab10 import PQ_OL, PQ_UL, Entry
else:
    from lab10 import PQ_OL, PQ_UL, Entry

random.seed(658)    # Fix the seed so it fails the same way every time if there is a bug

class TestEntry(unittest.TestCase):
    def setUp(self):
        """Set up the test case."""
        self.e1 = Entry("rachel", 0) # type: ignore
        self.e2 = Entry("jake", 1) # type: ignore
        self.e3 = Entry("marco", 2) # type: ignore
        self.e4 = Entry("cassie", 3) # type: ignore
        self.e5 = Entry("tobias", 4) # type: ignore
        self.e6 = Entry("ax", 5) # type: ignore

    def test_init(self):
        """Test that initialization is called correctly."""
        self.assertEqual(self.e1.item, 'rachel')
        self.assertEqual(self.e1.priority, 0)

    def test_lt(self):
        """Test the less than operator."""
        for e in [self.e2, self.e3, self.e4, self.e5, self.e6]:
            self.assertLess(self.e1, e)

        for e in [self.e1, self.e2, self.e3, self.e4, self.e5]:
            self.assertGreater(self.e6, e)

        self.assertFalse(self.e1 < Entry("alice", 0))

    def test_eq(self):
        """Test the equality operator."""
        self.assertEqual(self.e1, Entry("rachel", 0))       # same item & priority

        self.assertNotEqual(self.e1, Entry("rachel", 1))    # same item, different priority

        self.assertNotEqual(self.e1, Entry("jake", 0))      # same item, different priority

class TestPQ_UL(unittest.TestCase):
    def test_add_remove_sequential(self):
        """Add and remove items sequentially."""
        # Construct PQ
        n = 10
        pq = PQ_UL[str, int]()
        for i in range(n):
            self.assertEqual(len(pq), i)
            pq.insert(str(i), i)

        # Removes entries one at a time
        old = pq.find_min()
        for _ in range(n):
            peek = pq.find_min()
            new = pq.remove_min()
            assert new == peek
            assert old.priority <= new.priority # make sure we are removing in order
            old = new

    def test_add_remove_random(self):
        """Randomly add, then remove, a large number of items."""
        # Construct PQ
        n = 100
        pq = PQ_UL[str, int]()
        for _ in range(n):
            pq.insert('pikachu', random.randint(0, n))

        # Removes entries one at a time
        old = pq.find_min()
        for _ in range(n):
            peek = pq.find_min()
            new = pq.remove_min()
            assert new == peek
            assert old.priority <= new.priority # make sure we are removing in order
            old = new

class TestPQ_OL(unittest.TestCase):
    def test_add_remove_sequential(self):
        """Add and remove items sequentially."""
        # Construct PQ
        n = 1000
        pq = PQ_OL[str, int]()
        for i in range(n):
            self.assertEqual(len(pq), i)
            pq.insert(str(i), i)
        

        # Removes entries one at a time
        old = pq.find_min()
        for _ in range(n):
            peek = pq.find_min()
            new = pq.remove_min()
            assert new == peek
            assert old.priority <= new.priority # make sure we are removing in order
            old = new

    def test_add_remove_random(self):
        """Randomly add then remove a large number of items."""
        # Construct PQ
        n = 1000
        pq = PQ_OL[str, int]()
        for _ in range(n):
            pq.insert('pikachu', random.randint(0, n))

        # Removes entries one at a time
        old = pq.find_min()
        for _ in range(n):
            peek = pq.find_min()
            new = pq.remove_min()
            assert new == peek
            assert old.priority <= new.priority # make sure we are removing in order
            old = new

if __name__=="__main__":
    unittest.main()
