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
    skills = [Skill.Skill("Basic Attack", "sword.png", 1, 0, 0, 0, 100, 0, 0, 0, "Physical", 0), Skill.Skill("Basic Attack", "sword.png", 1, 0, 0, 0, 100, 0, 0, 0, "Physical", 0), Skill.Skill("Basic Attack", "sword.png", 1, 0, 0, 0, 100, 0, 0, 0, "Physical", 0)]
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
        
    
    def useSkill(self, Enemy1, Enemy2, Enemy3, Enemy4, skillNumber):
        skill = self.skills[skillNumber]
        if (self.mana < skill.manaCost): return
        if (skill.targetLevel == 1):
            Enemy1.HP = Enemy1.HP - skill.damageEnemy*self.ATK/100
            Enemy1.HP = Enemy1.HP + skill.healEnemy*self.magic/100
            Enemy1.mana = Enemy1.mana + skill.manaGiveEnemy*self.magic/100
            Enemy1.mana = Enemy1.mana - skill.manaDrainEnemy*self.magic/100
            self.HP = self.HP - skill.damagePlayer*self.ATK/100
            self.HP = self.HP + skill.healPlayer*self.magic/100
            self.mana = self.mana + skill.manaGivePlayer*self.magic/100


            if (Enemy1.HP < 0): Enemy1.HP = 0
            if (Enemy1.HP > Enemy1.maxHP): Enemy1.HP = Enemy1.maxHP
            if (Enemy1.mana < 0): Enemy1.mana = 0
            if (Enemy1.mana > Enemy1.maxMana): Enemy1.mana = Enemy1.maxMana
            if (self.HP < 0): self.HP = 0
            if (self.HP > self.maxHP): self.HP = self.maxHP
            if (self.mana < 0): self.mana = 0
            if (self.mana > self.maxMana): self.mana = self.maxMana
        if (skill.targetLevel == 2):
            Enemy1.HP = Enemy1.HP - skill.damageEnemy*self.ATK/100
            Enemy1.HP = Enemy1.HP + skill.healEnemy*self.magic/100
            Enemy1.mana = Enemy1.mana + skill.manaGiveEnemy*self.magic/100
            Enemy1.mana = Enemy1.mana - skill.manaDrainEnemy*self.magic/100
            Enemy2.HP = Enemy1.HP - skill.damageEnemy*self.ATK/100
            Enemy2.HP = Enemy1.HP + skill.healEnemy*self.magic/100
            Enemy2.mana = Enemy1.mana + skill.manaGiveEnemy*self.magic/100
            Enemy2.mana = Enemy1.mana - skill.manaDrainEnemy*self.magic/100
            Enemy3.HP = Enemy1.HP - skill.damageEnemy*self.ATK/100
            Enemy3.HP = Enemy1.HP + skill.healEnemy*self.magic/100
            Enemy3.mana = Enemy1.mana + skill.manaGiveEnemy*self.magic/100
            Enemy3.mana = Enemy1.mana - skill.manaDrainEnemy*self.magic/100
            Enemy4.HP = Enemy1.HP - skill.damageEnemy*self.ATK/100
            Enemy4.HP = Enemy1.HP + skill.healEnemy*self.magic/100
            Enemy4.mana = Enemy1.mana + skill.manaGiveEnemy*self.magic/100
            Enemy4.mana = Enemy1.mana - skill.manaDrainEnemy*self.magic/100

            self.HP = self.HP - skill.damagePlayer*self.ATK/100
            self.HP = self.HP + skill.healPlayer*self.magic/100
            self.mana = self.mana + skill.manaGivePlayer*self.magic/100

            if (Enemy1.HP < 0): Enemy1.HP = 0
            if (Enemy1.HP > Enemy1.maxHP): Enemy1.HP = Enemy1.maxHP
            if (Enemy1.mana < 0): Enemy1.mana = 0
            if (Enemy1.mana > Enemy1.maxMana): Enemy1.mana = Enemy1.maxMana
            if (Enemy2.HP < 0): Enemy2.HP = 0
            if (Enemy2.HP > Enemy2.maxHP): Enemy2.HP = Enemy2.maxHP
            if (Enemy2.mana < 0): Enemy2.mana = 0
            if (Enemy2.mana > Enemy2.maxMana): Enemy2.mana = Enemy2.maxMana
            if (Enemy3.HP < 0): Enemy3.HP = 0
            if (Enemy3.HP > Enemy3.maxHP): Enemy3.HP = Enemy3.maxHP
            if (Enemy3.mana < 0): Enemy3.mana = 0
            if (Enemy3.mana > Enemy3.maxMana): Enemy3.mana = Enemy3.maxMana
            if (Enemy4.HP < 0): Enemy4.HP = 0
            if (Enemy4.HP > Enemy4.maxHP): Enemy4.HP = Enemy4.maxHP
            if (Enemy4.mana < 0): Enemy4.mana = 0
            if (Enemy4.mana > Enemy4.maxMana): Enemy4.mana = Enemy4.maxMana
            if (self.HP < 0): self.HP = 0
            if (self.HP > self.maxHP): self.HP = self.maxHP
            if (self.mana < 0): self.mana = 0
            if (self.mana > self.maxMana): self.mana = self.maxMana
        else:
            self.HP = self.HP - skill.damagePlayer*self.ATK/100
            self.HP = self.HP + skill.healPlayer*self.magic/100
            self.mana = self.mana + skill.manaGivePlayer*self.magic/100
            if (self.HP < 0): self.HP = 0
            if (self.HP > self.maxHP): self.HP = self.maxHP
            if (self.mana < 0): self.mana = 0
            if (self.mana > self.maxMana): self.mana = self.maxMana

