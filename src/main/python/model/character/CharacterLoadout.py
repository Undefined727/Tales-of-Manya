from util.Messages import Error
from model.item.Item import Item
from model.item.ItemSlotType import ItemSlotType
from model.effect.EffectType import EffectType
from util.IllegalArgumentException import IllegalArgumentException

class CharacterLoadout:
    slots : dict[ ItemSlotType, Item ]

    def __init__(self, slots : dict[ ItemSlotType, Item ] = {
        ItemSlotType.HEAD : None,
        ItemSlotType.CHEST : None,
        ItemSlotType.LEGS : None,
        ItemSlotType.WAIST : None,
        ItemSlotType.WEAPON : None,
        ItemSlotType.ACCESSORY1 : None,
        ItemSlotType.ACCESSORY2 : None
    }):
        self.slots = slots

    def isSlotEmpty(self, slot : ItemSlotType) -> bool:
        if slot not in self.slots: raise IllegalArgumentException(Error.INEXISTENT_SLOT)
        return self.slots is None

    def equip(self, item : Item) -> list[ ItemSlotType ]:
        for slot in item.getItemType():
            if slot not in self.slots: raise IllegalArgumentException(Error.INEXISTENT_SLOT)
            if self.slots[slot] is not None: raise IllegalArgumentException(Error.SLOT_TAKEN)
        for slot in item.getItemType(): self.slots[slot] = item
        return item.getItemType()

    def unequip(self, slot : ItemSlotType) -> Item:
        if slot not in self.slots: raise IllegalArgumentException(Error.INEXISTENT_SLOT)
        if self.slots[slot] is None: raise IllegalArgumentException(Error.NO_ITEM)
        item = self.slots[slot]
        for slot in item.getItemType(): self.slots[slot] = None
        return item

    def getBonuses(self) -> dict[ EffectType, int ]:
        result = dict()
        for key in self.slots:
            item = self.slots.get(key)
            item_bonuses = item.getBonuses()
            for bonus in item_bonuses:
                if bonus in result: result[bonus] += item_bonuses[bonus]
                result[bonus] = item_bonuses[bonus]
        return result