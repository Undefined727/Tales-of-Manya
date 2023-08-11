from model.openworld.Tile import Tile
from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.ShapeEntity import ShapeEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ShapeButton import ShapeButton
from model.visualentity.ImageButton import ImageButton
from displayHandler import displayEntity
from JSONParser import loadJson
import numpy, math, pygame, time
from PIL import Image

visualEntities = []
buttons = []
quit = False
nextScreen = "Quit"

def refreshMenu(screen):
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    pygame.display.flip()

def exitButton():
    global quit
    quit = True

def combatButton():
    global quit
    global nextScreen
    quit = True
    nextScreen = "Combat"

def loadOpenWorld(screen, screenX, screenY):
    global quit
    global visualEntities
    global nextScreen
    global buttons
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
    


    loadJson("openWorldScreen.json", screenX, screenY, [visualEntities, buttons])

    spawnX = width/2
    spawnY = height/2
    characterSize = 0.85*tileSize
    radius = characterSize/(2*tileSize)
    character = pygame.image.load("sprites/catgirl_head.png")
    character = pygame.transform.scale(character, (characterSize, characterSize))
    characterX = spawnX
    characterY = spawnY
    cameraX = characterX
    cameraY = characterY
    speedX = 0
    speedY = 0
    FRICTION_GRASS = 0.005
    accX = 0
    accY = 0
    currentHeight = tiles[math.floor(characterX) + math.floor(characterY)*width].height
    

    def convertToScreen(xValue, yValue):
        xValue = (xValue-cameraX)*tileSize + screenX/2
        yValue = (yValue-cameraY)*tileSize + screenY/2
        return (xValue, yValue)

    def isInCircle(circleX, circleY, radius, x, y):
        return ((x-circleX)*(x-circleX) + (y-circleY)*(y-circleY)) < (radius*radius)
    
    movedX = 0
    movedY = 0
    
    def collision(playerX, playerY, x, y):
        nonlocal radius
        nonlocal tiles
        tile = tiles[math.floor(x) + math.floor(y)*width]
        return (isInCircle(playerX, playerY, radius, x, y) and (((currentHeight-tile.height > 1) or (currentHeight-tile.height < -1) or tile.isSolid())))


    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "exit"): buttonFunc = exitButton
                        if (entity.func == "combat"): buttonFunc = combatButton
                        if (len(entity.args) == 0): buttonFunc()
                        else: buttonFunc(entity.args)
                        break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            speedX = -0.1
        if keys[pygame.K_RIGHT]:
            speedX = 0.1
        if keys[pygame.K_UP]:
            speedY = 0.1
        if keys[pygame.K_DOWN]:
            speedY = -0.1

        accX = 0
        accY = 0
        if (speedX < -0.03): accX = FRICTION_GRASS
        elif (speedX > 0.03): accX = -FRICTION_GRASS
        else: speedX = 0
        if (speedY < -0.03): accY = FRICTION_GRASS
        elif (speedY > 0.03): accY = -FRICTION_GRASS
        else: speedY = 0

        speedX += accX
        speedY += accY

        delay = 1
        movedX = characterX + 0.5*accX*delay*delay + speedX*delay
        movedY = characterY - (0.5*accY*delay*delay + speedY*delay)
        radius = characterSize/(2*tileSize)

        if (collision(movedX, characterY, math.floor(movedX)-0.001, characterY) or collision(movedX, characterY, math.floor(movedX)-0.001, math.floor(characterY)-0.001) or collision(movedX, characterY, math.floor(movedX)-0.001, math.ceil(characterY))):
            if (speedX < 0): speedX = 0
        if (collision(movedX, characterY, math.ceil(movedX), characterY) or collision(movedX, characterY, math.ceil(movedX), math.floor(characterY)-0.001) or collision(movedX, characterY, math.ceil(movedX), math.ceil(characterY))):
            if (speedX > 0): speedX = 0
        if (collision(characterX, movedY, characterX, math.floor(movedY)-0.001) or collision(characterX, movedY, math.floor(characterX)-0.001, math.floor(movedY)-0.001) or collision(characterX, movedY, math.ceil(characterX), math.floor(movedY)-0.001)):
            if (speedY > 0): speedY = 0
        if (collision(characterX, movedY, characterX, math.ceil(movedY)) or collision(characterX, movedY, math.floor(characterX)-0.001, math.ceil(movedY)) or collision(characterX, movedY, math.ceil(characterX), math.ceil(movedY))):
            if (speedY < 0): speedY = 0

        
        characterY -= speedY
        cameraY = characterY
        characterX += speedX
        cameraX = characterX
        currentHeight = tiles[math.floor(characterX) + math.floor(characterY)*width].height


        if (tiles[math.floor(characterX) + math.floor(characterY)*width].solid):
            characterX = spawnX
            characterY = spawnY
        



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
        screen.blit(character, convertToScreen(characterX-radius, characterY-radius))
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        sleep_time = 1. / FPS - dt
        if sleep_time > 0:
            time.sleep(sleep_time)
        refreshMenu(screen)
        if (quit):
            quit = False 
            break
    return nextScreen