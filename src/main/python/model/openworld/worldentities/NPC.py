from model.openworld.openWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle
import json

class NPC:
    NPCID:int
    NPCName:str
    worldObject:OpenWorldEntity

    defaultDialogue:int
    currentDialogue:int

    def __init__(self, NPCID, position):
        if (type(NPCID) == str): self.NPCName = NPCID
        else: self.NPCID = NPCID

        file = open("src/main/python/npcs/NPCList.json", 'r')
        data = json.load(file)

        for NPCEntry in data:
            if (NPCEntry['NPCID'] == NPCID or NPCEntry['NPCName'] == NPCID):
                self.NPCID = NPCEntry['NPCID']
                self.NPCName = NPCEntry['NPCName']
                self.imgPath = f"entities/{NPCEntry['imgPath']}"
                self.defaultDialogue = NPCEntry['defaultDialogue']
                self.currentDialogue = NPCEntry['currentDialogue']
                break

        self.worldObject = OpenWorldEntity(self.imgPath, Circle((position), 0.5), "npc", "interact")
    

    def updateDialogue(self):
        file = open("src/main/python/npcs/NPCList.json", 'r')
        data = json.load(file)
        for NPCEntry in data:
            if (NPCEntry['NPCID'] == self.NPCID):
                self.currentDialogue = NPCEntry['currentDialogue']


    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)

    def getSprite(self):
        return self.worldObject.getSprite()
    
    def getImagePosition(self):
        return self.worldObject.getImagePosition()