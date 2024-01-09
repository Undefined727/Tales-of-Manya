import pygame
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
    
    loadJson("npcCreation.json", screenX, screenY, visualEntities, buttons)

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        refreshScreen(gameData.pygameWindow)
        if (leaveScreen):
            leaveScreen = False 
            break
    return gameData