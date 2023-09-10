import os, sys, time, pygame, math, random, json
from PIL import Image
import numpy as np
from view.JSONParser import loadJson
from view.displayHandler import displayEntity
from model.openworld.Tile import Tile
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ShapeEntity import ShapeEntity
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.Tag import Tag

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
displayedMap = savedMap
height, width, dim = savedMap.shape
tiles = []
tileSize = 48

file = open("src/main/python/maps/tileIndex.json", 'r')
tiledata = json.load(file)
tileImages = {}
tileImagesDisplayed = {}

for tile in tiledata:
    img = pygame.image.load(f"src/main/python/sprites/tiles/{tile['image']}")
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


## Tile Selection Menu ##
menuHeight = len(tiledata)*0.05
visualEntities.append(ShapeEntity("Tile_Selection_Background", False, 0.025, 0.09, 0.12, menuHeight, [Tag.EDITOR_TILE_SELECTION], "White", False, "rectangle"))
counter = 0
for tile in tiledata:
    if (tile['name'] == "tileNotFound"): break
    button = HoverShapeButton(f"Tile_Selection_Button_Entry{counter}", False, 0.025, 0.09 + 0.05*counter, 0.12, 0.05, [Tag.EDITOR_TILE_SELECTION], "white", "cyan", "rectangle", "equipTile", [tile['name']])
    visualEntities.append(button)
    buttons.append(button)
    visualEntities.append(TextEntity(f"Tile_Selection_Text_Entry{counter}", False, 0.0625, 0.115 + 0.05*counter, 0.075, 0.05, [Tag.EDITOR_TILE_SELECTION], tile['name'], "mono", 20))
    visualEntities.append(ImageEntity(f"Tile_Selection_Image_Entry{counter}", False, 0.11, 0.095 + 0.05*counter, 0.04*screenY/screenX, 0.04, [Tag.EDITOR_TILE_SELECTION], f"tiles/{tile['image']}"))
    counter += 1
button = HoverShapeButton(f"Empty_Tile_Selection_Button", False, 0.025, 0.09 + 0.05*counter, 0.12, 0.05, [Tag.EDITOR_TILE_SELECTION], "white", "cyan", "rectangle", "equipTile", ["tileNotFound"])
visualEntities.append(button)
buttons.append(button)
visualEntities.append(TextEntity(f"Empty_Tile_Selection_Text", False, 0.085, 0.115 + 0.05*counter, 0.12, 0.05, [Tag.EDITOR_TILE_SELECTION], "Remove Tile", "mono", 20))
for entity in visualEntities:
    if (Tag.EDITOR_TILE_SELECTION in entity.tags):
        entity.scale(screenX, screenY)

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

def convertToMap(xValue, yValue):
    global cameraX
    global cameraY
    xValue = (xValue - screenX/2)/tileSize + cameraX
    yValue = (yValue - screenY/2)/tileSize + cameraY
    return (xValue, yValue)

def exitButton():
    pygame.quit()




def save():
    global displayedMap
    im = Image.fromarray(displayedMap)
    im.save("src/main/python/maps/samplemap/map.png")

def tileSelectionMenuButton():
    for entity in visualEntities:
        if (Tag.EDITOR_TILE_SELECTION in entity.tags):
            entity.isShowing = not entity.isShowing

equippedTileName = tiledata[0]['name']
equippedTileImage = ImageEntity("Equipped_Tile_Image", True, 0, 0, 0.04*screenY/screenX, 0.04, [], f"tiles/{tiledata[0]['image']}")
equippedTileImage.scale(screenX, screenY)
equippedTileColor = tiledata[0]['color']
equippedTileSolid = tiledata[0]['defaultSolid']


equippedTileElevation = 0
elevationOffsetMode = False
elevationOffset = 0
visualEntities.append(equippedTileImage)
for entity in visualEntities:
    if (entity.name == "Current_Elevation_Label"):
        currentElevationLabel = entity
        break

for entity in buttons:
    if (entity.name == "ElevationToggleButton"):
        elevationToggleButton = entity
        break


def equipTile(tileName):
    global equippedTileImage
    global equippedTileName
    global equippedTileColor
    global equippedTileSolid
    equippedTileName = tileName
    if (tileName == "tileNotFound"):
        equippedTileColor = (0, 0, 0)
        equippedTileImage.updateImg("emptyimg.png")
        return
    for tile in tiledata:
        if (tile['name'] == tileName):
            equippedTileColor = tile['color']
            equippedTileSolid = tile['defaultSolid']
            equippedTileImage.updateImg(f"tiles/{tile['image']}")
            break

def elevationToggle():
    print("test")
    global elevationOffsetMode
    global currentElevationLabel
    global elevationOffset
    global equippedTileElevation
    elevationOffsetMode = not elevationOffsetMode
    if (elevationOffsetMode):
        if (elevationOffset >= 0): currentElevationLabel.updateText(f"Current Elevation: +{elevationOffset}")
        else: currentElevationLabel.updateText(f"Current Elevation: -{-1*elevationOffset}")
    else:
        currentElevationLabel.updateText(f"Current Elevation: {equippedTileElevation}")


frameCounter = 0
buttonPressed = False

