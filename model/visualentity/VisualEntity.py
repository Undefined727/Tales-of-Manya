class VisualEntity:
    name = "Default_Name"
    isShowing = True
    xPosition = 0
    yPosition = 0
    width = 0
    height = 0
    tags = []
    img = None

    def __init__(self, name, isShowing, xPosition, yPosition, width, height, tags):
        self.name = name
        self.isShowing = isShowing
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.width = width
        self.height = height
        self.tags = tags

    def jsonToEntity(self, object):
        self.__dict__.update(object)