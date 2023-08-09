from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.TransparentButtonEntity import TransparentButtonEntity

class ButtonImageEntity:
    button:TransparentButtonEntity
    img:ImageEntity
    xPosition = 0
    yPosition = 0
    width = 0
    height = 0

    def __init__(self, xPosition, yPosition, width, height, func, args, path):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.width = width
        self.height = height
        self.button = TransparentButtonEntity("ImageButton", True, 0, 0, 0, 0, [], path, func, args)
        self.img = ImageEntity("ButtonImage", True, 0, 0, 0, 0, [], path)



    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition

    def resize(self, width, height):
        self.width = width
        self.height = height
    
    def update(self):
        self.button.reposition(self.xPosition, self.yPosition)
        self.button.resize(self.width, self.height)
        self.img.reposition(self.xPosition, self.yPosition)
        self.img.resize(self.width, self.height)
    

    
