from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.engine.row import LegacyRow

class DatabaseFetcher:
    database:Engine
    connection:Connection

    def __init__(self, path):
        self.database = create_engine(f"sqlite:///{path}", echo = False)
        self.connection = self.database.connect()

    def retrieveAll(self, query : str) -> list[LegacyRow]:
        result = self.connection.execute(query)
        return result.fetchall()

    def retrieve(self, query : str) -> LegacyRow:
        result = self.connection.execute(query)
        return result.fetchone()

    def close(self):
        self.connection.close()
        self.database.dispose()

# repo = DatabaseFetcher("../itemdata.db")
# query = "SELECT * FROM itemdata"
# result = repo.retrieve(query)
# print(result)
# print(type(result))