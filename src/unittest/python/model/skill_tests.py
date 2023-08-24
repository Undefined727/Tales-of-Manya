import unittest
import os
import sys
sys.path.append(os.path.abspath("."))
from src.main.python.model.skill.Skill import Skill
from src.main.python.model.skill.SkillTag import SkillTag
from src.main.python.model.effect.Effect import Effect
from src.main.python.model.effect.EffectType import EffectType

class Test_Skill(unittest.TestCase):
    def test_default_values(self):
        skill = Skill()
        self.assertEqual(skill.name, "placeholder name")
        self.assertEqual(skill.manaCost, 0)
        self.assertEqual(skill.tags, list())
        self.assertEqual(skill.effects, list())

    def test_addTag(self):
        skill1 = Skill()
        skill1.addTag(SkillTag.AIR)

        skill2 = Skill("a", 0)
        skill2.tags.append(SkillTag.AIR)

        a_list = [SkillTag.AIR]
        skill3 = Skill()
        skill3.tags = a_list

        self.assertEqual(skill1.tags,skill2.tags)
        self.assertEqual(skill1.tags,skill3.tags)

    def test_addEffect(self):
        skill1 = Skill()
        skill2 = Skill("a", 0)

        effect = Effect("test", EffectType.ATTACK_FLAT, 10, -1)
        self.assertEqual(skill1.effects,skill2.effects)
        skill1.addEffect(effect)
        self.assertNotEqual(skill1.effects,skill2.effects)
        skill2.addEffect(effect)
        self.assertEqual(skill1.effects,skill2.effects)

    def test_removeTag(self):
        skill1 = Skill()
        skill1.addTag(SkillTag.AIR)

        skill2 = Skill("a", 0)
        skill2.tags.append(SkillTag.AIR)

        self.assertEqual(skill1.tags,skill2.tags)
        skill2.removeTag(SkillTag.AIR)
        self.assertNotEqual(skill1.tags,skill2.tags)

    def test_removeEffect(self):
        skill1 = Skill()
        skill2 = Skill("a", 0)

        effect = Effect("test", EffectType.ATTACK_FLAT, 10, -1)
        skill1.addEffect(effect)
        skill2.addEffect(effect)
        skill1.removeEffect(effect)
        self.assertNotEqual(skill1.effects,skill2.effects)

if __name__ == '__main__':
    unittest.main()