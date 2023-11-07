from util.Messages import Error
from model.item.Item import Item
from model.item.ItemSlotType import ItemSlotType
from model.effect.EffectType import EffectType
from util.IllegalArgumentException import IllegalArgumentException

class CharacterLoadout:
    slots : dict[ ItemSlotType, Item ]

    def __init__(self, slots:dict[ ItemSlotType, Item ] = None):
        if (slots is not None): self.slots = slots
        else: self.slots = {
            ItemSlotType.HEAD.value : None,
            ItemSlotType.CHEST.value : None,
            ItemSlotType.LEGS.value : None,
            ItemSlotType.WAIST.value : None,
            ItemSlotType.WEAPON.value : None,
            ItemSlotType.ACCESSORY1.value : None,
            ItemSlotType.ACCESSORY2.value : None
        }

    def isSlotEmpty(self, slot : ItemSlotType) -> bool:
        if slot not in self.slots: raise IllegalArgumentException(Error.INEXISTENT_SLOT)
        return self.slots is None

    def equip(self, item : Item) -> list[ ItemSlotType ]:
        slot = item.getType()
        if slot.value not in self.slots: raise IllegalArgumentException(Error.INEXISTENT_SLOT)
        oldItem = self.slots[slot.value]
        self.slots[slot.value] = item
        return oldItem

    def unequip(self, slot : ItemSlotType) -> Item:
        if slot not in self.slots: raise IllegalArgumentException(Error.INEXISTENT_SLOT)
        if self.slots[slot] is None: raise IllegalArgumentException(Error.NO_ITEM)
        item = self.slots[slot]
        for slot in item.getItemType(): self.slots[slot] = None
        return item

    def getStats(self) -> dict[ EffectType, int ]:
        result = dict()
        for gearPiece in self.slots.values():
            if (gearPiece == None): continue
            for stat, value in gearPiece.getStats().items():
                if stat.value not in result: result.update({stat.value: value})
                else: result[stat.value] += value
        return result