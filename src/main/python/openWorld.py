from model.openworld.Tile import Tile
from model.openworld.worldentities.NPC import NPC
from model.openworld.worldentities.Enemy import Enemy
from model.openworld.worldentities.PlayerAttackObject import PlayerAttackObject
from model.openworld.worldentities.PlayerInteractionObject import PlayerInteractionObject
from model.openworld.worldentities.PlayerObject import PlayerObject
from model.openworld.Rectangle import Rectangle
from model.openworld.Circle import Circle
from model.character.Character import Character
import model.openworld.ShapeMath as ShapeMath
from view.visualentity.VisualNovel import VisualNovel
from view.visualentity.HoverShapeButton import HoverShapeButton
from model.player.Player import Player
from model.player.Quest import Quest
from view.displayHandler import displayEntity
from view.JSONParser import loadJson
import numpy as np
import math, pygame, time, random, json
from PIL import Image

visualEntities = []
buttons = []
quit = False
newSceneData = []
currentSceneData:list

visualNovel:VisualNovel
currentNPC = None

playerData:Player

def refreshMenu(screen):
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    pygame.display.flip()

def exitButton():
    global quit
    quit = True

def combatButton(screen, enemies):
    global quit
    global newSceneData
    global currentSceneData
    quit = True
    newSceneData = [screen, "Combat", enemies, playerData, currentSceneData[2]]

def continueText(renderedEntities, buttons):
    global visualNovel
    global currentNPC
    result = visualNovel.continueText()
    if (result == "Options"):
        for button in visualNovel.optionButtons:
            buttons.append(button)
    elif (result == "Finished"):
        currentQuests = playerData.getCurrentQuests()
        for quest in currentQuests:
            if (quest.questType == "NPCInteractionQuest"):
                if (quest.questData == currentNPC):
                    quest.questProgress += 1
                    if (quest.questProgress >= quest.questGoal): 
                        completeQuest(quest, renderedEntities)
        visualNovel.isShowing = False
        visualNovel.optionButtons = []

def textOption(optionType, data, renderedEntities, buttons):
    global visualNovel
    global playerData

    for optionButton in visualNovel.optionButtons:
            if optionButton in buttons[:]:
                buttons.remove(optionButton)
    visualNovel.hideOptions()
    visualNovel.isShowing = False
    

    if (optionType == "End"):
        pass
    elif (optionType == "Quest"):
        playerData.addQuest(data)
        for entity in visualEntities:
            if entity.name == "CurrentQuestListing":
                currentQuests = playerData.getCurrentQuests()
                if (len(playerData.getCurrentQuests()) > 0):
                    listingString = ""
                    first = True
                    for quest in currentQuests:
                        if (first): listingString = listingString + quest.questName
                        else: listingString = listingString + "%/n%" + quest.questName
                        first = False
                else: listingString = "No current quests :/"
                entity.updateText(listingString)
        updateNPCS(renderedEntities)
    elif (optionType == "Dialogue"):
        visualNovel.isShowing = True
        visualNovel.updateDialogue(data)


def updateNPCS(renderedEntities):
    global playerData
    for quest in playerData.getCurrentQuests():
        for npc in renderedEntities:
            if (type(npc) == NPC):
                if (npc.NPCID in quest.NPCDialogue.keys()):
                    npc.dialogue = quest.NPCDialogue[npc.NPCID]

def completeQuest(quest, renderedEntities):
    global playerData

    quest.questProgress = quest.questGoal
    playerData.currentQuests.remove(quest)
    for npc in renderedEntities:
        if (type(npc) == NPC):
            if (npc.NPCID in quest.NPCDialogue.keys()):
                npc.dialogue = npc.defaultDialogue

    for id in quest.followUpQuests: 
        playerData.addQuest(id)
    updateNPCS(renderedEntities)

    for entity in visualEntities:
            if entity.name == "CurrentQuestListing":
                currentQuests = playerData.getCurrentQuests()
                if (len(playerData.getCurrentQuests()) > 0):
                    listingString = ""
                    first = True
                    for quest in currentQuests:
                        if (first): listingString = listingString + quest.questName
                        else: listingString = listingString + "%/n%" + quest.questName
                        first = False
                else: listingString = "No current quests :/"
                entity.updateText(listingString)

        

