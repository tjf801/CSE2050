# ruff: noqa: ANN201
from __future__ import annotations

import typing
import unittest

if typing.TYPE_CHECKING:
    from hw8.hashmap import CustomHashMap
else:
    from hashmap import CustomHashMap


class TestCustomHashMap(unittest.TestCase):
    # NOTE: I made each of these methods short enough and with descriptive enough names
    # that if i really need a doctring for THESE, u might want to get ur eyes checked
    
    def test_basic_initialization(self):
        hashmap = CustomHashMap()
        
		# NOTE: this is the only place where we use the private variables
        self.assertEqual(hashmap._capacity, CustomHashMap._INITIAL_SIZE) # type: ignore
        self.assertEqual(hashmap._used, 0) # type: ignore
        self.assertEqual(hashmap._table, [None] * CustomHashMap._INITIAL_SIZE) # type: ignore # noqa: E501
    
    def test_len_zero_after_initialization(self):
        hashmap = CustomHashMap()
        self.assertEqual(len(hashmap), 0)
    
    def test_kwarg_init_and_len(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        self.assertEqual(len(hashmap), 3)
    
    def test_kwarg_type_checking(self):
        if typing.TYPE_CHECKING:
            hashmap_str_str = CustomHashMap(key1="value1")
            typing.reveal_type(hashmap_str_str)
            hashmap_str_str: CustomHashMap[str, str] = hashmap_str_str
    
    
    def test_value_lookup(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        self.assertEqual(hashmap["key1"], "value1")
        self.assertEqual(hashmap["key2"], "value2")
        self.assertEqual(hashmap["key3"], "value3")
    
    def test_value_lookup_keyerror(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        with self.assertRaises(KeyError):
            hashmap["key4"]
    
    def test_value_lookup_type_checking(self):
        if typing.TYPE_CHECKING:
            hashmap: CustomHashMap[str, str] = CustomHashMap(key1="value1")
            value = hashmap["key1"]
            typing.reveal_type(value)
            value: str = value
    
    
    def test_value_assignment(self):
        hashmap = CustomHashMap()
        hashmap["key1"] = "value1"
        hashmap["key2"] = "value2"
        hashmap["key3"] = "value3"
        self.assertEqual(hashmap["key1"], "value1")
        self.assertEqual(hashmap["key2"], "value2")
        self.assertEqual(hashmap["key3"], "value3")
        self.assertEqual(len(hashmap), 3)
    
    def test_value_assignment_overwrite(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        hashmap["key1"] = "value4"
        hashmap["key2"] = "value5"
        hashmap["key3"] = "value6"
        self.assertEqual(hashmap["key1"], "value4")
        self.assertEqual(hashmap["key2"], "value5")
        self.assertEqual(hashmap["key3"], "value6")
        self.assertEqual(len(hashmap), 3)
    
    def test_value_assignment_type_checking(self):
        if typing.TYPE_CHECKING:
            hashmap = CustomHashMap()
            hashmap["key1"] = 1
            hashmap["key2"] = 2
            hashmap["key3"] = 3
            typing.reveal_type(hashmap)
            _: CustomHashMap[str, int] = hashmap
    
    
    def test_value_deletion(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        del hashmap["key1"]
        del hashmap["key2"]
        del hashmap["key3"]
        self.assertEqual(len(hashmap), 0)
    
    def test_value_deletion_keyerror(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        with self.assertRaises(KeyError):
            del hashmap["key4"]
    
    
    def test_init_with_dict(self):
        hashmap = CustomHashMap({
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
        })
        self.assertEqual(hashmap["one"], 1)
        self.assertEqual(hashmap["two"], 2)
        self.assertEqual(hashmap["three"], 3)
        self.assertEqual(hashmap["four"], 4)
    
    def test_init_with_dict_type_checking(self):
        if typing.TYPE_CHECKING:
            hashmap: CustomHashMap[str, int] = CustomHashMap({
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
            })
            typing.reveal_type(hashmap)
    
    def test_init_with_dict_and_kwargs(self):
        hashmap = CustomHashMap({
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
        }, five=5, six=6)
        self.assertEqual(hashmap["one"], 1)
        self.assertEqual(hashmap["two"], 2)
        self.assertEqual(hashmap["three"], 3)
        self.assertEqual(hashmap["four"], 4)
        self.assertEqual(hashmap["five"], 5)
        self.assertEqual(hashmap["six"], 6)
    
    def test_init_with_dict_and_kwargs_type_checking(self):
        if typing.TYPE_CHECKING:
            hashmap = CustomHashMap({
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
            }, five=5, six=6)
            typing.reveal_type(hashmap)
            _: CustomHashMap[str, int] = hashmap
    
    
    def test_contains(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        self.assertIn("key1", hashmap)
        self.assertIn("key2", hashmap)
        self.assertIn("key3", hashmap)
        self.assertNotIn("key4", hashmap)
    
    def test_contains_edge_cases(self):
        hashmap = CustomHashMap()
        
        self.assertNotIn("key1", hashmap)
        hashmap["key1"] = "value1"
        self.assertIn("key1", hashmap)
        del hashmap["key1"]
        self.assertNotIn("key1", hashmap)
        
        self.assertNotIn(None, hashmap)
        hashmap[None] = "value1"
        self.assertEqual(hashmap[None], "value1")
        self.assertIn(None, hashmap)
        del hashmap[None]
        self.assertNotIn(None, hashmap)
        
        self.assertNotIn("key1", hashmap)
        hashmap["key1"] = None
        self.assertIs(hashmap["key1"], None)
        self.assertIn("key1", hashmap)
        del hashmap["key1"]
        self.assertNotIn("key1", hashmap)
        
        # looking at this gives me brain cancer
        self.assertNotIn(None, hashmap)
        hashmap[None] = None
        self.assertIs(hashmap[None], None)
        self.assertIn(None, hashmap)
        del hashmap[None]
        self.assertNotIn(None, hashmap)
    
    def test_contains_with_ellipsis(self):
        hashmap = CustomHashMap()
        
        for i in range(3):
            hashmap[i] = f"value{i}"
            del hashmap[i]
        
        self.assertNotIn(..., hashmap)
        hashmap[...] = None
        self.assertIs(hashmap[...], None)
        self.assertIn(..., hashmap)
        del hashmap[...]
        self.assertNotIn(..., hashmap)
        
        self.assertNotIn(None, hashmap)
        hashmap[None] = ...
        self.assertIs(hashmap[None], ...)
        self.assertIn(None, hashmap)
        del hashmap[None]
        self.assertNotIn(None, hashmap)
    
    
    def test_iter(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        self.assertEqual(set(hashmap), {"key1", "key2", "key3"})
    
    def test_iter_items(self):
        hashmap = CustomHashMap(key1="value1", key2="value2", key3="value3")
        # use set since order is not guaranteed
        self.assertEqual(set(hashmap.items()), {
            ("key1", "value1"),
            ("key2", "value2"),
            ("key3", "value3")
        })

if __name__ == "__main__":
    unittest.main()
