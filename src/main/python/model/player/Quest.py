

class Quest:
    questID = -1
    questName = "Kill The Slimes!"
    questType = "killQuest"
    questData = "Slime"
    questGoal = 10
    questProgress = 0

    NPCDialogue = {"Test_NPC": ["Please help us kill these slimes!", "Good Luck!"]}
    followUpQuests = [1]

    questXPReward = 0
    questItemReward = []

    def __init__(self, questID):
        # In the future we will pull from a database with a quest ID for now we just use the default values
        self.questID = questID
        self.questProgress = 0
        if (questID == 0):
            self.questName = "Kill The Slimes!"
            self.questType = "killQuest"
            self.questData = "Slime"
            self.questGoal = 2
            self.NPCDialogue = {"Test_NPC": ["Please help us kill these slimes!", "Good Luck!"]}
            self.followUpQuests = [1]
            self.questXPReward = 0
            self.questItemReward = []
        else:
            self.questName = "Kill The Slimes! - Accept Reward"
            self.questType = "NPCInteractionQuest"
            self.questData = "Test_NPC"
            self.questGoal = 1
            self.NPCDialogue = {"Test_NPC": ["Thank you for saving us!", "Take This Reward!"]}
            self.followUpQuests = []
            self.questXPReward = 0
            self.questItemReward = []

    
