from model.character.Character import Character
from view.visualentity.DynamicStatEntity import DynamicStatEntity
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.TextEntity import TextEntity

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
    isShowing = True

    def __init__(self, character):
        self.character = character
        self.img = ImageEntity(character.name + "img", True, 0, 0, 0, 0, [], character.img)
        self.level = TextEntity("text", True, 0, 0, 0, 0, [], str(character.level), "mono", 10, "black", None)
        self.name = TextEntity("text", True, 0, 0, 0, 0, [], character.name, "mono", 10, "black", None)
        self.maxHealth = TextEntity("text", True, 0, 0, 0, 0, [], str(character.health.getMaxValue()), "mono", 10, "black", None)
        self.maxMana = TextEntity("text", True, 0, 0, 0, 0, [], str(character.mana.getMaxValue()), "mono", 10, "black", None)
        self.atk = TextEntity("text", True, 0, 0, 0, 0, [], str(character.attack()), "mono", 10, "black", None)
        self.defense = TextEntity("text", True, 0, 0, 0, 0, [], str(character.defense()), "mono", 10, "black", None)
        self.spellPower = TextEntity("text", True, 0, 0, 0, 0, [], str(character.spellpower()), "mono", 10, "black", None)
        self.isShowing = True
        

    def getItems(self):
        return [self.img, self.level, self.name, self.maxHealth, self.maxMana, self.atk, self.defense, self.spellPower]

    def scale(self, screenX, screenY):
        self.level.scale(screenX, screenY)
        self.name.scale(screenX, screenY)
        self.img.scale(screenX, screenY)
        self.maxHealth.scale(screenX, screenY)
        self.maxMana.scale(screenX, screenY)
        self.atk.scale(screenX, screenY)
        self.defense.scale(screenX, screenY)
        self.spellPower.scale(screenX, screenY)
    
    def changeCharacter(self, character):
        if (character == None):
            self.level.isShowing = False
            self.name.isShowing = False
            self.img.isShowing = False
            self.maxHealth.isShowing = False
            self.maxMana.isShowing = False
            self.atk.isShowing = False
            self.defense.isShowing = False
            self.spellPower.isShowing = False
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
        self.img.updateImg(character.img)
        self.maxHealth.updateText("HP " + str(character.health.getMaxValue()))
        self.maxMana.updateText("Mana " + str(character.mana.getMaxValue()))
        self.atk.updateText("ATK " + str(character.attack()))
        print(character.attack())
        self.defense.updateText("DEF " + str(character.defense()))
        self.spellPower.updateText("SP " + str(character.spellpower()))
    
    def updateCharacter(self):
        self.changeCharacter(self.character)

    @staticmethod
    def createFrom(json_object, character):
        newObject = InventoryCharacterEntity(character)
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
        return newObject
    