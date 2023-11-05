from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.VisualEntity import VisualEntity

class Animation(VisualEntity):
    images:list[ImageEntity]
    paths:list[str]
    currentImage:int
    keepQuality:bool

    def __init__(self, name = "Default_Name", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], files = [], keepQuality = True):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.currentImage = 0
        self.images = []
        counter = 0 
        for file in files:
            self.images.append(ImageEntity(f"Image{counter}", True, 0, 0, 0, 0, [], file, keepQuality))
            counter += 1
    
    def updateImages(self, files):
        counter = 0
        if (len(files) == len(self.images)):
            for file in files:
                self.images[counter].updateImg(file)
        else:
            self.images = []
            for file in files:
                self.images.append(ImageEntity(f"Image{counter}", True, self.xPosition, self.yPosition, self.width, self.height, [], file, self.keepQuality))
                counter += 1

    def getImage(self):
        self.currentImage = (self.currentImage+1)%len(self.images)
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
