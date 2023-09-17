from sqlalchemy.engine.row import Row
from model.item.ItemSlotType import ItemSlotType
from model.item.ItemTag import ItemTag
from model.effect.EffectType import EffectType
import uuid

class Item:
    id : str
    name : str
    itemType : list[ ItemSlotType ]
    item_tags : list[ ItemTag ]
    item_bonuses : dict[ EffectType, int ]
    description : str
    imgPath: str
    #Statuses below when implemented

    def __init__(self, name:str = "Placeholder Name", itemType:list[ItemSlotType] = [ItemSlotType.WEAPON], description:str = "", item_tags:list[ItemTag] = list()):
        self.id = str(uuid.uuid5(uuid.NAMESPACE_DNS,"basedstudios.dev"))
        if (name == "Purveyor of the Nyaight"): self.imgPath = "katana.png"
        else: self.imgPath = "iron_helm.png"
        self.name = name
        self.itemType = itemType
        self.description = description
        self.item_tags = item_tags

    def getItemType(self) -> list[ItemSlotType]:
        return self.itemType

    def getBonuses(self) -> dict[ EffectType, int]:
        return self.item_bonuses
    
    def equals(self, item):
        if (type(item) == Item):
            if (item.name == self.name): return True
        return False
