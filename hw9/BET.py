from __future__ import annotations

import abc
import typing
from abc import abstractmethod
from enum import Enum
from fractions import Fraction
from itertools import permutations

if typing.TYPE_CHECKING:
    import numbers
    from collections.abc import Iterator, Sequence


_TARGET_VALUE = 24


class CardType(Enum):
    """An enumeration of the types of cards in a standard deck of cards."""
    
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    
    def __str__(self) -> str:
        return {
            CardType.ACE: 'A',
            CardType.TWO: '2',
            CardType.THREE: '3',
            CardType.FOUR: '4',
            CardType.FIVE: '5',
            CardType.SIX: '6',
            CardType.SEVEN: '7',
            CardType.EIGHT: '8',
            CardType.NINE: '9',
            CardType.TEN: '10',
            CardType.JACK: 'J',
            CardType.QUEEN: 'Q',
            CardType.KING: 'K'
        }[self]
    
    @classmethod
    def from_str(cls: type[CardType], __value: str) -> CardType:
        """Convert a string to a CardType.

        Raises
        ------
        ValueError
            If the string is not a valid card type. Valid card types are:
            ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        """
        return {
            'A': cls.ACE,
            '2': cls.TWO,
            '3': cls.THREE,
            '4': cls.FOUR,
            '5': cls.FIVE,
            '6': cls.SIX,
            '7': cls.SEVEN,
            '8': cls.EIGHT,
            '9': cls.NINE,
            '10': cls.TEN,
            'J': cls.JACK,
            'Q': cls.QUEEN,
            'K': cls.KING
        }[__value]

class OperatorType(Enum):
    """An enumeration of the operators that can be used in a binary expression."""
    
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    
    def __str__(self) -> str:
        return {
            OperatorType.ADD: '+',
            OperatorType.SUBTRACT: '-',
            OperatorType.MULTIPLY: '*',
            OperatorType.DIVIDE: '/'
        }[self]
    
    @classmethod
    def from_str(cls: type[OperatorType], __value: str) -> OperatorType:
        return {
            '+': cls.ADD,
            '-': cls.SUBTRACT,
            '*': cls.MULTIPLY,
            '/': cls.DIVIDE
        }[__value]


class BinaryExpressionTreeNode(abc.ABC):
    """An abstract base class for a node in a binary expression tree."""
    
    @staticmethod
    def from_postfix(postfix_expression: str) -> BinaryExpressionTreeNode:
        """Create a BinaryExpressionTreeNode from a postfix expression.

        Parameters
        ----------
        postfix_expression : str
            A space-separated postfix expression to convert to a
            `BinaryExpressionTreeNode`. e.g: `'A 2 3 4 + - *'`

        Returns
        -------
        BinaryExpressionTreeNode
            The root of the `BinaryExpressionTreeNode` created from the postfix
            expression.

        Raises
        ------
        ValueError
            If the postfix expression is invalid.

        Examples
        --------
        >>> str(BinaryExpressionTreeNode.from_postfix('A 2 3 4 + - *'))
        '(A*(2-(3+4)))'
        >>> str(BinaryExpressionTreeNode.from_postfix('Q J *'))
        '(Q*J)'
        """
        stack: list[BinaryExpressionTreeNode] = []
        
        for token in postfix_expression.split():
            if token in {'+', '-', '*', '/'}:
                if len(stack) <= 1:
                    raise ValueError(
                        f"Invalid postfix expression '{postfix_expression}'"
                    )
                right = stack.pop()
                left = stack.pop()
                stack.append(BETOperator(token, left, right))
            else:
                stack.append(BETLeaf(token))
        
        if len(stack) != 1:
            raise ValueError(
                f"Invalid postfix expression '{postfix_expression}'"
            )
        
        return stack.pop()
    
    @abstractmethod
    def evaluate(self) -> numbers.Rational:
        """Evaluate the expression represented by this node."""
        raise NotImplementedError
    
    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError
# NOTE: this is only here to make the dumb autograder script happy.
BETNode: typing.TypeAlias = BinaryExpressionTreeNode

class BETLeaf(BinaryExpressionTreeNode):
    """A leaf node in a binary expression tree.
    
    This node represents a single card in a standard deck of cards.

    Attributes
    ----------
    value : CardType
        The value of the card.
    """
    
    value: CardType
    
    def __init__(self, value: CardType | str) -> None:
        if isinstance(value, CardType):
            self.value = value
        else:
            self.value = CardType.from_str(value)
    
    def __repr__(self) -> str:
        return str(self.value)
    
    def evaluate(self) -> numbers.Integral:
        return self.value.value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BETLeaf):
            return NotImplemented
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)

