import pygame
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ItemDisplay import ItemDisplay
from view.visualentity.InventoryCharacterEntity import InventoryCharacterEntity
from model.player.Player import Player
from model.Singleton import Singleton
from view.displayHandler import displayEntity
from view.JSONParser import loadJson

visualEntities = []
buttons = []
leaveScreen = False

gameData:Singleton
playerData:Player
screen:pygame.surface

def refreshScreen(screen):
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)

    pygame.display.flip()

def inventory():
    global leaveScreen
    global gameData
    leaveScreen = True
    gameData.screenOpen = "Inventory"

def loadSkillSelection(transferredData:Singleton):
    global visualEntities
    global buttons
    global gameData
    global playerData
    global screen
    global leaveScreen
    global currentCharacter
    
    leaveScreen = False
    gameData = transferredData
    playerData = gameData.player
    currentCharacter = gameData.currentCharacter
    screen = gameData.pygameWindow
    screenX, screenY = screen.get_size()
    
    loadJson("skillSelection.json", screenX, screenY, visualEntities, buttons)

    characterImg = ImageEntity("Character", True, 0.68, 0.1, 0.15, 0.3, [], f"entities/{gameData.currentCharacter.name}.png", True)
    characterImg.scale(screenX, screenY)
    visualEntities.append(characterImg)

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "inventory"): buttonFunc = inventory
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break

        refreshScreen(screen)
        if (leaveScreen):
            leaveScreen = False 
            break
    return gameData