from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.Animation import Animation
from view.visualentity.ShapeEntity import ShapeEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.Paragraph import Paragraph
from view.visualentity.VisualNovel import VisualNovel
from view.visualentity.ItemDisplay import ItemDisplay
from view.visualentity.InventoryCharacterEntity import InventoryCharacterEntity
from view.visualentity.CombatCharacterEntity import CombatCharacterEntity
from view.visualentity.ShapeButton import ShapeButton
from view.visualentity.HoverShapeButton import HoverShapeButton
from view.visualentity.ScrollBar import ScrollBar
from view.visualentity.ImageButton import ImageButton
from view.visualentity.DynamicStatEntity import DynamicStatEntity
import pygame

def displayEntity(entity, screen):
    if (type(entity) == ImageEntity):
        screen.blit(entity.img, (entity.xPosition, entity.yPosition))
    elif (type(entity) == ShapeEntity):
        if entity.shape == "rectangle":
            if (len(entity.color) > 3 and not (entity.color[3] == "e" or entity.color[3] == "n")):
                transparentRect = pygame.Surface((entity.width,entity.height)).convert_alpha()
                transparentRect.fill(entity.color)
                screen.blit(transparentRect, (entity.xPosition,entity.yPosition)) 
            elif entity.isBorder:
                pygame.draw.rect(screen, entity.color ,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.height), 2)
            else:
                pygame.draw.rect(screen, entity.color ,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.height))
        if entity.shape == "ellipse":
            if entity.isBorder:
                pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.height), 2)
            else:
                pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.height))
    elif (type(entity) == ShapeButton or type(entity) == HoverShapeButton):
        displayEntity(entity.buttonVisual(), screen)
    elif (type(entity) == ScrollBar):
        displayEntity(entity.button, screen)
        # If more is added to the scroll bar that can be added here :thumbeline:
    elif (type(entity) == ImageButton):
        displayEntity(entity.buttonVisual(), screen)
    elif (type(entity) == Animation):
        displayEntity(entity.getImage(), screen)
    elif (type(entity) == TextEntity):
        screen.blit(entity.textLabel, entity.textRect)
    elif (type(entity) == Paragraph):
        for item in entity.texts:
            displayEntity(item, screen)
    elif (type(entity) == VisualNovel):
        displayEntity(entity.backgroundBox, screen)
        displayEntity(entity.frame, screen)
        displayEntity(entity.paragraph, screen)
        displayEntity(entity.continueButton, screen)
        for option in entity.optionButtons:
            displayEntity(option, screen)
        for option in entity.optionParagraphs:
            displayEntity(option, screen)
    elif (type(entity) == ItemDisplay or type(entity) == InventoryCharacterEntity or type(entity) == CombatCharacterEntity or type(entity) == DynamicStatEntity):
        for item in entity.getItems():
            if item.isShowing: displayEntity(item, screen)
    elif (type(entity) == list):
        for item in entity:
            displayEntity(item, screen)
        
