from model.item.Item import Item
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from model.database.DatabaseModels import engine, DBDialogue

class Dialogue:
    id : int
    tag : str
    content : str
    character_id : int
    emotion : str
    reward_friendship : int
    reward_xp : int
    reward_items : list [ Item ]

    def __init__(self,
                 tag : str = "",
                 content : str = "",
                 character_id : int = 0,
                 emotion : str = "",
                 reward_friendship : int = 0,
                 reward_xp : int = 0,
                 reward_items : list [ Item ] = [],
                 id : int = 0):
        if id == 0: self.id = self.generateID()
        else: self.id = id

        self.setTag(tag)
        self.setContent(content)
        self.setCharacterID(character_id)
        self.setEmotion(emotion)
        self.setFriendshipRewards(reward_friendship)
        self.setXPRewards(reward_xp)
        self.setItemRewards(reward_items)

    ## Getters ##
    def getID(self) -> int:
        return self.id

    def getTag(self) -> str:
        return self.tag

    def getContent(self) -> str:
        return self.content

    def getCharacterID(self) -> str:
        return self.character

    def getEmotion(self) -> str:
        return self.emotion

    def getFriendshipRewards(self) -> int:
        return self.reward_friendship

    def getXPRewards(self) -> int:
        return self.reward_xp

    def getItemRewards(self) -> list [ Item ]:
        return self.reward_items

    ## Setters ##
    def setTag(self, new_tag : str):
        self.tag = new_tag

    def setContent(self, new_content : str):
        self.content = new_content

    def setCharacterID(self, new_character : str):
        self.character = new_character

    def setEmotion(self, new_emotion : str):
        self.emotion = new_emotion

    def setFriendshipRewards(self, new_friendship_value : int):
        self.friendship = new_friendship_value

    def setItemRewards(self, new_items : list [ Item ]):
        self.reward_items = new_items

    def setXPRewards(self, new_xp : int):
        self.reward_xp = new_xp

    ## Misc ##
    def __eq__(self, another_object) -> bool:
        if type(self) != type(another_object):
            return False
        if self.getID() == another_object.getID() and self.getContent() == another_object.getContent():
            return True

    def __hash__(self) -> int:
        return hash((self.id, self.tag, self.character_id, self.emotion))

    def __repr__(self) -> str:
        result = f"ID: {self.getID()}"
        result += f"   Tag: {self.getTag()}\n"
        result += f"Character: {self.getCharacterID()}"
        result += f"   Character expression: {self.getEmotion()}\n"
        result += f"Content: {self.getContent()}\n"
        result += f"Rewards:\n"
        result += f"Friendship: {self.getFriendshipRewards()}    "
        result += f"XP: {self.getXPRewards()}\n"
        result += f"Items: {self.getItemRewards()}\n"
        return result

    # @staticmethod
    # def generateID() -> int:
    #     with Session(engine) as session:
    #         query = session.query(func.max(DBDialogue.id)).all()
    #         max_id = query[0][0]
    #         return max_id + 1

    ## TODO implement ##