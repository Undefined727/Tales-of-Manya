import VisualEntity
import pygame

class TextEntity(VisualEntity):
    textLabel = None
    textRect = None

    def __init__(self, name = "Default_Text", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], text = "", font = None, fontSize = 0, fontColor = None, highlightColor = None):
        super().__init__(self, name, isShowing, xPosition, yPosition, width, height, tags)
        self.updateText(text, font, fontSize, fontColor, highlightColor)

    def updateText(self, text, font, fontSize, fontColor, highlightColor):
        textFont = pygame.font.SysFont(font, fontSize)
        if (highlightColor != None):
            self.textLabel = textFont.render(text, True, fontColor, highlightColor)
        else:
            self.textLabel = textFont.render(text, False, fontColor)
        self.textRect = self.textLabel.get_rect()
        self.textRect.center = (self.xPosition, self.yPosition)

    @staticmethod
    def createFrom(json_object):
        newObject = TextEntity()
        newObject.__dict__.update(json_object)
        return newObject