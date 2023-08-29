from view.visualentity.Paragraph import Paragraph
from view.visualentity.ImageButton import ImageButton
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.VisualEntity import VisualEntity

class VisualNovel(VisualEntity):
    paragraph:Paragraph
    continueButton:ImageButton
    background:ImageEntity
    text = "default_text"


    def __init__(self, name = "Default_Text", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], text = ""):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.text = text
        self.background = ImageEntity("background", True, xPosition, yPosition, width, height, tags, "text_background.png")
        self.paragraph = Paragraph("text", True, xPosition + width/5, yPosition + 6*height/16, 0.4*width, 0.55*height, tags, text, "mono", 24)
        self.paragraph.align = "Left"
        self.continueButton = ImageButton("continue_button", True, xPosition + 0.85*width, yPosition + 6*height/16, width/10, height/8, tags, "change_active_right.png", "continueText")
        

    def updateText(self, text, font = None, fontSize = None, fontColor = None, highlightColor = None):
        self.text = text
        self.paragraph.updateText(text, font, fontSize, fontColor, highlightColor)
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.background.resize(width, height)
        self.paragraph.resize(0.4*width, 0.55*height)
        self.continueButton.resize(width/10, height/8)
    
    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.background.reposition(xPosition, yPosition)
        self.paragraph.reposition(xPosition + self.width/5, yPosition + 6*self.height/16)
        self.continueButton.reposition(xPosition + 0.85*self.width, yPosition + 6*self.height/16)
    
    def scale(self, screenX, screenY):
        self.resize(self.width, self.height)
        self.reposition(self.xPosition, self.yPosition)
        self.background.scale(screenX, screenY)
        self.paragraph.scale(screenX, screenY)
        self.continueButton.scale(screenX, screenY)
        self.resize(self.width*screenX, self.height*screenY)
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)
        self.updateText(self.text)


    @staticmethod
    def createFrom(json_object):
        newObject = VisualNovel()
        newObject.__dict__.update(json_object)
        newObject.background = ImageEntity("background", True, newObject.xPosition, newObject.yPosition, newObject.width, newObject.height, newObject.tags, "text_background.png")
        newObject.paragraph = Paragraph("text", True, newObject.xPosition + newObject.width/5, newObject.yPosition + 6*newObject.height/16, 0.4*newObject.width, 0.55*newObject.height, newObject.tags, newObject.text, "mono", 24)
        newObject.paragraph.align = "Left"
        newObject.continueButton = ImageButton("continue_button", True, newObject.xPosition + 0.85*newObject.width, newObject.yPosition + 6*newObject.height/16, newObject.width/10, newObject.height/8, newObject.tags, "change_active_right.png", "continueText")
        return newObject