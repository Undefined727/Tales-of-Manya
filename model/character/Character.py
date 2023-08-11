from model.character.CharacterLoadout import CharacterLoadout
from model.character.DynamicStat import DynamicStat
from model.effect.EffectsList import EffectsList
from model.effect.EffectType import EffectType
from model.skill.Skill import Skill
from model.item.Item import Item


class Character:
    ### Base Stats ###
    name:str
    level:int
    attack      = lambda self, type1 = EffectType.ATTACK_FLAT, type2 = EffectType.ATTACK_PCT: ((int(self.level / 10)) + self.getBonuses(type1)) * (1 + self.getBonuses(type2))
    defense     = lambda self, type1 = EffectType.DEFENSE_FLAT, type2 = EffectType.DEFENSE_PCT: ((int(self.level / 10)) + self.getBonuses(type1)) * (1 + self.getBonuses(type2))
    spellpower  = lambda self, type1 = EffectType.SPELLPOWER_FLAT, type2 = EffectType.SPELLPOWER_PCT: ((int(self.level / 10)) + self.getBonuses(type1)) * (1 + self.getBonuses(type2))

    ### Dynamic Stats ###
    health:DynamicStat
    mana:DynamicStat
    loadout:CharacterLoadout
    buffs:EffectsList
    debuffs:EffectsList

    ### Collections ###
    skills = []
    spells = []

    ### Listeners ###
    loadout_bonuses = {}
    buff_bonuses = {}


    ### Temporary Stuff Until New Class ###
    img = "nekoarc.png"
    headImg = "nekoarc.png"
    overworldImg = "nekoarc.png"
    hasActed = False


    def __init__(self, name = "Placeholder Name", img = "nekoarc.png", headImg = "nekoarc.png", level = 1):
        self.name       = name
        self.level      = level
        self.img = img
        self.headImg = headImg
        self.overworldImg = headImg

        self.health     = DynamicStat(level * 100)
        self.mana       = DynamicStat(1000 + level * 10)
        self.loadout    = CharacterLoadout()

        self.skills     = [Skill(1), Skill(1), Skill(1)]
        self.hasActed = False

    

    ### Getters ###

    def getBonuses(self, bonus_type):
        # This helps other functions to fetch the flat and percentage bonuses of
        # their respective stat and add them up into a single value

        return 10
        #from_buffs = self.buff_bonuses.get(bonus_type)
        #from_loadout = self.loadout_bonuses.get(bonus_type)
        #return from_loadout + from_buffs
    
    def getCurrentHP(self):
        return self.health.getCurrentValue()
    
    def getMaxHP(self):
        return self.health.getMaxValue()
    
    def getHealth(self):
        return self.health
    
    
    

    ### Setters ###

    def setCurrentHP(self, value):
        self.health.setCurrentValue(value)


    def update(self):
        # This is what should be used to update a character's stats at the end
        # of a turn

        new_max_health = ((self.level * 100) + self.getBonuses(EffectType.HEALTH_FLAT)) * (1 + self.getBonuses(EffectType.HEALTH_PCT))
        new_max_mana = ((self.level * 10) + 1000 + self.getBonuses(EffectType.MANA_FLAT)) * (1 + self.getBonuses(EffectType.MANA_PCT))
        self.health.setMaxValue(new_max_health)
        self.mana.setMaxValue(new_max_mana)

        self.loadout_bonuses = self.loadout.getBonuses()
        self.buff_bonuses = self.buffs.calculate().update(self.debuffs.calculate())
        self.buffs.update()
        self.debuffs.update()