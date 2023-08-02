from model.visualentity.VisualEntity import VisualEntity

class DrawingEntity(VisualEntity):
    color = None
    isBorder = None
    shape = None

    def __init__(self, name = "Default_Drawing", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], color = None, isBorder = None, shape = None):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.color = color
        self.isBorder = isBorder
        self.shape = shape

    @staticmethod
    def createFrom(json_object):
        newObject = DrawingEntity()
        newObject.__dict__.update(json_object)
        return newObject