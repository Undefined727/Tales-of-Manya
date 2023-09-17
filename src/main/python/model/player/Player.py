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
        self.inventory.addItem(Item("Purveyor of the Nyaight", [ItemSlotType.WEAPON], "This sword looks like it was made by a catgirl trying to be very dramatic", []), 1)
        self.inventory.addItem(Item("Purveyor of the Nyaight", [ItemSlotType.WEAPON], "This sword looks like it was made by a catgirl trying to be very dramatic", []), 1)
        self.inventory.addItem(Item("Flower Crown", [ItemSlotType.HEAD], "A pretty circlet of flowers", []), 1)
        inventoryItems = self.inventory.getItems()
        for item in inventoryItems:
            print(item.item.name + ": " + str(item.count))



    def getCurrentQuests(self):
        return self.currentQuests
    
    def addQuest(self, addedQuest):
        for quest in self.currentQuests:
            if (not (quest.questName == addedQuest or quest.questID == addedQuest)):
                self.currentQuests.append(Quest(addedQuest))