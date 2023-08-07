from src.main.python.model.openworld.Tile import Tile
import numpy
import math
from PIL import Image
import pygame



img = Image.open("maps/" + "test.png")
npArray = numpy.array(img)
height, width, dim = npArray.shape

print(height, width)







img = Image.open("maps/" + "test.png")
npArray = numpy.array(img)
height, width, dim = npArray.shape

image = Image.fromarray(npArray, "RGB")
image.save("maps/convert.png")


pygame.init()
screenX, screenY = 1000, 700
tileSize = 48
screen = pygame.display.set_mode([screenX, screenY])
character = Tile("sprites/catgirl_head.png", 1)

tiles = []

for y in range(0, height):
    for x in range(0, width):
        if (npArray[y, x, 1] == 255): tiles.append(Tile("sprites/tiles/grass.png", 1))
        elif (npArray[y, x, 2] == 255): tiles.append(Tile("sprites/tiles/grass2.png", 1))
        else: tiles.append(Tile("sprites/tiles/grass3.png", 4))




cameraX = width/2
cameraY = height/2
characterX = cameraX
characterY = cameraY
speed = 0.02


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
    if keys[pygame.K_RIGHT]:
        if (not ((math.floor(characterX+1+speed) + math.ceil(characterY)*width) >= len(tiles))):
            rect.x, rect.y = convertToScreen(characterX+1+speed, characterY)
            floorRect.x, floorRect.y = convertToScreen(math.floor(characterX+1+speed), math.floor(characterY))
            ceilRect.x, ceilRect.y = convertToScreen(math.floor(characterX+1+speed), math.ceil(characterY))
            if (not (rect.colliderect(floorRect) and (not character.canPass(tiles[math.floor(characterX+1+speed) + math.floor(characterY)*width])))):
                if  (not (rect.colliderect(ceilRect) and (not character.canPass(tiles[math.floor(characterX+1+speed) + math.ceil(characterY)*width])))):
                    characterX += speed
                    cameraX = characterX
    if keys[pygame.K_UP]:
        rect.x, rect.y = convertToScreen(characterX, characterY-speed)
        floorRect.x, floorRect.y = convertToScreen(math.floor(characterX), math.floor(characterY-speed))
        ceilRect.x, ceilRect.y = convertToScreen(math.ceil(characterX), math.floor(characterY-speed))
        if (not (rect.colliderect(floorRect) and (not character.canPass(tiles[math.floor(characterX) + math.floor(characterY-speed)*width])))):
            if  (not (rect.colliderect(ceilRect) and (not character.canPass(tiles[math.ceil(characterX) + math.floor(characterY-speed)*width])))):
                characterY -= speed
                cameraY = characterY
    if keys[pygame.K_DOWN]:
        if (not ((math.floor(characterX) + math.floor(characterY+1+speed)*width) >= len(tiles))):
            rect.x, rect.y = convertToScreen(characterX, characterY+1+speed)
            floorRect.x, floorRect.y = convertToScreen(math.floor(characterX), math.floor(characterY+1+speed))
            ceilRect.x, ceilRect.y = convertToScreen(math.ceil(characterX), math.floor(characterY+1+speed))
            if (not (rect.colliderect(floorRect) and (not character.canPass(tiles[math.floor(characterX) + math.floor(characterY+1+speed)*width])))):
                if  (not (rect.colliderect(ceilRect) and (not character.canPass(tiles[math.ceil(characterX) + math.floor(characterY+1+speed)*width])))):
                    characterY += speed
                    cameraY = characterY


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
    pygame.display.flip()





