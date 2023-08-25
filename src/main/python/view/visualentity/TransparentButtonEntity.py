from PIL import Image
from src.main.python.model.visualentity.VisualEntity import VisualEntity
import numpy

class TransparentButtonEntity(VisualEntity):
    func = None
    args = None
    img = None
    path = "nekoarc.png"

    def __init__(self, name = "Default_Transparent_Button", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], path = "nekoarc.png", func = None, *args):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        self.img = Image.open("../sprites/" + path)
        

    def mouseInRegion(self, mouse):
        npArray = numpy.asarray(self.img)
        x = int(mouse[0]-self.xPosition)
        y = int(mouse[1]-self.yPosition)
        if (x >= 0 and x < int(self.width) and y >= 0 and y < int(self.length)): 
            transparency = npArray[y, x, 3]
            if (transparency != 0): return True
        return False
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.img = self.img.resize(self.width, self.height)

    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition

    @staticmethod
    def createFrom(json_object):
        newObject = TransparentButtonEntity()
        newObject.__dict__.update(json_object)
        return newObject