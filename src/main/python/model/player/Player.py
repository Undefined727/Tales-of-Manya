from model.quest.Quest import Quest
from model.quest.Subquest import Subquest
from model.character.Character import Character
from model.character.Inventory import Inventory
from model.character.Skill import Skill
from model.item.Item import Item
from model.item.ItemSlotType import ItemSlotType

class Player:

    currentQuests:list[Quest]
    currentSubquests:list[Subquest]
    party:list[Character]
    inventory:Inventory
    unlockedSkills:list[Skill]

    def __init__(self, database, fileName = None):
        # This will pull from a file in the future
        self.currentQuests = []
        self.currentSubquests = []
        for quest in self.currentQuests:
            self.currentSubquests.append(quest.subquests[0])
        

        self.party = [database.fetchCharacter(2), database.fetchCharacter(3), database.fetchCharacter(4)]
        self.party[0].changeLevel(10)
        self.party[1].changeLevel(15)
        self.party[2].changeLevel(20)
        
        self.unlockedSkills = []
        unlockedSkillNames = []
        for char in self.party:
            for skill in char.skills:
                if skill.name not in unlockedSkillNames:
                    self.unlockedSkills.append(skill)
                    unlockedSkillNames.append(skill.name)

        self.inventory = Inventory()
        self.inventory.addItem("Purrveyor of the Nyaight", 5)
        self.inventory.addItem("Flower Crown")
        self.inventory.addItem("Plate Mail Skirt")
        self.inventory.addItem("Shark Tooth Necklace")
        self.inventory.addItem("Stone Ring")
        self.inventory.addItem("Leather Boots")
        self.inventory.addItem("Warrior Helmet")

    def getCurrentQuests(self):
        return self.currentQuests
    
    def getCurrentSubquests(self):
        return self.currentSubquests
    
    def getCurrentChangedDialogue(self):
        changedDialogue = {}
        for subquest in reversed(self.currentSubquests):
            changedDialogue.update(subquest.conversations)
        return changedDialogue
    
    def completeSubquest(self, subquest:Subquest):
        for currentsubquest in self.currentSubquests[:]:
            if subquest.id == currentsubquest.id:
                self.currentSubquests.remove(currentsubquest)

        self.currentSubquests.extend(subquest.follow_up)
        for item, count in subquest.rewards.items():
            self.inventory.addItem(item, count)
        # Add xp later

    def addQuest(self, addedQuest:Quest):
        if (addedQuest == None): return
        duplicateFound = False
        for quest in self.currentQuests:
            if ((quest.name == addedQuest.name or quest.id == addedQuest.id)):
                duplicateFound = True
        if (not duplicateFound): 
            self.currentQuests.append(addedQuest)
            self.currentSubquests.append(addedQuest.subquests[0])

        for subquest in self.currentSubquests:
            print(subquest.name)