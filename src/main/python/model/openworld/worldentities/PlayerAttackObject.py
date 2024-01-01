from model.openworld.openWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle
from model.openworld.Rectangle import Rectangle

class PlayerAttackObject:
    id:int
    worldObject:OpenWorldEntity
    elementType:str
    attackType:str
    attackShape:str
    attackRatio:float
    swing:int
    speed:int
    duration:int
    currentDuration = 0

    def __init__(self, elementType, attackShape, attackSize, attackRatio, swingSpeed, projectileSpeed, duration, img):
        self.elementType = elementType
        self.attackShape = attackShape
        self.attackSize = attackSize
        self.attackRatio = attackRatio
        self.swingSpeed = swingSpeed
        self.projectileSpeed = projectileSpeed
        self.duration = duration
        self.currentDuration = 0
        if (attackShape == "Circle"): self.worldObject = OpenWorldEntity(img, Circle((0, 0), attackSize), "attack", None)
        elif (attackShape == "Rectangle"): self.worldObject = OpenWorldEntity(img, Rectangle([(0, 0),  (0, attackRatio*attackSize), (attackSize, 0), (attackSize, attackRatio*attackSize)]), "attack", None)
        else: self.worldObject = OpenWorldEntity(img, Circle((0, 0), attackSize), "attack", None)

    def rotate(self, angle, point):
        self.worldObject.rotate(angle, point)

    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)

    def getSprite(self):
        return self.worldObject.getSprite()

    def getImagePosition(self):
        return self.worldObject.getImagePosition()