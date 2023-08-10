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
        self.id = id
        # TODO implement