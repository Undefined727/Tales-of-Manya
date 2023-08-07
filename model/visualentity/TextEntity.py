from model.visualentity.VisualEntity import VisualEntity
import pygame

class TextEntity(VisualEntity):
    textLabel = None
    textRect = None
    text = None
    font = "mono"
    fontSize = 32
    fontColor = "black"
    highlightColor = "green"

    def __init__(self, name = "Default_Text", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], text = "", font = "mono", fontSize = 32, fontColor = "black", highlightColor = None):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.updateText(text, font, fontSize, fontColor, highlightColor)

    def updateText(self, text, font, fontSize, fontColor, highlightColor):
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
    
    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.updateText(self.text, self.font, self.fontSize, self.fontColor, self.highlightColor)

    @staticmethod
    def createFrom(json_object):
        newObject = TextEntity()
        newObject.__dict__.update(json_object)
        newObject.updateText(newObject.text, newObject.font, newObject.fontSize, newObject.fontColor, newObject.highlightColor)
        return newObject