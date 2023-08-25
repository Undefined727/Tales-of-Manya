from src.main.python.model.character.CharacterLoadout import CharacterLoadout
from src.main.python.model.character.ExperienceStat import ExperienceManager
from src.main.python.model.character.DynamicStat import DynamicStat
from src.main.python.model.effect.EffectsList import EffectsList
from src.main.python.model.character.Inventory import Inventory
from src.main.python.model.effect.EffectType import EffectType
from src.main.python.model.skill.Skill import Skill
from src.main.python.model.item.Item import Item
from uuid import uuid4


class Character:
    ### Base Stats ###
    id : str
    name : str
    attack      = lambda self, type1 = EffectType.ATTACK_FLAT, type2 = EffectType.ATTACK_PCT: ((self.level * 10) + self.getBonuses(type1)) * (1 + self.getBonuses(type2))
    defense     = lambda self, type1 = EffectType.DEFENSE_FLAT, type2 = EffectType.DEFENSE_PCT: ((self.level * 10) + self.getBonuses(type1)) * (1 + self.getBonuses(type2))
    spellpower  = lambda self, type1 = EffectType.SPELLPOWER_FLAT, type2 = EffectType.SPELLPOWER_PCT: ((self.level * 10) + self.getBonuses(type1)) * (1 + self.getBonuses(type2))

    ### Dynamic Stats ###
    health : DynamicStat
    mana : DynamicStat
    experience : ExperienceManager
    loadout : CharacterLoadout
    inventory : Inventory
    buffs : EffectsList
    debuffs : EffectsList

    ### Collections ###
    skills:list[Skill]
    # spells:list[Spell] TODO #16 Implement

    ### Listeners ###
    loadout_bonuses : dict[ EffectType, int ]
    buff_bonuses : dict[ EffectType, int ]


    ### Temporary Stuff Until New Class ###
    img : str = "nekoarc.png"
    inactiveImg : str = "nekoarc.png"
    overworldImg : str = "nekoarc.png"
    hasActed : bool = False


    def __init__(self, name : str = "Placeholder Name", img : str = "nekoarc.png", level : int = 1):
        self.id             = uuid4()
        self.name           = name
        self.level          = level
        self.img            = img
        self.inactiveImg    = img
        self.overworldImg   = img

        self.health     = DynamicStat(level * 100)
        self.mana       = DynamicStat((level * 10) + 1000)
        self.experience = DynamicStat(level * 100)
        self.loadout    = CharacterLoadout()

        self.skills = [Skill(1), Skill(1), Skill(1)]
        self.spells = list()

        self.loadout_bonuses    = dict()
        self.buff_bonuses       = dict()
        self.hasActed           = False

    ### Getters ###

    def getBonuses(self, bonus_type : EffectType) -> int:
        # This helps other functions to fetch either the flat and percentage
        # bonuses of their respective stat and add them up into a single
        # value.

        from_buffs = self.buff_bonuses.get(bonus_type)
        from_loadout = self.loadout_bonuses.get(bonus_type)
        return from_loadout + from_buffs

    def getCurrentHP(self) -> int:
        return self.health.getCurrentValue()

    def getMaxHP(self) -> int:
        return self.health.getMaxValue()

    def getCurrentMana(self) -> int:
        return self.mana.getCurrentValue()

    def getMaxMana(self) -> int:
        return self.mana.getMaxValue()

    def getCurrentXP(self) -> int:
        return self.experience.getXP()

    ### Setters ###

    def setCurrentHP(self, value : int):
        self.health.setCurrentValue(value)

    def setCurrentMana(self, value : int):
        self.mana.setCurrentValue(value)

    ## Class specific methods ##

    def heal(self, amount : int):
        amount *= 1 + self.getBonuses(EffectType.HEALING_PCT)
        self.health.increaseBy(amount)

    def harm(self, amount : int):
        amount += 1 + self.getBonuses(EffectType.INCOMING_DAMAGE_FLAT)
        amount *= 1 + self.getBonuses(EffectType.INCOMING_DAMAGE_PCT)
        self.health.decreaseBy(amount)

    def recoverMana(self, amount : int):
        amount *= 1 + self.getBonuses(EffectType.MANA_RECOVERY)
        self.mana.increaseBy(amount)

    def spendMana(self, amount : int):
        amount *= 1 + self.getBonuses(EffectType.MANA_EFFICIENCY)
        self.mana.decreaseBy(amount)

    def earnXP(self, amount : int):
        self.experience.earnXP(amount)

    def setXPFormula(self, new_formula : function):
        self.experience.setFormula(new_formula)

    def update(self):
        # This is what should be used to update a character's stats at the end
        # of a turn

        # Calculating maximum health
        base_health = (self.level * 100)
        extra_health_flat = self.getBonuses(EffectType.HEALTH_FLAT)
        extra_health_pct = 1 + self.getBonuses(EffectType.HEALTH_PCT)
        new_max_health = (base_health + extra_health_flat) * extra_health_pct

        # Calculating maximum mana
        base_mana = 1000 + (self.level * 10)
        extra_mana_flat = self.getBonuses(EffectType.MANA_FLAT)
        extra_mana_pct = 1 + self.getBonuses(EffectType.MANA_PCT)
        new_max_mana = (base_mana + extra_mana_flat) * extra_mana_pct

        self.health.setMaxValue(new_max_health)
        self.mana.setMaxValue(new_max_mana)

        self.loadout_bonuses = self.loadout.getBonuses()
        self.buff_bonuses = self.buffs.calculate().update(self.debuffs.calculate())
        self.buffs.update()
        self.debuffs.update()