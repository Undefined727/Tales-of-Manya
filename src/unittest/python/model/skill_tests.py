import unittest
import os
import sys
sys.path.append(os.path.abspath("."))
from src.main.python.model.skill.Skill import Skill

class Test_Skill(unittest.TestCase):
    def test_default_values(self):
        skill = Skill()
        self.assertEqual(skill.name, "placeholder name")
        self.assertEqual(skill.manaCost, 0)
        self.assertEqual(skill.tags, [])
        self.assertEqual(skill.effects, [])

if __name__ == '__main__':
    unittest.main()