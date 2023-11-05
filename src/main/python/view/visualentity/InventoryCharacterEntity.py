from model.character.Character import Character
from view.visualentity.DynamicStatEntity import DynamicStatEntity
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.TextEntity import TextEntity
from model.item.ItemSlotType import ItemSlotType

class InventoryCharacterEntity:

    #levelBar:DynamicStatEntity
    img:ImageEntity
    level:TextEntity
    name:TextEntity
    maxHealth:TextEntity
    maxMana:TextEntity
    atk:TextEntity
    defense:TextEntity
    spellpower:TextEntity
    character:Character

    headImg:ImageEntity
    chestImg:ImageEntity
    waistImg:ImageEntity
    legsImg:ImageEntity
    weaponImg:ImageEntity
    accessory1Img:ImageEntity
    accessory2Img:ImageEntity
    isShowing:bool

    def __init__(self):
        self.character = None
        self.isShowing = True
        self.img = ImageEntity("characterImg", True, 0, 0, 0, 0, [], "nekoarc.png", True)
        self.level = TextEntity("text", True, 0, 0, 0, 0, [], "lvl", "mono", 10, "black", None)
        self.name = TextEntity("text", True, 0, 0, 0, 0, [], "name", "mono", 10, "black", None)
        self.maxHealth = TextEntity("text", True, 0, 0, 0, 0, [], "727", "mono", 10, "black", None)
        self.maxMana = TextEntity("text", True, 0, 0, 0, 0, [], "727", "mono", 10, "black", None)
        self.atk = TextEntity("text", True, 0, 0, 0, 0, [], "727", "mono", 10, "black", None)
        self.defense = TextEntity("text", True, 0, 0, 0, 0, [], "727", "mono", 10, "black", None)
        self.spellPower = TextEntity("text", True, 0, 0, 0, 0, [], "727", "mono", 10, "black", None)
        self.headImg = ImageEntity("img", True, 0, 0, 0, 0, [], "items/helmet_transparent.png", True)
        self.chestImg = ImageEntity("img", True, 0, 0, 0, 0, [], "items/chestplate_transparent.png", True)
        self.waistImg = ImageEntity("img", True, 0, 0, 0, 0, [], "items/leggings_transparent.png", True)
        self.legsImg = ImageEntity("img", True, 0, 0, 0, 0, [], "items/waist_transparent.png", True)
        self.weaponImg = ImageEntity("img", True, 0, 0, 0, 0, [], "items/weapon_transparent.png", True)
        self.accessory1Img = ImageEntity("img", True, 0, 0, 0, 0, [], "items/accessory_transparent.png", True)
        self.accessory2Img = ImageEntity("img", True, 0, 0, 0, 0, [], "items/accessory2_transparent.png", True)
        

    def getItems(self):
        gearList = [self.headImg, self.chestImg, self.waistImg, self.legsImg, self.weaponImg, self.accessory1Img, self.accessory2Img]
        statList = [self.maxHealth, self.maxMana, self.atk, self.defense, self.spellPower]
        charInfoList = [self.img, self.level, self.name]
        return charInfoList + gearList + statList

    def scale(self, screenX, screenY):
        self.level.scale(screenX, screenY)
        self.name.scale(screenX, screenY)
        self.img.scale(screenX, screenY)
        self.maxHealth.scale(screenX, screenY)
        self.maxMana.scale(screenX, screenY)
        self.atk.scale(screenX, screenY)
        self.defense.scale(screenX, screenY)
        self.spellPower.scale(screenX, screenY)
        self.headImg.scale(screenX, screenY)
        self.chestImg.scale(screenX, screenY)
        self.waistImg.scale(screenX, screenY)
        self.legsImg.scale(screenX, screenY)
        self.weaponImg.scale(screenX, screenY)
        self.accessory1Img.scale(screenX, screenY)
        self.accessory2Img.scale(screenX, screenY)
    
    def changeCharacter(self, character:Character):
        if (character == None):
            self.level.isShowing = False
            self.name.isShowing = False
            self.img.isShowing = False
            self.maxHealth.isShowing = False
            self.maxMana.isShowing = False
            self.atk.isShowing = False
            self.defense.isShowing = False
            self.spellPower.isShowing = False
            self.headImg.isShowing = False
            self.chestImg.isShowing = False
            self.waistImg.isShowing = False
            self.legsImg.isShowing = False
            self.weaponImg.isShowing = False
            self.accessory1Img.isShowing = False
            self.accessory2Img.isShowing = False
            return

        self.character = character
        self.level.fontSize = (int(self.level.width/10))
        self.name.fontSize = (int(self.level.width/10))
        self.maxHealth.fontSize = (int(self.level.width/10))
        self.maxMana.fontSize = (int(self.level.width/10))
        self.atk.fontSize = (int(self.level.width/10))
        self.defense.fontSize = (int(self.level.width/10))
        self.spellPower.fontSize = (int(self.level.width/10))
        self.level.updateText("Level " + str(character.level))
        self.name.updateText(character.name)
        self.img.updateImg(f"entities/{character.img}")
        self.maxHealth.updateText("HP " + str(character.health.getMaxValue()))
        self.maxMana.updateText("Mana " + str(character.mana.getMaxValue()))
        self.atk.updateText("ATK " + str(character.attack))
        self.defense.updateText("DEF " + str(character.defense))
        self.spellPower.updateText("SP " + str(character.spellpower))

        if (character.loadout.slots[ItemSlotType.HEAD.value] == None): self.headImg.updateImg("items/helmet_transparent.png")
        else: self.headImg.updateImg("items/" + character.loadout.slots[ItemSlotType.HEAD.value].image_path)
        if (character.loadout.slots[ItemSlotType.CHEST.value] == None): self.chestImg.updateImg("items/chestplate_transparent.png")
        else: self.chestImg.updateImg("items/" + character.loadout.slots[ItemSlotType.CHEST.value].image_path)
        if (character.loadout.slots[ItemSlotType.LEGS.value] == None): self.legsImg.updateImg("items/leggings_transparent.png")
        else: self.legsImg.updateImg("items/" + character.loadout.slots[ItemSlotType.LEGS.value].image_path)
        if (character.loadout.slots[ItemSlotType.WAIST.value] == None): self.waistImg.updateImg("items/waist_transparent.png")
        else: self.waistImg.updateImg("items/" + character.loadout.slots[ItemSlotType.WAIST.value].image_path)
        if (character.loadout.slots[ItemSlotType.WEAPON.value] == None): self.weaponImg.updateImg("items/weapon_transparent.png")
        else: self.weaponImg.updateImg("items/" + character.loadout.slots[ItemSlotType.WEAPON.value].image_path)
        if (character.loadout.slots[ItemSlotType.ACCESSORY1.value] == None): self.accessory1Img.updateImg("items/accessory_transparent.png")
        else: self.accessory1Img.updateImg("items/" + character.loadout.slots[ItemSlotType.ACCESSORY1.value].image_path)
        if (character.loadout.slots[ItemSlotType.ACCESSORY2.value] == None): self.accessory2Img.updateImg("items/accessory2_transparent.png")
        else: self.accessory2Img.updateImg("items/" + character.loadout.slots[ItemSlotType.ACCESSORY2.value].image_path)

    
    def updateCharacter(self):
        self.changeCharacter(self.character)

    @staticmethod
    def createFrom(json_object):
        newObject = InventoryCharacterEntity()
        newObject.level.reposition(json_object["levelXPosition"], json_object["levelYPosition"])
        newObject.level.resize(json_object["levelWidth"], json_object["levelHeight"])
        newObject.name.reposition(json_object["nameXPosition"], json_object["nameYPosition"])
        newObject.name.resize(json_object["nameWidth"], json_object["nameHeight"])
        newObject.img.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
        newObject.img.resize(json_object["imgWidth"], json_object["imgHeight"])
        newObject.maxHealth.reposition(json_object["HPXPosition"], json_object["HPYPosition"])
        newObject.maxHealth.resize(json_object["HPWidth"], json_object["HPHeight"])
        newObject.maxMana.reposition(json_object["ManaXPosition"], json_object["ManaYPosition"])
        newObject.maxMana.resize(json_object["ManaWidth"], json_object["ManaHeight"])
        newObject.defense.reposition(json_object["DEFXPosition"], json_object["DEFYPosition"])
        newObject.defense.resize(json_object["DEFWidth"], json_object["DEFHeight"])
        newObject.atk.reposition(json_object["ATKXPosition"], json_object["ATKYPosition"])
        newObject.atk.resize(json_object["ATKWidth"], json_object["ATKHeight"])
        newObject.spellPower.reposition(json_object["spellPowerXPosition"], json_object["spellPowerYPosition"])
        newObject.spellPower.resize(json_object["spellPowerWidth"], json_object["spellPowerHeight"])
        newObject.headImg.reposition(json_object["headSlotXPosition"], json_object["headSlotYPosition"])
        newObject.headImg.resize(json_object["gearSlotWidth"], json_object["gearSlotHeight"])
        newObject.chestImg.reposition(json_object["chestSlotXPosition"], json_object["chestSlotYPosition"])
        newObject.chestImg.resize(json_object["gearSlotWidth"], json_object["gearSlotHeight"])
        newObject.waistImg.reposition(json_object["waistSlotXPosition"], json_object["waistSlotYPosition"])
        newObject.waistImg.resize(json_object["gearSlotWidth"], json_object["gearSlotHeight"])
        newObject.legsImg.reposition(json_object["legsSlotXPosition"], json_object["legsSlotYPosition"])
        newObject.legsImg.resize(json_object["gearSlotWidth"], json_object["gearSlotHeight"])
        newObject.weaponImg.reposition(json_object["weaponSlotXPosition"], json_object["weaponSlotYPosition"])
        newObject.weaponImg.resize(json_object["gearSlotWidth"], json_object["gearSlotHeight"])
        newObject.accessory1Img.reposition(json_object["accessory1SlotXPosition"], json_object["accessory1SlotYPosition"])
        newObject.accessory1Img.resize(json_object["gearSlotWidth"], json_object["gearSlotHeight"])
        newObject.accessory2Img.reposition(json_object["accessory2SlotXPosition"], json_object["accessory2SlotYPosition"])
        newObject.accessory2Img.resize(json_object["gearSlotWidth"], json_object["gearSlotHeight"])
        return newObject
    