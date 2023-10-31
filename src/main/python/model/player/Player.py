from model.player.Quest import Quest
from model.character.Character import Character
from model.character.Inventory import Inventory
from model.item.Item import Item
from model.item.ItemSlotType import ItemSlotType

class Player:

    currentQuests:list[Quest]
    party:list
    inventory:Inventory

    def __init__(self, fileName = None):
        # This will pull from a file in the future
        self.currentQuests = [Quest(0)]
        self.party = [Character("Catgirl1", "catgirl.png", 10), Character("Catgirl2", "catgirl.png", 15), Character("Catgirl3", "catgirl.png", 20)]
        
        self.inventory = Inventory()
        self.inventory.addItem("Purrveyor of the Nyaight", 5)
        self.inventory.addItem("Flower Crown", 1)
        self.inventory.addItem("Slimy Helmet", 1)
        self.inventory.addItem("Plate Mail Skirt", 1)
        self.inventory.addItem("Shark Tooth Necklace", 1)
        self.inventory.addItem("Stone Ring", 1)
        self.inventory.addItem("Leather Boots", 1)
        self.inventory.addItem("Warrior Helmet", 1)

    def getCurrentQuests(self):
        return self.currentQuests

    def addQuest(self, addedQuest):
        duplicateFound = False
        for quest in self.currentQuests:
            if ((quest.questName == addedQuest or quest.questID == addedQuest)):
                duplicateFound = True
        if (not duplicateFound): self.currentQuests.append(Quest(addedQuest))