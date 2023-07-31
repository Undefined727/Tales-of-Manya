import model.VisualEntity as VisualEntity

class ButtonEntity(VisualEntity):
    func = None
    args = None
    shape = None

    def __init__(self, name, isShowing, xPosition, yPosition, width, height, tags, shape, func, *args):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        self.shape = shape