from model.dialogue.Dialogue import Dialogue
from model.dialogue.DialogueTree import DialogueTree
from model.dialogue.Conversation import Conversation


class DialogueTreeNode:
    parent_tree : DialogueTree
    parent_node = None
    parent_conversation : Conversation
    leaves : dict() # { DialogueTreeNode : Dialogue }
    main_dialogue : Dialogue
    
    def __init__(self,
                 main_dialogue : Dialogue,
                 parent_tree : DialogueTree,
                 parent_node = None,
                 parent_conversation : Conversation = None,
                 leaves : dict = {}
                 ):
        self.setMainDialogue(main_dialogue)
        self.setParentNode(parent_node)
        self.setParentTree(parent_tree)
        self.setParentConversation(parent_conversation)
        self.setLeaves(leaves)

    def getMainDialogue(self) -> Dialogue:
        return self.main_dialogue

    def getParentNode(self):
        return self.parent_node

    def getParentTree(self) -> DialogueTree:
        return self.parent_tree

    def getParentConversation(self) -> Conversation:
        return self.parent_conversation

    def getNodeHeight(self) -> int:
        if not self.parent_node: return 0
        else: return self.parent_node.getNodeHeight() + 1

    def setMainDialogue(self, new_dialogue : Dialogue):
        self.main_dialogue = new_dialogue

    def setParentNode(self, new_node):
        self.parent_node = new_node

    def setParentTree(self, new_tree : DialogueTree):
        self.parent_tree = new_tree

    def setParentConversation(self, new_conversation : Conversation):
        self.parent_conversation = new_conversation

    def setLeaves(self, new_leaves : dict):
        self.leaves = new_leaves

    def checkLeaves(self) -> list:
        if not self.leaves:
            return [self]
        else:
            result = []
            for node in self.leaves:
                result.extend(node.checkLeaves())
            return result

    def __repr__(self) -> str:
        return f"{self.getMainDialogue()[0:5]}"
    ## TODO implement ##
    pass