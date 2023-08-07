from model.character.Character import Character
from model.visualentity.DynamicStatEntity import DynamicStatEntity
from model.visualentity.ImageEntity import ImageEntity

class CharacterEntities:

    HPBar:DynamicStatEntity
    ManaBar:DynamicStatEntity
    img:ImageEntity
    headImg:ImageEntity
    character:Character

    def __init__(self, character):
        self.character = character


        self.HPBar = DynamicStatEntity(character.health, "health")
        self.ManaBar = DynamicStatEntity(character.mana, "mana")
        self.img = ImageEntity()
        self.headImg = ImageEntity()


    def updateHPBarPlacement(self, xPosition, yPosition, width, height):
        self.HPBar.reposition(xPosition, yPosition)
        self.HPBar.resize(width, height)
    
    def updateManaBarPlacement(self, xPosition, yPosition, width, height):
        self.ManaBar.reposition(xPosition, yPosition)
        self.ManaBar.resize(width, height)
    
    def updateImgPlacement(self, xPosition, yPosition, width, height):
        self.img.reposition(xPosition, yPosition)
        self.img.resize(width, height)
    
    def updateHeadImgPlacement(self, xPosition, yPosition, width, height):
        self.headImg.reposition(xPosition, yPosition)
        self.headImg.resize(width, height)

        