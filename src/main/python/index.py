import os, sys
sys.path.append(os.path.abspath("."))

from view.displayHandler import displayEntity
from openWorld import loadOpenWorld
from combat import loadCombat
from inventory import loadInventory
from view.JSONParser import loadJson
import json, pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()
screenX,screenY = info.current_w,info.current_h
#screenX, screenY = 960, 600
pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('src/main/python/sprites/catgirl_head.png'))
screen = pygame.display.set_mode([screenX, screenY])

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
    leaveScreen = False
    nextScreen = None

    loadJson("menuScreen.json", screenX, screenY, [visualEntities, buttons])

    def exit():
        pygame.quit()

    def openWorldButton():
        nonlocal nextScreen
        nonlocal leaveScreen
        nextScreen = "Open World"
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
    switchScreens(nextScreen)


def switchScreens(newScreen):
    global visualEntities
    global buttons
    visualEntities = []
    buttons = []
    screen.fill((0, 0, 0))
    loadJson("loadingScreen.json", screenX, screenY, [visualEntities, buttons])
    refreshScreen()

    if (newScreen == "Open World"): newScreen = loadOpenWorld(screen, screenX, screenY)
    elif (newScreen == "Combat"): newScreen = loadCombat(screen, screenX, screenY)
    elif (newScreen == "Inventory"): newScreen = loadInventory(screen, screenX, screenY)
    switchScreens(newScreen)


run()
pygame.quit()