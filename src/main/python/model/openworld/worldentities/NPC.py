from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle

class NPC:
    NPCID:int
    spawnX:int
    spawnY:int
    worldObject:OpenWorldEntity

    defaultDialogue:int
    dialogue:int
    name = "Test NPC"

    # In the future dialogue/img/name and id will be connected directly using a database and thus dialogue will no longer be required for initialization
    def __init__(self, defaultDialogue, img, position, NPCID, quests):
        self.defaultDialogue = defaultDialogue
        self.dialogue = defaultDialogue
        self.spawnX, self.spawnY = position
        self.NPCID = NPCID
        self.name = "Test NPC"
        self.worldObject = OpenWorldEntity(img, Circle((self.spawnX, self.spawnY), 0.5), "npc", "interact")

        for quest in quests:
            if (self.NPCID in quest.NPCDialogue.keys()):
                self.dialogue = quest.NPCDialogue[self.NPCID]
    

    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)

    def getSprite(self):
        return self.worldObject.getSprite()
    
    def getImagePosition(self):
        return self.worldObject.getImagePosition()