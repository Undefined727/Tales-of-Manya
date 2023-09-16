from model.item.Item import Item

class InventorySlot:

    item:Item
    count:int

    def __init__(self, item = None, count = 1):
        self.item = item
        self.count = count

    def addItem(self, item:Item):
        if (item.equals(self.item) and (self.count+1) <= item.stackLimit):
            self.count += 1
            return True
        else: return False