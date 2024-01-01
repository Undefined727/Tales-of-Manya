from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from model.dialogue.DialogueTree import DialogueTree
from model.database.DatabaseModels import engine, DBConversation

class Conversation:
    id : int
    name : str
    dialogues : DialogueTree

    def __init__(self, name : str):
        # self.id = self.generateID()
        self.setName(name)

    ## Getters ##
    def getID(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name

    def getDialogues(self) -> DialogueTree:
        return self.dialogues

    ## Setters ##
    def setName(self, new_name : str):
        self.name = new_name

    def setDialogues(self, new_dialogues : DialogueTree):
        self.dialogues = new_dialogues

    ## Misc ##
    # @staticmethod
    # def generateID() -> int:
    #     with Session(engine) as session:
    #         query = session.query(func.max(DBConversation.id)).all()
    #         max_id = query[0][0]
    #         return max_id + 1
    ## TODO implement

    def __hash__(self) -> int:
        return hash((self.id, self.name))