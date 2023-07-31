import model.VisualEntity as VisualEntity
import pygame

class TextEntity(VisualEntity):
    textLabel = None
    textRect = None

    def __init__(self, name, isShowing, xPosition, yPosition, width, height, tags, text, font, fontSize, fontColor, highlightColor):
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