from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ShapeEntity import ShapeEntity
from model.character.Character import Character
from view.visualentity.HoverShapeButton import HoverShapeButton

class CombatCharacterEntity:

    character:Character
    isEnemy:bool
    isSelected:bool
    isShowing:bool

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

    DEFAULT_VALUES = {
        "checkmarkWidth": 0.02,
        "checkmarkHeight": 0.02,
        "BorderWidth": 0.1,
        "BorderHeight": 0.07,
        "BarWidth": 0.06,
        "BarHeight": 0.02,
        "TextWidth": 0.1,
        "TextHeight": 0.07,
    }

    def __init__(self):
       self.character = None
       self.isShowing = True
       self.isEnemy = False
       self.isSelected = False
       self.characterImg = ImageEntity("img", True, 0, 0, 0, 0, [], "nekoarc.png")
       self.characterCheckmark = ImageEntity("checkmark", True, 0, 0, 0, 0, [], "Checkmark.png")
       self.characterHPBarBorder = ImageEntity("HPBorder", True, 0, 0, 0, 0, [], "HPBar.png")
       self.characterHPBarRed = ShapeEntity("HPRed", True, 0, 0, 0, 0, [], "red", False, "rectangle")
       self.characterHPBarGreen = ShapeEntity("HPGreen", True, 0, 0, 0, 0, [], "green", False, "rectangle")
       self.characterHPBarText = TextEntity("HPText", True, 0, 0, 0, 0, [], "0/0", "mono", 16, "black", None)
       self.characterManaBarBorder = ImageEntity("ManaBorder", True, 0, 0, 0, 0, [], "ManaBar.png")
       self.characterManaBarRed = ShapeEntity("ManaRed", True, 0, 0, 0, 0, [], "red", False, "rectangle")
       self.characterManaBarBlue = ShapeEntity("ManaBlue", True, 0, 0, 0, 0, [], "blue", False, "rectangle")
       self.characterManaBarText = TextEntity("ManaText", True, 0, 0, 0, 0, [], "0/0", "mono", 16, "black", None)
       self.selectionButton = HoverShapeButton("Selection_Button", True, 0, 0, 0,  0, [], "Blue", "cyan", "ellipse", "characterSelection", [self], True)

    def getItems(self):
        hpBar = [self.characterHPBarBorder, self.characterHPBarRed, self.characterHPBarGreen, self.characterHPBarText]
        manaBar = [self.characterManaBarBorder, self.characterManaBarRed, self.characterManaBarBlue, self.characterManaBarText]
        characterVisuals = [self.characterImg]
        characterUI = [self.characterCheckmark]
        if (self.isEnemy): return hpBar + characterVisuals
        return hpBar + manaBar + characterVisuals + characterUI
    
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
        self.character = character
        if (character == None): return

        self.isEnemy = isEnemy
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
        if ("imgXPosition" in json_object):
            newObject.characterImg.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
            newObject.characterImg.resize(json_object["imgWidth"], json_object["imgHeight"])
        if ("checkmarkXPosition" in json_object):
            newObject.characterCheckmark.reposition(json_object["checkmarkXPosition"], json_object["checkmarkYPosition"])
            newObject.characterCheckmark.resize(newObject.DEFAULT_VALUES["checkmarkWidth"], newObject.DEFAULT_VALUES["checkmarkHeight"])
        if ("HPBorderXPosition" in json_object):
            newObject.characterHPBarBorder.reposition(json_object["HPBorderXPosition"], json_object["HPBorderYPosition"])
            newObject.characterHPBarBorder.resize(newObject.DEFAULT_VALUES["BorderWidth"], newObject.DEFAULT_VALUES["BorderHeight"])
            newObject.characterHPBarRed.reposition(json_object["HPBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["HPBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
            newObject.characterHPBarRed.resize(newObject.DEFAULT_VALUES["BarWidth"], newObject.DEFAULT_VALUES["BarHeight"])
            newObject.characterHPBarGreen.reposition(json_object["HPBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["HPBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
            newObject.characterHPBarGreen.resize(newObject.DEFAULT_VALUES["BarWidth"], newObject.DEFAULT_VALUES["BarHeight"])
            newObject.characterHPBarText.reposition(json_object["HPBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/2, json_object["HPBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/2)
            newObject.characterHPBarText.resize(newObject.DEFAULT_VALUES["TextWidth"], newObject.DEFAULT_VALUES["TextHeight"])
        if ("ManaBorderXPosition" in json_object):
            newObject.characterManaBarBorder.reposition(json_object["ManaBorderXPosition"], json_object["ManaBorderYPosition"])
            newObject.characterManaBarBorder.resize(newObject.DEFAULT_VALUES["BorderWidth"], newObject.DEFAULT_VALUES["BorderHeight"])
            newObject.characterManaBarRed.reposition(json_object["ManaBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["ManaBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
            newObject.characterManaBarRed.resize(newObject.DEFAULT_VALUES["BarWidth"], newObject.DEFAULT_VALUES["BarHeight"])
            newObject.characterManaBarBlue.reposition(json_object["ManaBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["ManaBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
            newObject.characterManaBarBlue.resize(newObject.DEFAULT_VALUES["BarWidth"], newObject.DEFAULT_VALUES["BarHeight"])
            newObject.characterManaBarText.reposition(json_object["ManaBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/2, json_object["ManaBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/2)
            newObject.characterManaBarText.resize(newObject.DEFAULT_VALUES["TextWidth"], newObject.DEFAULT_VALUES["TextHeight"])
        return newObject
        