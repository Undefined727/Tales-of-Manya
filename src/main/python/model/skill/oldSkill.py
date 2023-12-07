from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from src.main.python.model.skill.SkillTag import SkillTag
from src.main.python.model.effect.Effect import Effect
from src.main.python.model.database.DatabaseModels import engine, DBSkill
from src.main.python.util.IllegalArgumentException import IllegalArgumentException

class Skill:
    id : str
    name : str
    mana_cost : int
    ## tags:list[SkillTag] ##
    ## effects:list[Effect] ##

    def __init__(self, name : str = "placeholder name", mana_cost : int = 0):
        self.setID(self.generateID())
        self.setID()
        self.setName(name)
        self.setManaCost(mana_cost)
        self.tags : list[SkillTag] = list()
        self.effects : list[Effect] = list()

    ## Getters ##
    def getID(self) -> str:
        return self.id

    def getName(self) -> str:
        return self.name

    def getManaCost(self) -> int:
        return self.mana_cost

    def getTags(self) -> list[ SkillTag ]:
        return self.tags

    ## Setters ##
    def setID(self, new_id : str):
        self.id = new_id

    def setName(self, new_name : str):
        self.name = new_name

    def setManaCost(self, new_cost : int):
        self.mana_cost = new_cost

    ## Misc ##
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

    def generateID() -> int:
        with Session(engine) as session:
            query = session.query(func.max(DBSkill.id)).all()
            max_id = query[0][0]
            return max_id + 1

    ## Python built ins ##
    def __eq__(self, object) -> bool:
        if (type(self) != type(object)):
            return False
        if (self.getName() != object.getName()):
            return False
        return True

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, mana cost: {self.mana_cost}, tags: {self.tags}"