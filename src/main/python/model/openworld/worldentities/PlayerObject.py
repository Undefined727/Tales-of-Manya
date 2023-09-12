from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle

class PlayerObject:
    worldObject:OpenWorldEntity


    def __init__(self, position):
        self.worldObject = OpenWorldEntity("catgirl_head.png", Circle(position, 0.425), "player", "enemy")

    def setCenter(self, point):
        self.worldObject.setCenter(point)
    
    def getCenter(self):
        return self.worldObject.getCenter()

    def move(self, diff):
        self.worldObject.move(diff)

    def getSprite(self):
        return self.worldObject.getSprite()
    
    def getImagePosition(self):
        return self.worldObject.getImagePosition()