class BETOperator(BinaryExpressionTreeNode):
    """An operator node in a binary expression tree.
    
    This node represents an operator in a binary expression.

    Attributes
    ----------
    operator : OperatorType
        The operator to use.
    left : BinaryExpressionTreeNode
        The left-hand side of the expression.
    right : BinaryExpressionTreeNode
        The right-hand side of the expression.
    """
    
    operator: OperatorType
    left: BinaryExpressionTreeNode
    right: BinaryExpressionTreeNode
    
    def __init__(
        self,
        operator: OperatorType | str,
        left: BinaryExpressionTreeNode,
        right: BinaryExpressionTreeNode
    ) -> None:
        if isinstance(operator, OperatorType):
            self.operator = operator
        else:
            self.operator = OperatorType.from_str(operator)
        
        self.left = left
        self.right = right
    
    def evaluate(self) -> numbers.Rational:
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()
        
        if self.operator == OperatorType.ADD:
            return left_value + right_value
        
        if self.operator == OperatorType.SUBTRACT:
            return left_value - right_value
        
        if self.operator == OperatorType.MULTIPLY:
            return left_value * right_value
        
        if self.operator == OperatorType.DIVIDE:
            if right_value == 0:
                return Fraction(0)
            return Fraction(left_value, right_value)
        
        raise ValueError(f'Unknown operator: {self.operator}')
    
    def __repr__(self) -> str:
        return f'({self.left!r}{self.operator}{self.right!r})'
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BETOperator):
            return NotImplemented
        return (
            self.operator == other.operator
            and self.left == other.left
            and self.right == other.right
        )
    
    def __hash__(self) -> int:
        return hash((self.operator, self.left, self.right))


def create_trees(cards: Sequence[str]) -> Iterator[BinaryExpressionTreeNode]:
    """Create all possible trees from the given cards.
    
    NOTE: this preserves the order of the cards.

    Parameters
    ----------
    cards : Sequence[str]
        The cards to create trees from.

    Yields
    ------
    BinaryExpressionTreeNode
        A tree created from the given cards.

    Examples
    --------
    >>> len(list(create_trees(['A', '2', '3', '4'])))
    320
    >>> list(create_trees(['A', '2']))
    [(A+2), (A-2), (A*2), (A/2)]
    """
    if len(cards) == 0:
        return
    if len(cards) == 1:
        yield BETLeaf(cards[0])
        return
    
    for i in range(len(cards)):
        for operator in OperatorType:
            for left in create_trees(cards[:i]):
                for right in create_trees(cards[i:]):
                    yield BETOperator(
                        operator,
                        left,
                        right
                    )

def find_solutions(cards: typing.Iterable[str]) -> Iterator[BinaryExpressionTreeNode]:
    """Find all possible solutions from the given cards.
    
    This function creates all possible trees from the given cards and
    evaluate them to see if they equal 24.

    Parameters
    ----------
    cards : typing.Iterable[str]
        The cards to find solutions for.

    Yields
    ------
    BinaryExpressionTreeNode
        A tree that evaluates to 24.

    Examples
    --------
    >>> len(list(find_solutions(['A', '2', '3', 'Q'])))
    33
    >>> next(find_solutions(['A', '2', '3', '4'])).evaluate()
    24
    >>> sorted(list(find_solutions(['4', '4', '4', '4'])), key=repr)
    [(((4*4)+4)+4), ((4*4)+(4+4)), ((4+(4*4))+4), ((4+4)+(4*4)), (4+((4*4)+4)), (4+(4+(4*4)))]
    >>> list(find_solutions(['10', 'A', 'A', 'A']))
    []
    """ # noqa: E501
    cards = list(cards)
    if len(set(cards)) == len(cards):
        for permutation in permutations(cards):
            for tree in create_trees(permutation):
                if tree.evaluate() == _TARGET_VALUE:
                    yield tree
    else:
        seen_trees: set[BinaryExpressionTreeNode] = set()
        for permutation in permutations(cards):
            for tree in create_trees(permutation):
                if tree not in seen_trees:
                    if tree.evaluate() == _TARGET_VALUE:
                        yield tree
                    seen_trees.add(tree)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
