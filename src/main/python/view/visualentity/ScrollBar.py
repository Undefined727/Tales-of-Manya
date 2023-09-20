from view.visualentity.VisualEntity import VisualEntity
from view.visualentity.HoverShapeButton import HoverShapeButton

class ScrollBar(VisualEntity):
    button:HoverShapeButton
    ratio:float
    isVertical:bool

    def __init__(self, name = "ScrollBar", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], ratio = 1, isVertical = True):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.ratio = ratio
        self.isVertical = isVertical
        if (isVertical):
            self.button = HoverShapeButton("ScrollBarButton", True, xPosition, yPosition, width, height*ratio, self.tags, "gray", (0, 80, 255, 190), "rectangle", "scroll", [name])
        else:
            self.button = HoverShapeButton("ScrollBarButton", True, xPosition, yPosition, width*ratio, height, self.tags, "gray", (0, 80, 255, 190), "rectangle", "scroll", [name])
        self.button.activatesOnHover = False

    def mouseInRegion(self, mouse):
        return self.button.mouseInRegion(mouse)

    def resize(self, width, height):
        self.width = width
        self.height = height
        if (self.isVertical): self.button.resize(width, height*self.ratio)
        else: self.button.resize(width*self.ratio, height)
    
    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.button.reposition(xPosition, yPosition)
    
    def scale(self, screenX, screenY):
        self.resize(self.width, self.height)
        self.reposition(self.xPosition, self.yPosition)
        self.button.scale(screenX, screenY)
        self.resize(self.width*screenX, self.height*screenY)
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)

    @staticmethod
    def createFrom(json_object):
        newObject = ScrollBar()
        newObject.__dict__.update(json_object)
        newObject.button = HoverShapeButton("ScrollBarButton", True, newObject.xPosition, newObject.yPosition, newObject.width, newObject.height, newObject.tags, (0, 0, 0, 0), (0, 80, 255, 190), "rectangle", "scrollBar")
        return newObject