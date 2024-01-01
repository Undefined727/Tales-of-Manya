from model.dialogue.DialogueTreeNode import DialogueTreeNode

class DialogueTree:
    head : DialogueTreeNode

    def __init__(self, head = None):
        self.setHead(head)

    ## Getters ##
    def getHead(self) -> DialogueTreeNode:
        return self.head

    def getLeaves(self) -> list [ DialogueTreeNode ]:
        return self.getHead().getLeaves()

    ## Setters ##
    def setHead(self, new_head : DialogueTreeNode):
        self.head = new_head

