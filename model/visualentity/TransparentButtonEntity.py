from PIL import Image
import VisualEntity
import numpy

class TransparentButtonEntity(VisualEntity):
    func = None
    args = None
    npArray = None

    def __init__(self, name = "Default_Transparent_Button", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], path = "", func = None, *args):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        img = Image.open("../sprites/" + path).resize(width, height)
        self.npArray = numpy.asarray(img)

    def mouseInRegion(self, mouse):
        x = int(mouse[0]-self.xPosition)
        y = int(mouse[1]-self.yPosition)
        if (x >= 0 and x < int(self.width) and y >= 0 and y < int(self.length)): 
            transparency = self.npArray[y, x, 3]
            if (transparency != 0): return True
        return False

    @staticmethod
    def createFrom(json_object):
        newObject = TransparentButtonEntity()
        newObject.__dict__.update(json_object)
        return newObject