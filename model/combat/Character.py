from model.combat.Skill import Skill
from model.combat.Item import Item

class Character:
    maxHP = 100
    HP = 100
    maxMana = 100
    mana = 100
    # Magic Strength
    magic = 20
    DEF = 10
    ATK = 20
    HPPercent = 0
    manaPercent = 0
    magicPercent = 0
    DEFPercent = 0
    ATKPercent = 0
    level = 10
    skills = [Skill(1), Skill(1), Skill(1)]
    name = "Filler"
    img = "catgirl.png"
    headImg = "catgirl_head.png"
    weapon = Item(1)
    helmet = None
    chestplate = None
    leggings = Item(4)
    boots = Item(5)
    accessory1 = Item(6)
    accessory2 = Item(7)
    hasActed = False

    def __init__(self, name, img, level):
        self.name = name
        self.img = img
        self.level = level
        self.maxHP = level*100
        self.HP = level*100
        self.maxMana = 1000 + level*10
        self.mana = 1000 + level*10
        self.magic = level*10
        self.DEF = level*10
        self.ATK = level*10
        self.skills = [Skill(1), Skill(1), Skill(1)]
        self.weapon = Item(1)
        self.helmet = None
        self.chestplate = None
        self.leggings = Item(4)
        self.boots = Item(5)
        self.accessory1 = Item(6)
        self.accessory2 = Item(7)
        self.hasActed = False
        self.updateItems()
        
    def updateItems(self):
        self.maxHP = self.level*100
        self.maxMana = 1000 + self.level*10
        self.magic = self.level*10
        self.DEF = self.level*10
        self.ATK = self.level*10
        self.HPPercent = 0
        self.manaPercent = 0
        self.magicPercent = 0
        self.DEFPercent = 0
        self.ATKPercent = 0
        self.addItemStat(self.weapon)
        self.addItemStat(self.helmet)
        self.addItemStat(self.chestplate)
        self.addItemStat(self.leggings)
        self.addItemStat(self.boots)
        self.addItemStat(self.accessory1)
        self.addItemStat(self.accessory2)
        self.maxHP = self.maxHP*(100+self.HPPercent)/100
        self.maxMana = self.maxMana*(100+self.manaPercent)/100
        self.magic = self.magic*(100+self.magicPercent)/100
        self.DEF = self.DEF*(100+self.DEFPercent)/100
        self.ATK = self.ATK*(100+self.ATKPercent)/100
        self.HP = self.maxHP
        self.mana = self.maxMana

    
    def addItemStat(self, item):
        if (item == None): return
        self.maxHP = self.maxHP+ int(item.flatHP)
        self.maxMana = self.maxMana + int(item.flatMana)
        self.magic = self.magic + int(item.flatMagic)
        self.DEF = self.DEF + int(item.flatDEF)
        self.ATK = self.ATK + int(item.flatATK)
        self.HPPercent = self.HPPercent + int(item.HPPercent)
        self.manaPercent = self.manaPercent + int(item.manaPercent)
        self.magicPercent = self.magicPercent + int(item.magicPercent)
        self.DEFPercent = self.DEFPercent + int(item.DEFPercent)
        self.ATKPercent = self.ATKPercent + int(item.ATKPercent)