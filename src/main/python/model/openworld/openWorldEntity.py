from model.openworld.Circle import Circle
from model.openworld.Rectangle import Rectangle
import model.openworld.ShapeMath as ShapeMath
from model.character.Character import Character
import pygame

class OpenWorldEntity:
    speedX = 0
    speedY = 0

    TILE_SIZE = 48
    
    name = "default_name"
    currentHeight = 0
    shape = Circle(0, 0)
    imgPath = "nekoarc.png"
    img = pygame.image.load("sprites/nekoarc.png")
    rotImg = img
    currentRotation = 0
    # entityType replaced by some sort of enum/database later maybe
    # For now we have Grass, and Enemy for entityType
    # "data" has whatever data matches the type, so the enemy/enemies for Enemy and whatever the grass drops
    # "trigger" is the type of entity that activates the entity with whatever data is contained within it
    # This will likely be replaced with a dictionary later so different triggers can cause different effects
    entityType = "grass"
    
    trigger = "attack"

    def __init__(self, imgPath, shape, entityType, trigger):
        self.shape = shape
        self.imgPath = imgPath
        self.entityType = entityType
        self.trigger = trigger
        self.name = imgPath
        self.currentHeight = 0
        self.speedX = 0
        self.speedY = 0


        img = pygame.image.load("sprites/" + imgPath)
        imgSize = shape.getImageSize()
        imgSize = (self.TILE_SIZE * imgSize[0], self.TILE_SIZE * imgSize[1])
        self.img = pygame.transform.scale(img, imgSize)
        self.rotImg = self.img
        self.currentRotation = 0
    
    def rotate(self, angle, pivot):
        changedAngle = ShapeMath.rotate(self.shape, angle, pivot)
        self.currentRotation += changedAngle
        self.currentRotation %= 360
        self.rotImg = pygame.transform.rotate(self.img, int(-self.currentRotation))
    
    def getSprite(self):
        return self.rotImg
    
    def getImagePosition(self):
        return self.shape.getImagePosition()
    
    def getImageSize(self):
        return self.shape.getImageSize()
    
    def getCenter(self):
        return self.shape.getCenter()
    
    def setCenter(self, newCenter):
        self.shape.setCenter(newCenter)

    def move(self, diff):
        self.shape.move(diff)

    def newMoved(self, diff):
        return self.shape.newMoved(diff)
