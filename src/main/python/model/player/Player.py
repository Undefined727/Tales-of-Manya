from model.player.Quest import Quest
from model.character.Character import Character

class Player:

    currentQuests:list
    party:list

    def __init__(self, fileName = None):
        # This will pull from a file in the future
        self.currentQuests = [Quest(0)]
        self.party = [Character("Catgirl", "catgirl.png", 10), Character("Catgirl", "catgirl.png", 10), Character("lmao", "catgirl.png", 20)]


    def getCurrentQuests(self):
        return self.currentQuests
    
    def addQuest(self, addedQuest):
        for quest in self.currentQuests:
            if (not (quest.questName == addedQuest or quest.questID == addedQuest)):
                self.currentQuests.append(Quest(addedQuest))