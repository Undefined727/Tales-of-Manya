from model.openworld.Tile import Tile
from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.ShapeEntity import ShapeEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ShapeButton import ShapeButton
from model.visualentity.ImageButton import ImageButton
from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Rectangle import Rectangle
from model.openworld.Circle import Circle
import model.openworld.ShapeMath as ShapeMath
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
            if ((npArray[y, x] == [107, 82, 10, 255]).all()): tiles.append(Tile("tree.png", 1, True))
            elif ((npArray[y, x] == (210, 132, 53, 255)).all()): tiles.append(Tile("bridge.png", 1))
            elif ((npArray[y, x] == (0, 0, 0, 255)).all()): tiles.append(Tile("wall.png", 1, True))
            elif ((npArray[y, x] == (36, 98, 200, 255)).all()): tiles.append(Tile("water.png", 1, True))
            elif ((npArray[y, x] == (193, 174, 2, 255)).all()): tiles.append(Tile("wet_sand.png", 1))
            elif ((npArray[y, x] == (204, 225, 77, 255)).all()): tiles.append(Tile("sand.png", 1))
            elif ((npArray[y, x] == (58, 255, 0, 255)).all()): tiles.append(Tile("grass4.png", 4))
            elif ((npArray[y, x] == (51, 223, 0, 255)).all()): tiles.append(Tile("grass3.png", 3))
            elif ((npArray[y, x] == (44, 189, 1, 255)).all()): tiles.append(Tile("grass2.png", 2))
            elif ((npArray[y, x] == (30, 133, 0, 255)).all()): tiles.append(Tile("grass1.png", 1))
            else: tiles.append(Tile("nekoarc.png", 4))
    


    loadJson("openWorldScreen.json", screenX, screenY, [visualEntities, buttons])

    FRICTION_GRASS = 0.005
    CHAR_SIZE_MULTIPLIER = 0.85
    TILE_SIZE = 48

    spawnX = width/2
    spawnY = height/2
    characterSize = CHAR_SIZE_MULTIPLIER*TILE_SIZE
    radius = characterSize/(2*TILE_SIZE)
    characterX = spawnX
    characterY = spawnY
    cameraX = characterX
    cameraY = characterY
    character = OpenWorldEntity("catgirl_head.png", Circle((characterX, characterY), radius), "player", None, None)
    sword = OpenWorldEntity("sample_sword.png", Rectangle([(0, 0),  (0, 4*radius), (2*radius, 0), (2*radius, 4*radius)]), "attack", None, None)
    sword.setCenter((characterX, characterY-3*radius))
    swordSwinging = 0

    currentEntities = []
    currentEntities.append(character)

    
    movementSpeed = 0.1
    character.currentHeight = tiles[math.floor(characterX) + math.floor(characterY)*width].height
    

    def convertToScreen(xValue, yValue):
        xValue = (xValue-cameraX)*TILE_SIZE + screenX/2
        yValue = (yValue-cameraY)*TILE_SIZE + screenY/2
        return (xValue, yValue)

    def isInCircle(circleX, circleY, radius, x, y):
        return ((x-circleX)*(x-circleX) + (y-circleY)*(y-circleY)) < (radius*radius)
    
    def collision(playerX, playerY, x, y):
        nonlocal radius
        nonlocal tiles
        tile = tiles[math.floor(x) + math.floor(y)*width]
        return (isInCircle(playerX, playerY, radius, x, y) and (((character.currentHeight-tile.height > 1) or (character.currentHeight-tile.height < -1) or tile.isSolid())))















    ### Running Game :D ###
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



        ### Inputs ###
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            movementSpeed = 0.1
        else:
            movementSpeed = 0.05
        if keys[pygame.K_LEFT]:
            character.speedX = -movementSpeed
        if keys[pygame.K_RIGHT]:
            character.speedX = movementSpeed
        if keys[pygame.K_UP]:
            character.speedY = movementSpeed
        if keys[pygame.K_DOWN]:
            character.speedY = -movementSpeed

        if keys[pygame.K_SPACE]:
            if (swordSwinging <= 0):
                swordSwinging = 30
                if keys[pygame.K_RIGHT]:
                    if keys[pygame.K_UP]:
                        sword.rotate(15, character.getCenter())
                    elif keys[pygame.K_DOWN]:
                        sword.rotate(105, character.getCenter())
                    else:
                        sword.rotate(55, character.getCenter())
                elif keys[pygame.K_LEFT]:
                    if keys[pygame.K_UP]:
                        sword.rotate(285, character.getCenter())
                    elif keys[pygame.K_DOWN]:
                        sword.rotate(195, character.getCenter())
                    else: sword.rotate(235, character.getCenter())
                elif keys[pygame.K_UP]: 
                    sword.rotate(330, character.getCenter())
                elif keys[pygame.K_DOWN]: 
                    sword.rotate(150, character.getCenter())
                else: sword.rotate(55, character.getCenter())
                currentEntities.append(sword)


        ### Physics ###
        character.accX = 0
        character.accY = 0
        if (character.speedX < -FRICTION_GRASS): character.accX += FRICTION_GRASS
        elif (character.speedX > FRICTION_GRASS): character.accX += -FRICTION_GRASS
        else: character.speedX = 0
        if (character.speedY < -FRICTION_GRASS): character.accY += FRICTION_GRASS
        elif (character.speedY > FRICTION_GRASS): character.accY += -FRICTION_GRASS
        else: character.speedY = 0

        character.speedX += character.accX
        character.speedY += character.accY
        
        delay = 1
        movedX = characterX + 0.5*character.accX*delay*delay + character.speedX*delay
        movedY = characterY - (0.5*character.accY*delay*delay + character.speedY*delay)
        radius = characterSize/(2*TILE_SIZE)


        ### Player Collision with Tiles ##
        justCorrected = False
        if (collision(movedX, characterY, math.floor(movedX)-0.001, characterY) or collision(movedX, characterY, math.floor(movedX)-0.001, math.floor(characterY)-0.001) or collision(movedX, characterY, math.floor(movedX)-0.001, math.ceil(characterY))):
            if (character.speedX < 0): character.speedX = 0
            if (not collision(movedX, characterY, math.floor(movedX)-0.001, characterY) and character.speedY == 0):
                justCorrected = True
                if collision(movedX, characterY, math.floor(movedX)-0.001, math.floor(characterY)-0.001):
                    characterY += 0.05
                else:
                    characterY -= 0.05
        if (collision(movedX, characterY, math.ceil(movedX), characterY) or collision(movedX, characterY, math.ceil(movedX), math.floor(characterY)-0.001) or collision(movedX, characterY, math.ceil(movedX), math.ceil(characterY))):
            if (character.speedX > 0): character.speedX = 0
            if (not collision(movedX, characterY, math.ceil(movedX), characterY) and character.speedY == 0):
                justCorrected = True
                if collision(movedX, characterY, math.ceil(movedX), math.floor(characterY)-0.001):
                    characterY += 0.05
                else:
                    characterY -= 0.05
        if (collision(characterX, movedY, characterX, math.floor(movedY)-0.001) or collision(characterX, movedY, math.floor(characterX)-0.001, math.floor(movedY)-0.001) or collision(characterX, movedY, math.ceil(characterX), math.floor(movedY)-0.001)):
            if (character.speedY > 0): character.speedY = 0
            if (not collision(characterX, movedY, characterX, math.floor(movedY)-0.001) and character.speedX == 0):
                justCorrected = True
                if collision(characterX, movedY, math.floor(characterX)-0.001, math.floor(movedY)-0.001):
                    characterX += 0.05
                else:
                    characterX -= 0.05
        if (collision(characterX, movedY, characterX, math.ceil(movedY)) or collision(characterX, movedY, math.floor(characterX)-0.001, math.ceil(movedY)) or collision(characterX, movedY, math.ceil(characterX), math.ceil(movedY))):
            if (character.speedY < 0): character.speedY = 0
            if (not collision(characterX, movedY, characterX, math.ceil(movedY)) and character.speedX == 0):
                justCorrected = True
                if collision(characterX, movedY, math.floor(characterX)-0.001, math.ceil(movedY)):
                    characterX += 0.05
                else:
                    characterX -= 0.05
        


        ## Update Player and Camera Position ##
        characterY -= character.speedY
        characterX += character.speedX
        character.setCenter((characterX, characterY))
        sword.move((character.speedX, -1*character.speedY))
        if (not justCorrected):
            cameraY = characterY
            cameraX = characterX
        character.currentHeight = tiles[math.floor(characterX) + math.floor(characterY)*width].height


        ## If the character is stuck respawn them ##
        if (tiles[math.floor(characterX) + math.floor(characterY)*width].solid):
            characterX = spawnX
            characterY = spawnY
        if (characterX < 0): characterX = spawnX
        elif (characterX > width-1): characterX = spawnX
        if (characterY < 0): characterY = spawnY
        elif (characterY > height-1): characterY = spawnY


        ## If the camera goes out of bounds bound it ##
        if (cameraX < (screenX/TILE_SIZE)/2): cameraX = (screenX/TILE_SIZE)/2
        elif (cameraX > width-(screenX/TILE_SIZE)/2): cameraX = width-(screenX/TILE_SIZE)/2
        if (cameraY > height-(screenY/TILE_SIZE)/2): cameraY = height-(screenY/TILE_SIZE)/2
        elif (cameraY < (screenY/TILE_SIZE)/2): cameraY = (screenY/TILE_SIZE)/2

        ## Entity Collision Logic ##
        for entity in currentEntities:
         if (not entity.trigger == None):
              for trigger in currentEntities:
                   if (trigger.entityType == entity.trigger):
                        if (ShapeMath.collides(trigger.shape, entity.shape)):
                             if (entity.entityType == "enemy"):
                                  entity.data.health.setCurrentValue(entity.data.health.getCurrentValue()-10)
                                  print(str(entity.data.health.getCurrentValue()) + "/" + str(entity.data.health.getMaxValue()))

        ## Swing Sword ##
        if (swordSwinging > 0):
            swordSwinging -=1
            sword.rotate(2, character.getCenter())
            if (swordSwinging == 0):
                if (sword in currentEntities):
                    currentEntities.remove(sword)
                sword = OpenWorldEntity("sample_sword.png", Rectangle([(0, 0),  (0, 4*radius), (2*radius, 0), (2*radius, 4*radius)]), "attack", None, None)
                sword.setCenter((characterX, characterY-3*radius))


        ## Display ##
        screen.fill((0, 0, 0))
        for x in range(0, width):
            for y in range(0, height):
                screen.blit(tiles[width*y + x].img, ((screenX/2-(cameraX-x)*TILE_SIZE), (screenY/2-(cameraY-y)*TILE_SIZE)))
        for entity in currentEntities:
            screen.blit(entity.getSprite(), convertToScreen(*entity.getImagePosition()))
        refreshMenu(screen)


        ## Frame Limiter ##
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        sleep_time = (1. / FPS) - dt
        if sleep_time > 0:
            time.sleep(sleep_time)
        

        ## Quit ##
        if (quit):
            quit = False 
            break
    return nextScreen