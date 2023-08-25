from model.openworld.Tile import Tile
from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.ShapeEntity import ShapeEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ShapeButton import ShapeButton
from model.visualentity.ImageButton import ImageButton
from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.openworld.Rectangle import Rectangle
from model.openworld.Circle import Circle
from model.character.Character import Character
import model.openworld.ShapeMath as ShapeMath
from displayHandler import displayEntity
from JSONParser import loadJson
import numpy as np
import math, pygame, time, random
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
    npArray = np.array(img)
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
    character = OpenWorldEntity("catgirl_head.png", Circle((spawnX, spawnY), radius), "player", None, "enemy")
    cameraX = character.getCenter()[0]
    cameraY = character.getCenter()[1]

    sword = OpenWorldEntity("sample_sword.png", Rectangle([(0, 0),  (0, 4*radius), (2*radius, 0), (2*radius, 4*radius)]), "attack", None, None)
    # Sets height to -1 to indicate no corner correction
    sword.currentHeight = -1
    swordSwinging = 0

    testEnemyStats = Character("Wizard", "wizard.png", 5)
    testEnemy = OpenWorldEntity("frog_head.png", Circle((character.getCenter()[0]+5, character.getCenter()[1]+1), radius), "enemy", testEnemyStats, "attack")

    currentEntities = []
    currentEntities.append(character)
    currentEntities.append(testEnemy)

    
    movementSpeed = 0.1
    character.currentHeight = tiles[math.floor(character.getCenter()[0]) + math.floor(character.getCenter()[1])*width].height
    

    def convertToScreen(xValue, yValue):
        xValue = (xValue-cameraX)*TILE_SIZE + screenX/2
        yValue = (yValue-cameraY)*TILE_SIZE + screenY/2
        return (xValue, yValue)
    
    # Compares entity and shape
    def collisionTile(entity, tile, movedVector):
        nonlocal tiles
        moved = entity.newMoved(movedVector)
        minX = tile.getImagePosition()[0]
        minY = tile.getImagePosition()[1]
        movedCenter = moved.getCenter()
        entityHeight = tiles[math.floor(movedCenter[0]) + math.floor(movedCenter[1])*width].height
        
        tileData = tiles[round(minX) + round(minY)*width]
        if ((abs(entityHeight - tileData.height) > 1) or tileData.isSolid()):
            if (ShapeMath.collides(moved, tile)):
                return True
        return False





    lastInput = "Right"
    changeEnemyDirection = 0
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

        if (keys[pygame.K_LEFT] and keys[pygame.K_UP]):
            character.speedX = -0.707*movementSpeed
            character.speedY = -0.707*movementSpeed
            lastInput = "UpLeft"
        elif (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]):
            character.speedX = -0.707*movementSpeed
            character.speedY = 0.707*movementSpeed
            lastInput = "DownLeft"
        elif (keys[pygame.K_LEFT]):
            character.speedX = -movementSpeed
            lastInput = "Left"
        elif (keys[pygame.K_RIGHT] and keys[pygame.K_UP]):
            character.speedX = 0.707*movementSpeed
            character.speedY = -0.707*movementSpeed
            lastInput = "UpRight"
        elif (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]):
            character.speedX = 0.707*movementSpeed
            character.speedY = 0.707*movementSpeed
            lastInput = "DownRight"
        elif (keys[pygame.K_RIGHT]):
            character.speedX = movementSpeed
            lastInput = "Right"
        elif (keys[pygame.K_UP]):
            character.speedY = -movementSpeed
            lastInput = "Up"
        elif (keys[pygame.K_DOWN]):
            character.speedY = movementSpeed
            lastInput = "Down"

        

        if keys[pygame.K_SPACE]:
            if (swordSwinging <= 0):
                swordSwinging = 30
                if (lastInput == "UpLeft"): sword.rotate(285, character.getCenter())
                elif (lastInput == "DownLeft"): sword.rotate(195, character.getCenter())
                elif (lastInput == "Left"): sword.rotate(235, character.getCenter())
                elif (lastInput == "UpRight"): sword.rotate(15, character.getCenter())
                elif (lastInput == "DownRight"): sword.rotate(105, character.getCenter())
                elif (lastInput == "Right"): sword.rotate(55, character.getCenter())
                elif (lastInput == "Up"): sword.rotate(330, character.getCenter())
                elif (lastInput == "Down"): sword.rotate(150, character.getCenter())
                currentEntities.append(sword)


        ### Physics ###
        for entity in currentEntities:
            ## Friction ##
            if (abs(entity.speedX) < FRICTION_GRASS):
                entity.speedX = 0
            else:
                entity.speedX = entity.speedX - math.copysign(FRICTION_GRASS, entity.speedX)
            if (abs(entity.speedY) < FRICTION_GRASS):
                entity.speedY = 0
            else:
                entity.speedY = entity.speedY - math.copysign(FRICTION_GRASS, entity.speedY)

        
            movedXVector = np.array([entity.speedX, 0])
            movedYVector = np.array([0, entity.speedY])
            
            #### Entity Collision with Tiles ####
            if (not entity.currentHeight == -1):

                ## Generate Tiles entity may collide with ##
                minX = entity.getImagePosition()[0]
                minY = entity.getImagePosition()[1]
                maxX = (entity.getImagePosition() + entity.getImageSize())[0]
                maxY = (entity.getImagePosition() + entity.getImageSize())[1]

                scannedWidth = int(math.ceil(maxX)-math.floor(minX)+2)
                scannedHeight = int(math.ceil(maxY)-math.floor(minY)+2)

                scannedTiles = []
                for y in range(0, scannedHeight):
                    for x in range(0, scannedWidth):
                        corner1 = np.array([(math.floor(minX)-1 + x), (math.floor(minY)-1 + y)])
                        corner2 = np.array([(math.floor(minX) + x), (math.floor(minY)-1 + y)])
                        corner3 = np.array([(math.floor(minX)-1 + x), (math.floor(minY) + y)])
                        corner4 = np.array([(math.floor(minX) + x), (math.floor(minY) + y)])
                        scannedTiles.append(Rectangle([corner1, corner2, corner3, corner4]))


                ## Check Collision ##
                for y in range(0, scannedHeight):
                    for x in range(0, scannedWidth):
                        tile = scannedTiles[x + y*scannedWidth]
                        if (collisionTile(entity, tile, movedXVector)):
                            movedXVector[0] = 0
                        if (collisionTile(entity, tile, movedYVector)):
                            movedYVector[1] = 0
                        if (movedXVector[0] == 0 and movedYVector[1] == 0): 
                            break
                    else:
                        continue
                    break


            movedVector = movedXVector + movedYVector

            ## Move Thing ##
            entity.shape.move(movedVector)
            entity.currentHeight = tiles[math.floor(entity.getCenter()[0]) + math.floor(entity.getCenter()[1])*width].height
            if (movedVector[0] == 0): entity.speedX = 0
            if (movedVector[1] == 0): entity.speedY = 0



        ## Update Camera Position ##
        cameraY = character.getCenter()[1]
        cameraX = character.getCenter()[0]
        


        ## If the character is stuck respawn them ##
        if (tiles[math.floor(character.getCenter()[0]) + math.floor(character.getCenter()[1])*width].solid):
            character.getCenter()[0] = spawnX
            character.getCenter()[1] = spawnY
        if (character.getCenter()[0] < 0): character.getCenter()[0] = spawnX
        elif (character.getCenter()[0] > width-1): character.getCenter()[0] = spawnX
        if (character.getCenter()[1] < 0): character.getCenter()[1] = spawnY
        elif (character.getCenter()[1] > height-1): character.getCenter()[1] = spawnY


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
                                  combatButton()
                             if (entity.entityType == "player"):
                                  combatButton()


        ## Update Sword Position ##
        charCenter = character.getCenter()
        swordCenter = ShapeMath.rotatePoint((charCenter[0], charCenter[1]-3*radius), charCenter, -sword.currentRotation)
        sword.setCenter(swordCenter)

        ## Swing Sword ##
        if (swordSwinging > 0):
            swordSwinging -=1
            sword.rotate(2, charCenter)
            if (swordSwinging == 0):
                sword.rotate((sword.currentRotation-360), charCenter)
                if (sword in currentEntities):
                    currentEntities.remove(sword)

        ## Move Enemies ##
        if (changeEnemyDirection <= 0):
            enemyMoveDirection = random.randint(1, 9)
            changeEnemyDirection += random.randint(90, 180)
        else: changeEnemyDirection -= 1
        for entity in currentEntities:
                if entity.entityType == "enemy":
                    enemyMovementSpeed = 0.03
                    if (enemyMoveDirection == 1):
                        entity.speedX = 0
                        entity.speedY = enemyMovementSpeed
                    elif (enemyMoveDirection == 2):
                        entity.speedX = 0.707*enemyMovementSpeed
                        entity.speedY = 0.707*enemyMovementSpeed
                    elif (enemyMoveDirection == 3):
                        entity.speedX = -0.707*enemyMovementSpeed
                        entity.speedY = 0.707*enemyMovementSpeed
                    elif (enemyMoveDirection == 4):
                        entity.speedX = enemyMovementSpeed
                        entity.speedY = 0
                    elif (enemyMoveDirection == 5):
                        entity.speedX = -enemyMovementSpeed
                        entity.speedY = 0
                    elif (enemyMoveDirection == 6):
                        entity.speedX = 0
                        entity.speedY = 0
                    elif (enemyMoveDirection == 7):
                        entity.speedX = 0.707*enemyMovementSpeed
                        entity.speedY = -0.707*enemyMovementSpeed
                    elif (enemyMoveDirection == 8):
                        entity.speedX = 0
                        entity.speedY = -enemyMovementSpeed
                    elif (enemyMoveDirection == 9):
                        entity.speedX = -0.707*enemyMovementSpeed
                        entity.speedY = -0.707*enemyMovementSpeed
        


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