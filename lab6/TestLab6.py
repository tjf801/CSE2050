import unittest, random, typing

if typing.TYPE_CHECKING:
    from lab6.lab6 import OrderedList as OL
else:
    from lab6 import OrderedList as OL

random.seed(652) # Fix the random seed so when a test fails, it fails the same way every time

def is_sorted(L):
    """Check that a list is sorted"""
    return not any(L[i] > L[i+1] for i in range(len(L)-1))
    # Requires:
    #   * OL.__getitem__() (called w/ L[i])
    #   * OL.__len__()

class TestOrderedList(unittest.TestCase):
    def test_init(self):
        """Tests initialization w/ no items, sorted list, and unsorted list."""
        # Requires:
        #   * OL.__init__()
        #   * OL.__len__()

        # no items
        ol1 = OL()
        self.assertEqual(len(ol1), 0)

        # sorted list
        ol2 = OL([1, 2, 3, 4, 5])
        self.assertEqual(len(ol2), 5)
        self.assertTrue(is_sorted(ol2))

        # unsorted list
        ol3 = OL([1, 5, 2, 4, 3])
        self.assertEqual(len(ol3), 5)
        self.assertTrue(is_sorted(ol3))

    def test_add(self):
        """tests that list stays sorted while adding items"""
        # Requires:
        #   * OL.__init__()
        #   * OL.__len__()
        #   * OL.__contains()
        #   * OL.__iter__()
        #   * OL.add()

        n = 1000 # Note how we parameterize the length. Reduce this to a small number (e.g. 5)
                # when debugging, then scale it up when everything appears to be working to
                # thoroughly test our algorithm.

        # create empty OrderedList and unsorted list to compare
        ol1 = OL()
        unsorted = []

        for i in range(n):
            # generate random int, ensure it's not already in OL if this is the first time seeing it
            new_int = random.randint(0, 100)
            if not new_int in unsorted:
                self.assertNotIn(new_int, ol1)

            # add to list
            ol1.add(new_int)
            self.assertTrue(is_sorted(ol1)) # sorted
            self.assertIn(new_int, ol1)     # contains
            self.assertEqual(len(ol1), i+1) # length

            # add item to unordered list, make sure count is the same in both collections
            unsorted.append(new_int)
            self.assertCountEqual(ol1, unsorted) # Requires OrderedList.__iter__()

    def test_remove(self):
        """Ensures items are removed correctly (OL stays sorted, count is correct)"""
        # Requires:
        #   * OL.__init__()
        #   * OL.__len__()
        #   * OL.__contains()
        #   * OL.__iter__()
        #   * OL.__getitem__()
        #   * OL.add()
        #   * OL.remove()


        n = 1000

        # create empty OrderedList and unsorted list to compare
        ol1 = OL()
        unsorted = []
        for i in range(n):
            new_int = random.randint(0, 100)
            ol1.add(new_int)
            unsorted.append(new_int)


        for i in range(n):     
            # pick a random item to remove
            item = random.choice(ol1)

            # remove item
            ol1.remove(item)
            unsorted.remove(item)

            self.assertTrue(is_sorted(ol1))     # sorted

            if not item in unsorted:            # contains
                self.assertFalse(item in ol1)
                with self.assertRaises(ValueError):
                    ol1.remove(item)
            else:
                self.assertIn(item, ol1)

            self.assertEqual(len(ol1), n-i-1)   # length

            # remove item from unordered list, make sure count is the same in both collections
            self.assertCountEqual(ol1, unsorted)

unittest.main()