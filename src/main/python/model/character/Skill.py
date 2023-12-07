class Skill:
    id : str
    name : str
    description : str
    character: str
    element : str
    affinity : int
    manaCost : int
    motionValue : int

    def __init__(self, name, description, character, element, affinity, manaCost, motionValue):
        self.name = name
        self.description = description
        self.character = character
        self.element = element
        self.affinity = affinity
        self.manaCost = manaCost
        self.motionValue = motionValue
