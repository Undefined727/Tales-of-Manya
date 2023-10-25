from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ShapeEntity import ShapeEntity
from model.character.Character import Character
from view.visualentity.HoverShapeButton import HoverShapeButton

class CombatCharacterEntity:

    character:Character
    isEnemy:False
    isSelected:False

    characterImg:ImageEntity
    characterCheckmark:ImageEntity

    characterHPBarBorder:ImageEntity
    characterHPBarGreen:ShapeEntity
    characterHPBarRed:ShapeEntity
    characterHPBarText:TextEntity
    characterManaBarBorder:ImageEntity
    characterManaBarBlue:ShapeEntity
    characterManaBarRed:ShapeEntity
    characterManaBarText:TextEntity

    selectionButton:HoverShapeButton

    def __init__(self):
       self.character = None
       self.characterImg = ImageEntity("img", True, 0, 0, 0, 0, [], "nekoarc.png")
       self.characterCheckmark = ImageEntity("checkmark", True, 0, 0, 0, 0, [], "nekoarc.png")
       self.characterHPBarBorder = ImageEntity("HPBorder", True, 0, 0, 0, 0, [], "HPBar.png")
       self.characterHPBarRed = ShapeEntity("HPRed", True, 0, 0, 0, 0, [], "red", False, "rectangle")
       self.characterHPBarGreen = ShapeEntity("HPGreen", True, 0, 0, 0, 0, [], "green", False, "rectangle")
       self.characterHPBarText = TextEntity("HPText", True, 0, 0, 0, 0, [], "0/0", "mono", 10, "black", None)
       self.characterManaBarBorder = ImageEntity("ManaBorder", True, 0, 0, 0, 0, [], "HPBar.png")
       self.characterManaBarRed = ShapeEntity("ManaRed", True, 0, 0, 0, 0, [], "red", False, "rectangle")
       self.characterManaBarBlue = ShapeEntity("ManaBlue", True, 0, 0, 0, 0, [], "blue", False, "rectangle")
       self.characterManaBarText = TextEntity("ManaText", True, 0, 0, 0, 0, [], "0/0", "mono", 10, "black", None)
       self.selectionButton = HoverShapeButton("Selection_Button", True, 0, 0, 0,  0, [], "Blue", "cyan", "ellipse", "characterSelection", [self], True)

    def getItems(self):
        hpBar = [self.characterHPBarBorder, self.characterHPBarRed, self.characterHPBarGreen, self.characterHPBarText]
        manaBar = [self.characterManaBarBorder, self.characterManaBarRed, self.characterManaBarBlue, self.characterManaBarText]
        characterVisuals = [self.characterImg + self.characterCheckmark]
        return hpBar + manaBar + characterVisuals
    
    def getButtons(self):
        return None

    def scale(self, screenX, screenY):
        self.characterImg.scale(screenX, screenY)
        self.characterCheckmark.scale(screenX, screenY)
        self.characterHPBarBorder.scale(screenX, screenY)
        self.characterHPBarRed.scale(screenX, screenY)
        self.characterHPBarGreen.scale(screenX, screenY)
        self.characterHPBarText.scale(screenX, screenY)
        self.characterManaBarBorder.scale(screenX, screenY)
        self.characterManaBarRed.scale(screenX, screenY)
        self.characterManaBarBlue.scale(screenX, screenY)
        self.characterManaBarText.scale(screenX, screenY)

    def changeCharacter(self, character:Character, isEnemy:bool):
        self.isEnemy = isEnemy
        if (character == None):
            self.characterImg.isShowing = False
            self.characterCheckmark.isShowing = False
            self.characterHPBarBorder.isShowing = False
            self.characterHPBarRed.isShowing = False
            self.characterHPBarGreen.isShowing = False
            self.characterHPBarText.isShowing = False
            self.characterManaBarBorder.isShowing = False
            self.characterManaBarRed.isShowing = False
            self.characterManaBarBlue.isShowing = False
            self.characterManaBarText.isShowing = False
            return

        self.characterImg.updateImg(character.img)
        self.characterCheckmark.isShowing = character.hasActed
        self.characterHPBarGreen.width = self.characterHPBarRed.width * (character.health.current_value/character.health.max_value)
        self.characterManaBarBlue.width = self.characterManaBarRed.width * (character.mana.current_value/character.mana.max_value)
        self.characterHPBarText.updateText(f"{character.health.current_value}/{character.health.max_value}")
        self.characterManaBarText.updateText(f"{character.mana.current_value}/{character.mana.max_value}")

    def updateCharacter(self):
        self.changeCharacter(self.character, self.isEnemy)

    @staticmethod
    def createFrom(json_object):
        newObject = CombatCharacterEntity()
        newObject.characterImg.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
        newObject.characterImg.resize(json_object["imgWidth"], json_object["imgHeight"])
        newObject.characterCheckmark.reposition(json_object["checkmarkXPosition"], json_object["checkmarkYPosition"])
        newObject.characterCheckmark.resize(json_object["checkmarkWidth"], json_object["checkmarkHeight"])
        newObject.characterHPBarBorder.reposition(json_object["HPBorderXPosition"], json_object["HPBorderYPosition"])
        newObject.characterHPBarBorder.resize(json_object["BorderWidth"], json_object["BorderHeight"])
        newObject.characterHPBarRed.reposition(json_object["HPXPosition"], json_object["HPYPosition"])
        newObject.characterHPBarRed.resize(json_object["BarWidth"], json_object["BarHeight"])
        newObject.characterHPBarGreen.reposition(json_object["HPXPosition"], json_object["HPYPosition"])
        newObject.characterHPBarGreen.resize(json_object["BarWidth"], json_object["BarHeight"])
        newObject.characterHPBarText.reposition(json_object["HPXPosition"], json_object["HPYPosition"])
        newObject.characterHPBarText.resize(json_object["TextWidth"], json_object["TextHeight"])
        newObject.characterManaBarBorder.reposition(json_object["ManaBorderXPosition"], json_object["ManaBorderYPosition"])
        newObject.characterManaBarBorder.resize(json_object["BorderWidth"], json_object["BorderHeight"])
        newObject.characterManaBarRed.reposition(json_object["ManaXPosition"], json_object["ManaYPosition"])
        newObject.characterManaBarRed.resize(json_object["BarWidth"], json_object["BarHeight"])
        newObject.characterManaBarBlue.reposition(json_object["ManaXPosition"], json_object["ManaYPosition"])
        newObject.characterManaBarBlue.resize(json_object["BarWidth"], json_object["BarHeight"])
        newObject.characterManaBarText.reposition(json_object["ManaXPosition"], json_object["ManaYPosition"])
        newObject.characterManaBarText.resize(json_object["TextWidth"], json_object["TextHeight"])
        return newObject
        