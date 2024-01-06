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
from model.dialogue.DialogueTreeNode import DialogueTreeNode
from view.visualentity.HoverShapeButton import HoverShapeButton
from model.player.Player import Player
from model.quest.Quest import Quest
from model.quest.Subquest import Subquest
from model.Singleton import Singleton
from view.displayHandler import displayEntity
from view.JSONParser import loadJson
import numpy as np
import sys
import math, pygame, time, random, json
from PIL import Image

visualEntities = []
buttons = []
quit = False
gameData:Singleton
currentSceneData:list

visualNovel:VisualNovel
currentNPC = None

def refreshMenu(screen):
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    pygame.display.flip()

def exitButton():
    global quit
    quit = True

def combatButton(enemies):
    global quit
    global gameData
    quit = True
    gameData.screenOpen = "Combat"
    gameData.currentEnemies = enemies

def inventoryButton():
    global quit
    global gameData
    quit = True
    gameData.screenOpen = "Inventory"


def refreshQuestListing():
    global visualEntities
    for entity in visualEntities:
        if entity.name == "CurrentQuestListing":
            currentQuests = gameData.player.getCurrentQuests()
            currentSubquests = gameData.player.getCurrentSubquests()
            if (len(gameData.player.getCurrentQuests()) > 0):
                listingString = ""
                first = True
                for quest in currentQuests:
                    if (first): listingString = listingString + "- " + quest.name
                    else: listingString = listingString + "%/n%- " + quest.name
                    first = False
                    for subquest in currentSubquests:
                        if subquest.parent == quest.id:
                            if (subquest.type == "kill"):
                                listingString = f"{listingString} %/n%     - Kill {subquest.progress}/{subquest.goal} {subquest.data}"
                                if (subquest.goal > 1):
                                    listingString = f"{listingString}s"
                            if (subquest.type == "talk"):
                                listingString = f"{listingString} %/n%     - {subquest.name}"
            else: listingString = "No current quests :/"
            entity.updateText(listingString)
            

def continueText(buttons:list):
    global visualNovel
    global currentNPC
    global gameData

    result = visualNovel.continueText()

    if (result != "Finished" and visualNovel.currentDialogue.follow_up is not None):
        gameData.player.addQuest(visualNovel.currentDialogue.follow_up)

    # Add friendship and xp handling here later

    if (result == "Options"):
        buttons.extend(visualNovel.optionButtons)
    elif (result == "Finished"):
        currentSubquests = gameData.player.getCurrentSubquests()
        for quest in currentSubquests:
            if (quest.type == "talk"):
                if (quest.data == currentNPC):
                    gameData.player.completeSubquest(quest)
                    refreshQuestListing()
        visualNovel.isShowing = False
        visualNovel.optionButtons = []

def textOption(data:DialogueTreeNode, buttons):
    global visualNovel
    global visualEntities
    global gameData

    for optionButton in visualNovel.optionButtons:
            if optionButton in buttons[:]:
                buttons.remove(optionButton)
    visualNovel.hideOptions()
    visualNovel.isShowing = False
    
    if (data.main_dialogue.follow_up is not None):
        gameData.player.addQuest(data.main_dialogue.follow_up)
        refreshQuestListing()
        refreshCurrentNPCDialogue(gameData)

    # Add friendship and xp handling here later

    if (data.main_dialogue.content is not None):
        visualNovel.isShowing = True
        visualNovel.updateDialogue(data)



def refreshCurrentNPCDialogue(gameData:Singleton):
    changedDialogue = gameData.player.getCurrentChangedDialogue()
    for npc in gameData.renderedMapEntities:
        if (type(npc) == NPC):
            if (npc.NPCID in changedDialogue.keys()):
                npc.setDialogue(changedDialogue[npc.NPCID])
            else: npc.setDialogue(npc.defaultDialogue)

