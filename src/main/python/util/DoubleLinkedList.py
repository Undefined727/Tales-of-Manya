import LinkedListNode

class DoubleLinkedList:
    head : LinkedListNode
    tail : LinkedListNode

    def __init__(self, head : LinkedListNode, tail : LinkedListNode):
        self.head = head
        self.tail = tail

    def add(self, item):
        if (self.head is None):
            head = LinkedListNode(item)
            return

    def addNode(self, node : LinkedListNode):
        if (self.head is None):
            self.head = node
            return
        self.head.addNode(node)
        self.updateTail()

    def updateTail(self):
        if self.head is not None:
            current = self.head
            while current.hasNext():
                if (current.next().__eq__(current)):
                    pass