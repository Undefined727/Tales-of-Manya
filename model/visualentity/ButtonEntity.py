from model.visualentity.VisualEntity import VisualEntity

class ButtonEntity(VisualEntity):
    func = None
    args = None
    shape = None

    def __init__(self, name = "Default_Button", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], shape = None, func = None, *args):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        self.shape = shape
    
    def mouseInRegion(self, mouse):
        if (self.shape == "rectangle"):
            return (self.xPosition <= mouse[0] <= self.xPosition+self.width and self.yPosition <= mouse[1] <= self.yPosition+self.length)
        elif (self.shape == "ellipse"):
            return ((mouse[0]-(self.xPosition+self.width/2))*(mouse[0]-(self.xPosition+self.width/2)) + (self.width/self.length)*(self.width/self.length)*(mouse[1]-(self.yPosition+self.length/2))*(mouse[1]-(self.yPosition+self.length/2)) < ((self.width/2)*(self.width/2)))

    @staticmethod
    def createFrom(json_object):
        newObject = ButtonEntity()
        newObject.__dict__.update(json_object)
        return newObject