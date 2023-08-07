from src.main.python.model.character.DynamicStat import DynamicStat
from src.main.python.util.IllegalArgumentException import IllegalArgumentException
from src.main.python.util.InvalidOperationException import InvalidOperationException

class ExperienceManager:
    level:int
    max_level:int
    formula:function
    experience:DynamicStat

    BASE_FORMULA = lambda level: level * 100

    def __init__(self, max_level = 100, experience_formula = BASE_FORMULA):
        self.level = 1
        self.max_level = max_level
        self.formula = experience_formula
        max_xp = self.formula(self.level)
        self.experience = DynamicStat(max_xp)

    def earnXP(self, value):
        if (value < 0):
            raise IllegalArgumentException("Cannot increase by a negative amount")
        new_amount = self.experience.getCurrentValue() + value
        if (new_amount > self.experience.getMaxValue()):
            new_amount -= self.experience.getMaxValue()
            self.levelUp(new_amount)
        else:
            self.experience.setCurrentValue(new_amount)

    def levelUp(self, carry_over_experience = 0):
        self.experience.setCurrentValue(0)
        self.level += 1
        new_max_xp = self.formula(self.level)
        self.experience.setMaxValue(new_max_xp)
        self.earnXP(carry_over_experience)

