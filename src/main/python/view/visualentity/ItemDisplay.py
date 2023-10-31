from model.item.Item import Item
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.Paragraph import Paragraph
from model.item.ItemStatType import ItemStatType

class ItemDisplay:

    img:ImageEntity
    name:TextEntity
    stats:Paragraph
    item:Item
    isShowing = True

    def __init__(self, item:Item):
        self.item = item
        self.img = ImageEntity("img", True, 0, 0, 0, 0, [], "nekoarc.png", True)
        self.name = TextEntity("text", True, 0, 0, 0, 0, [], "default_name", "mono", 10, "black", None)
        self.stats = Paragraph("stats", True, 0, 0, 0, 0, [], "", "mono", 12, "black", None, "Left")
        self.isShowing = True
        

    def getItems(self):
        return [self.img, self.name, self.stats]

    def scale(self, screenX, screenY):
        self.stats.scale(screenX, screenY)
        self.name.scale(screenX, screenY)
        self.img.scale(screenX, screenY)
    
    def changeItem(self, item:Item):
        if (item == None):
            self.stats.isShowing = False
            self.name.isShowing = False
            self.img.isShowing = False
            return

        self.item = item
        self.name.fontSize = 18
        self.stats.fontSize = 16
        self.name.updateText(item.name)
        statText = ''
        for stat, value in item.stats.items():
            if (value >= 0): sign = "+"
            else: sign = ""

            if (stat.value == ItemStatType.ATTACK.value): statText = statText + f"{sign}{value} Attack%/n%"
            elif (stat.value == ItemStatType.DEFENSE.value): statText = statText + f"{sign}{value} Defense%/n%"
            elif (stat.value == ItemStatType.SPELLPOWER.value): statText = statText + f"{sign}{value} Spell Power%/n%"
            elif (stat.value == ItemStatType.HEALTH.value): statText = statText + f"{sign}{value} Health%/n%"
            elif (stat.value == ItemStatType.MANA.value): statText = statText + f"{sign}{value} Mana%/n%"
        self.stats.updateText(statText)
        self.img.updateImg("items/" + item.image_path)
    
    def updateItem(self):
        self.changeItem(self.item)

    @staticmethod
    def createFrom(json_object):
        newObject = ItemDisplay(None)
        newObject.name.reposition(json_object["nameXPosition"], json_object["nameYPosition"])
        newObject.name.resize(json_object["nameWidth"], json_object["nameHeight"])
        newObject.img.reposition(json_object["imgXPosition"], json_object["imgYPosition"])
        newObject.img.resize(json_object["imgWidth"], json_object["imgHeight"])
        newObject.stats.reposition(json_object["statsXPosition"], json_object["statsYPosition"])
        newObject.stats.resize(json_object["statsWidth"], json_object["statsHeight"])
        return newObject
    