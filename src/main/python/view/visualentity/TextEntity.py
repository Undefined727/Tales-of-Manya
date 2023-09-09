from view.visualentity.VisualEntity import VisualEntity
import pygame

class TextEntity(VisualEntity):
    textLabel = None
    textRect = None
    text = None
    font = "mono"
    fontSize = 32
    fontColor = "black"
    highlightColor = None

    def __init__(self, name = "Default_Text", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], text = "", font = "mono", fontSize = 32, fontColor = "black", highlightColor = None):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.text = text
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.highlightColor = highlightColor
        self.updateText(text, font, fontSize, fontColor, highlightColor)

    def updateText(self, text, font = None, fontSize = None, fontColor = None, highlightColor = None):
        if (font == None): font = self.font
        if (fontSize == None): fontSize = self.fontSize
        if (fontColor == None): fontColor = self.fontColor
        if (highlightColor == None): highlightColor = self.highlightColor

        textFont = pygame.font.SysFont(font, fontSize)
        if (highlightColor != None):
            self.textLabel = textFont.render(text, True, fontColor, highlightColor)
        else:
            self.textLabel = textFont.render(text, False, fontColor)
        self.textRect = self.textLabel.get_rect()
        self.textRect.center = (self.xPosition, self.yPosition)


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

    @staticmethod
    def createFrom(json_object):
        newObject = TextEntity()
        newObject.__dict__.update(json_object)
        newObject.updateText(newObject.text, newObject.font, newObject.fontSize, newObject.fontColor, newObject.highlightColor)
        return newObject