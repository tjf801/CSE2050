import typing
import unittest

if typing.TYPE_CHECKING:
	from hw2.Cards import Card, Deck, Hand
else:
	from Cards import Card, Deck, Hand

class TestCard(unittest.TestCase):
	"Test cases specific to the Card class"
	def test_init(self):
		"tests that we can initialize a card with a value and a suit"
		card = Card(8, "clubs")
		self.assertEqual(card.value, 8)
		self.assertEqual(card.suit, "clubs")
	
	def test_str_repr(self):
		"tests that we can get a good string and repr representation of a card"
		card = Card(3, "hearts")
		self.assertEqual(str(card), "Card(3 of hearts)")
		self.assertEqual(repr(card), "Card(3, 'hearts')")
	
	def test_eq(self):
		"tests that two cards are equal if they have the same value and suit"
		card1 = Card(3, "hearts")
		card2 = Card(3, "hearts")
		card3 = Card(3, "diamonds")
		card4 = Card(4, "hearts")
		self.assertEqual(card1, card2)
		self.assertNotEqual(card1, card3)
		self.assertNotEqual(card1, card4)
	
	def test_lt(self):
		"tests that a card is less than another card if it has a lower suit or if it has the same suit but a lower value"
		card1 = Card(3, "hearts")
		card2 = Card(3, "hearts")
		card3 = Card(3, "diamonds")
		card4 = Card(4, "hearts")
		self.assertFalse(card1 < card2)
		self.assertFalse(card1 < card3)
		self.assertTrue(card1 < card4)

class TestDeck(unittest.TestCase):
	def test_init(self):
		"Tests that you can initialize a deck of cards"
		deck = Deck()
		self.assertEqual(len(deck), 52)
		
		deck = Deck(
			values = {1, 2},
			suits = {'maroon', 'aqua', 'perywinkle', 'blue'},
		)
		self.assertEqual(len(deck), 8)
		self.assertEqual(deck.card_list[0], Card(1, 'maroon'))
	
	def test_str_repr(self):
		"""test that we can get a good str and repr of Deck instances"""
		deck = Deck({'hearts'}, {1, 2})
		self.assertEqual(repr(deck), "Deck([Card(value=1, suit='hearts'), Card(value=2, suit='hearts')])")
		self.assertEqual(str(deck), "Deck([Card(1 of hearts), Card(2 of hearts)])")
	
	def test_len(self):
		"Tests that we can get the length of a deck of cards"
		deck = Deck()
		self.assertEqual(len(deck), 52)
		
		deck = Deck(
			values = {1, 2},
			suits = {'maroon', 'aqua', 'perywinkle', 'blue'},
		)
		self.assertEqual(len(deck), 8)
	
	def test_sort(self):
		"Tests that we can sort a deck of cards"
		deck = Deck()
		deck.sort()
		self.assertEqual(deck.card_list[0], Card(1, 'clubs'))
		self.assertEqual(deck.card_list[51], Card(13, 'spades'))
	
	def test_draw(self):
		"Tests that we can draw a card from a deck"
		deck = Deck()
		card = deck.draw_top()
		self.assertEqual(len(deck), 51)
		self.assertEqual(card, Card(1, 'clubs'))
	
	def test_shuffle(self):
		"Tests that we can shuffle a deck of cards"
		import random
		random.seed(0)
		
		deck = Deck()
		deck.shuffle()
		
		self.assertNotEqual(deck.card_list[0], Card(1, 'clubs'))
		self.assertNotEqual(deck.card_list[51], Card(13, 'spades'))

class TestHand(unittest.TestCase):
	def test_init(self):
		"Tests that we can initialize a hand of cards"
		hand = Hand()
		self.assertEqual(len(hand), 0)
		
		hand = Hand([Card(1, 'clubs'), Card(2, 'clubs')])
		self.assertEqual(len(hand), 2)
	
	def test_str_repr(self):
		"""test that we can get a good str and repr of Hand instances"""
		hand = Hand([Card(1, 'clubs'), Card(2, 'clubs')])
		self.assertEqual(repr(hand), "Hand([Card(value=1, suit='clubs'), Card(value=2, suit='clubs')])")
		# self.assertEqual(str(hand), "Hand([Card(1 of clubs), Card(2 of clubs)])")
	
	def test_play(self):
		"Tests that we can play a card from a hand"
		hand = Hand([Card(1, 'clubs'), Card(2, 'clubs')])
		card = hand.play(Card(1, 'clubs'))
		self.assertEqual(card, Card(1, 'clubs'))
		self.assertEqual(len(hand), 1)
		with self.assertRaises(ValueError):
			hand.play(Card(3, 'clubs'))

unittest.main()