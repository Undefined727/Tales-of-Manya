from model.character.Character import Character
from model.visualentity.DynamicStatEntity import DynamicStatEntity
from model.visualentity.ImageEntity import ImageEntity

class CharacterEntities:

    HPBar:DynamicStatEntity
    ManaBar:DynamicStatEntity
    img:ImageEntity
    headImg:ImageEntity
    checkmark:ImageEntity
    character:Character

    def __init__(self, character):
        self.character = character
        self.HPBar = DynamicStatEntity(character.health, "health")
        self.ManaBar = DynamicStatEntity(character.mana, "mana")
        self.img = ImageEntity(character.name + "img", True, 0, 0, 0, 0, [], character.img)
        self.headImg = ImageEntity(character.name + "headImg", True, 0, 0, 0, 0, [], character.headImg)
        self.checkmark = ImageEntity(character.name + "checkmark", True, 0, 0, 0, 0, [], "Checkmark.png")

    def getItems(self):
        return [self.img, self.headImg, self.HPBar, self.ManaBar, self.checkmark]

    def scale(self, screenX, screenY):
        self.HPBar.scale(screenX, screenY)
        self.ManaBar.scale(screenX, screenY)
        self.img.scale(screenX, screenY)
        self.headImg.scale(screenX, screenY)
        self.checkmark.scale(screenX, screenY)
    
    def changeCharacter(self, character):
        if (character == None):
            self.HPBar.isShowing = False
            self.ManaBar.isShowing = False
            self.img.isShowing = False
            self.headImg.isShowing = False
            self.checkmark.isShowing = False
            return

        self.character = character
        self.HPBar.changeStat(character.health, "health")
        self.ManaBar.changeStat(character.mana, "mana")
        self.img.updateImg(character.img)
        self.headImg.updateImg(character.headImg)
        self.checkmark.isShowing = not character.hasActed
    
    def updateCharacter(self):
        self.HPBar.updateItems()
        self.ManaBar.updateItems()
        self.checkmark.isShowing = not self.character.hasActed

    @staticmethod
    def createFrom(json_object, character):
        newObject = CharacterEntities(character)
        if ("HPXPosition" in json_object):
            newObject.HPBar.reposition(json_object["HPXPosition"], json_object["HPYPosition"])
            newObject.HPBar.resize(json_object["HPWidth"], json_object["HPHeight"])
        else: newObject.HPBar.isShowing = False
        if ("ManaXPosition" in json_object):
            newObject.ManaBar.reposition(json_object["ManaXPosition"], json_object["ManaYPosition"])
            newObject.ManaBar.resize(json_object["ManaWidth"], json_object["ManaHeight"])
        else: newObject.ManaBar.isShowing = False
        if ("imgXPosition" in json_object):
            newObject.img.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
            newObject.img.resize(json_object["imgWidth"], json_object["imgHeight"])
        else: newObject.img.isShowing = False
        if ("headImgXPosition" in json_object):
            newObject.headImg.reposition(json_object["headImgXPosition"], json_object["headImgYPosition"])
            newObject.headImg.resize(json_object["headImgWidth"], json_object["headImgHeight"])
        else: newObject.headImg.isShowing = False
        if ("checkmarkXPosition" in json_object):
            newObject.checkmark.reposition(json_object["checkmarkXPosition"], json_object["checkmarkYPosition"])
            newObject.checkmark.resize(json_object["checkmarkWidth"], json_object["checkmarkHeight"])
        else: newObject.checkmark.isShowing = False
        return newObject
    