def loadOpenWorld(sceneData):
    global quit
    global visualEntities
    global buttons
    global visualNovel
    global playerData
    global currentNPC
    global currentSceneData
    currentSceneData = sceneData

    screen = sceneData[0]
    playerData = sceneData[3]
    FPS = 60
    screenX, screenY = screen.get_size()
    prev_time = time.time()
    img = Image.open(f"src/main/python/maps/{sceneData[2]}/map.png")
    npArray = np.array(img)
    height, width, dim = npArray.shape
    tiles = []
    TILE_SIZE = 48

    pygame.mixer.init()
    randInt = random.randint(1, 300)
    if (randInt == 69): 
        song = "ram_ranch_bass_boosted.mp3"
        volume = 1
    else: 
        song = "zelda_lost_woods.mp3"
        volume = 0.2
    pygame.mixer.music.load(f"src/main/python/audio/music/{song}")
    pygame.mixer.music.set_volume(volume)

    file =  open(f'src/main/python/maps/{sceneData[2]}/entityData.json', 'r')
    entitydata = json.load(file)

    spawnX = 0
    spawnY = 0
    allEntities = []
    simulatedObjects = []
    for entity in entitydata:
        if (entity['type'] == "spawnPoint"):
            spawnX = entity['position'][0]
            spawnY = entity['position'][1]
        elif(entity['type'] == "enemy"):
            enemy = Enemy(entity['enemyType'], entity['level'], f"entities/{entity['image']}", entity['position'], 30)
            allEntities.append(enemy)
            simulatedObjects.append(enemy)
        elif(entity['type'] == "npc"):
            npc = NPC(entity['defaultDialogue'], f"entities/{entity['image']}", entity['position'], entity['NPCID'], playerData.currentQuests)
            allEntities.append(npc)
            simulatedObjects.append(npc)

    file = open("src/main/python/maps/tileIndex.json", 'r')
    tiledata = json.load(file)
    tileImages = {}

    for tile in tiledata:
        img = pygame.image.load(f"src/main/python/sprites/tiles/{tile['image']}").convert()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        tileImages.update({tile['name']:img})


    for y in range(0, height):
        for x in range(0, width):
            tileFound = False
            tileColor = npArray[y, x][:3]
            tileHeight = npArray[y, x][3]
            for tile in tiledata:
                if ((tileColor == tile['color']).all()): 
                    tiles.append(Tile(tile['name'], tileHeight, tile['defaultSolid']))
                    tileFound = True
                    break
            if (not tileFound): tiles.append(Tile("tileNotFound", tileHeight, True))

    backgroundHeight = 3*screenY
    backgroundFog = pygame.image.load("src/main/python/sprites/tiles/Gofhres.png").convert()
    backgroundFog = pygame.transform.scale(backgroundFog, (screenX, backgroundHeight))
    


    loadJson("openWorldScreen.json", screenX, screenY, [visualEntities, buttons])
    visualNovel = VisualNovel("vn", True, 0, 0.6, 1, 0.4, [], 0)
    visualEntities.append(visualNovel)
    visualNovel.scale(screenX, screenY)
    visualNovel.isShowing = False
    buttons.append(visualNovel.continueButton)

    for entity in visualEntities:
        if entity.name == "CurrentQuestListing":
            currentQuests = playerData.getCurrentQuests()
            if (len(playerData.getCurrentQuests()) > 0):
                listingString = ""
                for quest in currentQuests:
                    listingString = listingString + quest.questName
            else: listingString = "No current quests :/"
            entity.updateText(listingString)


    FRICTION_GRASS = 0.005
    CHAR_SIZE_MULTIPLIER = 0.85

    characterSize = CHAR_SIZE_MULTIPLIER*TILE_SIZE
    radius = characterSize/(2*TILE_SIZE)
    cameraX = 0
    cameraY = 0


    character = PlayerObject((spawnX, spawnY))
    testInteractionObject = PlayerInteractionObject((0, 0))
    testAttack = PlayerAttackObject("Physical", "Rectangle", 0.5, 4, 2, 0, 30, "sample_sword.png")
    
    allEntities.append(character)
    allEntities.append(testAttack)
    allEntities.append(testInteractionObject)

    simulatedObjects.append(character)

    
    movementSpeed = 0.1
    character.worldObject.currentHeight = tiles[math.floor(character.getCenter()[0]) + math.floor(character.getCenter()[1])*width].height
    

    def convertToScreen(xValue, yValue):
        nonlocal cameraX
        nonlocal cameraY
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
        heightDifference = abs(int(entityHeight) - int(tileData.height))
        if ((heightDifference > 1) or tileData.isSolid()):
            if (ShapeMath.collides(moved, tile)):
                return True
        return False





    lastInput = "Right"
    changeEnemyDirection = 0
    frameCounter = 0
    continueTextCooldown = 20
    keyboardMode = False

    pygame.mixer.music.play(-1)
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
                        if (entity.func == "textOption"): 
                            textOption(*entity.args, simulatedObjects, buttons)
                            break
                        if (entity.func == "continueText"): 
                            continueText(simulatedObjects, buttons)
                            break
                        if (len(entity.args) == 0): buttonFunc()
                        else: buttonFunc(*entity.args)
                        break
            if (event.type == pygame.MOUSEMOTION):
                keyboardMode = False

        ### Make Hover Buttons shine funny color
        if (keyboardMode == False):
            for button in buttons:
                if (type(button) == HoverShapeButton):
                    button.mouseInRegion(mouse)


        ### Inputs ###
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            movementSpeed = 0.1
        else:
            movementSpeed = 0.05

        if (keyboardMode == False and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN])):
            keyboardMode = True
            for button in buttons:
                if (type(button) == HoverShapeButton):
                    button.shapeEntity.color = button.primaryColor

        if (keys[pygame.K_LEFT] and keys[pygame.K_UP]):
            character.worldObject.speedX = -0.707*movementSpeed
            character.worldObject.speedY = -0.707*movementSpeed
            lastInput = "UpLeft"
        elif (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]):
            character.worldObject.speedX = -0.707*movementSpeed
            character.worldObject.speedY = 0.707*movementSpeed
            lastInput = "DownLeft"
        elif (keys[pygame.K_LEFT]):
            character.worldObject.speedX = -movementSpeed
            lastInput = "Left"
        elif (keys[pygame.K_RIGHT] and keys[pygame.K_UP]):
            character.worldObject.speedX = 0.707*movementSpeed
            character.worldObject.speedY = -0.707*movementSpeed
            lastInput = "UpRight"
        elif (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]):
            character.worldObject.speedX = 0.707*movementSpeed
            character.worldObject.speedY = 0.707*movementSpeed
            lastInput = "DownRight"
        elif (keys[pygame.K_RIGHT]):
            character.worldObject.speedX = movementSpeed
            lastInput = "Right"
        elif (keys[pygame.K_UP]):
            character.worldObject.speedY = -movementSpeed
            lastInput = "Up"
        elif (keys[pygame.K_DOWN]):
            character.worldObject.speedY = movementSpeed
            lastInput = "Down"

        

        if keys[pygame.K_z]:
            if (testAttack.currentDuration <= 0):
                testAttack.currentDuration = testAttack.duration

                charCenter = character.getCenter()
                startAngle = 0
                if (lastInput == "UpLeft"): startAngle = 315
                elif (lastInput == "DownLeft"): startAngle = 225
                elif (lastInput == "Left"): startAngle = 270
                elif (lastInput == "UpRight"): startAngle = 45
                elif (lastInput == "DownRight"): startAngle = 135
                elif (lastInput == "Right"): startAngle = 90
                elif (lastInput == "Up"): startAngle = 0
                elif (lastInput == "Down"): startAngle = 180
                startAngle -= ((testAttack.duration*testAttack.swingSpeed)/2)
                startAngle %= 360
                testAttack.rotate(-testAttack.worldObject.currentRotation, testAttack.worldObject.getCenter())
                attackCenter = (charCenter[0], charCenter[1]-(testAttack.attackRatio*testAttack.attackSize/2))
                testAttack.setCenter(attackCenter)
                testAttack.rotate(startAngle, charCenter)

                simulatedObjects.append(testAttack)

        ## Trigger Attack Movement ##
        if (testAttack.currentDuration > 0):
            testAttack.currentDuration -=1
            charCenter = character.getCenter()
            testAttack.rotate(testAttack.swingSpeed, charCenter)
            if (testAttack.currentDuration <= 0):
                if (testAttack in simulatedObjects):
                    simulatedObjects.remove(testAttack)

        

        ## Update InteractBox ##
        if (testInteractionObject in simulatedObjects):
            simulatedObjects.remove(testInteractionObject)

        if keys[pygame.K_c]:
            charCenter = character.getCenter()
            angle = 0
            if (lastInput == "UpLeft"): angle = 315
            elif (lastInput == "DownLeft"): angle = 225
            elif (lastInput == "Left"): angle = 270
            elif (lastInput == "UpRight"): angle = 45
            elif (lastInput == "DownRight"): angle = 135
            elif (lastInput == "Right"): angle = 90
            elif (lastInput == "Up"): angle = 0
            elif (lastInput == "Down"): angle = 180
            interactObjectCenter = ShapeMath.rotatePoint((charCenter[0], charCenter[1]-2*radius), charCenter, angle)
            testInteractionObject.setCenter(interactObjectCenter)
            if (not testInteractionObject in simulatedObjects):
                simulatedObjects.append(testInteractionObject)


        
        if keys[pygame.K_SPACE]:
            if (continueTextCooldown <= 0):
                if (visualNovel.isShowing):
                    continueText(simulatedObjects, buttons)
                    continueTextCooldown += 20
        if (continueTextCooldown > 0): continueTextCooldown -= 1

        ### Physics ###
        for object in simulatedObjects:
            entity = object.worldObject
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
            if (object == character):
                testAttack.worldObject.shape.move(movedVector)
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
        for entity in list(simulatedObjects):
            if (not entity.worldObject.trigger == None):
                for trigger in list(simulatedObjects):
                    if (trigger.worldObject.entityType == entity.worldObject.trigger):
                        if (ShapeMath.collides(trigger.worldObject.shape, entity.worldObject.shape)):
                            if (type(entity) == Enemy):
                                currentQuests = playerData.getCurrentQuests()
                                for quest in currentQuests:
                                    if (quest.questType == "killQuest"):
                                        if (quest.questData == entity.enemyID):
                                            quest.questProgress += 1
                                            if (quest.questProgress >= quest.questGoal): 
                                                completeQuest(quest, simulatedObjects)
                                combatButton(screen, [entity.enemyStats])
                                simulatedObjects.remove(entity)
                                entity.respawnTimer = 60
                            if (type(entity) == PlayerObject):
                                combatButton(screen, [trigger.enemyStats])
                            if (type(entity) == NPC):
                                visualNovel.updateDialogue(entity.dialogue)
                                visualNovel.isShowing = True
                                currentNPC = entity.NPCID
                                 

        ## Move Enemies ##
        if (changeEnemyDirection <= 0):
            enemyMoveDirection = random.randint(1, 9)
            changeEnemyDirection += random.randint(90, 180)
        else: changeEnemyDirection -= 1
        for entity in simulatedObjects:
                if type(entity) == Enemy:
                    enemyMovementSpeed = 0.015
                    if (enemyMoveDirection == 1):
                        entity.worldObject.speedX = 0
                        entity.worldObject.speedY = enemyMovementSpeed
                    elif (enemyMoveDirection == 2):
                        entity.worldObject.speedX = 0.707*enemyMovementSpeed
                        entity.worldObject.speedY = 0.707*enemyMovementSpeed
                    elif (enemyMoveDirection == 3):
                        entity.worldObject.speedX = -0.707*enemyMovementSpeed
                        entity.worldObject.speedY = 0.707*enemyMovementSpeed
                    elif (enemyMoveDirection == 4):
                        entity.worldObject.speedX = enemyMovementSpeed
                        entity.worldObject.speedY = 0
                    elif (enemyMoveDirection == 5):
                        entity.worldObject.speedX = -enemyMovementSpeed
                        entity.worldObject.speedY = 0
                    elif (enemyMoveDirection == 6):
                        entity.worldObject.speedX = 0
                        entity.worldObject.speedY = 0
                    elif (enemyMoveDirection == 7):
                        entity.worldObject.speedX = 0.707*enemyMovementSpeed
                        entity.worldObject.speedY = -0.707*enemyMovementSpeed
                    elif (enemyMoveDirection == 8):
                        entity.worldObject.speedX = 0
                        entity.worldObject.speedY = -enemyMovementSpeed
                    elif (enemyMoveDirection == 9):
                        entity.worldObject.speedX = -0.707*enemyMovementSpeed
                        entity.worldObject.speedY = -0.707*enemyMovementSpeed
        

        ## Respawn Enemies ##
        # for entity in allEntities:
        #     if (type(entity) == Enemy):
        #         if (not entity.respawnTimer == 0):
        #             entity.respawnTimer -= 1
        #             if (entity.respawnTimer <= 0):
        #                 entity.respawnTimer = 0
        #                 entity.setCenter((entity.spawnX, entity.spawnY))
        #                 simulatedObjects.append(entity)


        currentQuests = playerData.getCurrentQuests()
        for quest in currentQuests:
            if (quest.questType == "freeQuest"):
                completeQuest(quest, simulatedObjects)


        ## Display ##
        screen.fill((0, 0, 0))
        fogParallax = 0.2
        ratio = ((frameCounter%6000)/6000)
        bgY = (ratio*backgroundHeight) - fogParallax*cameraY*TILE_SIZE
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
                if (not tiles[width*y + x].name == "tileNotFound"):
                    screen.blit(tileImages[tiles[width*y + x].name], ((screenX/2-(cameraX-x)*TILE_SIZE), (screenY/2-(cameraY-y)*TILE_SIZE)))
        for entity in simulatedObjects:
            if (not entity.worldObject.imgPath == "emptyimg.png"):
                screen.blit(entity.getSprite(), convertToScreen(*entity.getImagePosition()))

        # corners = testAttack.worldObject.shape.corners().copy()
        # pygame.draw.line(screen,  (255, 0, 0),  convertToScreen(*corners[0]), convertToScreen(*corners[1]))
        # pygame.draw.line(screen,  (255, 0, 0),  convertToScreen(*corners[1]), convertToScreen(*corners[2]))
        # pygame.draw.line(screen,  (255, 0, 0),  convertToScreen(*corners[2]), convertToScreen(*corners[3]))
        # pygame.draw.line(screen,  (255, 0, 0),  convertToScreen(*corners[3]), convertToScreen(*corners[0]))
        # pygame.draw.polygon(screen, (0, 255, 0), convertToScreen(corners))

            
        refreshMenu(screen)

        ## Frame Limiter ##
        frameCounter += 1
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
    return newSceneData