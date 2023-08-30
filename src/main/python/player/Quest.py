

class Quest:
    questID = -1
    questName = "Kill The Slimes!"
    questType = "killQuest"
    questData = "Slime"
    questGoal = 10
    questProgress = 0

    def __init__(self, questType = None, questData = None, questGoal = None):
        # In the future we will pull from a database with a quest ID for now we just use the default values
        self.questID = 0

        self.questType = questType
        self.questData = questData
        self.questGoal = questGoal

    
