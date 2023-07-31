from PIL import Image
import model.VisualEntity as VisualEntity
import numpy

class TransparentButtonEntity(VisualEntity):
    func = None
    args = None
    npArray = None

    def __init__(self, name, isShowing, xPosition, yPosition, width, height, tags, path, func, *args):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.func = func
        self.args = args
        img = Image.open("../sprites/" + path).resize(width, height)
        self.npArray = numpy.asarray(img)
