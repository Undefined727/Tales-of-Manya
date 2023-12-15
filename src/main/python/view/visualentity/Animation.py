from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.VisualEntity import VisualEntity
import os

class Animation(VisualEntity):
    images:list[ImageEntity]
    paths:list[str]
    currentImage:int
    delay:int
    currentDelayPosition:int
    keepQuality:bool
    playOnce:bool

    def __init__(self, name = "Default_Name", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], imageFolder = "nekoarc", delay = 5, keepQuality = True, playOnce = False):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.keepQuality = keepQuality
        self.playOnce = playOnce
        self.delay = delay
        self.currentImage = 0
        self.currentDelayPosition = 0
        self.images = []
        files = os.listdir(os.path.join(os.path.abspath("."), f"src\\main\\python\\sprites\\animations\\{imageFolder}"))
        counter = 0 
        for file in files:
            self.images.append(ImageEntity(f"Image{counter}", True, 0, 0, 0, 0, [], f"animations/{imageFolder}/{file}", keepQuality))
            counter += 1
    
    def updateImages(self, imageFolder):
        files = os.listdir(os.path.join(os.path.abspath("."), f"src\\main\\python\\sprites\\animations\\{imageFolder}"))
        counter = 0
        if (len(files) == len(self.images)):
            for file in files:
                self.images[counter].updateImg(f"animations/{imageFolder}/{file}")
        else:
            self.images = []
            for file in files:
                self.images.append(ImageEntity(f"Image{counter}", True, self.xPosition, self.yPosition, self.width, self.height, [], f"animations/{imageFolder}/{file}", self.keepQuality))
                counter += 1
            for image in self.images:
                image.resize(self.width, self.height)

    def getImage(self):
        if (self.currentDelayPosition >= 0): 
            self.currentDelayPosition -= 1
            return self.images[self.currentImage]
        else:
            self.currentImage = (self.currentImage+1)%len(self.images)
            if (self.currentImage == 0 and self.playOnce == True):
                self.currentImage = -1
                return self.images[len(self.images) - 1]
            self.currentDelayPosition = self.delay
            return self.images[self.currentImage]


    def resize(self, width, height):
        self.width = width
        self.height = height
        for image in self.images:
            image.resize(width, height)

    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition
        for image in self.images:
            image.reposition(xPosition, yPosition)

    def scale(self, screenX, screenY):
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)
        self.resize(self.width*screenX, self.height*screenY)

    @staticmethod
    def createFrom(json_object):
        newObject = Animation()
        newObject.__dict__.update(json_object)
        newObject.updateImages(newObject.paths)
        return newObject
