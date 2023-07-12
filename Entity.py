class Entity:
    maxHP = 100
    HP = 100
    DEF = 10
    ATK = 20
    SPD = 100
    level = 10
    name = "Filler"
    img = "catgirl.png"

    def __init__(self, name, level, img):
        self.level = level
        self.maxHP = level*100
        self.HP = level*100
        self.DEF = level*10
        self.ATK = level*20
        self.name = name
        self.img = img
    
    def attack(self, attackedEntity, amount):
        attackedEntity.HP = attackedEntity.HP - amount*self.ATK/100