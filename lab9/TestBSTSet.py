import unittest

from BSTSet import BSTSet


class TestBSTSet(unittest.TestCase):
    def test_put(self) -> None:
        """Test that put operation works with correct ordering."""
        bst = BSTSet()

        # In-order puts
        # Create a balanced tree with 7 nodes
        #       3
        #    /     \
        #   1       5
        #  / \     / \
        # 0   2   4   6
        for i in [3, 1, 0, 2, 5, 4, 6]:
            bst.put(i)

        ino: list[int] = []
        for item in bst.in_order():
            ino.append(item)
        assert ino == [0, 1, 2, 3, 4, 5, 6]

    def test_preorder(self) -> None:
        """Test that preorder traversal works in correct direction."""
        # Unbalanced tree
        # 0
        #  `-1
        #     `-2
        #        `-3
        # Build Set
        bst = BSTSet()
        for i in [0, 1, 2, 3]:
            bst.put(i)

        # Traverse Set
        preo: list[int] = []
        for item in bst.pre_order():
            preo.append(item)
        assert preo == [0, 1, 2, 3]


        # Create a balanced tree with 7 nodes
        #       3
        #    /     \
        #   1       5
        #  / \     / \
        # 0   2   4   6
        # Build Set
        bst = BSTSet()
        for i in [3, 1, 0, 2, 5, 4, 6]:
            bst.put(i)
        
        # Traverse Set
        preo = list(bst.pre_order())
        assert preo == [3, 1, 0, 2, 5, 4, 6]
    
    def test_postorder(self) -> None:
        """Test that preorder traversal works in correct direction."""
        # Unbalanced tree
        # 0
        #  `-1
        #     `-2
        #        `-3
        # Build Set
        bst = BSTSet()
        for i in [0, 1, 2, 3]:
            bst.put(i)
        
        # Traverse Set
        posto = list(bst.post_order())
        assert posto == [3, 2, 1, 0]
        
        # Create a balanced tree with 7 nodes
        #       3
        #    /     \
        #   1       5
        #  / \     / \
        # 0   2   4   6
        # Build Set
        bst = BSTSet()
        for i in [3, 1, 0, 2, 5, 4, 6]:
            bst.put(i)
        
        # Traverse Set
        posto = list(bst.post_order())
        assert posto == [0, 2, 1, 4, 6, 5, 3]

if __name__=="__main__":
    unittest.main()
