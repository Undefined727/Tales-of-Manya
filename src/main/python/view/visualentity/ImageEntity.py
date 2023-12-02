from view.visualentity.VisualEntity import VisualEntity
import pygame

class ImageEntity(VisualEntity):
    img = pygame.image.load("src/main/python/sprites/" + "nekoarc.png")
    path = "nekoarc.png"
    keepQuality = False

    def __init__(self, name = "Default_Image", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], path = "nekoarc.png", keepQuality = False):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        try:
            self.img = pygame.image.load(f"src/main/python/sprites/{path}")
        except:
            self.img = pygame.image.load("src/main/python/sprites/nekoarc.png")
        self.keepQuality = keepQuality

    def updateImg(self, path):
        self.path = path
        try:
            self.img = pygame.image.load(f"src/main/python/sprites/{path}")
        except:
            self.img = pygame.image.load("src/main/python/sprites/nekoarc.png")
        if self.keepQuality: self.img = pygame.transform.smoothscale(self.img, (self.width, self.height))
        else: self.img = pygame.transform.scale(self.img, (self.width, self.height))
        

    def resize(self, width, height):
        self.width = width
        self.height = height
        if (width > 1 and height > 1):
            if self.keepQuality: self.img = pygame.transform.smoothscale(self.img, (self.width, self.height))
            else: self.img = pygame.transform.scale(self.img, (self.width, self.height))

    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition

    def scale(self, screenX, screenY):
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)
        self.resize(self.width*screenX, self.height*screenY)
        if (self.width > 1 and self.height > 1):
            if self.keepQuality: self.img = pygame.transform.smoothscale(self.img, (self.width, self.height))
            else: self.img = pygame.transform.scale(self.img, (self.width, self.height))
        


    @staticmethod
    def createFrom(json_object):
        newObject = ImageEntity()
        newObject.__dict__.update(json_object)
        try:
             newObject.img = pygame.image.load(f"src/main/python/sprites/{newObject.path}")
        except:
             newObject.img = pygame.image.load("src/main/python/sprites/nekoarc.png")
        return newObject