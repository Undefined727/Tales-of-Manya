from sqlalchemy.engine.row import Row
import json
from src.main.python.model.item.ItemSlotType import ItemSlotType
from src.main.python.model.item.ItemTag import ItemTag
from src.main.python.model.effect.EffectType import EffectType
from src.main.python.util.IDHandler import IDHandler

class Item:
    id : str
    name : str
    type : ItemSlotType
    tags : list[ ItemTag ]
    bonuses : dict[ EffectType, int ]
    description : str
    image_path: str
    #Statuses below when implemented

    def __init__(self,
                 name : str,
                 type : ItemSlotType,
                 description : str,
                 image_path : str,
                 tags : list[ ItemTag ] = None,
                 bonuses : dict[ EffectType, int ] = None,
                 id : str = None):
        self.setName(name)
        self.setType(type)
        self.setDescription(description)
        self.setImagePath(image_path)
        self.setTags(tags)
        self.setBonuses(bonuses)
        if id is None: self.setID(str(IDHandler.generateID(Item)))
        else: self.setID(id)

    def getID(self) -> str:
        return self.id

    def getName(self) -> str:
        return self.name

    def getDescription(self) -> str:
        return self.description

    def getPath(self) -> str:
        return self.image_path

    def getTags(self) -> list[ ItemTag ]:
        return self.tags

    def getType(self) -> ItemSlotType:
        return self.type

    def getBonuses(self) -> dict[ EffectType, int]:
        return self.bonuses

    def setID(self, new_id : str):
        self.id = new_id

    def setName(self, new_name : str):
        self.name = new_name

    def setType(self, new_type : ItemSlotType):
        self.type = new_type

    def setDescription(self, new_description : str):
        self.description = new_description

    def setImagePath(self, new_image_path : str):
        self.image_path = new_image_path

    def setTags(self, new_tags : list[ ItemTag ]):
        self.tags = new_tags

    def setBonuses(self, bonuses : dict[ EffectType, int ]):
        self.bonuses = bonuses

    def equals(self, item):
        if (type(item) == Item):
            if (item.getName() == self.getName()): return True
        return False

    def toString(self):
        return f"Name: {self.getName()}; Type: {self.getType()}; Tags: {self.getTags()}; Bonuses: {self.getBonuses()}; Description: {self.getDescription()}; Path: {self.getPath()}"
