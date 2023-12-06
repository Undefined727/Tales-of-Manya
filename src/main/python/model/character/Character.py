from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from src.main.python.model.database.DatabaseModels import engine, DBCharacter
from model.character.CharacterLoadout import CharacterLoadout
from model.character.ExperienceStat import ExperienceManager
from model.character.DynamicStat import DynamicStat
#from model.effect.EffectsList import EffectsList
from model.effect.EffectType import EffectType
from model.item.ItemStatType import ItemStatType
from model.skill.Skill import Skill

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
    def __init__(self, name, description, 
                 skill1, skill2, skill3, ultimate,
                 brilliance, surge, blaze, passage, clockwork,
                 void, foundation, frost, flow, abundance,
                 basehealth, basemana, basedef, basespellpower, baseattack):

        self.name = name
        self.description = description
        self.skills = [skill1, skill2, skill3, ultimate]
        self.baseBrilliance = brilliance
        self.baseSurge = surge
        self.baseBlaze = blaze
        self.basePassage = passage
        self.baseClockwork = clockwork
        self.baseVoid = void
        self.baseFoundation = foundation
        self.baseFrost = frost
        self.baseFlow = flow
        self.baseAbundance = abundance
        self.basehealth = basehealth
        self.basemana = basemana
        self.basedef = basedef
        self.basespellpower = basespellpower
        self.baseattack = baseattack
        self.loadout    = CharacterLoadout()

        # Default Level is 1 until initialized later #
        self.level = 1
        self.health     = DynamicStat(100)
        self.mana       = DynamicStat(1000)
        self.experience = DynamicStat(100)


        self.img            = f"{self.name}.png"
        if (self.name == "Slime"): self.selectedImg = "selectedSlimeAnimation"
        else: self.selectedImg = "selectedCatgirlAnimation"
        self.overworldImg   = f"{self.name}.png"


        self.loadout_bonuses    = dict()
        self.buff_bonuses       = dict()
        self.hasActed           = False
        self.update()

    ### Getters ###

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getImage(self):
        return self.img

    def getDescription(self):
        return self.description

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

    def setID(self, new_id : int):
        self.id = new_id

    def setName(self, new_name : str):
        self.name = new_name

    def setImage(self, new_image : str):
        self.img = new_image

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
        flatHP = (20 + self.level) * self.basehealth * 100
        flatMana = self.level * self.basemana * 100
        flatAttack = self.level * self.baseattack
        flatDEF = self.level * self.basedef
        flatSP = self.level * self.basespellpower

        # Add Item stats
        for stat, value in self.loadout.getStats().items():
            if (stat == ItemStatType.ATTACK.value): flatAttack += value
            elif (stat == ItemStatType.DEFENSE.value): flatDEF += value
            elif (stat == ItemStatType.SPELLPOWER.value): flatSP += value
            elif (stat == ItemStatType.HEALTH.value): flatHP += value
            elif (stat == ItemStatType.MANA.value): flatMana += value

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
        self.health.setMaxValue(flatHP)
        self.mana.setMaxValue(flatMana)
        self.attack = flatAttack
        self.defense = flatDEF
        self.spellpower = flatSP

    ## Misc ##
    @staticmethod
    def generateID() -> int:
        with Session(engine) as session:
            query = session.query(func.max(DBCharacter.id)).all()
            max_id = query[0][0]
            return max_id + 1
