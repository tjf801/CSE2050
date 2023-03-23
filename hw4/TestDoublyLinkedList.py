from DoublyLinkedList import DoublyLinkedList as DLL
import unittest

# Basic tests are provided for you, but you need to implement the last 3 unittests
class testDLL(unittest.TestCase):
    def test_addfirst_removefirst(self):
        'adds items to front, then removes from front'
        dll = DLL()
        n = 100

        for _ in range(5): # repeat a few times to make sure removing last item doesn't break anything
            for i in range(n):
                self.assertEqual(len(dll), i)
                dll.add_first(i)

            for i in range(n):
                self.assertEqual(len(dll), n-i)
                self.assertEqual(dll.remove_first(), n-1-i)

            with self.assertRaises(RuntimeError):
                dll.remove_first()

    def test_addlast_removelast(self):
        'adds items to end, then removes from end'
        dll = DLL()
        n = 100

        for _ in range(5): # repeat a few times to make sure removing last item doesn't break anything
            for i in range(n):
                self.assertEqual(len(dll), i)
                dll.add_last(i)

            for i in range(n):
                self.assertEqual(len(dll), n-i)
                self.assertEqual(dll.remove_last(), n-1-i)

            with self.assertRaises(RuntimeError):
                dll.remove_last()

    def test_add_remove_mix(self):
        'various add/remove patterns'
        dll = DLL()
        n = 100

        # addfirst/removelast
        for _ in range(5): # repeat a few times to make sure removing final node doesn't break anything
            for i in range(n):
                self.assertEqual(len(dll), i)
                dll.add_first(i)

            for i in range(n):
                self.assertEqual(len(dll), n-i)
                self.assertEqual(dll.remove_last(), i)

        # addlast/removefirst
        for _ in range(5): # repeat a few times to make sure removing final node doesn't break anything
            for i in range(n):
                self.assertEqual(len(dll), i)
                dll.add_last(i)

            for i in range(n):
                self.assertEqual(len(dll), n-i)
                self.assertEqual(dll.remove_first(), i)

        # mix of first/last
        for _ in range(5): # repeat a few times to make sure removing final node doesn't break anything
            for i in range(n):
                self.assertEqual(len(dll), i)
                if i%2: dll.add_last(i) # odd numbers - add last
                else: dll.add_first(i)  # even numbers - add first

            for i in range(n):
                self.assertEqual(len(dll), n-i)
                if i%2: self.assertEqual(dll.remove_last(), n-i) # odd numbers: remove last
                else: self.assertEqual(dll.remove_first(), n-2-i) # even numbers: remove first

    def test_contains(self):
        "test contains method"
        L = DLL()
        
        for i in range(10):
            L.add_first(i)
        
        for i in range(10):
            self.assertTrue(i in L)
        
        self.assertTrue(10 not in L)
        L.remove_first()
        self.assertTrue(9 not in L)
        L.add_last(10)
        self.assertTrue(10 in L)
    
    def test_neighbors(self):
        "test neighbors method"
        L = DLL()
        
        for i in range(10):
            L.add_first(i)
        
        for i in range(1, 9):
            self.assertEqual(L.neighbors(i), (i+1, i-1))
        
        self.assertEqual(L.neighbors(0), (1, None))
        self.assertEqual(L.neighbors(9), (None, 8))
    
    def test_remove_item(self):
        'test remove_node method'
        L = DLL()
        
        for i in range(10):
            L.add_first(i)
        
        L.remove_node(5)
        self.assertTrue(5 not in L)
        
        L.remove_node(0)
        self.assertTrue(0 not in L)
        
        for i in range(1, 10):
            if i != 5:
                self.assertTrue(i in L)
        
        L.remove_node(9)
        self.assertTrue(9 not in L)
        
        for i in (1, 2, 3, 4, 6, 7, 8):
            self.assertTrue(i in L)
            L.remove_node(i)
        
        with self.assertRaises(ValueError):
            L.remove_node(0)

unittest.main()
