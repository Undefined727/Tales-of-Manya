class LinkedListNode:
    def __init__(self, data, nextNode, prevNode, position : int = 0):
        self.data = data
        self.nextNode = nextNode
        self.prevNode = prevNode
        self.position = position

    def addNode(self, node):
        if self.nextNode is None:
            self.nextNode = node
            return
        self.nextNode.addNode(node)
        return

    def hasNext(self) -> bool:
        return self.nextNode is None

    def setPos(self, position):
        self.position = position
        if self.hasNext():
            self.nextNode.setPos(position + 1)

    def __eq__(self, __value: object) -> bool:
        if type(__value) != LinkedListNode: return False
        if self.data != __value.data: return False
        if self.position != __value.position: return False
        return True