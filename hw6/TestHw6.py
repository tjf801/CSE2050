import typing
import unittest

if typing.TYPE_CHECKING:
    from hw6.hw6 import find_zero, sort_halfsorted, bubble, selection, insertion
    from hw6.TestHelpers import generate_halfsorted, is_sorted
else:
    from hw6 import find_zero, sort_halfsorted, bubble, selection, insertion
    from TestHelpers import generate_halfsorted, is_sorted

class Test_SortHalfSorted(unittest.TestCase):
    def _test_sort_halfsorted(self, sort: typing.Callable[[typing.MutableSequence, int, int], None]):
        # use sort_halfsorted(L, sort) to test
        
        max_n = 50
        
        # test that it works for random lists
        for n in range(1, max_n):
            for i in range(n):
                with self.subTest(n=n, i=i):
                    L, _ = generate_halfsorted(n, idx_zero=i, pattern='random')
                    L_init = L.copy()
                    sort_halfsorted(L, sort)
                    self.assertTrue(is_sorted(L), f"n={n}, i={i}, L={L_init}")
        
        # test that it works for reverse lists
        for n in range(1, max_n):
            for i in range(n):
                with self.subTest(n=n, i=i):
                    L, _ = generate_halfsorted(n, idx_zero=i, pattern='reverse')
                    sort_halfsorted(L, sort)
                    self.assertTrue(is_sorted(L))
        
        # test that it works for sorted lists
        for n in range(1, max_n):
            for i in range(n):
                with self.subTest(n=n, i=i):
                    L, _ = generate_halfsorted(n, idx_zero=i, pattern='sorted')
                    sort_halfsorted(L, sort)
                    self.assertTrue(is_sorted(L))
    
    def test_halfsorted_bubble(self):
        # use sort_halfsorted(L, bubble) to test
        self._test_sort_halfsorted(bubble)
    
    def test_halfsorted_selection(self):
        # use sort_halfsorted(L, selection) to test
        self._test_sort_halfsorted(selection)
    
    def test_halfsorted_insertion(self):
        # use sort_halfsorted(L, insertion) to test
        self._test_sort_halfsorted(insertion)

# Test provided for you
class Test_FindZero(unittest.TestCase):
    def test1_allLengthsAllIndices(self):
        '''Tests find_zero for every possible index, for lists from 1 to 100 items

            Lists
            -----
                '-' and '+' denote negative and positive ingeters, respectively
                                            idx_zero
                n = 1                     
                    L = [0]              0

                n = 2
                    L = [0, +]          0
                    L = [-, 0]          1

                n = 3                     
                    L = [0, +, +]      0
                    L = [-, 0, +]      1  
                    L = [-, -, 0]      2

                n = 4
                    L = [0, +, +, +]  0
                    L = [-, 0, +, +]  1
                    L = [-, -, 0, +]  2
                    L = [-, -, -, 0]  3
                ...
                n = 100
                    L = [0, ..., +]    0
                    ...
                    L = [-, ..., 0]    99
        '''
        
        # note the use of `subTest`. These all count as 1 unittest if they pass,
        # but all that fail will be displayed independently
        for pattern in ('random', 'reverse', 'sorted'):
            with self.subTest(pattern=pattern):
                for n in range(1, 50):
                    with self.subTest(n=n):
                        for i in range(n):
                            with self.subTest(i=i):
                                L, idx_zero = generate_halfsorted(n, idx_zero=i, pattern=pattern)
                                self.assertEqual(find_zero(L), idx_zero)

unittest.main()

