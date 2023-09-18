from model.player.Quest import Quest
from model.character.Character import Character
from model.character.Inventory import Inventory
from model.item.Item import Item
from model.item.ItemSlotType import ItemSlotType

class Player:

    currentQuests:list
    party:list
    inventory:Inventory

    def __init__(self, fileName = None):
        # This will pull from a file in the future
        self.currentQuests = [Quest(0)]
        self.party = [Character("Catgirl", "catgirl.png", 10), Character("Catgirl", "catgirl.png", 10), Character("lmao", "catgirl.png", 20)]
        self.inventory = Inventory()
        self.inventory.addItem(Item(0),1)
        self.inventory.addItem(Item("Purveyor of the Nyaight"),2)
        self.inventory.addItem(Item("Flower Crown"),1)


    def getCurrentQuests(self):
        return self.currentQuests
    
    def addQuest(self, addedQuest):
        duplicateFound = False
        for quest in self.currentQuests:
            if ((quest.questName == addedQuest or quest.questID == addedQuest)):
                duplicateFound = True
        if (not duplicateFound): self.currentQuests.append(Quest(addedQuest))