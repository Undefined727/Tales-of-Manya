from model.dialogue.Dialogue import Dialogue
from util.IllegalArgumentException import IllegalArgumentException

class DialogueTreeNode:
    main_dialogue : Dialogue
    parent_tree = None
    parent_conversation = None
    children : list = None # [DialogueTreeNode]

    def __init__(self,
                 main_dialogue : Dialogue,
                 parent_tree = None,
                 parent_conversation = None,
                 children : list = []
                 ):
        self.setMainDialogue(main_dialogue)
        self.setParentTree(parent_tree)
        self.setParentConversation(parent_conversation)
        self.setChildren(children)

    ## Getters ##
    def getMainDialogue(self) -> Dialogue:
        return self.main_dialogue

    def getParentTree(self):
        return self.parent_tree

    def getParentConversation(self):
        return self.parent_conversation

    def getChildren(self) -> list:
        return self.children

    def getNodeHeight(self) -> int:
        if not self.parent_node: return 1
        return self.parent_node.getNodeHeight() + 1

    def getTreeHeight(self) -> int:
        if not self.leaves: return 1
        heights = set(node.getTreeHeight() + 1 for node in self.leaves.keys())
        return max(heights)

    def getLeaves(self) -> list:
        if not self.leaves:
            return [self]
        result = []
        for node in self.leaves:
            result.extend(node.checkLeaves())
        return result

    ## Setters ##
    def setMainDialogue(self, new_dialogue : Dialogue):
        self.main_dialogue = new_dialogue

    def setParentNode(self, new_node):
        self.parent_node = new_node

    def setParentTree(self, new_tree):
        self.parent_tree = new_tree
        if self.getChildren() is not None:
            for child in self.getChildren():
                child.setParentTree(new_tree)

    def setParentConversation(self, new_conversation):
        self.parent_conversation = new_conversation

    def setChildren(self, new_children : list):
        self.children = new_children
        # for child in self.children:
        #     child.attachSelf(self.getParentConversation(), self.getParentTree())

    ## Misc ##
    def addChild(self, new_node):
        if type(new_node) != type(self): raise IllegalArgumentException("The argument must be a DialogueTreeNode.")
        if new_node == self: raise IllegalArgumentException("A node can't be its own child.")
        if new_node in self.getChildren(): raise IllegalArgumentException("The node passed is already a child.")
        new_node.setParentNode(self)
        new_node.attachSelf(self.getParentConversation(), self.getParentTree())
        self.getChildren().append(new_node)

    def removeChild(self, child_node):
        if child_node not in self.getChildren(): raise IllegalArgumentException("The node passed is not a child.")
        self.getChildren().pop(child_node)
        child_node.setParentNode(None)
        child_node.detachSelf()
        return child_node

    def attachSelf(self, new_conversation, new_tree):
        self.setParentConversation(new_conversation)
        self.setParentTree(new_tree)
        for child in self.getChildren():
            child.attachSelf(new_conversation, new_tree)

    def detachSelf(self):
        self.setParentConversation(None)
        self.setParentTree(None)
        for child in self.getChildren():
            child.detachSelf()

    def __eq__(self, another_object) -> bool:
        if type(another_object) != type(self):
            return False
        if self.getMainDialogue() != another_object.getMainDialogue():
            return False
        return True

    def __hash__(self) -> int:
        return hash((self.getMainDialogue(), self.getParentConversation()))

    def __repr__(self) -> str:
        return f"Dialogue: {self.getMainDialogue()[0:5]}"