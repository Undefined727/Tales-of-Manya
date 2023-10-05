from sqlalchemy import create_engine
from src.main.python.model.skill.SkillTag import SkillTag
from src.main.python.model.effect.Effect import Effect
from src.main.python.util.IllegalArgumentException import IllegalArgumentException
from src.main.python.util.IDHandler import IDHandler

class Skill:
    id : str
    name : str
    mana_cost : int
    ## tags:list[SkillTag] ##
    ## effects:list[Effect] ##

    def __init__(self, name : str = "placeholder name", mana_cost : int = 0, id : str = None):
        if id is None: self.setID(IDHandler.generateID(Skill))
        else: self.setID(id)
        self.setID(IDHandler.generateID(Skill))
        self.setName(name)
        self.setManaCost(mana_cost)
        self.tags : list[SkillTag] = list()
        self.effects : list[Effect] = list()

    def getID(self) -> str:
        return self.id

    def getName(self) -> str:
        return self.name

    def getManaCost(self) -> int:
        return self.mana_cost
    
    def getTags(self) -> list[ SkillTag ]:
        return self.tags

    def setID(self, new_id : str):
        self.id = new_id

    def setName(self, new_name : str):
        self.name = new_name

    def setManaCost(self, new_cost : int):
        self.mana_cost = new_cost

    def addTag(self, tag : SkillTag):
        if (tag not in self.tags):
            self.tags.append(tag)
        else:
            raise IllegalArgumentException("This skill already has that tag")

    def addEffect(self, effect : Effect):
        if (effect not in self.effects):
            self.effects.append(effect)
        else:
            raise IllegalArgumentException("This skill already has that effect")

    def removeTag(self, tag : SkillTag):
        self.tags.remove(tag)

    def removeEffect(self, effect : Effect):
        self.effects.remove(effect)