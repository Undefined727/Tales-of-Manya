from view.visualentity.VisualEntity import VisualEntity
from view.visualentity.ShapeEntity import ShapeEntity

class ShapeButton(VisualEntity):
    func = None
    args = None
    shapeEntity = None
    color = None
    isBorder = None
    shape = None
    isActive = True

    def __init__(self, name = "Default_Button", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], color = "Blue", isBorder = False, shape = "ellipse", func = None, args = [], isActive = True):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        self.shapeEntity = ShapeEntity("Button_Shape", isShowing, xPosition, yPosition, width, height, tags, color, isBorder, shape)
        self.color = color
        self.isBorder = isBorder
        self.shape = shape
        self.isActive = isActive

    def mouseInRegion(self, mouse):
        if (self.shapeEntity.shape == "rectangle"):
            return (self.xPosition <= mouse[0] <= self.xPosition+self.width and self.yPosition <= mouse[1] <= self.yPosition+self.height)
        elif (self.shapeEntity.shape == "ellipse"):
            return ((mouse[0]-(self.xPosition+self.width/2))*(mouse[0]-(self.xPosition+self.width/2)) + (self.width/self.height)*(self.width/self.height)*(mouse[1]-(self.yPosition+self.height/2))*(mouse[1]-(self.yPosition+self.height/2)) < ((self.width/2)*(self.width/2)))

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.shapeEntity.resize(width, height)

    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.shapeEntity.reposition(xPosition, yPosition)

    def scale(self, screenX, screenY):
        self.reposition(self.xPosition, self.yPosition)
        self.resize(self.width, self.height)
        self.shapeEntity.scale(screenX, screenY)
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)
        self.resize(self.width*screenX, self.height*screenY)
    
    def buttonVisual(self):
        return self.shapeEntity

    @staticmethod
    def createFrom(json_object):
        newObject = ShapeButton()
        newObject.__dict__.update(json_object)
        newObject.shapeEntity = ShapeEntity("Button_Shape", newObject.isShowing, newObject.xPosition, newObject.yPosition, newObject.width, newObject.height, newObject.tags, newObject.color, newObject.isBorder, newObject.shape)
        return newObject