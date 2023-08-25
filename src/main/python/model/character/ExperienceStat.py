from src.main.python.util.Messages import Error
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

    def getXP(self) -> int:
        return self.experience.getCurrentValue()

    def getXPToNextLevel(self) -> int:
        return self.experience.getMaxValue()

    def getFormula(self) -> function:
        return self.formula

    def getLevel(self) -> int:
        return self.level

    def getMaxLevel(self) -> int:
        return self.max_level

    def setXP(self, new_value : int):
        self.experience.setCurrentValue(new_value)

    def setFormula(self, new_formula : function):
        self.formula = new_formula

    def setLevel(self, new_value : int):
        if new_value < 1: raise IllegalArgumentException(Error.CANNOT_BE_BELOW_ONE)
        self.level = new_value
        self.experience.setMaxValue(self.formula(new_value))
        if self.getXP() > self.getXPToNextLevel(): self.setXPPercentage(.99)

    def earnXP(self, value):
        if (value < 0): raise IllegalArgumentException(Error.CANNOT_BE_NEGATIVE)
        new_amount = self.experience.getCurrentValue() + value
        if (new_amount > self.experience.getMaxValue()):
            new_amount -= self.experience.getMaxValue()
            self.levelUp(new_amount)
        self.experience.setCurrentValue(new_amount)

    def levelUp(self, carry_over_experience = 0):
        self.experience.setCurrentValue(0)
        self.level += 1
        new_max_xp = self.formula(self.level)
        self.experience.setMaxValue(new_max_xp)
        self.earnXP(carry_over_experience)

