from sqlalchemy import create_engine
from model.skill.SkillTag import SkillTag
from model.effect.Effect import Effect
from util.IllegalArgumentException import IllegalArgumentException
import uuid

class Skill:
    id:str
    name:str
    manaCost:int
    ## tags:list[SkillTag] ##
    ## effects:list[Effect] ##

    def __init__(self, name:str = "placeholder name", manaCost:int = 0):
        self.id = uuid.uuid5(uuid.NAMESPACE_DNS, 'basedstudios.dev')
        self.name = name
        self.manaCost = manaCost
        self.tags:list[SkillTag] = list()
        self.effects:list[Effect] = list()


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