from model.character.CharacterLoadout import CharacterLoadout
from model.character.ExperienceStat import ExperienceManager
from model.character.DynamicStat import DynamicStat
from model.effect.EffectsList import EffectsList
from model.character.Inventory import Inventory
from model.effect.EffectType import EffectType
from model.item.ItemStatType import ItemStatType
from model.skill.Skill import Skill
from model.item.Item import Item
from uuid import uuid4


class Character:
    ## Character Identifiers ##
    id : str
    name : str

    ## Basic Stats ##
    # Base Stats #
    baseattack:int
    basespellpower:int
    basehealth:int
    basemana:int
    # 0 for characters
    basedef:int

    # Variable Stats #
    attack:int
    spellpower:int
    defense:int
    # These are handled with a class due to them being a bar and a stat #
    health : DynamicStat
    mana : DynamicStat

    ## Elemental Affinities ##
    # Base Stats #
    baseBrilliance:int
    baseVoid:int
    baseSurge:int
    baseFoundation:int
    baseBlaze:int
    baseFrost:int
    basePassage:int
    baseFlow:int
    baseAbundance:int
    baseClockwork:int

    # Variable Stats #
    brilliance:int
    void:int
    surge:int
    foundation:int
    blaze:int
    frost:int
    passage:int
    flow:int
    abundance:int
    clockwork:int

    ## Skills ##
    skills:list[str]

    ## Inventory ##
    loadout : CharacterLoadout
    inventory : Inventory
    experience : ExperienceManager

    ## Effects ##
    buffs : list[str]

    ### Visuals ###
    ## Combat ##
    img : str = "nekoarc.png"
    selectedImg : str = "nekoarc.png"
    
    ## Overworld ##
    overworldImg : str = "nekoarc.png"


    # Move this to the combat turn taking section
    hasActed : bool = False


    # Add Pulling from Database with ID in the future #
    def __init__(self, id:int = 1, level : int = 1):
        self.id             = uuid4()
        self.name           = name
        self.level          = level
        self.img            = img
        if (name == "Slime"): self.selectedImg = "selectedSlimeAnimation"
        else: self.selectedImg = "selectedCatgirlAnimation"
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
        self.update()

    ### Getters ###

    def getBonuses(self, bonus_type : EffectType) -> int:
        # This helps other functions to fetch either the flat and percentage
        # bonuses of their respective stat and add them up into a single
        # value.

        #from_buffs = self.buff_bonuses.get(bonus_type)
        #from_loadout = self.loadout_bonuses.get(bonus_type)
        #return from_loadout + from_buffs
        return -1

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

    def takeDamage(self, amount : int):
        # Add defense to scale this
        self.health.decreaseBy(amount)

    def recoverMana(self, amount : int):
        amount *= 1 + self.getBonuses(EffectType.MANA_RECOVERY)
        self.mana.increaseBy(amount)

    def spendMana(self, amount : int):
        amount *= 1 + self.getBonuses(EffectType.MANA_EFFICIENCY)
        self.mana.decreaseBy(amount)

    def earnXP(self, amount : int):
        self.experience.earnXP(amount)

    def setXPFormula(self, new_formula):
        self.experience.setFormula(new_formula)

    def update(self):
        # This is what should be used to update a character's stats at the end
        # of a turn

        # Set base values from level
        base_health = (self.level * 100)
        base_mana = 1000 + (self.level * 10)
        base_attack = (self.level * 10)
        base_defense = (self.level * 10)
        base_spellpower = (self.level * 10)

        # Add Item stats
        for stat, value in self.loadout.getStats().items():
            if (stat == ItemStatType.ATTACK.value): base_attack += value
            elif (stat == ItemStatType.DEFENSE.value): base_defense += value
            elif (stat == ItemStatType.SPELLPOWER.value): base_spellpower += value
            elif (stat == ItemStatType.HEALTH.value): base_health += value
            elif (stat == ItemStatType.MANA.value): base_mana += value
       


        # Augment base stats with buffs
        # extra_health_flat = self.getBonuses(EffectType.HEALTH_FLAT)
        # extra_health_pct = 1 + self.getBonuses(EffectType.HEALTH_PCT)
        # new_max_health = (base_health + extra_health_flat) * extra_health_pct

        # extra_mana_flat = self.getBonuses(EffectType.MANA_FLAT)
        # extra_mana_pct = 1 + self.getBonuses(EffectType.MANA_PCT)
        # new_max_mana = (base_mana + extra_mana_flat) * extra_mana_pct

        # Manage buff status
        #self.buff_bonuses = self.buffs.calculate().update(self.debuffs.calculate())
        #self.buffs.update()
        #self.debuffs.update()

        # Set Values
        self.health.setMaxValue(base_health)
        self.mana.setMaxValue(base_mana)
        self.attack = base_attack
        self.defense = base_defense
        self.spellpower = base_spellpower



       


        