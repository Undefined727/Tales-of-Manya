from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.ShapeEntity import ShapeEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ShapeButton import ShapeButton
from model.visualentity.ImageButton import ImageButton
from model.visualentity.DynamicStatEntity import DynamicStatEntity
import pygame

def displayEntity(entity, screen):
    if (type(entity) == DynamicStatEntity):
        ls = entity.getItems()
        for item in ls:
            displayEntity(item, screen)
    if (type(entity) == ImageEntity or type(entity) == ImageButton):
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