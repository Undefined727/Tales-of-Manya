from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from model.database.DatabaseModels import engine, DBItem
from model.item.ItemSlotType import ItemSlotType
from model.item.ItemTag import ItemTag
from model.item.ItemStatType import ItemStatType

class Item:
    id : str
    name : str
    type : ItemSlotType
    tags : list[ ItemTag ]
    stats : dict[ ItemStatType, int ]
    item_set : str
    description : str
    image_path: str

    def __init__(self,
                 name : str,
                 type : ItemSlotType,
                 description : str,
                 image_path : str,
                 tags : list[ ItemTag ] = None,
                 stats : dict[ ItemStatType, int ] = None,
                 item_set : str = None,
                 id : str = None):
        self.setName(name)
        self.setType(type)
        self.setDescription(description)
        self.setImagePath(image_path)
        self.setTags(tags)
        self.setItemSet(item_set)
        self.setStats(stats)

        if id is None: self.setID(self.generateID())
        else: self.setID(id)

    ## Getters ##
    def getID(self) -> str:
        return self.id

    def getName(self) -> str:
        return self.name

    def getDescription(self) -> str:
        return self.description

    def getPath(self) -> str:
        return self.image_path

    def getTags(self) -> list[ ItemTag ]:
        return self.tags

    def getType(self) -> ItemSlotType:
        return self.type

    def getStats(self) -> dict[ ItemStatType, int ]:
        return self.stats

    def getItemSet(self) -> str:
        return self.item_set

    ## Setters ##
    def setID(self, new_id : str):
        self.id = new_id

    def setName(self, new_name : str):
        self.name = new_name

    def setType(self, new_type : ItemSlotType):
        self.type = new_type

    def setDescription(self, new_description : str):
        self.description = new_description

    def setImagePath(self, new_image_path : str):
        self.image_path = new_image_path

    def setTags(self, new_tags : list[ ItemTag ]):
        self.tags = new_tags

    def setStats(self, stats : dict[ ItemStatType, int ]):
        self.stats = stats

    def setItemSet(self, item_set : str):
        self.item_set = item_set

    ## Misc ##
    def __eq__(self, item):
        if (type(item) == Item):
            if (item.getName() == self.getName()): return True
        return False

    def __repr__(self):
        return f"Name: {self.getName()}; Type: {self.getType()}; Tags: {self.getTags()}; Stats: {self.getStats()}; Set: {self.getStats()}; Description: {self.getDescription()}; Path: {self.getPath()}"

    @staticmethod
    def generateID() -> int:
        with Session(engine) as session:
            query = session.query(func.max(DBItem.id)).all()
            max_id = query[0][0]
            return max_id + 1