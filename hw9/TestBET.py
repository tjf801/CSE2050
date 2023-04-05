# ruff: noqa: ANN201
import unittest

from BET import (
    BETLeaf,
    BETOperator,
    BinaryExpressionTreeNode,
    CardType,
    create_trees,
    find_solutions,
)


class TestBETNode(unittest.TestCase):
    def test_repr(self):
        """Test the repr of a node."""
        node = BETOperator(
            '*',
            BETLeaf('A'),
            BETOperator(
                '-',
                BETLeaf('2'),
                BETOperator(
                    '+',
                    BETLeaf('3'),
                    BETLeaf('4')
                )
            )
        )
        expected_str = '(A*(2-(3+4)))'
        self.assertEqual(repr(node), expected_str)
    
    def test_evaluate(self):
        """Test the evaluate method of a node."""
        for operator in ('+', '-', '*', '/'):
            for card1 in CardType:
                for card2 in CardType:
                    with self.subTest(
                        operator=operator,
                        card1=str(card1),
                        card2=str(card2)
                    ):
                        node = BETOperator(
                            operator,
                            BETLeaf(str(card1)),
                            BETLeaf(str(card2))
                        )
                        # allow for floating point error in division
                        self.assertAlmostEqual(
                            node.evaluate(),
                            eval(f'{card1.value} {operator} {card2.value}')
                        )
    
    def test_from_postfix(self):
        """Test the BinaryExpressionTreeNode.from_postfix method."""
        result = BinaryExpressionTreeNode.from_postfix('A 2 3 4 + - *')
        tree = BETOperator(
            '*',
            BETLeaf('A'),
            BETOperator(
                '-',
                BETLeaf('2'),
                BETOperator(
                    '+',
                    BETLeaf('3'),
                    BETLeaf('4')
                )
            )
        )
        self.assertEqual(result, tree)
    
    def test_from_postfix_invalid(self):
        """Test the BinaryExpressionTreeNode.from_postfix method."""
        with self.assertRaises(ValueError):
            BinaryExpressionTreeNode.from_postfix('A 2 3 4 + -')
        
        with self.assertRaises(ValueError):
            BinaryExpressionTreeNode.from_postfix('A 2 3 4 + - * *')
        
        with self.assertRaises(ValueError):
            BinaryExpressionTreeNode.from_postfix('A 2')

class TestCreateTrees(unittest.TestCase):
    def test_hand1(self):
        """Test the create_trees function."""
        trees = list(create_trees('A23Q'))
        self.assertEqual(len(trees), 320)
        self.assertIn(
            BinaryExpressionTreeNode.from_postfix('A 2 3 Q + - *'),
            trees
        )
    
    def test_hand2(self):
        """Edge cases for create_trees."""
        self.assertEqual(list(create_trees('')), [])
        self.assertEqual(list(create_trees('A')), [BETLeaf('A')])
        self.assertEqual(len(list(create_trees('AA'))), 4)

class TestFindSolutions(unittest.TestCase):
    def test_eval_to_24(self):
        """Test to make sure all solutions evaluate to 24."""
        for hand in ('QQ54', 'A234', 'A23Q', 'A2345'):
            for tree in find_solutions(hand):
                self.assertEqual(tree.evaluate(), 24)
    
    def test_no_sols(self):
        """Test the find_solutions function with a set of cards with no solution."""
        self.assertEqual(list(find_solutions('AAAA')), [])
    
    def test_A23Q(self): # noqa: N802
        """Test the find_solutions function with An ace, a two, a three, and a queen."""
        trees = list(find_solutions('A23Q'))
        self.assertEqual(len(trees), 33)
        self.assertIn(
            BinaryExpressionTreeNode.from_postfix('3 2 - A + Q *'),
            trees
        )


if __name__ == '__main__':
    unittest.main()
