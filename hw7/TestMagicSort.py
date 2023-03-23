# ruff: noqa: ANN201

import unittest

from MagicSort import (
    EdgeCase,
    insertionsort,
    linear_scan,
    magic_sort,
    mergesort,
    quicksort,
    reverse_list,
)


class TestLinearScan(unittest.TestCase):
    def test_linear_scan_sorted(self):
        self.assertEqual(linear_scan([1,2,3,4,5]), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan([]), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan(()), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan(''), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan([1]), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan('a'), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan([1,2]), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan([1,2,3]), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan([1,2,3,4]), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan([69] * 69), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan(range(100000)), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan(range(32486, 92347, 13)), EdgeCase.AlreadySorted)
        self.assertEqual(linear_scan('abcde'), EdgeCase.AlreadySorted)
    
    def test_linear_scan_reverse_sorted(self):
        self.assertEqual(linear_scan([5,4,3,2,1]), EdgeCase.ReverseSorted)
        self.assertEqual(linear_scan([2,1]), EdgeCase.ReverseSorted)
        self.assertEqual(linear_scan([3,2,1]), EdgeCase.ReverseSorted)
        self.assertEqual(linear_scan([4,3,2,1]), EdgeCase.ReverseSorted)
        self.assertEqual(linear_scan(reversed(range(100000))), EdgeCase.ReverseSorted)
        self.assertEqual(linear_scan('zyxcba'), EdgeCase.ReverseSorted)
        self.assertEqual(
            linear_scan(['zzyzx', 'zoology', 'zebra', 'zany']),
            EdgeCase.ReverseSorted
        )
    
    def test_linear_scan_few_elements_out_of_order(self):
        import random
        
        _list = list(range(5))
        
        for _ in range(100):
            random.shuffle(_list)
            if list(range(5)) == _list:
                continue
            if list(reversed(range(5))) == _list:
                continue
            self.assertEqual(linear_scan(_list), EdgeCase.MostlySorted)
        
        _list_2 = [1,3,4,6,7,8,9,10,11,5,12,13,14,15,2]
        
        self.assertEqual(linear_scan(_list_2), EdgeCase.MostlySorted)
        
        self.assertEqual(linear_scan([1, 3, 2]), EdgeCase.MostlySorted)
        
        almost_alphabet = 'abcdeghjiklmnoprstquvrwxyz'
        
        self.assertEqual(linear_scan(almost_alphabet), EdgeCase.MostlySorted)
    
    def test_linear_scan_no_edge_case(self):
        import random
        _list = list(range(100000))
        
        # if this test ever fails, buy a lottery ticket.
        for _ in range(100):
            random.shuffle(_list)
            self.assertIsNone(linear_scan(_list))

class TestReverseList(unittest.TestCase):
    def test_edge_cases(self):
        __list = []
        reverse_list(__list)
        self.assertEqual(__list, [])
        
        a = object()
        __list = [a]
        reverse_list(__list)
        self.assertIs(__list[0], a)
        
        b = object()
        __list.append(b)
        reverse_list(__list)
        self.assertIs(__list[0], b)
        self.assertIs(__list[1], a)
    
    def test_reverse_list(self):
        __list = [1, 2, 3, 4, 5, 6, 7, 8]
        
        reverse_list(__list)
        
        self.assertEqual(__list, [8, 7, 6, 5, 4, 3, 2, 1])
        
        reverse_list(__list)
        
        self.assertEqual(__list, [1, 2, 3, 4, 5, 6, 7, 8])


class TestInsertionsort(unittest.TestCase):
    def test_edge_cases(self):
        __list = []
        insertionsort(__list)
        self.assertEqual(__list, [])
        
        a = object()
        __list = [a]
        # NOTE: technically, this should be a TypeError, since there is no guarantee
        # that the list is sortable. However, we can say that this is just a special
        # test for the single element case.
        insertionsort(__list) # type: ignore
        self.assertIs(__list[0], a)
    
    def test_insertionsort(self):
        import random
        
        sorted_list = list(range(16))
        *__list, = range(16)
        
        for _ in range(1000):
            random.shuffle(__list)
            with self.subTest(f"Testing with list: {__list}"):
                insertionsort(__list)
                self.assertEqual(__list, sorted_list)

class TestMergesort(unittest.TestCase):
    def test_small_lists(self):
        __list = []
        mergesort(__list)
        self.assertEqual(__list, [])
        
        a = object()
        __list = [a]
        mergesort(__list) # type: ignore
        self.assertIs(__list[0], a)
    
    def test_mergesort_random(self):
        import random
        
        random.seed(0)
        
        test_list_len = 128
        
        sorted_list = list(range(test_list_len))
        *__list, = range(test_list_len)
        
        for _ in range(1000):
            random.shuffle(__list)
            with self.subTest(f"Testing with list: {__list}"):
                _algs = mergesort(__list)
                self.assertEqual(__list, sorted_list)
                self.assertEqual(_algs, {"mergesort", "insertionsort"})
    
    def test_mergesort_already_sorted(self):
        import time
        
        big_list_size = 100000
        
        __list = list(range(big_list_size))
        
        start = time.perf_counter()
        _algs = mergesort(__list)
        end = time.perf_counter()
        
        self.assertEqual(__list, list(range(big_list_size))) # sanity check
        self.assertEqual(_algs, {"mergesort", "insertionsort"})
        
        # this should be fast since it is already sorted, and the algorithm
        # should be adaptive and not bother with merging sorted sublists
        
        # TODO: this might fail on a slow computer, but i dont rlly care
        # considering that on my pc, sorting a random list of 100000 elements
        # takes around 3 seconds.
        self.assertLess(end - start, 1.0)

