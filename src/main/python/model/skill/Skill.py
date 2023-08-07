from sqlalchemy import create_engine

class Skill:
    id = 0
    name = None
    img = None
    element = None
    singleTarget = True
    manaCost = None
    damage = None
    aoeDamage = None
    healing = None
    aoeHealing = None
    # AoE effects do NOT include the target.


    def __init__(self, id):
        skilldata_engine = create_engine('sqlite:///skilldata.db', echo = False)
        skilldata_connection = skilldata_engine.connect()
        s = f"SELECT * FROM skilldata WHERE id='{id}'"
        result = skilldata_connection.execute(s)
        result = str(result.fetchone())
        result = result[1:]
        self.id = int(result[:result.index(',')])
        result = result[result.index(',')+2:]
        self.name = result[1:result.index(',')-1]
        result = result[result.index(',')+2:]
        self.img = result[1:result.index(',')-1]
        result = result[result.index(',')+2:]
        self.element = result[1:result.index(',')-1]
        result = result[result.index(',')+2:]
        self.singleTarget = int(result[:result.index(',')])
        result = result[result.index(',')+2:]
        self.manaCost = int(result[:result.index(',')])
        result = result[result.index(',')+2:]
        self.damage = int(result[:result.index(',')])
        result = result[result.index(',')+2:]
        self.aoeDamage = int(result[:result.index(',')])
        result = result[result.index(',')+2:]
        self.healing = int(result[:result.index(',')])
        result = result[result.index(',')+2:]
        self.aoeHealing = int(result[:result.index(')')])