from model.openworld.openWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle
from model.openworld.Rectangle import Rectangle

class PlayerInteractionObject:
    worldObject:OpenWorldEntity


    def __init__(self, position):
        self.worldObject = OpenWorldEntity("emptyimg.png", Circle(position, 1.5), "interact", None)

    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)

    def getSprite(self):
        return self.worldObject.getSprite()
    
    def getImagePosition(self):
        return self.worldObject.getImagePosition()