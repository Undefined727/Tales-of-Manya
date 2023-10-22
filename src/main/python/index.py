import os, sys, pygame
sys.path.append(os.path.abspath("."))

from model.Singleton import Singleton
from view.displayHandler import displayEntity
from openWorld import loadOpenWorld
from combat import loadCombat
from inventory import loadInventory
from view.JSONParser import loadJson

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()
screenX,screenY = info.current_w,info.current_h
#screenX, screenY = 960, 600
pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('src/main/python/sprites/catgirl_head.png'))
screen = pygame.display.set_mode([screenX, screenY])
gameData = Singleton(screen, None)

visualEntities = []
buttons = []




def refreshScreen():
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    pygame.display.flip()


def run():
    global buttons
    global visualEntities
    global gameData
    leaveScreen = False

    loadJson("menuScreen.json", screenX, screenY, [visualEntities, buttons])

    def exit():
        pygame.quit()

    def openWorldButton():
        nonlocal leaveScreen
        global gameData
        gameData.screenOpen = "Open World"
        gameData.currentMap = "samplemap"
        leaveScreen = True

    buttonFunc = exit
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "exit"): buttonFunc = exit
                        elif (entity.func == "openWorld"): buttonFunc = openWorldButton
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break

        refreshScreen()
        if (leaveScreen): break
    switchScreens(gameData)


def switchScreens(gameData):
    global visualEntities
    global buttons
    visualEntities = []
    buttons = []
    screen.fill((0, 0, 0))
    loadJson("loadingScreen.json", screenX, screenY, [visualEntities, buttons])
    refreshScreen()

    if (gameData.screenOpen == "Open World"): gameData = loadOpenWorld(gameData)
    elif (gameData.screenOpen == "Combat"): gameData = loadCombat(gameData)
    elif (gameData.screenOpen == "Inventory"): gameData = loadInventory(gameData)
    switchScreens(gameData)


run()
pygame.quit()