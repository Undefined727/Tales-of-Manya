from util.Messages import Error
from model.item.Item import Item
from util.IllegalArgumentException import IllegalArgumentException

class Inventory:
    space : int
    slots : dict[ Item, int ]

    def __init__(self, maximum_slots : int = 28):
        self.space = maximum_slots
        self.slots = dict()

    def getLoad(self) -> int:
        return self.slots.__len__()

    def getTotalSpace(self) -> int:
        return self.space

    def setTotalSpace(self, new_value : int):
        if new_value < self.space: raise IllegalArgumentException(Error.CANNOT_BE_NEGATIVE)
        self.space = new_value

    def addItem(self, item : Item) -> bool:
        if (item.isStackable() and item in self.slots):
            if (self.slots[item] >= 99): return False
            self.slots[item] += 1
            return True
        if (self.getLoad() >= self.space): return False
        self.slots[item] = 1
        return True

    def removeItem(self, item : Item) -> int:
        if item not in self.slots: raise IllegalArgumentException(Error.ITEM_NOT_FOUND)
        if not item.isStackable() or self.slots.get(item) == 1:
            self.slots.pop(item)
            return 0
        self.slots[item] -= 1
        return self.slots[item]

    def searchItem(self, name : str) -> Item:
        for item in self.slots.keys():
            if (item.name == name): return item
        return None

    def howMany(self, item : Item) -> int:
        if item not in self.slots: raise IllegalArgumentException(Error.ITEM_NOT_FOUND)
        return self.slots.get(item)

    def searchHowMany(self, name : str) -> tuple[ Item, int ]:
        item = self.searchItem(name)
        if item is None: raise IllegalArgumentException(Error.ITEM_NOT_FOUND)
        return (item, self.slots[item])

    def searchByID(self, id : str) -> Item:
        for item in self.slots:
            if (item.id == id): return item
        return None

    def searchHowManyByID(self, id : str) -> tuple[ Item, int ]:
        item = self.searchByID(id)
        if item is None: raise IllegalArgumentException(Error.ITEM_NOT_FOUND)
        return (item, self.slots[item])