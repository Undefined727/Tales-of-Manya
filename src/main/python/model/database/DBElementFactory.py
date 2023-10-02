import os, sys
sys.path.append(os.path.abspath("."))
from src.main.python.model.item.Item import Item
from src.main.python.model.item.ItemSlotType import ItemSlotType
from src.main.python.model.item.ItemTag import ItemTag
from src.main.python.model.effect.Effect import Effect
from src.main.python.model.effect.EffectType import EffectType
from src.main.python.model.effect.EffectTag import EffectTag
from src.main.python.model.skill.Skill import Skill
from src.main.python.model.skill.SkillTag import SkillTag
from src.main.python.model.player.Quest import Quest
from src.main.python.model.database.DatabaseModels import *
from src.main.python.util.IllegalArgumentException import IllegalArgumentException
from src.main.python.util.IDHandler import IDHandler
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import select

class DBElementFactory:
    # TODO Missing method to test if the IDs are unique
    # TODO complete a few methods, finish relationships

    def __init__(self, path : str = "src/main/python/catgirl-dungeon.db", echo : bool = False):
        self.engine = create_engine(f"sqlite:///{path}", echo = echo)

    def fetchItem(self, name : str):
        connection = self.engine.connect()
        statement = select(DBItem).where(DBItem.name == name)
        row = connection.execute(statement).first()
        if row is None: raise IllegalArgumentException("The item is not in the database")
        return self.buildItem(row)

    def fetchItemByID(self, item_id : str):
        connection = self.engine.connect()
        statement = select(DBItem).where(DBItem.id == item_id)
        row = connection.execute(statement).first()
        if row is None: raise IllegalArgumentException("The item is not in the database")
        return self.buildItem(row)

    def buildItem(self, row) -> Item:
        # TODO Not handling tags and bonuses yet
        item = Item(row.name,
                    ItemSlotType[row.type],
                    row.description,
                    row.image_path,
                    None,
                    None,
                    row.id)
        return item

    def buildSkill(self, row) -> Skill:
        skill = Skill(row.name,
                      row.mana_cost,
                      row.id)
        return skill

    def buildEffect(self, row) -> Effect:
        effect = Effect(row.name,
                        EffectType[row.effect_type],
                        row.value,
                        row.duration,
                        None,
                        row.id)
        return effect

    def store(self, element):
        if type(element) is Item: self.pushItem(element)
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
    def pushTag(self, tag, parent_id : str) -> str:
        if type(tag) is ItemTag:
            return self.pushItemTag(tag, parent_id)
        elif type(tag) is EffectTag:
            return self.pushEffectTag(tag, parent_id)
        elif type(tag) is SkillTag:
            return self.pushSkillTag(tag, parent_id)
        else: raise IllegalArgumentException("Type not recognized")

    def pushItemTag(self, tag : ItemTag, parent_id : str) -> str:
        new_id = IDHandler.generateID(ItemTag)
        dbTag = DBTag(
            id = new_id,
            item_id = parent_id,
            tag = tag.name,
            value = tag.value
        )
        self.add(dbTag)
        return new_id

    def pushEffectTag(self, tag : EffectTag, parent_id : str) -> str:
        new_id = IDHandler.generateID(EffectTag)
        dbTag = DBTag(
            id = new_id,
            effect_id = parent_id,
            tag = tag.name,
            value = tag.value
        )
        self.add(dbTag)
        return new_id

    def pushSkillTag(self, tag : SkillTag, parent_id : str) -> str:
        new_id = IDHandler.generateID(SkillTag)
        dbTag = DBTag(
            id = new_id,
            skill_id = parent_id,
            tag = tag.name,
            value = tag.value
        )
        self.add(dbTag)
        return new_id

# ## SETUP ###
factory = DBElementFactory()

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

# ## Fetching from the database ###
item = factory.fetchItem("Flower Crown")
print(item.toString())
