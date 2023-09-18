from sqlalchemy.engine.row import Row
import json
from model.item.ItemSlotType import ItemSlotType
from model.item.ItemTag import ItemTag
from model.effect.EffectType import EffectType
import uuid

class Item:
    itemID : int
    itemName : str
    itemType : ItemSlotType
    itemTags : list[ ItemTag ]
    itemBonuses : dict[ EffectType, int ]
    description : str
    imgPath: str
    #Statuses below when implemented

    def __init__(self, itemID):
        if (type(itemID) == str): self.itemName = itemID
        else: self.itemID = itemID

        file = open("src/main/python/items/itemList.json", 'r')
        data = json.load(file)

        for itemEntry in data:
            if (itemEntry['itemID'] == itemID or itemEntry['itemName'] == itemID):
                self.itemID = itemEntry['itemID']
                self.itemName = itemEntry['itemName']
                self.itemType = itemEntry['itemType']
                self.itemTags = itemEntry['itemTags']
                self.itemBonuses = itemEntry['itemBonuses']
                self.description = itemEntry['description']
                self.imgPath = itemEntry['imgPath']
                break

    def getItemType(self) -> list[ItemSlotType]:
        return self.itemType

    def getBonuses(self) -> dict[ EffectType, int]:
        return self.itemBonuses
    
    def equals(self, item):
        if (type(item) == Item):
            if (item.itemName == self.itemName): return True
        return False
