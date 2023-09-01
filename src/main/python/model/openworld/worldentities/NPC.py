from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle

class NPC:
    id:int
    spawnX:int
    spawnY:int
    worldObject:OpenWorldEntity

    dialogue = ["Test Dialogue", "Test2"]

    # In the future dialogue and id will be connected directly using a database and thus dialogue will no longer be required for initialization
    def __init__(self, dialogue, img, position, id):
        self.dialogue = dialogue
        self.spawnX, self.spawnY = position
        self.id = id
        self.worldObject = OpenWorldEntity(img, Circle((self.spawnX, self.spawnY), 0.5), "npc", "interact")
    

    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)