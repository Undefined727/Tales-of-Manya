from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle
from model.character.Character import Character

class Enemy:
    enemyID:int
    spawnX:int
    spawnY:int
    img:str
    respawnTimer:int
    worldObject:OpenWorldEntity
    enemyStats:list[Character]

    # In the future img and id will be connected directly using a database and thus dialogue will no longer be required for initialization
    def __init__(self, enemyTypes, levels, img, position):
        if (len(position) > 1): position = tuple(position)
        self.enemyStats = []
        for i in range(0, len(enemyTypes)):
            self.enemyStats.append(Character(enemyTypes[i], "slime.png", levels[i]))
        self.spawnX, self.spawnY = position
        self.img = img
        self.respawnTimer = 0
        self.enemyID = enemyTypes[0]
        self.worldObject = OpenWorldEntity(img, Circle((self.spawnX, self.spawnY), 0.5), "enemy", "attack")

    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)

    def getSprite(self):
        return self.worldObject.getSprite()
    
    def getImagePosition(self):
        return self.worldObject.getImagePosition()