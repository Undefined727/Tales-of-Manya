from src.main.python.model.item.Item import Item
from src.main.python.model.item.ItemSlot import ItemSlot
from src.main.python.util.IllegalArgumentException import IllegalArgumentException
from src.main.python.model.database.DatabaseFetcher import DatabaseFetcher


class ItemRepository:
    all_items : list[ Item ]
    new_items : list[ Item ]
    database_path : str

    DEFAULT_PATH = "../itemdata.db"
    DEFAULT_QUERY = "SELECT * FROM items"

    def __init__(self, query = DEFAULT_QUERY, path = DEFAULT_PATH):
        self.all_items = list()
        self.new_items = list()
        self.database_path = path
        engine = DatabaseFetcher(path)
        collection = engine.retrieveAll(query)
        engine.close()
        for item in collection:
            self.all_items.append(Item(item[1], ItemSlot.__getitem__(item[2]), list(), item[4]))

    def addItem(self, item : Item):
        if (item in self.new_items or item in self.all_items):
            raise IllegalArgumentException("The item is already inside the repository")
        self.new_items.append(item)

    def saveToDatabase(self):
        final_list:list()
        for item in self.new_items:
            final_list.append(item.toDatabaseItem())
        engine = DatabaseFetcher(self.database_path)
        # TODO finish
