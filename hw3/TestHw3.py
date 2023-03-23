import typing
import unittest

if typing.TYPE_CHECKING:
	from hw3.hw3 import find_pairs_naive, find_pairs_optimized
else:
	from hw3 import find_pairs_naive, find_pairs_optimized

class TestFindPairsNaive(unittest.TestCase):
	def test_empty(self):
		"Tests that the empty list returns the empty set"
		self.assertEqual(find_pairs_naive([], 0), set())
		self.assertEqual(find_pairs_naive([], 21381), set())
	
	def test_single(self):
		"Tests that a single element list returns the empty set"
		self.assertEqual(find_pairs_naive([1], 0), set())
		self.assertEqual(find_pairs_naive([1], 1), set())
		self.assertEqual(find_pairs_naive([1], 2), set())
	
	def test_duplicate(self):
		"Tests that duplicate elements are handled correctly"
		self.assertEqual(find_pairs_naive([1, 2, 3, 4, 5], 10), set())
		self.assertEqual(find_pairs_naive([1, 2, 3, 4, 5], 6), {(1, 5), (2, 4)})
	
	def test_zero_target(self):
		"Test the function with a target of zero"
		self.assertEqual(find_pairs_naive([1, 2, 3, -2], 0), {(2, -2)})
		self.assertEqual(find_pairs_naive([1, 2, 3, 0], 0), {})

class TestFindPairsOptimized(unittest.TestCase):
	def test_empty(self):
		"Tests that the empty list returns the empty set"
		self.assertEqual(find_pairs_optimized([], 0), set())
		self.assertEqual(find_pairs_optimized([], 21381), set())
	
	def test_single(self):
		"Tests that a single element list returns the empty set"
		self.assertEqual(find_pairs_optimized([1], 0), set())
		self.assertEqual(find_pairs_optimized([1], 1), set())
		self.assertEqual(find_pairs_optimized([1], 2), set())
	
	def test_duplicate(self):
		"Tests that duplicate elements are handled correctly"
		self.assertEqual(find_pairs_optimized([1, 2, 3, 4, 5], 10), set())
		self.assertEqual(find_pairs_optimized([1, 2, 3, 4, 5], 6), {(1, 5), (2, 4)})
	
	def test_zero_target(self):
		"Test the function with a target of zero"
		self.assertEqual(find_pairs_optimized([1, 2, 3, -2], 0), {(2, -2)})
		self.assertEqual(find_pairs_optimized([1, 2, 3, 0], 0), {})


if __name__ == '__main__':
	unittest.main()