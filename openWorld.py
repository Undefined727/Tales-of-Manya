from model.openworld.Tile import Tile
from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.DrawingEntity import DrawingEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ButtonEntity import ButtonEntity
from model.visualentity.TransparentButtonEntity import TransparentButtonEntity
import numpy
import math
from PIL import Image
import json
import pygame
import time

visualEntities = []
buttons = []
quit = False

def refreshMenu(screen):
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            if (type(entity) == ImageEntity):
                screen.blit(entity.img, (entity.xPosition, entity.yPosition))
            elif (type(entity) == DrawingEntity):
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

def exitButton():
    global quit
    quit = True

def run(screen, screenX, screenY):
    global quit
    global visualEntities
    quit = False
    FPS = 60
    prev_time = time.time()
    img = Image.open("maps/samplemap.png")
    npArray = numpy.array(img)
    height, width, dim = npArray.shape
    tiles = []

    for y in range(0, height):
        for x in range(0, width):
            if ((npArray[y, x] == [107, 82, 10, 255]).all()): tiles.append(Tile("sprites/tiles/tree.png", 1, True))
            elif ((npArray[y, x] == (210, 132, 53, 255)).all()): tiles.append(Tile("sprites/tiles/bridge.png", 1))
            elif ((npArray[y, x] == (0, 0, 0, 255)).all()): tiles.append(Tile("sprites/tiles/wall.png", 1, True))
            elif ((npArray[y, x] == (36, 98, 200, 255)).all()): tiles.append(Tile("sprites/tiles/water.png", 1, True))
            elif ((npArray[y, x] == (193, 174, 2, 255)).all()): tiles.append(Tile("sprites/tiles/wet_sand.png", 1))
            elif ((npArray[y, x] == (204, 225, 77, 255)).all()): tiles.append(Tile("sprites/tiles/sand.png", 1))
            elif ((npArray[y, x] == (58, 255, 0, 255)).all()): tiles.append(Tile("sprites/tiles/grass4.png", 4))
            elif ((npArray[y, x] == (51, 223, 0, 255)).all()): tiles.append(Tile("sprites/tiles/grass3.png", 3))
            elif ((npArray[y, x] == (44, 189, 1, 255)).all()): tiles.append(Tile("sprites/tiles/grass2.png", 2))
            elif ((npArray[y, x] == (30, 133, 0, 255)).all()): tiles.append(Tile("sprites/tiles/grass1.png", 1))
            else: tiles.append(Tile("sprites/nekoarc.png", 4))
    tileSize = 48
    character = Tile("sprites/catgirl_head.png", 1)


    
    file = open("screens/openWorldScreen.json", 'r')
    data = json.load(file)
    for item in data:
        if item["entityType"] == "Image":
             entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Drawing":
            entity = DrawingEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "Button":
            entity = ButtonEntity.createFrom(item)
        elif item["entityType"] == "TransparentButton":
            entity = TransparentButtonEntity.createFrom(item)
            
        entity.resize(entity.width*screen.get_width(), entity.height*screen.get_height())
        entity.reposition(entity.xPosition * screen.get_width(),entity.yPosition * screen.get_height())
        if (item["entityType"] == "TransparentButton" or item["entityType"] == "Button"): buttons.append(entity)
        else: visualEntities.append(entity)


















    cameraX = width/2
    cameraY = height/2
    characterX = cameraX
    characterY = cameraY
    speed = 0.1
    characterSize = 0.85*tileSize

    rect = pygame.Rect(0, 0, characterSize, characterSize)
    compareRect = pygame.Rect(0, 0, tileSize, tileSize)

    def convertToScreen(xValue, yValue):
        xValue = (xValue-cameraX)*tileSize + screenX/2
        yValue = (yValue-cameraY)*tileSize + screenY/2
        return (xValue, yValue)

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "exit"): buttonFunc = exitButton
                        if (len(entity.args) == 0): buttonFunc()
                        else: buttonFunc(entity.args)
                        break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect.x, rect.y = convertToScreen(characterX-speed-(characterSize/tileSize)/2, characterY-(characterSize/tileSize)/2)
            compareRect.x, compareRect.y = convertToScreen(math.floor(characterX-speed), math.floor(characterY))
            if (not (rect.colliderect(compareRect) and (not character.canPass(tiles[math.floor(characterX-speed) + math.floor(characterY)*width])))):
                    characterX -= speed
                    cameraX = characterX
                    character.height = tiles[math.floor(characterX) + math.floor(characterY)*width].height
        if keys[pygame.K_RIGHT]:
            if (not ((math.floor(characterX+speed) + math.floor(characterY)*width) >= len(tiles))):
                rect.x, rect.y = convertToScreen(characterX-(characterSize/tileSize)/2+speed, characterY-(characterSize/tileSize)/2)
                compareRect.x, compareRect.y = convertToScreen(math.floor(characterX+speed), math.floor(characterY))
                if (not (rect.colliderect(compareRect) and (not character.canPass(tiles[math.floor(characterX+speed) + math.floor(characterY)*width])))):
                        characterX += speed
                        cameraX = characterX
                        character.height = tiles[math.floor(characterX) + math.floor(characterY)*width].height
        if keys[pygame.K_UP]:
            rect.x, rect.y = convertToScreen(characterX-(characterSize/tileSize)/2, characterY-(characterSize/tileSize)/2-speed)
            compareRect.x, compareRect.y = convertToScreen(math.floor(characterX), math.floor(characterY-speed))
            if (not (rect.colliderect(compareRect) and (not character.canPass(tiles[math.floor(characterX) + math.floor(characterY-speed)*width])))):
                characterY -= speed
                cameraY = characterY
                character.height = tiles[math.floor(characterX) + math.floor(characterY)*width].height
        if keys[pygame.K_DOWN]:
            if (not ((math.floor(characterX) + math.floor(characterY+speed)*width) >= len(tiles))):
                rect.x, rect.y = convertToScreen(characterX-(characterSize/tileSize)/2, characterY-(characterSize/tileSize)/2+speed)
                compareRect.x, compareRect.y = convertToScreen(math.floor(characterX), math.floor(characterY+speed))
                if (not (rect.colliderect(compareRect) and (not character.canPass(tiles[math.floor(characterX) + math.floor(characterY+speed)*width])))):
                        characterY += speed
                        cameraY = characterY
                        character.height = tiles[math.floor(characterX) + math.floor(characterY)*width].height


        if (characterX < 0): characterX = 0
        elif (characterX > width-1): characterX = width-1
        if (cameraX < (screenX/tileSize)/2): cameraX = (screenX/tileSize)/2
        elif (cameraX > width-(screenX/tileSize)/2): cameraX = width-(screenX/tileSize)/2
        if (characterY < 0): characterY = 0
        elif (characterY > height-1): characterY = height-1
        if (cameraY > height-(screenY/tileSize)/2): cameraY = height-(screenY/tileSize)/2
        elif (cameraY < (screenY/tileSize)/2): cameraY = (screenY/tileSize)/2
        screen.fill((0, 0, 0))
        for x in range(0, width):
            for y in range(0, height):
                screen.blit(tiles[width*y + x].img, ((screenX/2-(cameraX-x)*tileSize), (screenY/2-(cameraY-y)*tileSize)))
        screen.blit(character.img, convertToScreen(characterX-(characterSize/tileSize)/2, characterY-(characterSize/tileSize)/2))
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        sleep_time = 1. / FPS - dt
        if sleep_time > 0:
            time.sleep(sleep_time)
        refreshMenu(screen)
        pygame.display.flip()
        if (quit): break