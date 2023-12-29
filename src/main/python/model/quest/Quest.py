from model.quest.Subquest import Subquest
from model.Region import Region

class Quest:
    name : str
    description : str
    subquests : list [ Subquest ]
    region : list [ Region ]

    def __init__(self, name : str, description : str):
        self.setName(name)
        self.setDescription(description)

    ## Getters ##
    def getName(self) -> str:
        return self.name

    def getDescription(self) -> str:
        return self.description

    def getSubquests(self) -> list [ Subquest ]:
        return self.subquests

    def getRegions(self) -> list [ Region ]:
        return self.region

    ## Setters ##
    def setName(self, new_name : str):
        self.name = new_name

    def setDescription(self, new_description : str):
        self.description = new_description

    ## Misc ##
    def __eq__(self, another_object) -> bool:
        if (type(another_object) != type(self)):
            return False
        if (self.getName() != another_object.getName()):
            return False
        obj_subquests = self.getSubquests()
        anth_subquests = another_object.getSubquests()
        if (obj_subquests.__len__() != anth_subquests.__len__()):
            return False
        for i in range(obj_subquests.__len__()):
            if (obj_subquests[i] not in anth_subquests or anth_subquests[i] not in obj_subquests):
                return False
        return True

    def __repr__(self) -> str:
        result = f"name: {self.getName()}"
        result += f" description: {self.getDescription()}"
        result += f" region(s):"
        for region in self.getRegions():
            result += f" {region}"
        result += f" subquests:"
        for subquest in self.getSubquests():
            result += f" {subquest}"
        return result