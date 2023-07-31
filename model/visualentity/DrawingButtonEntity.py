import model.VisualEntity as VisualEntity

class DrawingButtonEntity(VisualEntity):
    color = None
    isBorder = None
    shape = None

    def __init__(self, name, isShowing, xPosition, yPosition, width, height, tags, color, isBorder, shape):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.color = color
        self.isBorder = isBorder
        self.shape = shape