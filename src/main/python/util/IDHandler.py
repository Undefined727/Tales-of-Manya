from uuid import uuid4

class IDHandler:
    
    @staticmethod
    def generateID(object_type):
        return str(uuid4())