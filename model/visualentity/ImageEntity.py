import model.VisualEntity as VisualEntity
import pygame

class ImageEntity(VisualEntity):
    img = None

    def __init__(self, name, isShowing, xPosition, yPosition, width, height, tags, path):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.updateImg(path)

    def updateImg(self, path):
        self.img = pygame.image.load("sprites/" + path)
        self.img = pygame.transform.scale(self.img, (self.width, self.length))