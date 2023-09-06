from view.visualentity.ShapeButton import ShapeButton
from view.visualentity.ShapeEntity import ShapeEntity

class HoverShapeButton(ShapeButton):
    primaryColor:str
    secondaryColor:str

    def __init__(self, name = "Default_Button", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], color = "Blue", secondaryColor = "cyan", shape = "ellipse", func = None, args = [], isActive = True):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags, color, False, shape, func, args, isActive)
        self.primaryColor = color
        self.secondaryColor = secondaryColor
        self.shapeEntity.color = color

    def mouseInRegion(self, mouse):
        inRegion = super().mouseInRegion(mouse)
        if (inRegion and (self.shapeEntity.color == self.primaryColor)): 
            self.shapeEntity.color = self.secondaryColor
        elif ((not inRegion) and (self.shapeEntity.color == self.secondaryColor)): 
            self.shapeEntity.color = self.primaryColor
        return inRegion

    @staticmethod
    def createFrom(json_object):
        newObject = HoverShapeButton()
        newObject.__dict__.update(json_object)
        newObject.shapeEntity = ShapeEntity("Button_Shape", newObject.isShowing, newObject.xPosition, newObject.yPosition, newObject.width, newObject.height, newObject.tags, newObject.primaryColor, False, newObject.shape)
        return newObject