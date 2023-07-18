import Skill

class Entity:
    maxHP = 100
    HP = 100
    maxMana = 100
    mana = 100
    # Magic Strength
    magic = 20
    DEF = 10
    ATK = 20
    SPD = 100
    level = 10
    skills = [Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0), Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0), Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0)]
    name = "Filler"
    img = "catgirl.png"

    def __init__(self, name, img, level):
        self.name = name
        self.img = img
        self.level = level
        self.maxHP = level*100
        self.HP = level*100
        self.maxMana = level*100
        self.mana = level*100
        self.magic = level*10
        self.DEF = level*10
        self.ATK = level*10
        

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


