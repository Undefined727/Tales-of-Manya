import Skill, Item

class Entity:
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
    skills = [Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0, 1), Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0, 1), Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0, 1)]
    name = "Filler"
    img = "catgirl.png"
    weapon = Item.Item(1)
    helmet = Item.Item(10)
    chestplate = Item.Item(3)
    leggings = Item.Item(4)
    boots = Item.Item(5)
    accessory1 = Item.Item(6)
    accessory2 = Item.Item(7)

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





    def useSkill(self, enemy, enemies, skillNumber):
        skill = self.skills[skillNumber]

        if (self.mana < skill.manaCost): return
        else: self.mana = self.mana - skill.manaCost

        self.HP = self.HP - skill.damagePlayer*self.ATK/100
        self.HP = self.HP + skill.healPlayer*self.magic/100
        self.mana = self.mana + skill.manaGivePlayer*self.magic/100
        self.mana = self.mana - skill.manaDrainPlayer*self.magic/100
        if (self.HP < 0): self.HP = 0
        if (self.HP > self.maxHP): self.HP = self.maxHP
        if (self.mana < 0): self.mana = 0
        if (self.mana > self.maxMana): self.mana = self.maxMana


        enemy.HP = enemy.HP - skill.damageEnemy*self.ATK/100
        enemy.HP = enemy.HP + skill.healEnemy*self.magic/100
        enemy.mana = enemy.mana + skill.manaGiveEnemy*self.magic/100
        enemy.mana = enemy.mana - skill.manaDrainEnemy*self.magic/100
        if (enemy.HP < 0): enemy.HP = 0
        if (enemy.HP > enemy.maxHP): enemy.HP = enemy.maxHP
        if (enemy.mana < 0): enemy.mana = 0
        if (enemy.mana > enemy.maxMana): enemy.mana = enemy.maxMana



        for currEnemy in enemies:
            currEnemy.HP = currEnemy.HP - skill.damageAoE*self.ATK/100
            currEnemy.HP = currEnemy.HP + skill.healAoE*self.magic/100
            currEnemy.mana = currEnemy.mana + skill.manaGiveAoE*self.magic/100
            currEnemy.mana = currEnemy.mana - skill.manaDrainAoE*self.magic/100
            if (currEnemy.HP < 0): currEnemy.HP = 0
            if (currEnemy.HP > currEnemy.maxHP): currEnemy.HP = currEnemy.maxHP
            if (currEnemy.mana < 0): currEnemy.mana = 0
            if (currEnemy.mana > currEnemy.maxMana): currEnemy.mana = currEnemy.maxMana