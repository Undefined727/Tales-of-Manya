from sqlalchemy.engine.row import LegacyRow
from src.main.python.model.item.ItemSlot import ItemSlot
from src.main.python.model.item.ItemTag import ItemTag
from src.main.python.model.effect.EffectType import EffectType

class Item:
    id : int
    name : str
    slots : list[ ItemSlot ]
    item_tags : list[ ItemTag ]
    item_bonuses : dict[ EffectType, int ]
    description : str
    #Statuses below when implemented

    def __init__(self, name = "Placeholder Name", slot = ItemSlot.WEAPON, item_tags = list(), description = ""):
       self.name = name
       self.slot = slot
       self.item_tags = item_tags
       self.description = description

    @staticmethod
    def createFrom(tuple : LegacyRow):
        item_bonuses = {EffectType.SPELLPOWER_PCT:tuple[3],
                        EffectType.DEFENSE_PCT:tuple[4],
                        EffectType.ATTACK_PCT:tuple[5],
                        EffectType.HEALTH_PCT:tuple[6],
                        EffectType.SPELLPOWER_FLAT:tuple[7],
                        EffectType.DEFENSE_FLAT:tuple[8],
                        EffectType.ATTACK_FLAT:tuple[9],
                        EffectType.HEALTH_FLAT:tuple[10]}
        resulting_item = Item( tuple[1], ItemSlot(tuple[2]), item_bonuses, tuple[11] )
        return resulting_item

    def getSlot(self):
        return self.slot