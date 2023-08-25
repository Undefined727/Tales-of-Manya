import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.engine.row import Row
sys.path.append(os.path.abspath("."))
from src.main.python.model.item.Item import Item
from src.main.python.model.database.item.DatabaseModels import DBItem

# TODO Working fine, but incomplete
class DatabaseFetcher:
    database:Engine
    connection:Connection

    def __init__(self, path : str):
        self.database = create_engine(f"sqlite:///{path}", echo = False)
        self.connection = self.database.connect()

    def retrieveAll(self, query : str) -> list[ Row ]:
        result = self.connection.execute(text(query))
        return result.fetchall()

    def retrieve(self, query : str) -> Row:
        result = self.connection.execute(text(query))
        return result.fetchone()

    def close(self):
        self.connection.close()
        self.database.dispose()

repo = DatabaseFetcher("src/main/python/catgirl-dungeon.db")
query = "SELECT * FROM Item"
result = repo.retrieveAll(query)
for item in result:
    print(item)
print(type(result[0]))
#test = Item()
#print(test.id)
#dbitem = DBItem.fromItem(test)
#print(dbitem)
repo.close()