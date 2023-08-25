from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ShapeEntity import ShapeEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ShapeButton import ShapeButton
from view.visualentity.ImageButton import ImageButton
from view.visualentity.DynamicStatEntity import DynamicStatEntity
import pygame

def displayEntity(entity, screen):
    if (type(entity) == DynamicStatEntity):
        ls = entity.getItems()
        for item in ls:
            displayEntity(item, screen)
    if (type(entity) == ImageEntity):
        screen.blit(entity.img, (entity.xPosition, entity.yPosition))
    elif (type(entity) == ShapeEntity):
        if entity.shape == "rectangle":
            if entity.isBorder:
                pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.height), 2)
            else:
                pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.height))
        if entity.shape == "ellipse":
            if entity.isBorder:
                pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.height), 2)
            else:
                pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.height))
    elif (type(entity) == TextEntity):
        screen.blit(entity.textLabel, entity.textRect)