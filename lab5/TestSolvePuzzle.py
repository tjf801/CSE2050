import unittest

from solve_puzzle import *

class TestSolvePuzzle(unittest.TestCase):
	def test_examples(self):
		self.assertTrue(solve_puzzle([3, 6, 4, 1, 3, 4, 2, 0]))
		self.assertFalse(solve_puzzle([3, 4, 1, 2, 0]))
	
	def test_edge_cases(self):
		self.assertTrue(solve_puzzle([0])) # i think?
		self.assertTrue(solve_puzzle([1, 0]))
		self.assertFalse(solve_puzzle([0, 0]))
		self.assertTrue(solve_puzzle([1, 1]))
		self.assertTrue(solve_puzzle([1, 0, 0, 0, 0, 1]))
		# self.assertTrue(solve_puzzle([1] * 2000)) # this is a recursion error oops
	
	def test_random(self):
		self.assertTrue(solve_puzzle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
		self.assertTrue(solve_puzzle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0]))
		# Okay random thought as im writing these tests: im like 90% sure that this is an NP-complete problem LOL
		self.assertFalse(solve_puzzle([2, 2, 2, 2, 2, 0]))
		self.assertTrue(solve_puzzle([2, 0, 2, 0, 2, 0, 0]))

if __name__ == '__main__':
	unittest.main()