from view.visualentity.VisualEntity import VisualEntity

class ButtonEntity(VisualEntity):
    func = None
    args = None
    shape = None

    def __init__(self, name = "Default_Button", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], shape = None, func = None, *args):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        self.shape = shape

    def mouseInRegion(self, mouse):
        if (self.shape == "rectangle"):
            return (self.xPosition <= mouse[0] <= self.xPosition+self.width and self.yPosition <= mouse[1] <= self.yPosition+self.height)
        elif (self.shape == "ellipse"):
            return ((mouse[0]-(self.xPosition+self.width/2))*(mouse[0]-(self.xPosition+self.width/2)) + (self.width/self.height)*(self.width/self.height)*(mouse[1]-(self.yPosition+self.height/2))*(mouse[1]-(self.yPosition+self.height/2)) < ((self.width/2)*(self.width/2)))

    def resize(self, width, height):
        self.width = width
        self.height = height

    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition

    @staticmethod
    def createFrom(json_object):
        newObject = ButtonEntity()
        newObject.__dict__.update(json_object)
        return newObject