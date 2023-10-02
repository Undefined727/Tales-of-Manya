import os
import sys
import unittest
from unittest import TestCase
sys.path.append(os.path.abspath("."))
from src.main.python.model.character.Inventory import Inventory
from src.main.python.model.item.Item import Item

class InventoryTests(TestCase):
    # def test_default_values(self):
    #     # arbitrary_id = "9fb3ee4f-38d4-45a5-8198-c0365727529b"
    #     # inv = Inventory(arbitrary_id)
    #     # self.assertEqual(inv.parent_id, arbitrary_id)
    #     # self.assertEqual(inv.space, 28)
    #     # self.assertEqual(inv.slots, dict())
    #     pass

    # def test_proper_instantiation(self):
    #     arbitrary_id1 = "9fb3ee4f-38d4-45a5-8198-c0365727529b"
    #     arbitrary_id2 = "c0ae4696-50c2-49a5-a300-543f0383cc5b"
    #     inv1 = Inventory(arbitrary_id1)
    #     inv2 = Inventory(arbitrary_id2)
    #     inv1.slots["test"] = 1
    #     self.assertEqual(inv1.slots, {"test":1})
    #     self.assertEqual(inv2.slots, {})

    # def test_add_placeholder_item(self):
    #     # arbitrary_id = "9fb3ee4f-38d4-45a5-8198-c0365727529b"
    #     # inv = Inventory(arbitrary_id)
    #     # item = Item()
    #     # self.assertTrue(inv.addItem(item))
    #     # self.assertEqual(inv.slots[item],1)
    #     pass
    pass

if __name__ == '__main__':
    unittest.main()