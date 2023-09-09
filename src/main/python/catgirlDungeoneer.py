import os, sys, time, pygame, math, random, json, copy
from PIL import Image
import numpy as np
from view.JSONParser import loadJson
from view.displayHandler import displayEntity
from model.openworld.Tile import Tile
from view.visualentity.TextEntity import TextEntity

from view.visualentity.HoverShapeButton import HoverShapeButton
sys.path.append(os.path.abspath("."))


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()
screenX,screenY = info.current_w,info.current_h
pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('src/main/python/sprites/catgirl_head.png'))
screen = pygame.display.set_mode([screenX, screenY])

visualEntities = []
buttons = []

FPS = 60
prev_time = time.time()
savedMap = Image.open("src/main/python/maps/samplemap/map.png")
savedMap = np.array(savedMap)
height, width, dim = savedMap.shape
tiles = []
tileSize = 48

file = open("src/main/python/maps/tileIndex.json", 'r')
tiledata = json.load(file)
tileImages = {}
tileImagesDisplayed = {}

for tile in tiledata:
    img = pygame.image.load(f"src/main/python/sprites/tiles/{tile['image']}").convert()
    tileImages.update({tile['name']:img})
    img2 = pygame.transform.scale(img, (tileSize, tileSize))
    tileImagesDisplayed.update({tile['name']:img2})

for y in range(0, height):
    for x in range(0, width):
        tileFound = False
        tileColor = savedMap[y, x][:3]
        tileHeight = savedMap[y, x][3]
        for tile in tiledata:
            if ((tileColor == tile['color']).all()): 
                tiles.append(Tile(tile['name'], tileHeight, tile['defaultSolid']))
                tileFound = True
                break
        if (not tileFound): tiles.append(Tile("tileNotFound", tileHeight,  True))


loadJson("catgirlDungeoneer.json", screenX, screenY, [visualEntities, buttons])
for entity in visualEntities:
    if (type(entity) == TextEntity):
        print(entity.fontSize)

backgroundHeight = 3*screenY
backgroundFog = pygame.image.load("src/main/python/sprites/tiles/Gofhres.png").convert()
backgroundFog = pygame.transform.scale(backgroundFog, (screenX, backgroundHeight))

CHAR_SIZE_MULTIPLIER = 0.85

spawnX = width/2
spawnY = height/2
characterSize = CHAR_SIZE_MULTIPLIER*tileSize
radius = characterSize/(2*tileSize)
cameraX = spawnX
cameraY = spawnY


def refreshMenu():
    global visualEntities
    global screen
    for entity in visualEntities:
        if entity.isShowing:
            displayEntity(entity, screen)
    pygame.display.flip()

def convertToScreen(xValue, yValue):
    global cameraX
    global cameraY
    xValue = (xValue-cameraX)*tileSize + screenX/2
    yValue = (yValue-cameraY)*tileSize + screenY/2
    return (xValue, yValue)

def exitButton():
    pygame.quit()


frameCounter = 0
### Running Editor ###
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
                    else: buttonFunc(*entity.args)
                    break
        if event.type == pygame.MOUSEWHEEL:
            tileSize += 2*event.y
            if (tileSize <= 0): tileSize = 1
            for tile in tileImagesDisplayed:
                tileImagesDisplayed[tile] = pygame.transform.scale(tileImages[tile], (tileSize, tileSize))



    ### Make Hover Buttons shine funny color
    for button in buttons:
        if (type(button) == HoverShapeButton):
            button.mouseInRegion(mouse)


    ### Inputs ###
    keys = pygame.key.get_pressed()
    movementSpeed = (screenY/tileSize)*0.01

    if (keys[pygame.K_LEFT] and keys[pygame.K_UP]):
        cameraX += -0.707*movementSpeed
        cameraY += -0.707*movementSpeed
    elif (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]):
        cameraX += -0.707*movementSpeed
        cameraY += 0.707*movementSpeed
    elif (keys[pygame.K_LEFT]):
        cameraX += -movementSpeed
    elif (keys[pygame.K_RIGHT] and keys[pygame.K_UP]):
        cameraX += 0.707*movementSpeed
        cameraY += -0.707*movementSpeed
    elif (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]):
        cameraX += 0.707*movementSpeed
        cameraY += 0.707*movementSpeed
    elif (keys[pygame.K_RIGHT]):
        cameraX += movementSpeed
    elif (keys[pygame.K_UP]):
        cameraY += -movementSpeed
    elif (keys[pygame.K_DOWN]):
        cameraY += movementSpeed



    ## Display ##
    screen.fill((0, 0, 0))
    fogParallax = 0.2
    ratio = ((frameCounter%6000)/6000)
    bgY = (ratio*backgroundHeight) - fogParallax*cameraY*tileSize
    bgY2 = bgY - backgroundHeight
    bgY3 = bgY + backgroundHeight


    bgY -= screenY
    bgY2 -= screenY
    bgY3 -= screenY
    screen.blit(backgroundFog, (0, bgY))
    screen.blit(backgroundFog, (0, bgY2))
    screen.blit(backgroundFog, (0, bgY3))

    for x in range(0, width):
        for y in range(0, height):
            if (not tiles[width*y + x].img == "tileNotFound"):
                screen.blit(tileImagesDisplayed[tiles[width*y + x].img], ((screenX/2-(cameraX-x)*tileSize), (screenY/2-(cameraY-y)*tileSize)))
        
    refreshMenu()

    ## Frame Limiter ##
    frameCounter += 1
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    sleep_time = (1. / FPS) - dt
    if sleep_time > 0:
        time.sleep(sleep_time)