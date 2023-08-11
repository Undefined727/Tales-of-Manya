from model.visualentity.VisualEntity import VisualEntity
import pygame

class ImageEntity(VisualEntity):
    img = pygame.image.load("sprites/" + "nekoarc.png")
    path = "nekoarc.png"

    def __init__(self, name = "Default_Image", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], path = "nekoarc.png"):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.img = pygame.image.load("sprites/" + path)

    def updateImg(self, path):
        self.img = pygame.image.load("sprites/" + path)
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

    def resize(self, width, height):
        self.width = width
        self.height = height

    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition

    def scale(self, screenX, screenY):
        self.img = pygame.transform.scale(self.img, (self.width*screenX, self.height*screenY))
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)
        self.resize(self.width*screenX, self.height*screenY)


    @staticmethod
    def createFrom(json_object):
        newObject = ImageEntity()
        newObject.__dict__.update(json_object)
        newObject.img = pygame.image.load("sprites/" + newObject.path)
        return newObject