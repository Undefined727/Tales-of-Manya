import os, sys
sys.path.append(os.path.abspath("."))
from src.main.python.model.character.Character import Character
from src.main.python.model.character.Skill import Skill
from src.main.python.model.item.Item import Item
from src.main.python.model.item.ItemSlotType import ItemSlotType
from src.main.python.model.item.ItemStatType import ItemStatType
from src.main.python.model.item.ItemTag import ItemTag
import src.main.python.model.effect.Effect as Effect
from src.main.python.model.effect.EffectType import EffectType
from src.main.python.model.effect.EffectTag import EffectTag
from src.main.python.model.player.Quest import Quest
from src.main.python.model.database.DatabaseModels import *
from src.main.python.util.IllegalArgumentException import IllegalArgumentException
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

class DBElementFactory:
    # TODO Missing method to test if the IDs are unique
    # TODO complete a few methods, finish relationships

    def __init__(self, path : str = "src/main/python/catgirl-dungeon.db", echo : bool = False):
        self.engine = create_engine(f"sqlite:///{path}", echo = echo)

    ## Getting from Database ##

    def fetchItem(self, name : str):
        connection = self.engine.connect()
        statement = select(DBItem).where(DBItem.name == name)
        row = connection.execute(statement).first()
        connection.close()
        if row is None: raise IllegalArgumentException("The item is not in the database")
        return self.buildItem(row)

    def fetchItemByID(self, item_id : str):
        connection = self.engine.connect()
        statement = select(DBItem).where(DBItem.id == item_id)
        row = connection.execute(statement).first()
        connection.close()
        if row is None: raise IllegalArgumentException("The item is not in the database")
        return self.buildItem(row)

    def buildItem(self, row) -> Item:
        # TODO Not handling tags and bonuses yet
        connection = self.engine.connect()
        statement = select(DBItemStat).where(DBItemStat.item == row.name)
        itemStatsData = connection.execute(statement)

        itemStats = {}
        for itemStat in itemStatsData:
            itemStats.update({ItemStatType[itemStat.stat]: int(itemStat.value)})

        item = Item(row.name,
                    ItemSlotType[row.type],
                    row.description,
                    row.image_path,
                    None,
                    itemStats,
                    None,
                    row.id)
        connection.close()
        return item
    
    def fetchSkill(self, id):
        if (id is None): return None
        connection = self.engine.connect()
        if type(id) == int:
            statement = select(DBSkill).where(DBSkill.id == id)
        else:
            statement = select(DBSkill).where(DBSkill.name == id)
        row = connection.execute(statement).first()
        if row is None: 
            connection.close()
            raise IllegalArgumentException("The item is not in the database")

        skill = Skill(row.name, row.description, row.character, row.element, row.affinity, row.manaCost, row.motionValue)

        connection.close()
        return skill

    def fetchCharacter(self, id):
        connection = self.engine.connect()
        if type(id) == int:
            statement = select(DBCharacter).where(DBCharacter.id == id)
        else:
            statement = select(DBCharacter).where(DBCharacter.name == id)
        row = connection.execute(statement).first()
        if row is None: 
            connection.close()
            raise IllegalArgumentException("The item is not in the database")
        
        character = Character(row.name, row.description,
                              row.brilliance, row.surge, row.blaze, row.passage, row.clockwork,
                              row.void, row.foundation, row.frost, row.flow, row.abundance,
                              row.basehealth, row.basemana, row.basedef, row.basespellpower, row.baseattack)

        character.skills = [self.fetchSkill("Attack")]
        character.skills.append(self.fetchSkill(row.skill1))
        character.skills.append(self.fetchSkill(row.skill2))
        character.skills.append(self.fetchSkill(row.skill3))
        character.skills.append(self.fetchSkill(row.skill4))

        character.setCurrentHP(character.health.max_value)
        connection.close()
        return character

    

    def buildEffect(self, row) -> Effect:
        effect = Effect(row.name,
                        EffectType[row.effect_type],
                        row.value,
                        row.duration,
                        None,
                        row.id)
        return effect
    
    ## Adding to Database ##

    def store(self, element):
        if type(element) is Item: self.pushItem(element)
        elif type(element) is Character: self.pushCharacter(element)
        elif type(element) is ItemSlotType: self.pushItemSlot(element)
        elif type(element) is Effect: self.pushEffect(element)
        elif type(element) is Quest: self.pushQuest(element)
        elif type(element) is Skill: self.pushSkill(element)
        else: raise IllegalArgumentException("Type not recognized")

    def add(self, element):
        with Session(self.engine) as session:
            session.add(element)
            session.commit()

    def pushItem(self, item : Item) -> str:
        # TODO test if ID is unique
        if  item.getTags() is not None:
            for tag in item.getTags():
                self.pushTag(tag, item.getID())

        dbItem = DBItem(
            id = item.getID(),
            name = item.getName(),
            type = item.getType().name,
            image_path = item.getPath(),
            description = item.getDescription()
        )
        self.add(dbItem)
        return item.getID()

    def pushEffect(self, effect : Effect) -> str:
        # TODO find a way to pass item/skill id here
        if effect.getTags() is not None:
            for tag in effect.getTags():
                self.pushTag(tag, effect.getID())

        dbEffect = DBEffect(
            id = effect.getID(),
            name = effect.getName(),
            effect_type = str(effect.getType()),
            value = effect.getValue(),
            duration = effect.getDuration()
        )
        self.add(dbEffect)
        return effect.getID()

    def pushQuest(self, quest : Quest):
        # TODO need to redo constructor
        pass

    def pushSkill(self, skill : Skill) -> str:
        if (skill.getTags() is not None):
            for tag in skill.getTags():
                self.pushTag(tag, skill.getID())

        dbSkill = DBSkill(
            id = skill.getID(),
            name = skill.getName(),
            manaCost = skill.getManaCost()
        )
        self.add(dbSkill)
        return skill.getID()

    # TODO Each method will have to check if IDs are unique
    # def pushTag(self, tag, parent_id : str) -> str:
    #     if type(tag) is ItemTag:
    #         return self.pushItemTag(tag, parent_id)
    #     elif type(tag) is EffectTag:
    #         return self.pushEffectTag(tag, parent_id)
    #     elif type(tag) is SkillTag:
    #         return self.pushSkillTag(tag, parent_id)
    #     else: raise IllegalArgumentException("Type not recognized")

    # def pushItemTag(self, tag : ItemTag, parent_id : str) -> str:
    #     new_id = IDHandler.generateID(ItemTag)
    #     dbTag = DBTag(
    #         id = new_id,
    #         item_id = parent_id,
    #         tag = tag.name,
    #         value = tag.value
    #     )
    #     self.add(dbTag)
    #     return new_id

    # def pushEffectTag(self, tag : EffectTag, parent_id : str) -> str:
    #     new_id = IDHandler.generateID(EffectTag)
    #     dbTag = DBTag(
    #         id = new_id,
    #         effect_id = parent_id,
    #         tag = tag.name,
    #         value = tag.value
    #     )
    #     self.add(dbTag)
    #     return new_id

    # def pushSkillTag(self, tag : SkillTag, parent_id : str) -> str:
    #     new_id = IDHandler.generateID(SkillTag)
    #     dbTag = DBTag(
    #         id = new_id,
    #         skill_id = parent_id,
    #         tag = tag.name,
    #         value = tag.value
    #     )
    #     self.add(dbTag)
    #     return new_id

    def pushCharacter(self, character:Character) -> str:
        db_character = DBCharacter(
            id = character.getID(),
            name = character.getName(),
            skill1 = 1,
            skill2 = 1,
            skill3 = 1,
            ultimate = 1,
            brilliance = 0,
            surge = 0,
            blaze = 0,
            passage = 0,
            clockwork = 0,
            void = 0,
            foundation = 0,
            frost = 0,
            flow = 0,
            abundance = 0,
            description = "",
            basehealth = 100,
            basemana = 100,
            basedef = 10,
            basespellpower = 10,
            baseattack = 10
        )
        self.add(db_character)
        return character.getID()

    def getNextID(self, object_type):
        with Session(self.engine) as session:
            query = session.query(func.max(object_type.id)).all()
            max_id = query[0][0]
        return max_id

# ## SETUP ###
# factory = DBElementFactory()
# example_character = Character()
# factory.store(example_character)
# print(f"The max ID of ItemStats is {factory.getNextID(DBCharacter)}")

## Storing on the database ###
#example_item = Item("Slimy Helmet", ItemSlotType.HEAD, "A helmet covered in slime, it's pretty nasty but wearable", "slimy_helmet.png")
#example_item2 = Item("Purveyor of the Nyaight", ItemSlotType.WEAPON, "This sword looks like it was made by a catgirl trying to be very dramatic", "katana.png")
#example_item3 = Item("Flower Crown", ItemSlotType.HEAD, "A pretty circlet of flowers", "flower_crown.png")
#example_effect = Effect("Burning", EffectType.DAMAGE_OVER_TIME_FLAT, 5, -1)
#example_skill = Skill("Breathe Fire", 100)
#factory.store(example_item)
#factory.store(example_item2)
#factory.store(example_item3)
#factory.store(example_effect)
#factory.store(example_skill)
