from __future__ import annotations
from dataclasses import dataclass
import random
import typing


_V = typing.TypeVar("_V") # value type
_S = typing.TypeVar("_S") # suit type

@dataclass
class Card(typing.Generic[_V, _S]):
	value: _V
	suit: _S
	
	def __str__(self) -> str:
		return f"Card({self.value} of {self.suit})"
	
	def __lt__(self, other: Card) -> bool:
		return self.suit < other.suit or (self.suit == other.suit and self.value < other.value)

class Deck(typing.Generic[_S, _V]):
	__default_suits: typing.Iterable[typing.Literal["clubs", "diamonds", "hearts", "spades"]] = ("clubs", "diamonds", "hearts", "spades")
	__default_values: typing.Iterable[typing.Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]] = range(1, 14) # type: ignore
	
	card_list: list[Card[_V, _S]]
	
	def __init__(self,
		suits: typing.Iterable[_S] = __default_suits,
		values: typing.Iterable[_V] = __default_values,
	):
		self.card_list = []
		
		for value in values:
			for suit in suits:
				self.card_list.append(Card(value, suit))
		
		self.card_list.sort()
	
	def __len__(self) -> int:
		return len(self.card_list)
	
	def sort(self):
		"""Sorts the deck in ascending order."""
		self.card_list.sort()
	
	def __repr__(self) -> str:
		return f"Deck({self.card_list})"
	
	def draw_top(self) -> Card[_V, _S]:
		"""Removes and returns the top card. Raises an IndexError if the deck is empty."""
		if len(self.card_list) == 0:
			# ik the assignment wants me to raise a RuntimeError but
			# that makes me want to die, so im raising an IndexError 
			# instead bc it actually makes sense to do so
			raise IndexError("Cannot draw from empty deck") 
		return self.card_list.pop()
	
	def shuffle(self):
		"""Shuffles the deck in place."""
		random.shuffle(self.card_list)

class Hand(Deck, typing.Generic[_S, _V]):
	card_list: list[Card[_V, _S]]
	
	def __init__(self, cards: typing.Iterable[Card[_V, _S]] = ()):
		self.card_list = list(cards)
	
	def __repr__(self) -> str:
		return f"Hand({self.card_list})"
	
	def play(self, card: Card[_V, _S]) -> Card[_V, _S]:
		"""Removes and returns the specified card. Raises a ValueError if the card is not in the hand."""
		if card not in self.card_list:
			# again with the dumb RuntimeError thing stfu
			raise ValueError("Cannot play a card that is not in the hand")
		
		self.card_list.remove(card)
		
		return card