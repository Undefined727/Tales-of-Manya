from model.quest.Quest import Quest
from model.item.Item import Item

class Subquest:
    name : str
    parent : Quest
    type : str
    data : str
    goal : int
    progress : int
    xp : int
    rewards : list [ Item ]
    follow_up : list

    def __init__(self, name : str, parent : Quest, type : str, data : str = "", goal : int = 0, progress : int = 0, xp : int = 0, rewards : list [ Item ] = [], follow_up = []):
        self.name       = name
        self.parent     = parent
        self.type       = type
        self.data       = data
        self.goal       = goal
        self.progress   = progress
        self.xp         = xp
        self.rewards    = rewards
        self.follow_up  = follow_up

    def getName(self) -> str:
        return self.name
    def getParent(self) -> Quest:
        return self.parent
    def getType(self) -> str:
        return self.type
    def getData(self) -> str:
        return self.data
    def getGoal(self) -> int:
        return self.goal
    def getProgress(self) -> int:
        return self.progress
    def getXP(self) -> int:
        return self.xp
    def getRewards(self) -> list [ Item ]:
        return self.rewards
    def getFollowUp(self) -> list:
        return self.follow_up

    def setName(self, new_name : str):
        self.name = new_name
    def setParent(self, new_parent : Quest):
        self.parent = new_parent
    def setType(self, new_type : str):
        self.type = new_type
    def setData(self, new_data : str):
        self.data = new_data
    def setGoal(self, new_goal : int):
        self.goal = new_goal
    def setProgress(self, new_progress : int):
        self.progress = new_progress
    def setXP(self, new_xp : int):
        self.xp = new_xp
    def setRewards(self, new_rewards : list [ Item ]):
        self.rewards = new_rewards
    def setFollowUp(self, new_follow_up : list):
        self.follow_up = new_follow_up

    def __eq__(self, another_object) -> bool:
        if (type(self) != type(another_object)):
            return False
        if (self.getName() != another_object.getName()):
            return False
        if (self.getParent() != another_object.getParent() or self.getType() != another_object.getType()):
            return False

    def __repr__(self) -> str:
        result = f"name: {self.getName()}"
        result += f" parent: {self.getParent().getName()}"
        result += f" type: {self.getType()}"
        result += f" data: {self.getData()}"
        result += f" goal: {self.getGoal()}"
        result += f" progress: {self.getProgress()}"
        result += f" experience: {self.getXP()}"
        result += f" rewards:"
        for reward in self.rewards:
            result += f" {reward.getName()},"
        result += f" follow up:"
        for subquest in self.getFollowUp():
            result += f" {subquest.getName()},"