def loadOpenWorld(transferredData):
    global quit
    global visualEntities
    global buttons
    global visualNovel
    global gameData
    global currentNPC
    gameData = transferredData

    screen = gameData.pygameWindow
    FPS = 60
    screenX, screenY = screen.get_size()
    prev_time = time.time()
    img = Image.open(f"src/main/python/maps/{gameData.currentMap}/map.png")
    npArray = np.array(img)
    height, width, dim = npArray.shape
    tiles = []
    TILE_SIZE = 48

    visualEntities = []
    buttons = []

    pygame.mixer.init()
    randInt = random.randint(1, 200)
    if (randInt == 69): 
        song = "nyan_cat.mp3"
    else: 
        song = "zelda_lost_woods.mp3"
    pygame.mixer.music.load(f"src/main/python/audio/music/{song}")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    file =  open(f'src/main/python/maps/{gameData.currentMap}/entityData.json', 'r')
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
            enemy = Enemy(entity['enemyType'], entity['level'], f"entities/{entity['image']}", entity['position'], gameData.database_factory)
            enemy.move((0.5, 0.5))
            allEntities.append(enemy)
        elif(entity['type'] == "npc"):
            npc = gameData.database_factory.fetchNPC(entity['id'])
            npc.setPosition(entity['position'])
            allEntities.append(npc)


    if (gameData.renderedMapEntities is None):
        character = PlayerObject((spawnX, spawnY))
        allEntities.append(character)
        for entity in allEntities:
            simulatedObjects.append(entity)
        testInteractionObject = PlayerInteractionObject((0, 0))
        testAttack = PlayerAttackObject("Physical", "Rectangle", 0.5, 4, 2, 0, 30, "sample_sword.png")
        allEntities.append(testAttack)
        allEntities.append(testInteractionObject)
        gameData.renderedMapEntities = allEntities
    else: 
        allEntities = gameData.renderedMapEntities
        for entity in allEntities:
            if (type(entity) == Enemy and entity.respawnTimer <= 0): simulatedObjects.append(entity)
            elif (type(entity) == NPC): simulatedObjects.append(entity)
            elif (type(entity) == PlayerObject): simulatedObjects.append(entity)
        for entity in allEntities:
            if (type(entity) == PlayerObject): character = entity
            if (type(entity) == PlayerInteractionObject): testInteractionObject = entity
            if (type(entity) == PlayerAttackObject): testAttack = entity

    

    refreshCurrentNPCDialogue(gameData)

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
    


    loadJson("openWorldScreen.json", screenX, screenY, visualEntities, buttons)
    emptyConversation = gameData.database_factory.fetchConversation(0)
    visualNovel = VisualNovel("vn", True, 0, 0.6, 1, 0.4, [], emptyConversation.dialogues)
    visualEntities.append(visualNovel)
    visualNovel.scale(screenX, screenY)
    visualNovel.isShowing = False
    buttons.append(visualNovel.continueButton)

    refreshQuestListing()


    FRICTION_GRASS = 0.005
    CHAR_SIZE_MULTIPLIER = 0.85

    characterSize = CHAR_SIZE_MULTIPLIER*TILE_SIZE
    radius = characterSize/(2*TILE_SIZE)
    cameraX = 0
    cameraY = 0

    

    
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
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if (not ("MenuButton" in entity.tags and visualNovel.isShowing)):
                        if (entity.isActive and entity.mouseInRegion(mouse)):
                            if (entity.func == "exit"): buttonFunc = exitButton
                            if (entity.func == "combat"): buttonFunc = combatButton
                            if (entity.func == "inventory"): 
                                inventoryButton()
                                break
                            if (entity.func == "textOption"): 
                                textOption(*entity.args, buttons)
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
                    continueText(buttons)
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
                        # corner1 = entity.getCorner1() + (x, y)
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
                                combatButton(entity.enemyStats)
                                entity.respawnTimer = 120
                            if (type(entity) == PlayerObject):
                                combatButton(trigger.enemyStats)
                                trigger.respawnTimer = 120
                            if (type(entity) == NPC):
                                visualNovel.updateDialogue(entity.currentDialogue.dialogues.head)
                                visualNovel.isShowing = True
                                currentNPC = entity.NPCID
                                 

        ## Move Enemies ##
        
        for entity in simulatedObjects:
                if type(entity) == Enemy:
                    if (entity.changeDirectionTimer <= 0):
                        enemyMoveDirection = random.randint(1, 9)
                        if enemyMoveDirection == 1: entity.enemyMoveDirection = "Up"
                        elif enemyMoveDirection == 2: entity.enemyMoveDirection = "UpRight"
                        elif enemyMoveDirection == 3: entity.enemyMoveDirection = "Right"
                        elif enemyMoveDirection == 4: entity.enemyMoveDirection = "DownRight"
                        elif enemyMoveDirection == 5: entity.enemyMoveDirection = "Down"
                        elif enemyMoveDirection == 6: entity.enemyMoveDirection = "DownLeft"
                        elif enemyMoveDirection == 7: entity.enemyMoveDirection = "Left"
                        elif enemyMoveDirection == 8: entity.enemyMoveDirection = "UpLeft"
                        entity.changeDirectionTimer += random.randint(90, 180)
                    else: entity.changeDirectionTimer -= 1

                    enemyMovementSpeed = 0.015
                    if (entity.enemyMoveDirection == "Up"):
                        entity.worldObject.speedX = 0
                        entity.worldObject.speedY = -enemyMovementSpeed
                    elif (entity.enemyMoveDirection == "UpRight"):
                        entity.worldObject.speedX = 0.707*enemyMovementSpeed
                        entity.worldObject.speedY = -0.707*enemyMovementSpeed
                    elif (entity.enemyMoveDirection == "Right"):
                        entity.worldObject.speedX = enemyMovementSpeed
                        entity.worldObject.speedY = 0
                    elif (entity.enemyMoveDirection == "DownRight"):
                        entity.worldObject.speedX = 0.707*enemyMovementSpeed
                        entity.worldObject.speedY = 0.707*enemyMovementSpeed
                    elif (entity.enemyMoveDirection == "Down"):
                        entity.worldObject.speedX = 0
                        entity.worldObject.speedY = enemyMovementSpeed
                    elif (entity.enemyMoveDirection == "DownLeft"):
                        entity.worldObject.speedX = -0.707*enemyMovementSpeed
                        entity.worldObject.speedY = 0.707*enemyMovementSpeed
                    elif (entity.enemyMoveDirection == "Left"):
                        entity.worldObject.speedX = -enemyMovementSpeed
                        entity.worldObject.speedY = 0
                    elif (entity.enemyMoveDirection == "UpLeft"):
                        entity.worldObject.speedX = -0.707*enemyMovementSpeed
                        entity.worldObject.speedY = -0.707*enemyMovementSpeed
                        

        ## Respawn Enemies ##
        for entity in allEntities:
            if (type(entity) == Enemy):
                if (entity.respawnTimer > 0 and ShapeMath.distanceBetweenPoints((entity.spawnX, entity.spawnY), character.getCenter()) > 10):
                    entity.respawnTimer -= 1
                    if (entity.respawnTimer <= 0):
                        entity.respawnTimer = 0
                        entity.setCenter((entity.spawnX, entity.spawnY))
                        simulatedObjects.append(entity)


        ## Display ##
        screen.fill((0, 0, 0))
        fogParallax = 0.2
        ratio = ((frameCounter % 6000)/ 6000)
        bgY = (ratio * backgroundHeight) - fogParallax * cameraY*TILE_SIZE
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
            gameData.renderedMapEntities = allEntities
            break
    return gameData
