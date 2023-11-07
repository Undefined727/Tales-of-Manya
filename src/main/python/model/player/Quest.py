import json

class Quest:
    questID = -1
    questName = "Kill The Slimes!"
    # List of types of quests that you can have: killQuest, NPCInteractionQuest, freeQuest
    questType = "killQuest"
    questData = "Slime"
    questGoal = 10
    questProgress = 0

    NPCDialogue = {"Test_NPC": 0}
    followUpQuests = [1]

    questXPReward = 0
    questItemRewards = {}

    def __init__(self, questID):
        if (type(questID) == str): self.questName = questID
        else: self.questID = questID
        self.questProgress = 0

        file = open("src/main/python/quests/quests.json", 'r')
        data = json.load(file)

        for questEntry in data:
            if (questEntry['questID'] == questID or questEntry['questName'] == questID):
                self.questID = questEntry['questID']
                self.questName = questEntry['questName']
                self.questType = questEntry['questType']
                self.questData = questEntry['questData']
                self.questGoal = questEntry['questGoal']

                NPCDialogue = {}
                for npc in questEntry['NPCDialogue']:
                    NPCDialogue.update({npc['NPCID']:npc['Dialogue']})
                self.NPCDialogue = NPCDialogue

                self.followUpQuests = questEntry['followUpQuests']
                self.questXPReward = questEntry['questXPReward']

                itemRewards = {}
                for item in questEntry['questItemRewards']:
                    itemRewards.update({item['itemID']:item['count']})
                self.questItemRewards = itemRewards
                break
    
