from model.openworld.Tile import Tile
from model.openworld.OpenWorldEntity import OpenWorldEntity
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
from model.player.Player import Player
from model.player.Quest import Quest
from view.displayHandler import displayEntity
from view.JSONParser import loadJson
import numpy as np
import math, pygame, time, random
from PIL import Image

visualEntities = []
buttons = []
quit = False
newSceneData = []

visualNovel:VisualNovel
currentDialogue = []
currentDialoguePosition = 0
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
    quit = True
    newSceneData = [screen, "Combat", enemies, playerData]

def continueText(renderedEntities):
    global currentDialogue
    global currentDialoguePosition
    global visualNovel
    global currentNPC
    if (currentDialoguePosition >= len(currentDialogue)):
        currentQuests = playerData.getCurrentQuests()
        for quest in currentQuests:
            if (quest.questType == "NPCInteractionQuest"):
                if (quest.questData == currentNPC):
                    quest.questProgress += 1
                    if (quest.questProgress >= quest.questGoal): 
                        completeQuest(quest, renderedEntities)
        currentDialoguePosition = 0
        visualNovel.isShowing = False
    else:
        visualNovel.updateText(currentDialogue[currentDialoguePosition])
        currentDialoguePosition +=1

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
        playerData.currentQuests.append(Quest(id))
    updateNPCS(renderedEntities)

    for entity in visualEntities:
        if entity.name == "CurrentQuestListing":
            if (len(playerData.getCurrentQuests()) > 0):
                entity.updateText(playerData.getCurrentQuests()[0].questName)
            else: entity.updateText("No current quests :/")

        

