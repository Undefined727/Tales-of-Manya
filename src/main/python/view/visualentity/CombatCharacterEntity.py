from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.Animation import Animation
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ShapeEntity import ShapeEntity
from model.character.Character import Character
from view.visualentity.ShapeButton import ShapeButton

class CombatCharacterEntity:

    name:str
    tags:list

    character:Character
    isEnemy:bool
    isSelected:bool
    isShowing:bool
    damageDisplayingTimer:int
    damageTakenDisplay:list[ImageEntity]

    characterImg:ImageEntity

    selectedCharacterAnimation:Animation
    selectionButton:ShapeButton
    characterCheckmark:ImageEntity

    characterHPBarBorder:ImageEntity
    characterHPBarGreen:ShapeEntity
    characterHPBarRed:ShapeEntity
    characterHPBarText:TextEntity
    characterManaBarBorder:ImageEntity
    characterManaBarBlue:ShapeEntity
    characterManaBarRed:ShapeEntity
    characterManaBarText:TextEntity


    DEFAULT_VALUES = {
        "checkmarkWidth": 0.02,
        "checkmarkHeight": 0.02,
        "BorderWidth": 0.1,
        "BorderHeight": 0.07,
        "BarWidthMult": 0.6,
        "BarHeightMult": 0.3,
    }

    def __init__(self):
       self.name = 'CombatCharacterEntity'
       self.tags = []
       self.character = None
       self.isShowing = True
       self.isEnemy = False
       self.isSelected = False
       self.characterImg = ImageEntity("img", True, 0, 0, 0, 0, [], "nekoarc.png", True)
       self.selectedCharacterAnimation = Animation("Animation")
       self.characterCheckmark = ImageEntity("checkmark", True, 0, 0, 0, 0, [], "Checkmark.png", True)
       self.characterHPBarBorder = ImageEntity("HPBorder", True, 0, 0, 0, 0, [], "HPBar.png", True)
       self.characterHPBarRed = ShapeEntity("HPRed", True, 0, 0, 0, 0, [], "red", False, "rectangle")
       self.characterHPBarGreen = ShapeEntity("HPGreen", True, 0, 0, 0, 0, [], "green", False, "rectangle")
       self.characterHPBarText = TextEntity("HPText", True, 0, 0, 0, 0, [], "0/0", "mono", 18)
       self.characterManaBarBorder = ImageEntity("ManaBorder", True, 0, 0, 0, 0, [], "ManaBar.png", True)
       self.characterManaBarRed = ShapeEntity("ManaRed", True, 0, 0, 0, 0, [], "red", False, "rectangle")
       self.characterManaBarBlue = ShapeEntity("ManaBlue", True, 0, 0, 0, 0, [], "blue", False, "rectangle")
       self.characterManaBarText = TextEntity("ManaText", True, 0, 0, 0, 0, [], "0/0", "mono", 18)
       self.selectionButton = ShapeButton("Selection_Button", True, 0, 0, 0, 0, [], (255, 0, 0, 0), False, "rectangle", "characterSelection", [self], True)
       self.damageDisplayingTimer = -1

    def getItems(self):
        hpBar = [self.characterHPBarBorder, self.characterHPBarRed, self.characterHPBarGreen, self.characterHPBarText]
        manaBar = [self.characterManaBarBorder, self.characterManaBarRed, self.characterManaBarBlue, self.characterManaBarText]

        characterVisuals = [self.characterImg]
        characterStats = hpBar
        characterUI = [self.selectionButton]

        if (self.damageDisplayingTimer > 0):
            characterVisuals.extend(self.damageTakenDisplay)
            self.damageDisplayingTimer -= 1
        elif (self.damageDisplayingTimer == 0):
            self.damageDisplayingTimer = -1
            self.damageTakenDisplay = []
        if (self.isSelected): characterVisuals.append(self.selectedCharacterAnimation)
        if (not self.isEnemy): 
            characterUI.append(self.characterCheckmark)
            characterStats.extend(manaBar)
        return characterStats + characterVisuals + characterUI
    
    def getButtons(self):
        return self.selectionButton

    def scale(self, screenX, screenY):
        self.characterImg.scale(screenX, screenY)
        self.selectedCharacterAnimation.scale(screenX, screenY)
        self.selectionButton.scale(screenX, screenY)
        self.characterCheckmark.scale(screenX, screenY)
        self.characterHPBarBorder.scale(screenX, screenY)
        self.characterHPBarRed.scale(screenX, screenY)
        self.characterHPBarGreen.scale(screenX, screenY)
        self.characterHPBarText.scale(screenX, screenY)
        self.characterManaBarBorder.scale(screenX, screenY)
        self.characterManaBarRed.scale(screenX, screenY)
        self.characterManaBarBlue.scale(screenX, screenY)
        self.characterManaBarText.scale(screenX, screenY)


    def updateCharacter(self):
        self.character.update()
        self.characterCheckmark.isShowing = self.character.hasActed
        
        self.characterHPBarGreen.width = self.characterHPBarRed.width * (self.character.health.current_value/self.character.health.max_value)
        self.characterManaBarBlue.width = self.characterManaBarRed.width * (self.character.mana.current_value/self.character.mana.max_value)
        self.characterHPBarText.updateText(f"{self.character.health.current_value}/{self.character.health.max_value}")
        self.characterManaBarText.updateText(f"{self.character.mana.current_value}/{self.character.mana.max_value}")

    def changeCharacter(self, character:Character, isEnemy:bool):
        self.character = character
        if (character == None): return

        self.isEnemy = isEnemy
        self.characterImg.updateImg(f"entities/{character.img}")
        self.selectedCharacterAnimation.updateImages(character.selectedImg)
        self.updateCharacter()

    
    def dealDamage(self, rawDamage : float, damageType : str, target):
        realDamage = self.character.dealDamage(rawDamage, damageType)
        target.takeDamage(realDamage)

    def takeDamage(self, amount : int):
        self.damageDisplayingTimer = 20
        self.damageTakenDisplay = []
        digits = 0
        damage = self.character.takeDamage(amount)

        counter = damage
        while(counter > 0):
            digits += 1
            counter -= counter%10
            counter /= 10

        for i in range(digits):
            digit = int((damage/10**(digits-i-1))%10) 
            width = self.characterImg.width/digits
            image = ImageEntity(f"Number{i}", True, self.characterImg.xPosition + width*i, self.characterImg.yPosition, width, self.characterImg.height/4)
            image.updateImg(f"font/{digit}.png")
            self.damageTakenDisplay.append(image)


        

    @staticmethod
    def createFrom(json_object):
        newObject = CombatCharacterEntity()
        if ("imgXPosition" in json_object):
            newObject.characterImg.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
            newObject.selectionButton.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
            newObject.selectedCharacterAnimation.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
        if ("imgWidth" in json_object):
            newObject.characterImg.resize(json_object["imgWidth"], json_object["imgHeight"])
            newObject.selectionButton.resize(json_object["imgWidth"], json_object["imgHeight"])
            newObject.selectedCharacterAnimation.resize(json_object["imgWidth"], json_object["imgHeight"])
        if ("checkmarkXPosition" in json_object):
            newObject.characterCheckmark.reposition(json_object["checkmarkXPosition"], json_object["checkmarkYPosition"])
            newObject.characterCheckmark.resize(newObject.DEFAULT_VALUES["checkmarkWidth"], newObject.DEFAULT_VALUES["checkmarkHeight"])
        if ("BorderWidth" in json_object):
            if ("HPBorderXPosition" in json_object):
                newObject.characterHPBarBorder.reposition(json_object["HPBorderXPosition"], json_object["HPBorderYPosition"])
                newObject.characterHPBarRed.reposition(json_object["HPBorderXPosition"]+json_object["BorderWidth"]/5, json_object["HPBorderYPosition"]+json_object["BorderHeight"]/3)
                newObject.characterHPBarGreen.reposition(json_object["HPBorderXPosition"]+json_object["BorderWidth"]/5, json_object["HPBorderYPosition"]+json_object["BorderHeight"]/3)
                newObject.characterHPBarText.reposition(json_object["HPBorderXPosition"]+json_object["BorderWidth"]/2, json_object["HPBorderYPosition"]+json_object["BorderHeight"]/2)
            if ("ManaBorderXPosition" in json_object):
                newObject.characterManaBarBorder.reposition(json_object["ManaBorderXPosition"], json_object["ManaBorderYPosition"])
                newObject.characterManaBarRed.reposition(json_object["ManaBorderXPosition"]+json_object["BorderWidth"]/5, json_object["ManaBorderYPosition"]+json_object["BorderHeight"]/3)
                newObject.characterManaBarBlue.reposition(json_object["ManaBorderXPosition"]+json_object["BorderWidth"]/5, json_object["ManaBorderYPosition"]+json_object["BorderHeight"]/3)
                newObject.characterManaBarText.reposition(json_object["ManaBorderXPosition"]+json_object["BorderWidth"]/2, json_object["ManaBorderYPosition"]+json_object["BorderHeight"]/2)

            newObject.characterHPBarBorder.resize(json_object["BorderWidth"], json_object["BorderHeight"])
            newObject.characterManaBarBorder.resize(json_object["BorderWidth"], json_object["BorderHeight"])
            newObject.characterHPBarRed.resize(json_object["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], json_object["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterHPBarGreen.resize(json_object["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], json_object["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterHPBarText.resize(json_object["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], json_object["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterManaBarRed.resize(json_object["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], json_object["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterManaBarBlue.resize(json_object["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], json_object["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterManaBarText.resize(json_object["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], json_object["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
        else:
            if ("HPBorderXPosition" in json_object):
                newObject.characterHPBarBorder.reposition(json_object["HPBorderXPosition"], json_object["HPBorderYPosition"])
                newObject.characterHPBarRed.reposition(json_object["HPBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["HPBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
                newObject.characterHPBarGreen.reposition(json_object["HPBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["HPBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
                newObject.characterHPBarText.reposition(json_object["HPBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/2, json_object["HPBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/2)
            if ("ManaBorderXPosition" in json_object):
                newObject.characterManaBarBorder.reposition(json_object["ManaBorderXPosition"], json_object["ManaBorderYPosition"])
                newObject.characterManaBarRed.reposition(json_object["ManaBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["ManaBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
                newObject.characterManaBarBlue.reposition(json_object["ManaBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/5, json_object["ManaBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/3)
                newObject.characterManaBarText.reposition(json_object["ManaBorderXPosition"]+newObject.DEFAULT_VALUES["BorderWidth"]/2, json_object["ManaBorderYPosition"]+newObject.DEFAULT_VALUES["BorderHeight"]/2)

            newObject.characterHPBarBorder.resize(newObject.DEFAULT_VALUES["BorderWidth"], newObject.DEFAULT_VALUES["BorderHeight"])
            newObject.characterManaBarBorder.resize(newObject.DEFAULT_VALUES["BorderWidth"], newObject.DEFAULT_VALUES["BorderHeight"])
            newObject.characterHPBarRed.resize(newObject.DEFAULT_VALUES["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], newObject.DEFAULT_VALUES["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterHPBarGreen.resize(newObject.DEFAULT_VALUES["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], newObject.DEFAULT_VALUES["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterHPBarText.resize(newObject.DEFAULT_VALUES["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], newObject.DEFAULT_VALUES["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterManaBarRed.resize(newObject.DEFAULT_VALUES["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], newObject.DEFAULT_VALUES["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterManaBarBlue.resize(newObject.DEFAULT_VALUES["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], newObject.DEFAULT_VALUES["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
            newObject.characterManaBarText.resize(newObject.DEFAULT_VALUES["BorderWidth"]*newObject.DEFAULT_VALUES["BarWidthMult"], newObject.DEFAULT_VALUES["BorderHeight"]*newObject.DEFAULT_VALUES["BarHeightMult"])
        return newObject
        