# TODO implement
import uuid
from sqlalchemy.engine.row import Row
from src.main.python.model.item.Item import Item

class DBItemBuilder:
    def generateID():
        return uuid.uuid5(uuid.NAMESPACE_DNS, 'basedstudios.dev')
    
 #   def build(item : Item) :
        