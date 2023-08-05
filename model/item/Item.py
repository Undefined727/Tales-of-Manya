from sqlalchemy import create_engine
import ItemSlot

class Item:
    id = -1
    name = "Default"
    slot = ItemSlot
    img = "catgirl.png"
    magicPercent = 0
    manaPercent = 0
    DEFPercent = 0
    ATKPercent = 0
    HPPercent = 0
    flatMagic = 0
    flatMana = 0
    flatDEF = 0
    flatATK = 0
    flatHP = 0
    description = "owo"
    #Statuses below when implemented

    # In the future pulls from database, name, img, magic, DEF, ATK, HP, flatMagic, flatDEF, flatATK, flatHP
    def __init__(self, id):
       itemdata_engine = create_engine('sqlite:///itemdata.db', echo = False)
       itemdata_connection = itemdata_engine.connect()
       s = "SELECT * FROM itemdata WHERE id='" + str(id) + "'"
       result = itemdata_connection.execute(s)
       result = str(result.fetchone())
       result = result[1:]
       self.id = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.name = result[1:result.index(',')-1]
       result = result[result.index(',')+2:]
       self.type = result[1:result.index(',')-1]
       result = result[result.index(',')+2:]
       self.img = result[1:result.index(',')-1]
       result = result[result.index(',')+2:]
       self.magicPercent = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.manaPercent = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.DEFPercent = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.ATKPercent = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.HPPercent = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.flatMagic = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.flatMana = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.flatDEF = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.flatATK = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.flatHP = result[:result.index(',')]
       result = result[result.index(',')+2:]
       self.description = result[:result.index(')')]
       
    def getSlot(self):
        return self.slot