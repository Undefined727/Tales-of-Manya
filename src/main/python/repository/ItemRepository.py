from src.main.python.model.item.Item import Item
from src.main.python.repository.DatabaseFetcher import DatabaseFetcher

class ItemRepository:
    all_items:list[Item]

    DEFAULT_PATH = "../itemdata.db"
    DEFAULT_QUERY = "SELECT * FROM itemdata"

    def __init__(self, query = DEFAULT_QUERY):
        engine = DatabaseFetcher(ItemRepository.DEFAULT_PATH)
        collection = engine.retrieveAll(query)
        for item in collection:
            self.all_items.append(Item())