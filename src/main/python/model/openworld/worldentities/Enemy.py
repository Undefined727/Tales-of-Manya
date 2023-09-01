from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle
from model.character.Character import Character

class Enemy:
    id:int
    spawnX:int
    spawnY:int
    respawnTimer:int
    worldObject:OpenWorldEntity
    enemyStats:Character

    # In the future img and id will be connected directly using a database and thus dialogue will no longer be required for initialization
    def __init__(self, enemyID, level, img, position, respawnTimer):
        self.enemyStats = Character(enemyID, img, level)
        self.spawnX, self.spawnY = position
        self.respawnTimer = respawnTimer
        self.id = enemyID
        self.worldObject = OpenWorldEntity(img, Circle((self.spawnX, self.spawnY), 0.5), "enemy", "attack")

    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)