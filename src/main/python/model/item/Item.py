from sqlalchemy.engine.row import Row
from src.main.python.model.item.ItemSlot import ItemSlot
from src.main.python.model.item.ItemTag import ItemTag
from src.main.python.model.effect.EffectType import EffectType
import uuid

class Item:
    id : str
    name : str
    slot : ItemSlot
    item_tags : list[ ItemTag ]
    item_bonuses : dict[ EffectType, int ]
    description : str
    #Statuses below when implemented

    def __init__(self, name = "Placeholder Name", slot = ItemSlot.WEAPON, item_tags = list(), description = ""):
        self.id = str(uuid.uuid5(uuid.NAMESPACE_DNS,"basedstudios.dev"))
        self.name = name
        self.slot = slot
        self.item_tags = item_tags
        self.description = description

    def getSlot(self):
        return self.slot

    def toDatabaseItem(self):
        return {
            'id' : self.id,
            'name': self.name,
            'item_slot' : self.slot.name,
            'description': self.description
        }