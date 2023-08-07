from model.openworld.Tile import Tile
import numpy
import math
from PIL import Image
import pygame
import time



def run(screen, screenX, screenY):
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


    cameraX = width/2
    cameraY = height/2
    characterX = cameraX
    characterY = cameraY
    speed = 0.1


    rect = pygame.Rect(0, 0, tileSize, tileSize)
    floorRect = pygame.Rect(0, 0, tileSize, tileSize)
    ceilRect = pygame.Rect(0, 0, tileSize, tileSize)

    def convertToScreen(xValue, yValue):
        xValue = (cameraX-xValue)*tileSize + screenX/2
        yValue = (cameraY-yValue)*tileSize + screenX/2
        return (xValue, yValue)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect.x, rect.y = convertToScreen(characterX-speed, characterY)
            floorRect.x, floorRect.y = convertToScreen(math.floor(characterX-speed), math.floor(characterY))
            ceilRect.x, ceilRect.y = convertToScreen(math.floor(characterX-speed), math.ceil(characterY))
            if (not (rect.colliderect(floorRect) and (not character.canPass(tiles[math.floor(characterX-speed) + math.floor(characterY)*width])))):
                if  (not (rect.colliderect(ceilRect) and (not character.canPass(tiles[math.floor(characterX-speed) + math.ceil(characterY)*width])))):
                    characterX -= speed
                    cameraX = characterX
                    character.height = tiles[math.floor(characterX+0.5) + math.floor(characterY+0.5)*width].height
        if keys[pygame.K_RIGHT]:
            if (not ((math.floor(characterX+1+speed) + math.ceil(characterY)*width) >= len(tiles))):
                rect.x, rect.y = convertToScreen(characterX+1+speed, characterY)
                floorRect.x, floorRect.y = convertToScreen(math.floor(characterX+1+speed), math.floor(characterY))
                ceilRect.x, ceilRect.y = convertToScreen(math.floor(characterX+1+speed), math.ceil(characterY))
                if (not (rect.colliderect(floorRect) and (not character.canPass(tiles[math.floor(characterX+1+speed) + math.floor(characterY)*width])))):
                    if  (not (rect.colliderect(ceilRect) and (not character.canPass(tiles[math.floor(characterX+1+speed) + math.ceil(characterY)*width])))):
                        characterX += speed
                        cameraX = characterX
                        character.height = tiles[math.floor(characterX+0.5) + math.floor(characterY+0.5)*width].height
        if keys[pygame.K_UP]:
            rect.x, rect.y = convertToScreen(characterX, characterY-speed)
            floorRect.x, floorRect.y = convertToScreen(math.floor(characterX), math.floor(characterY-speed))
            ceilRect.x, ceilRect.y = convertToScreen(math.ceil(characterX), math.floor(characterY-speed))
            if (not (rect.colliderect(floorRect) and (not character.canPass(tiles[math.floor(characterX) + math.floor(characterY-speed)*width])))):
                if  (not (rect.colliderect(ceilRect) and (not character.canPass(tiles[math.ceil(characterX) + math.floor(characterY-speed)*width])))):
                    characterY -= speed
                    cameraY = characterY
                    character.height = tiles[math.floor(characterX+0.5) + math.floor(characterY+0.5)*width].height
        if keys[pygame.K_DOWN]:
            if (not ((math.floor(characterX) + math.floor(characterY+1+speed)*width) >= len(tiles))):
                rect.x, rect.y = convertToScreen(characterX, characterY+1+speed)
                floorRect.x, floorRect.y = convertToScreen(math.floor(characterX), math.floor(characterY+1+speed))
                ceilRect.x, ceilRect.y = convertToScreen(math.ceil(characterX), math.floor(characterY+1+speed))
                if (not (rect.colliderect(floorRect) and (not character.canPass(tiles[math.floor(characterX) + math.floor(characterY+1+speed)*width])))):
                    if  (not (rect.colliderect(ceilRect) and (not character.canPass(tiles[math.ceil(characterX) + math.floor(characterY+1+speed)*width])))):
                        characterY += speed
                        cameraY = characterY
                        character.height = tiles[math.floor(characterX+0.5) + math.floor(characterY+0.5)*width].height


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
        screen.blit(character.img, ((screenX/2-(cameraX-characterX)*tileSize), (screenY/2-(cameraY-characterY)*tileSize)))
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        sleep_time = 1. / FPS - dt
        if sleep_time > 0:
            time.sleep(sleep_time)
        pygame.display.flip()