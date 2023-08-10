from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.ShapeEntity import ShapeEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ShapeButton import ShapeButton
from model.visualentity.ImageButton import ImageButton
from displayHandler import displayEntity
from openWorld import loadOpenWorld
from combat import loadCombat
import json, pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()
screenX,screenY = info.current_w,info.current_h
#screenX, screenY = 960, 600
pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('sprites/catgirl_head.png'))
screen = pygame.display.set_mode([screenX, screenY])

visualEntities = []
buttons = []


def refreshScreen():
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    for entity in buttons:
        if entity.isShowing:
            if (type(entity) == ImageButton): displayEntity(entity, screen)
            #else: displayEntity(entity.shape)
    pygame.display.flip()


def run():
    global buttons
    global visualEntities
    leaveScreen = False
    nextScreen = None

    file = open("screens/menuScreen.json", 'r')
    data = json.load(file)
    for item in data:
        entity = None
        if item["entityType"] == "Image":
            entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Drawing":
            entity = ShapeEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "ShapeButton":
            entity = ShapeButton.createFrom(item)
        elif item["entityType"] == "ImageButton":
            entity = ImageButton.createFrom(item)


        if not (entity is None):
            entity.scale(screenX, screenY)
            if (item["entityType"] == "ImageButton" or item["entityType"] == "ShapeButton"): buttons.append(entity)
            else: visualEntities.append(entity)

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
                    print(entity.name)
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "exit"): buttonFunc = exit
                        elif (entity.func == "openWorld"): buttonFunc = openWorldButton
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break

        refreshScreen()
        if (leaveScreen): break
    if (nextScreen == "Combat"):
        loadCombat()
    if (nextScreen == "Open World"):
        openWorld()
    elif (nextScreen == "Quit"):
        pygame.quit()
    else:
        print("Screen Not Found")
        run()

def combatScreen(screen, screenX, screenY):
    global visualEntities
    global buttons
    visualEntities = []
    buttons = []
    screen.fill((0, 0, 0))
    file = open("screens/loadingScreen.json", 'r')
    data = json.load(file)
    for item in data:
        if item["entityType"] == "Image":
            entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Drawing":
            entity = ShapeEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "Button":
            entity = ShapeButton.createFrom(item)
        elif item["entityType"] == "ImageButton":
            entity = ImageButton.createFrom(item)
            
        entity.resize(entity.width*screen.get_width(), entity.height*screen.get_height())
        entity.reposition(entity.xPosition * screen.get_width(),entity.yPosition * screen.get_height())
        if (item["entityType"] == "ImageButton" or item["entityType"] == "Button"): buttons.append(entity)
        else: visualEntities.append(entity)
    
    refreshScreen()
    nextScreen = loadCombat(screen, screenX, screenY)
    if (nextScreen == "Open World"):
        openWorld()
    #elif (nextScreen == "Inventory"):
    #    inventoryScreen(screen, screenX, screenY)
    elif (nextScreen == "Quit"):
        pygame.quit()
    else:
        print("Screen Not Found")
        loadOpenWorld()

def openWorld():
    global visualEntities
    global buttons
    visualEntities = []
    buttons = []
    screen.fill((0, 0, 0))
    file = open("screens/loadingScreen.json", 'r')
    data = json.load(file)
    for item in data:
        if item["entityType"] == "Image":
            entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Drawing":
            entity = ShapeEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "Button":
            entity = ShapeButton.createFrom(item)
        elif item["entityType"] == "ImageButton":
            entity = ImageButton.createFrom(item)
            
        entity.resize(entity.width*screen.get_width(), entity.height*screen.get_height())
        entity.reposition(entity.xPosition * screen.get_width(),entity.yPosition * screen.get_height())
        if (item["entityType"] == "ImageButton" or item["entityType"] == "Button"): buttons.append(entity)
        else: visualEntities.append(entity)
    
    refreshScreen()
    nextScreen = loadOpenWorld(screen, screenX, screenY)
    if (nextScreen == "Combat"):
        combatScreen(screen, screenX, screenY)
    #elif (nextScreen == "Inventory"):
    #    inventoryScreen(screen, screenX, screenY)
    elif (nextScreen == "Quit"):
        pygame.quit()
    else:
        print("Screen Not Found")
        loadOpenWorld()



run()
pygame.quit()