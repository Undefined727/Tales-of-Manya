import pygame, time
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ImageButton import ImageButton
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

def refreshScreen(screen):
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)

    pygame.display.flip()


def loadNPCCreation(transferredData:Singleton):
    global visualEntities
    global buttons
    global gameData
    global screen
    global leaveScreen

    visualEntities = []
    buttons = []

    leaveScreen = False
    gameData = transferredData
    screenX, screenY = gameData.pygameWindow.get_size()
    FPS = 60

    loadJson("npcCreation.json", screenX, screenY, visualEntities, buttons)

    for entity in visualEntities:
        if entity.name == "NPCNameEntryParagraph":
            npcTextEntryParagraph = entity
            break

    delCharacterTimer = 40
    prev_time = time.time()
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                text = npcTextEntryParagraph.text
                if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        delCharacterTimer = 40
                else:
                    text = f"{text}{event.unicode}"
                npcTextEntryParagraph.updateText(text)


        keys = pygame.key.get_pressed()
        if (delCharacterTimer > 0): delCharacterTimer -= 1

        if (keys[pygame.K_BACKSPACE]):
            if (delCharacterTimer <= 0):
                npcTextEntryParagraph.updateText(npcTextEntryParagraph.text[:-1])
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