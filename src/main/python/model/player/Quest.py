import json

class Quest:
    questID = -1
    questName = "Kill The Slimes!"
    questType = "killQuest"
    questData = "Slime"
    questGoal = 10
    questProgress = 0

    NPCDialogue = {"Test_NPC": 0}
    followUpQuests = [1]

    questXPReward = 0
    questItemReward = []

    def __init__(self, questID):
        # In the future we will pull from a database with a quest ID for now we just use the default values
        self.questID = questID
        self.questProgress = 0

        file = open("src/main/python/quests/quests.json", 'r')
        data = json.load(file)

        for questEntry in data:
            if (questEntry['questID'] == questID):
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
                self.questItemReward = questEntry['questItemReward']
    
