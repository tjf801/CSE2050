from __future__ import annotations

import itertools
import random
import typing


Color: typing.TypeAlias = str
Shading: typing.TypeAlias = str
Shape: typing.TypeAlias = str

class Card:
	number: int
	color: Color
	shading: Shading
	shape: Shape
	
	def __init__(self, number: int, color: Color, shading: Shading, shape: Shape):
		self.number = number
		self.color = color
		self.shading = shading
		self.shape = shape

	def __str__(self) -> str:
		return f"Card({self.number}, {self.color}, {self.shading}, {self.shape})"

	# repr() is called instead of str() by some of pytho's built-ins. We'll always
	# want the same value returned in this course, so we can piggyback off of str
	def __repr__(self):
		return str(self)

	def __eq__(self, other) -> bool:
		return (
			self.number == other.number
			and self.color == other.color
			and self.shading == other.shading
			and self.shape == other.shape
		)


# Valid values for default game of GROUP! included here to avoid spelling
# issues. Feel free to copy/paste:
# [1, 2, 3]
# ['diamond', 'squiggle', 'oval']
# ['green', 'blue', 'purple']
# ['empty', 'striped', 'solid']
class Deck:
	_cards: list[Card]
	
	def __init__(self,
		numbers: typing.Iterable[int] = (1, 2, 3),
		colors: typing.Iterable[Color] = ('green', 'blue', 'purple'),
		shadings: typing.Iterable[Shading] = ('empty', 'striped', 'solid'),
		shapes: typing.Iterable[Shape] = ('diamond', 'squiggle', 'oval')
	):
		self._cards = [
			Card(*args) 
			for args in itertools.product(numbers, colors, shadings, shapes)
		][::-1] # reverse the list so we pop from the top of the deck instead
	
	# should remove and return top card
	def draw_top(self) -> Card:
		if not self._cards:
			# why tf do i have to raise an AttributeError and not an IndexError?
			raise AttributeError("Deck is empty")
		
		result = self._cards.pop()
		
		return result

	# should randomly shuffle cards. Does not need a return.
	def shuffle(self):
		random.shuffle(self._cards)
	
	# should return number of items in deck
	def __len__(self) -> int:
		return len(self._cards)



# Oonce Card and Deck are both finished, write tests for this algorithm, then
# write the algorithm

# True if, for all attributes, each card has the same or different values;
# e.g. {1, 1, 1} or {1, 2, 3}, but not {1, 1, 3}
def is_group(*cards: Card) -> bool:
	"""tests if the given cards form a group"""
	
	# iterate over all 4 attributes of the cards
	for attr in ('number', 'color', 'shading', 'shape'):
		values = {getattr(card, attr) for card in cards}
		
		# if the number of unique values is not 1 or `len(cards)`, the cards do not form a group
		# (if its 1, theyre all the same, if its `len(cards)`, theyre all different)
		if len(values) not in (1, len(cards)):
			return False
	
	return True
