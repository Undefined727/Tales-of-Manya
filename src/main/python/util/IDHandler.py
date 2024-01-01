from uuid import uuid4
from src.main.python.model.Singleton import global_states
from src.main.python.model.database.DatabaseModels import DBCharacter, DBItem

class IDHandler:
    @staticmethod
    def generateID(object_type):
        if (object_type == "Character"):
            new_id = global_states.database_factory.getNextID(DBCharacter) + 1
        # elif (object_type == "Drops")
        # elif (object_type == "Effect")
        elif (object_type == "Item"):
            new_id = global_states.database_factory.getNextID(DBItem) + 1
        # elif (object_type == "ItemStat")
        # elif (object_type == "Quest")
        # elif (object_type == "Skill")
        # elif (object_type == "Tag")
        return new_id