import unittest, time
from Lab4 import LinkedList


def time_f(func, *args, n_repeats=1):
    'times func(*args) n_repeats times, returns total time'
    start = time.time()
    
    for _ in range(n_repeats):
        func(*args)
    
    end = time.time()

    return end-start

class TestLinkedList(unittest.TestCase):
    'Test cases specific to LinkedList Class'

    def test_1_init(self):
        'initialize with or without a collection'
        # Initialize empty LL
        ll1 = LinkedList()
        self.assertEqual(len(ll1), 0)

        # Initialize an LL w/ 10 items
        ll2 = LinkedList(range(10))
        self.assertEqual(len(ll2), 10)

        L = [item for item in ll2]
        self.assertEqual(L, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_2_add_remove_first(self):
        'adds and removes 100 items to/from beginning of LL'
        ll1 = LinkedList()
        n = 100

        # repeat a few times to make sure removing the last item doesn't break
        # anything
        for _ in range(10):

            for i in range(n):
                self.assertEqual(len(ll1), i)
                ll1.add_first(i)

            for i in range(n):
                self.assertEqual(len(ll1), n-i)
                self.assertEqual(ll1.remove_first(), n-1-i)

    def test_3_add_remove_varied(self):
        'variety of add_first/add_last/remove_first patterns'
        ll1 = LinkedList()
        n = 100

        ##### add_first/remove_first #####
        for i in range(n):
            self.assertEqual(len(ll1), i)
            ll1.add_first(i)
        # ll1.head ->99->98...(96 items omitted)...->1->0->None

        for i in range(n):
            self.assertEqual(len(ll1), n-i)
            self.assertEqual(ll1.remove_first(), n-1-i)

        ##### add_last/remove_first #####
        for i in range(n):
            self.assertEqual(len(ll1), i)
            ll1.add_last(i)
        # ll1.head ->0->1->...(96 items omitted)...->98->99->None

        for i in range(n):
            self.assertEqual(len(ll1), n-i)
            self.assertEqual(ll1.remove_first(), i)

        # repeat a few times to make sure removing the last item doesn't break
        # anything
        for _ in range(10):

            for i in range(n):
                self.assertEqual(len(ll1), i)
                ll1.add_first(i)

            for i in range(n):
                self.assertEqual(len(ll1), n-i)
                self.assertEqual(ll1.remove_first(), n-1-i)

    def test_4_remove_empty_exception(self):
        'remove from empty'
        ll1 = LinkedList()
        with self.assertRaises(RuntimeError):
            ll1.remove_first()


    def test_5_timing_add_first(self):
        'add_first() 100k times in less than 250 ms'
        n = int(1E5)    # number of items to add
        TMAX = 250     # expected max time in ms

        ll1 = LinkedList(range(n))
        t_func = 1000*time_f(LinkedList.add_first, *(ll1, 0), n_repeats=n)
        print(f"t_add_first = {t_func:.2f} ms")
        self.assertLess(t_func, TMAX, f"{t_func:.2f} ms is longer than the expected upper limit of {TMAX} ms")

    def test_6_timing_add_last(self):
        'add_last() 100k times in less than 250 ms'
        n = int(1E5)    # number of items to add
        TMAX = 250     # expected max time in ms

        ll1 = LinkedList(range(n))
        t_func = 1000*time_f(LinkedList.add_last, *(ll1, 0), n_repeats=n)
        print(f"t_add_last = {t_func:.2f} ms")
        self.assertLess(t_func, TMAX, f"{t_func:.2f} ms is longer than the expected upper limit of {TMAX} ms")

    def test_7_timing_remove_first(self):
        'remove_first() 100k times in less than 250 ms'
        n = int(1E5)    # number of items to add
        TMAX = 250     # expected max time in ms

        ll1 = LinkedList(range(n))
        t_remove_last = 1000*time_f(LinkedList.remove_first, *(ll1,), n_repeats=n)
        print(f"t_remove_last = {t_remove_last:.2f} ms")
        self.assertLess(t_remove_last, TMAX, f"{t_remove_last:.2f} ms is longer than the expected upper limit of {TMAX} ms")

unittest.main()