### Running Editor ###
while True:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            buttonPressed = False
            for entity in buttons:
                if entity.isShowing:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "exit"): buttonFunc = exitButton
                        if (entity.func == "tileSelection"): buttonFunc = tileSelectionMenuButton
                        if (entity.func == "equipTile"): buttonFunc = equipTile
                        if (entity.func == "elevationToggle"): buttonFunc = elevationToggle
                        if (len(entity.args) == 0): buttonFunc()
                        else: buttonFunc(*entity.args)
                        buttonPressed = True
                        break
        if event.type == pygame.MOUSEBUTTONUP:
            buttonPressed = False
            for tile in tiles:
                tile.justChanged = False
        if event.type == pygame.MOUSEWHEEL:
            if (elevationToggleButton.mouseInRegion(mouse)):
                if (elevationOffsetMode): 
                    elevationOffset += event.y
                    if (elevationOffset >= 0): currentElevationLabel.updateText(f"Current Elevation: +{elevationOffset}")
                    else: currentElevationLabel.updateText(f"Current Elevation: -{-1*elevationOffset}")
                else: 
                    equippedTileElevation += event.y
                    currentElevationLabel.updateText(f"Current Elevation: {equippedTileElevation}")
            else:
                tileSize += 2*event.y
                if (tileSize <= 0): tileSize = 1
                for tile in tileImagesDisplayed:
                    tileImagesDisplayed[tile] = pygame.transform.scale(tileImages[tile], (tileSize, tileSize))
        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                if (type(button) == HoverShapeButton):
                    button.mouseInRegion(mouse)
            equippedTileImage.xPosition = mouse[0]
            equippedTileImage.yPosition = mouse[1]
            mouseX, mouseY = convertToMap(mouse[0], mouse[1])
            mouseX = math.floor(mouseX)
            mouseY = math.floor(mouseY)
            if (mouseX < 0): mouseX = 0
            if (mouseY < 0): mouseY = 0
            if (mouseX >= width): mouseX = width-1
            if (mouseY >= height): mouseY = height-1



    ### Inputs ###
    keys = pygame.key.get_pressed()
    keymods = pygame.key.get_mods()
    movementSpeed = (screenY/tileSize)*0.01

    if (pygame.mouse.get_pressed()[0] and not buttonPressed):
        mouseX, mouseY = convertToMap(mouse[0], mouse[1])
        mouseX = math.floor(mouseX)
        mouseY = math.floor(mouseY)
        if (mouseX < 0): mouseX = 0
        if (mouseY < 0): mouseY = 0
        if (mouseX >= width): mouseX = width-1
        if (mouseY >= height): mouseY = height-1
        displayedMap[mouseY, mouseX][:3] = equippedTileColor
        displayedMap[mouseY, mouseX][3] = equippedTileElevation
        if (not tiles[width*mouseY + mouseX].justChanged):
            tiles[width*mouseY + mouseX].name = equippedTileName
            if (elevationOffsetMode): tiles[width*mouseY + mouseX].height = tiles[width*mouseY + mouseX].height + elevationOffset
            else: tiles[width*mouseY + mouseX].height = equippedTileElevation
            tiles[width*mouseY + mouseX].solid = equippedTileSolid
            tiles[width*mouseY + mouseX].justChanged = True

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


    if (keymods and pygame.KMOD_CTRL and keys[pygame.K_s]):
        save()
        print("saved")



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

    ## Show Tiles ##
    for x in range(0, width):
        for y in range(0, height):
            screen.blit(tileImagesDisplayed[tiles[width*y + x].name], (convertToScreen(x, y)))
            
        
    LINE_THICKNESS = 1
    elevationMarkerTextFont = pygame.font.SysFont("mono", int(tileSize/3))
    ## Show Hitboxes and Elevation ##
    for x in range(0, width):
        for y in range(0, height):
            if (not tiles[width*y + x].name == "tileNotFound"):
                    if (tiles[width*y + x].solid): 
                        pygame.draw.line(screen, "Purple", convertToScreen(x, y), convertToScreen(x, y+1), LINE_THICKNESS)
                        pygame.draw.line(screen, "Purple", convertToScreen(x+1, y), convertToScreen(x+1, y+1), LINE_THICKNESS)
                        pygame.draw.line(screen, "Purple", convertToScreen(x, y), convertToScreen(x+1, y), LINE_THICKNESS)
                        pygame.draw.line(screen, "Purple", convertToScreen(x, y+1), convertToScreen(x+1, y+1), LINE_THICKNESS)
                    else:
                        textLabel = elevationMarkerTextFont.render(str(tiles[width*y + x].height), False, "Red")
                        textRect = textLabel.get_rect()
                        textRect.center = convertToScreen(x+0.75, y+0.75)
                        screen.blit(textLabel, textRect)
                        if (x < width-1 and (not tiles[width*y + x+1].name == "tileNotFound") and (not tiles[width*y + x+1].solid)):
                            heightDiff = abs(int(tiles[width*y + x].height) - int(tiles[width*y + x+1].height))
                            if (heightDiff == 1): pygame.draw.line(screen, "Yellow", convertToScreen(x+1, y), convertToScreen(x+1, y+1), LINE_THICKNESS)
                            elif (heightDiff > 1): pygame.draw.line(screen, "Red", convertToScreen(x+1, y), convertToScreen(x+1, y+1), LINE_THICKNESS)
                        if (y < height-1 and (not tiles[width*(y+1) + x].name == "tileNotFound") and (not tiles[width*(y+1) + x].solid)):
                            heightDiff = abs(int(tiles[width*y + x].height) - int(tiles[width*(y+1) + x].height))
                            if (heightDiff == 1): pygame.draw.line(screen, "Yellow", convertToScreen(x, y+1), convertToScreen(x+1, y+1), LINE_THICKNESS)
                            elif (heightDiff > 1): pygame.draw.line(screen, "Red", convertToScreen(x, y+1), convertToScreen(x+1, y+1), LINE_THICKNESS)

    refreshMenu()

    ## Frame Limiter ##
    frameCounter += 1
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    sleep_time = (1. / FPS) - dt
    if sleep_time > 0:
        time.sleep(sleep_time)