import model.item.Item as Item
import item.ItemSlot as ItemSlot
import util.IllegalArgumentException as IllegalArgumentException

class CharacterLoadout:
    slots = {}

    def __init__(self, slots = {
        ItemSlot.HEAD : None,
        ItemSlot.CHEST : None,
        ItemSlot.LEGS : None,
        ItemSlot.FEET : None,
        ItemSlot.WEAPON : None,
        ItemSlot.ACCESSORY1 : None,
        ItemSlot.ACCESSORY2 : None
    }):
        self.slots = slots

    def isSlotEmpty(self, slot:ItemSlot):
        if slot not in self.slots:
            raise IllegalArgumentException("The slot does not exist")
        return self.slots is None

    def equip(self, item = Item):
        if (item not in self.slots):
            raise IllegalArgumentException("The slot does not exist")
        if (self.slots[item.getSlot()] != None):
            raise IllegalArgumentException("There is already an item equipped on that slot")
        else:
            self.slots[item.getSlot()] = item

    def unequip(self, slot = ItemSlot):
        if (slot not in self.slots):
            raise IllegalArgumentException("The slot does not exist")
        if (self.slots[slot] == None):
            raise IllegalArgumentException("There is no item on that slot")
        else:
            item = self.slots[slot]
            self.slots[slot] = None
            return item

    def getBonuses(self) -> {}:
        result = {}
        for key in self.slots.keys():
            item_bonuses = self.slots[key].getBonuses()
            for bonus in item_bonuses.keys():
                if (bonus in result):
                    result[bonus] += item_bonuses[bonus]
                else:
                    result[bonus] = item_bonuses[bonus]
        return result