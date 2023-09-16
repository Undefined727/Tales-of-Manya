from util.Messages import Error
from model.item.Item import Item
from model.item.InventorySlot import InventorySlot
from util.IllegalArgumentException import IllegalArgumentException

class Inventory:
    maxSpace : int
    slots:list[InventorySlot]

    def __init__(self, maximum_slots : int = 64):
        self.maxSpace = maximum_slots
        self.slots = []

    def getItems(self) -> list[InventorySlot]:
        return self.slots
    
    def getInventorySize(self) -> int:
        return len(self.slots)

    def getLoad(self) -> int:
        currentAmount = 0
        for currentSlot in self.slots:
                currentAmount += currentSlot.count
        return currentAmount

    def getMaxSpace(self) -> int:
        return self.maxSpace

    def setMaxSpace(self, new_value : int):
        if new_value < len(self.slots): raise IllegalArgumentException(Error.CANNOT_BE_NEGATIVE)
        self.maxSpace = new_value

    def addItem(self, item : Item, count:int) -> bool:
        for i in range(count):
            added = False
            for currentSlot in self.slots:
                if (item.equals(currentSlot.item)):
                    added = currentSlot.addItem(item)
                    if (added): break
            if (not added):
                if (len(self.slots) < self.maxSpace):
                    self.slots.append(InventorySlot(item))
                    added = True
        return added

    def removeItem(self, item : Item, count:int) -> bool:
        currentAmount = 0
        for currentSlot in self.slots:
            if (item.equals(currentSlot.item)):
                currentAmount += currentSlot.count
        if (currentAmount < count): return False

        amountLeft = count
        for currentSlot in self.slots[::-1]:
            if (item.equals(currentSlot.item)):
                if (currentSlot.count > amountLeft): 
                    currentSlot.count -= amountLeft
                    break
                else: 
                    amountLeft -= currentSlot.count
                    self.slots.remove(currentSlot)
        return True

    def hasItem(self, name) -> bool:
        if (type(name) == Item): name = name.name
        for currentSlot in self.slots:
            if (currentSlot.item.name == name): return True
        return False

    def howMany(self, name) -> int:
        if (type(name) == Item): name = name.name
        currentAmount = 0
        for currentSlot in self.slots:
            if (name == currentSlot.item.name):
                currentAmount += currentSlot.count
        return currentAmount

    # Below implemented when IDs are a thing
    # def searchByID(self, id : str) -> Item:
    #     for item in self.slots:
    #         if (item.id == id): return item
    #     return None

    # def searchHowManyByID(self, id : str) -> tuple[ Item, int ]:
    #     item = self.searchByID(id)
    #     if item is None: raise IllegalArgumentException(Error.ITEM_NOT_FOUND)
    #     return (item, self.slots[item])