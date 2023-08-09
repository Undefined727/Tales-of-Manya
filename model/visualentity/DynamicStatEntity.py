from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.DrawingEntity import DrawingEntity
from model.visualentity.TextEntity import TextEntity
from model.character.Character import DynamicStat
from model.visualentity.Tag import Tag

class DynamicStatEntity:
    border:ImageEntity
    text:TextEntity
    emptyRect:DrawingEntity
    fullRect:DrawingEntity
    dynamicStat:DynamicStat
    statType:str
    isShowing:bool
    RECT_WIDTH_MULTIPLIER = 0.5
    RECT_HEIGHT_MULTIPLIER = 0.3
    xPosition:0
    yPosition:0
    width:0
    height:0


    def __init__(self, dynamicStat = DynamicStat(0), statType = "health"):
        self.statType = statType
        self.width = 0
        self.height = 0
        self.xPosition = 0
        self.yPosition = 0
        self.isShowing = True

        self.border = ImageEntity("HPBorder", True, 0, 0, 0, 0, [], "HPBar.png")
        self.emptyRect = DrawingEntity("emptyRect", True, 0, 0, 0, 0, [], "red", False, "rectangle")
        self.fullRect = DrawingEntity("fullRect", True, 0, 0, 0, 0, [], "green", False, "rectangle")
        self.text = TextEntity("text", True, 0, 0, 0, 0, [], str(int(dynamicStat.getCurrentValue())) + "/" + str(int(dynamicStat.getMaxValue())), "mono", int(self.width/10), "black", None)

        if (statType == "mana"):
            self.border.updateImg("ManaBar.png")
            self.fullRect.color = "blue"
        
    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition

    def resize(self, width, height):
        self.width = width
        self.height = height

    def updateItems(self):
        shiftX = (self.width - self.width*self.RECT_WIDTH_MULTIPLIER)/2
        shiftY = (self.height - self.height*self.RECT_HEIGHT_MULTIPLIER)/2
        self.border.reposition(self.xPosition, self.yPosition)
        self.border.resize(self.width, self.height)
        self.emptyRect.reposition(self.xPosition + shiftX, self.yPosition + shiftY)
        self.emptyRect.resize(self.width*self.RECT_WIDTH_MULTIPLIER, self.height*self.RECT_HEIGHT_MULTIPLIER)
        self.fullRect.reposition(self.xPosition + shiftX, self.yPosition + shiftY)
        self.fullRect.resize(self.width*self.RECT_WIDTH_MULTIPLIER, self.height*self.RECT_HEIGHT_MULTIPLIER)
        self.text.reposition(self.xPosition + self.width/2, self.yPosition + self.height/2)
        self.text.resize(self.width*self.RECT_WIDTH_MULTIPLIER, self.height*self.RECT_HEIGHT_MULTIPLIER)

    def scale(self, screenX, screenY):
        self.updateItems()
        self.border.scale(screenX, screenY)
        self.emptyRect.scale(screenX, screenY)
        self.fullRect.scale(screenX, screenY)
        self.text.scale(screenX, screenY)

    
    def getItems(self):
        return [self.border, self.emptyRect, self.fullRect, self.text]

