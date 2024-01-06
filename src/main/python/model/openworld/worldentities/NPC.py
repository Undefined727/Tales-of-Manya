from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Circle import Circle
from model.dialogue.Conversation import Conversation
import json

class NPC:
    NPCID:int
    NPCName:str
    worldObject:OpenWorldEntity

    defaultDialogue:Conversation
    currentDialogue:Conversation

    def __init__(self, NPCID, name, img, conversation):
        self.NPCID = NPCID
        self.NPCName = name
        self.imgPath = f"entities/{img}"
        self.defaultDialogue = conversation
        self.currentDialogue = conversation

        self.worldObject = OpenWorldEntity(self.imgPath, Circle((0, 0), 0.5), "npc", "interact")

    def setDialogue(self, dialogue):
        self.currentDialogue = dialogue

    def setPosition(self, position):
        position[0] += 0.5
        position[1] += 0.5
        self.worldObject.setCenter(position)

    def setCenter(self, point):
        self.worldObject.setCenter(point)

    def move(self, diff):
        self.worldObject.move(diff)

    def getSprite(self):
        return self.worldObject.getSprite()

    def getImagePosition(self):
        return self.worldObject.getImagePosition()