def loadOpenWorld(sceneData):
    global quit
    global visualEntities
    global buttons
    global visualNovel
    global playerData
    global currentDialoguePosition
    global currentDialogue
    global currentNPC
    screen = sceneData[0]
    playerData = sceneData[3]
    FPS = 60
    screenX, screenY = screen.get_size()
    prev_time = time.time()
    img = Image.open("src/main/python/maps/" + sceneData[2] + ".png")
    npArray = np.array(img)
    height, width, dim = npArray.shape
    tiles = []
    TILE_SIZE = 48
    tileImgIndex ={"tree":"tree.png", "bridge":"bridge.png","wall":"wall.png","water":"water.png","wet_sand":"wet_sand.png","sand":"sand.png","grass4":"grass4.png"}
    tileImgIndex.update({"grass3":"grass3.png","grass2":"grass2.png","grass1":"grass1.png","nekoarc":"nekoarc.png"})
    for name, image in tileImgIndex.items():
        img = image
        img = pygame.image.load(f"src/main/python/sprites/tiles/{img}").convert()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        tileImgIndex.update({name:img})
    backgroundHeight = 3*screenY
    backgroundFog = pygame.image.load("src/main/python/sprites/tiles/Gofhres.png").convert()
    backgroundFog = pygame.transform.scale(backgroundFog, (screenX, backgroundHeight))


    for y in range(0, height):
        for x in range(0, width):
            if ((npArray[y, x] == [107, 82, 10, 255]).all()): tiles.append(Tile("tree", 1, True)) # tree
            elif ((npArray[y, x] == (210, 132, 53, 255)).all()): tiles.append(Tile("bridge", 1)) # bridge
            elif ((npArray[y, x] == (0, 0, 0, 255)).all()): tiles.append(Tile("wall", 1, True)) # wall
            elif ((npArray[y, x] == (36, 98, 200, 255)).all()): tiles.append(Tile("water", 1, True)) # water
            elif ((npArray[y, x] == (193, 174, 2, 255)).all()): tiles.append(Tile("wet_sand", 1)) # wet_sand
            elif ((npArray[y, x] == (204, 225, 77, 255)).all()): tiles.append(Tile("sand", 1)) #sand
            elif ((npArray[y, x] == (58, 255, 0, 255)).all()): tiles.append(Tile("grass4", 4))
            elif ((npArray[y, x] == (51, 223, 0, 255)).all()): tiles.append(Tile("grass3", 3))
            elif ((npArray[y, x] == (44, 189, 1, 255)).all()): tiles.append(Tile("grass2", 2))
            elif ((npArray[y, x] == (30, 133, 0, 255)).all()): tiles.append(Tile("grass1", 1))
            else: tiles.append(Tile("nekoarc", 4))
    


    loadJson("openWorldScreen.json", screenX, screenY, [visualEntities, buttons])
    visualNovel = VisualNovel("vn", True, 0, 0.6, 1, 0.4, tags = [], text = "This is a text paragraph example it's supposed to be very long blah blah blah blah blah, this actually doesn't end lmaoThis is a text paragraph example it's supposed to be very long blah blah blah blah blah, this actually doesn't end lmaoThis is a text paragraph example it's supposed to be very long blah blah blah blah blah, this actually doesn't end lmaoThis is a text paragraph example it's supposed to be very long blah blah blah blah blah, this actually doesn't end lmao")
    visualEntities.append(visualNovel)
    visualNovel.scale(screenX, screenY)
    visualNovel.isShowing = False
    buttons.append(visualNovel.continueButton)

    for entity in visualEntities:
        if entity.name == "CurrentQuestListing":
            if (len(playerData.getCurrentQuests()) > 0):
                entity.updateText(playerData.getCurrentQuests()[0].questName)
            else: entity.updateText("No current quests :/")


    FRICTION_GRASS = 0.005
    CHAR_SIZE_MULTIPLIER = 0.85

    spawnX = width/2
    spawnY = height/2
    characterSize = CHAR_SIZE_MULTIPLIER*TILE_SIZE
    radius = characterSize/(2*TILE_SIZE)
    cameraX = 0
    cameraY = 0


    character = PlayerObject((spawnX, spawnY))
    testInteractionObject = PlayerInteractionObject((0, 0))
    testAttack = PlayerAttackObject("Physical", "Rectangle", 0.5, 4, 2, 0, 30, "sample_sword.png")
    testEnemy = Enemy("Slime", 5, "wizard.png", (character.getCenter()[0]+5, character.getCenter()[1]+1), 30)
    testNPC = NPC(["I am an NPC with default dialogue :D"], "catgirl.png", (character.getCenter()[0]+1, character.getCenter()[1]+5), "Test_NPC", playerData.currentQuests)
    

    



    allEntities = []
    allEntities.append(character)
    allEntities.append(testEnemy)
    allEntities.append(testNPC)
    allEntities.append(testAttack)
    allEntities.append(testInteractionObject)

    simulatedObjects = []
    simulatedObjects.append(character)
    simulatedObjects.append(testEnemy)
    simulatedObjects.append(testNPC)

    
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
        if ((abs(entityHeight - tileData.height) > 1) or tileData.isSolid()):
            if (ShapeMath.collides(moved, tile)):
                return True
        return False





    lastInput = "Right"
    changeEnemyDirection = 0
    frameCounter = 0
    continueTextCooldown = 20


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
                        if (entity.func == "continueText"): 
                            continueText(simulatedObjects)
                            break
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
                continueText(simulatedObjects)
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
                                            print(quest.questProgress)
                                            if (quest.questProgress >= quest.questGoal): 
                                                completeQuest(quest, simulatedObjects)
                                combatButton(screen, [entity.enemyStats])
                                simulatedObjects.remove(entity)
                                entity.respawnTimer = 60
                            if (type(entity) == PlayerObject):
                                combatButton(screen, [trigger.enemyStats])
                            if (type(entity) == NPC):
                                currentDialogue = entity.dialogue
                                visualNovel.isShowing = True
                                currentDialoguePosition = 0
                                currentNPC = entity.NPCID
                                continueText(simulatedObjects)
                                 

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
                if (not tiles[width*y + x].img == "nekoarc"):
                    screen.blit(tileImgIndex[tiles[width*y + x].img], ((screenX/2-(cameraX-x)*TILE_SIZE), (screenY/2-(cameraY-y)*TILE_SIZE)))
        for entity in simulatedObjects:
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