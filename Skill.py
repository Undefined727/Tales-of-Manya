class Skill:
    #skillNumber implemented later
    skillNumber = 0

    skillName = "null"
    img = "sword.png"
    singleTarget = True

    #AoE does not include Player
    healPlayer = 0
    healEnemy = 0
    healAoE = 0
    damagePlayer = 0
    damageEnemy = 0
    damageAoE = 0
    manaGivePlayer = 0
    manaGiveEnemy = 0
    manaGiveAoE = 0
    manaDrainPlayer = 0
    manaDrainEnemy = 0
    manaDrainAoE = 0
    element = "Physical"
    manaCost = 0
    actionPointCost = 1
    # Add Statuses


    # When we add statuses/database this will change to be skillNumber and self
    def __init__(self, skillName, img, singleTarget, healPlayer, healEnemy, healAoE, damagePlayer, damageEnemy, damageAoE, manaGivePlayer, manaGiveEnemy, manaGiveAoE, manaDrainPlayer, manaDrainEnemy, manaDrainAoE, element, manaCost, actionPointCost):
        self.skillName = skillName
        self.img = img
        self.singleTarget = singleTarget
        self.healPlayer = healPlayer
        self.healEnemy = healEnemy
        self.healAoE = healAoE
        self.damagePlayer = damagePlayer
        self.damageEnemy = damageEnemy
        self.damageAoE = damageAoE
        self.manaGivePlayer = manaGivePlayer
        self.manaGiveEnemy = manaGiveEnemy
        self.manaGiveAoE = manaGiveAoE
        self.manaDrainPlayer = manaDrainPlayer
        self.manaDrainEnemy = manaDrainEnemy
        self.manaDrainAoE = manaDrainAoE
        self.element = element
        self.manaCost = manaCost
        self.actionPointCost = actionPointCost