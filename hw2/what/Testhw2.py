# Start here. Once you have good test, move on to hw2.py

import typing
import unittest

if typing.TYPE_CHECKING:
	from hw2.what.hw2 import Card, Deck, is_group
else:
	from Cards import Card, Deck, is_group

class TestCard(unittest.TestCase):
	def test_init(self):
		"""Tests that we can initialize cards w/ number/color/shading/shaper"""
		c1 = Card(2, "green", "striped", "diamond")
		
		self.assertEqual(c1.number, 2)
		self.assertEqual(c1.color, "green")
		self.assertEqual(c1.shading, "striped")
		self.assertEqual(c1.shape, "diamond")
	
	def test_str(self):
		"""test that we can get a good string representation of GroupCard instances"""
		
		card = Card(2, "green", "striped", "diamond")
		self.assertEqual(str(card), "Card(2, green, striped, diamond)")
		
		card2 = Card(1, "blue", "empty", "oval")
		self.assertEqual(str(card2), "Card(1, blue, empty, oval)")

	def test_eq(self):
		"""Tests that two cards are equal iff all attributes (number, color, shading, shape) are equal"""
		card1 = Card(2, "green", "striped", "diamond")
		card2 = Card(2, "green", "striped", "oval")
		
		self.assertNotEqual(card1, card2)
		card2.shape = "diamond"
		card2.shading = "empty"
		self.assertNotEqual(card1, card2)
		card2.shading = "striped"
		card2.color = "blue"
		self.assertNotEqual(card1, card2)
		card2.color = "green"
		card2.number = 1
		self.assertNotEqual(card1, card2)
		card2.number = 2
		self.assertEqual(card1, card2)

# Write your own docstrings for the tests below
class TestDeck(unittest.TestCase):
	def test_init(self):
		"Tests that you can initialize a deck of cards"
		deck = Deck()
		self.assertEqual(len(deck), 81)
		
		deck = Deck(
			numbers = {1, 2},
			colors = {'maroon', 'aqua', 'perywinkle', 'blue'},
			shadings = {"striped"},
			shapes = {"circles", "squares", "ovals"}
		)
		self.assertEqual(len(deck), 24)
	
	def test_draw_top(self):
		"Tests that draw_top removes and returns the top card"
		deck = Deck()
		card = deck.draw_top()
		self.assertEqual(len(deck), 80)
		
		self.assertEqual(card.number, 1)
		self.assertEqual(card.color, 'green')
		self.assertEqual(card.shading, 'empty')
		self.assertEqual(card.shape, 'diamond')
		
		for _ in range(80):
			deck.draw_top()
		
		self.assertEqual(len(deck), 0)
		
		with self.assertRaises(AttributeError):
			deck.draw_top()
	
	def test_shuffle(self):
		"Tests that shuffle shuffles the deck"
		import random
		
		random.seed(0)
		
		deck = Deck()
		deck.shuffle()
		self.assertEqual(len(deck), 81)
		
		card = deck.draw_top()
		# wtf is the point of having this test if you have to program it 
		# correctly the first time to get the correct output??? it literally 
		# defeats the purpose of having the test in the first place
		self.assertEqual(card, Card(2, 'green', 'striped', 'squiggle'))

# After Card and Deck are working, write and test the alg below.
# Include a docstring.
class TestSimulator(unittest.TestCase):
	def test_is_group(self):
		"""Tests that is_group returns True iff the three cards form a group"""
		card1 = Card(1, 'green', 'empty', 'diamond')
		card2 = Card(2, 'green', 'empty', 'diamond')
		card3 = Card(3, 'green', 'empty', 'diamond')
		
		self.assertTrue(is_group(card1, card2, card3))
		
		card1 = Card(1, 'green', 'empty', 'diamond')
		card2 = Card(2, 'green', 'empty', 'diamond')
		card3 = Card(3, 'green', 'empty', 'oval')
		
		self.assertFalse(is_group(card1, card2, card3))
		
		card1 = Card(1, 'green', 'empty', 'diamond')
		card2 = Card(2, 'green', 'empty', 'oval')
		card3 = Card(3, 'green', 'empty', 'squiggle')
		
		self.assertTrue(is_group(card1, card2, card3))


unittest.main() # runs all unittests above