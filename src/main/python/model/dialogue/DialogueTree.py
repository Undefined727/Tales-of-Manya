from model.quest.Quest import Quest
from model.dialogue.DialogueTreeNode import DialogueTreeNode

class DialogueTree:
    head : DialogueTreeNode
    follow_up : Quest

    def __init__(self, head):
        self.setHead(head)

    ## Getters ##
    def getHead(self) -> DialogueTreeNode:
        return self.head

    def getLeaves(self) -> list [ DialogueTreeNode ]:
        return self.getHead().getLeaves()

    def getFollowUpQuest(self) -> Quest:
        return self.follow_up

    ## Setters ##
    def setHead(self, new_head : DialogueTreeNode):
        self.head = new_head

    def setFollowUpQuest(self, new_quest : Quest):
        self.follow_up = new_quest