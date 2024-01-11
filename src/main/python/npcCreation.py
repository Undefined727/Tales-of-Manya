import pygame, time
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ImageButton import ImageButton
from view.visualentity.HoverShapeButton import HoverShapeButton
from view.visualentity.TextEntity import TextEntity
from view.visualentity.Paragraph import Paragraph
from model.Singleton import Singleton
from view.displayHandler import displayEntity
from view.JSONParser import loadJson

visualEntities = []
buttons = []
leaveScreen = False

gameData:Singleton
screen:pygame.surface

selectedTextEntry = None

def refreshScreen(screen):
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)

    pygame.display.flip()

def selectTextEntry(selectedEntry):
    global selectedTextEntry
    global visualEntities
    print(selectedEntry)
    for entity in visualEntities:
        print(entity.name)
        if entity.name == selectedEntry:
            selectedTextEntry = entity

def loadNPCCreation(transferredData:Singleton):
    global visualEntities
    global buttons
    global gameData
    global screen
    global leaveScreen
    global selectedTextEntry

    visualEntities = []
    buttons = []

    leaveScreen = False
    gameData = transferredData
    screenX, screenY = gameData.pygameWindow.get_size()
    FPS = 60

    loadJson("npcCreation.json", screenX, screenY, visualEntities, buttons)

    
    selectedTextEntry = None
    delCharacterTimer = 40
    prev_time = time.time()
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                selectedTextEntry = None
                for entity in buttons:
                    if (entity.isActive and entity.mouseInRegion(mouse)):
                        if (entity.func == "selectTextEntry"): buttonFunc = selectTextEntry
                        if (len(entity.args) == 0): buttonFunc()
                        else: buttonFunc(*entity.args)
                        break
            if event.type == pygame.KEYDOWN:
                if (selectedTextEntry is None): break
                text = selectedTextEntry.text
                if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        delCharacterTimer = 40
                else:
                    text = f"{text}{event.unicode}"
                selectedTextEntry.updateText(text)


        ### Make Hover Buttons shine funny color
        for button in buttons:
            if (type(button) == HoverShapeButton):
                button.mouseInRegion(mouse)


        keys = pygame.key.get_pressed()
        if (delCharacterTimer > 0): delCharacterTimer -= 1

        if (keys[pygame.K_BACKSPACE]):
            if (selectedTextEntry is None): break
            if (delCharacterTimer <= 0):
                selectedTextEntry.updateText(selectedTextEntry.text[:-1])
                delCharacterTimer = 8

        ## Frame Limiter ##
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        sleep_time = (1. / FPS) - dt
        if sleep_time > 0:
            time.sleep(sleep_time)

        refreshScreen(gameData.pygameWindow)
        if (leaveScreen):
            leaveScreen = False 
            break
    return gameData