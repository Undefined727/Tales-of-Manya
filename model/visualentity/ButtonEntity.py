import model.VisualEntity as VisualEntity

class ButtonEntity(VisualEntity):
    func = None
    args = None
    shape = None

    def __init__(self, name = "Default_Button", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], shape = None, func = None, *args):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        self.shape = shape

    @staticmethod
    def createFrom(json_object):
        newObject = ButtonEntity()
        newObject.__dict__.update(json_object)
        return newObject