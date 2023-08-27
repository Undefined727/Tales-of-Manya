from view.visualentity.TextEntity import TextEntity
from view.visualentity.VisualEntity import VisualEntity
import math

class Paragraph(VisualEntity):
    texts:list[TextEntity]
    textRect = None
    font = "mono"
    fontSize = 12
    fontColor = "black"
    highlightColor = "green"
    scaled = False


    def __init__(self, name = "Default_Text", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], text = "", font = "mono", fontSize = 12, fontColor = "black", highlightColor = None, align = "Center"):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.text = text
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.highlightColor = highlightColor
        self.align = align
        self.texts = [TextEntity(name, self.isShowing, xPosition, yPosition, width, height, [], text, self.font, self.fontSize, self.fontColor, self.highlightColor)]

    def updateText(self, text, font = None, fontSize = None, fontColor = None, highlightColor = None):
        if (font == None): font = self.font
        if (fontSize == None): fontSize = self.fontSize
        if (fontColor == None): fontColor = self.fontColor
        if (highlightColor == None): highlightColor = self.highlightColor
        self.text = text

        # CHANGE THIS BASED ON THE FONT FIGURE THIS LATER IG
        fontRatio = 0.61
        textHeight = self.fontSize*1.2

        #Margins
        xPadding = 2
        yPadding = 1

        if (self.width >= self.fontSize):
            lettersPerLine = math.floor(self.width/(self.fontSize*fontRatio))-xPadding
            lines = math.ceil(len(self.text)/lettersPerLine)
        if (self.scaled):
            if(len(text) <= 0): return
            self.texts = []
            startIndex = 0
            endIndex = 0
            if(not text[len(text)-1] == " "):
                text = text + " "
            for i in range(0, lines+2):
                startIndex = endIndex
                endIndex += lettersPerLine
                if (endIndex >= len(text)): 
                    endIndex = len(text)
                else:
                    for j in range(0, endIndex):
                        if (text[endIndex-j] == " "):
                            endIndex = endIndex-j+1
                            break
                
                charCount = endIndex-startIndex+1
                if (charCount < 2): break
                textWidth = self.width
                textX = self.xPosition
                textY = self.yPosition + (i+yPadding)*textHeight
                if (self.align == "Left"):
                    textX -= (2 + lettersPerLine-charCount)*fontSize*0.5*fontRatio
                if (self.align == "Right"):
                    textX += (2 + lettersPerLine-charCount)*fontSize*0.5*fontRatio

                if (textY + textHeight * (yPadding) > self.yPosition + self.height): break
                self.texts.append(TextEntity(self.name + str(i), self.isShowing, textX, textY, textWidth, textHeight, [], " " + text[startIndex:endIndex], self.font, self.fontSize, self.fontColor, self.highlightColor))

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.updateText(self.text, self.font, self.fontSize, self.fontColor, self.highlightColor)
    
    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.updateText(self.text, self.font, self.fontSize, self.fontColor, self.highlightColor)
    
    def scale(self, screenX, screenY):
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)
        self.resize(self.width*screenX, self.height*screenY)
        self.scaled = True
        self.updateText(self.text)

    @staticmethod
    def createFrom(json_object):
        newObject = Paragraph()
        newObject.__dict__.update(json_object)
        return newObject