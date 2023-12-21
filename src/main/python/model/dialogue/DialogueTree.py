from model.quest.Quest import Quest
from model.dialogue.DialogueTreeNode import DialogueTreeNode

class DialogueTree:
    head : DialogueTreeNode
    leaves : list [ DialogueTreeNode ]
    follow_up : Quest

    def __init__(self, head):
        self.setHead(head)

    def getHead(self) -> DialogueTreeNode:
        return self.head

    def getLeaves(self) -> list [ DialogueTreeNode ]:
        return self.leaves

    def getFollowUpQuest(self) -> Quest:
        return self.follow_up

    def setHead(self, new_head : DialogueTreeNode):
        self.head = new_head

    def setFollowUpQuest(self, new_quest : Quest):
        self.follow_up = new_quest

    def updateLeaves(self):
        self.leaves = self.head.checkLeaves()

    ## TODO implement ##
    pass