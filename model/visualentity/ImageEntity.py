import model.VisualEntity as VisualEntity
import pygame

class ImageEntity(VisualEntity):
    img = None

    def __init__(self, name = "Default_Image", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], path = ""):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.updateImg(path)

    def updateImg(self, path):
        self.img = pygame.image.load("sprites/" + path)
        self.img = pygame.transform.scale(self.img, (self.width, self.length))

    @staticmethod
    def createFrom(json_object):
        newObject = ImageEntity()
        newObject.__dict__.update(json_object)
        return newObject