class TestQuicksort(unittest.TestCase):
    def test_small_lists(self):
        __list = []
        _algs = quicksort(__list)
        self.assertEqual(__list, [])
        self.assertEqual(_algs, set())
        
        a = object()
        __list = [a]
        _algs = quicksort(__list) # type: ignore
        self.assertIs(__list[0], a)
        self.assertEqual(_algs, set())
    
    def test_quicksort_random(self):
        import random
        
        random.seed(0) # get deterministic results
        # this also guarantees that it will not need to use mergesort
        
        test_list_len = 32
        
        sorted_list = list(range(test_list_len))
        *__list, = range(test_list_len)
        
        for _ in range(1000):
            random.shuffle(__list)
            with self.subTest(f"Testing with list: {__list}"):
                _algs = quicksort(__list)
                self.assertEqual(__list, sorted_list)
                self.assertEqual(_algs, {'quicksort', 'insertionsort'})
    
    def test_quicksort_adverserial(self):
        """Test quicksort with a list that is almost reverse sorted.
        
        This is an adverserial test, with the list being almost reverse sorted,
        so mergesort will end up being used instead in this implementation.
        (Since the pivot is always the last element)
        """
        import random
        
        random.seed(0) # get deterministic results
        
        # NOTE: the reason why the length is 200 is because smaller lists have a greater
        # chance of being sorted with insertionsort without falling into the mergesort
        # case, which is not what we want.
        test_list_len = 200
        
        for _ in range(1000):
            # almost reverse sort the list, but with a few random swaps
            __list = list(reversed(range(test_list_len)))
            
            for _ in range(10):
                i = random.randrange(test_list_len)
                j = random.randrange(test_list_len)
                __list[i], __list[j] = __list[j], __list[i]
            
            with self.subTest(f"Testing with list: {__list}"):
                _algs = quicksort(__list)
                self.assertEqual(__list, list(range(test_list_len)))
                self.assertEqual(_algs, {'quicksort', 'mergesort', 'insertionsort'})

class TestMagicsort(unittest.TestCase):
    def test_small_lists(self):
        __list = []
        _algs = magic_sort(__list)
        self.assertEqual(__list, [])
        self.assertEqual(_algs, set())
        
        a = object()
        __list = [a]
        _algs = magic_sort(__list) # type: ignore
        self.assertIs(__list[0], a)
        self.assertEqual(_algs, set())
    
    def test_magicsort_random(self):
        import random
        
        random.seed(0)
        
        test_list_len = 32
        
        sorted_list = list(range(test_list_len))
        __list = list(range(test_list_len))
        
        for _ in range(1000):
            random.shuffle(__list)
            with self.subTest(f"Testing with list: {__list}"):
                _algs = magic_sort(__list)
                self.assertEqual(__list, sorted_list)
                self.assertEqual(_algs, {'quicksort', 'insertionsort'})
    
    def test_magicsort_adverserial(self):
        import random
        
        random.seed(0)
        
        test_list_len = 200
        
        for _ in range(1000):
            __list = list(reversed(range(test_list_len)))
            
            for _ in range(10):
                i = random.randrange(test_list_len)
                j = random.randrange(test_list_len)
                __list[i], __list[j] = __list[j], __list[i]
            
            with self.subTest(f"Testing with list: {__list}"):
                _algs = magic_sort(__list)
                self.assertEqual(__list, list(range(test_list_len)))
                self.assertEqual(_algs, {'quicksort', 'mergesort', 'insertionsort'})
    
    def test_magicsort_already_sorted(self):
        __list = list(range(100000))
        
        _algs = magic_sort(__list)
        
        self.assertEqual(__list, list(range(100000)))
        self.assertEqual(_algs, set())
    
    def test_magicsort_reversed(self):
        import string
        
        __zyx = list(string.ascii_lowercase[::-1])
        
        _algs = magic_sort(__zyx)
        
        self.assertEqual(''.join(__zyx), string.ascii_lowercase)
        self.assertEqual(_algs, {'reverse_list'})
        
        __list = list(reversed(range(100000)))
        
        _algs = magic_sort(__list)
        
        self.assertEqual(__list, list(range(100000)))
        self.assertEqual(_algs, {'reverse_list'})
    
    def test_magicsort_almost_sorted(self):
        import random
        
        random.seed(0)
        
        test_list_len = 200
        
        for _ in range(1000):
            __list = list(range(test_list_len))
            
            for _ in range(2):
                i = random.randrange(test_list_len)
                j = random.randrange(test_list_len)
                __list[i], __list[j] = __list[j], __list[i]
            
            with self.subTest(f"Testing with list: {__list}"):
                _algs = magic_sort(__list)
                self.assertEqual(__list, list(range(test_list_len)))
                self.assertEqual(_algs, {'insertionsort'})


unittest.main()
