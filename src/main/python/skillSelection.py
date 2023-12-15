import pygame, math
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ImageButton import ImageButton
from view.visualentity.TextEntity import TextEntity
from view.visualentity.Paragraph import Paragraph
from view.visualentity.ItemDisplay import ItemDisplay
from view.visualentity.InventoryCharacterEntity import InventoryCharacterEntity
from model.player.Player import Player
from model.character.Skill import Skill
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

def showSkillDetails(skill:Skill):
    global visualEntities
    for entity in visualEntities[:]:
        if "SkillDetails" in entity.tags:
            visualEntities.remove(entity)
    desc = Paragraph("description", True, 0.6, 0.6, 0.3, 0.3, ["SkillDetails"], skill.description)
    desc.scale(*gameData.pygameWindow.get_size())
    visualEntities.append(desc)
    pass

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

    visualEntities = []
    buttons = []
    
    loadJson("skillSelection.json", screenX, screenY, visualEntities, buttons)

    characterImg = ImageEntity("Character", True, 0.68, 0.1, 0.15, 0.3, [], f"entities/{gameData.currentCharacter.name}.png", True)
    characterImg.scale(screenX, screenY)
    visualEntities.append(characterImg)
    for skill in gameData.player.unlockedSkills:
        pass

    count = 0
    for skill in currentCharacter.skills:
        xPos = 0.71 + 0.1*math.sin(2*math.pi*count/4)
        yPos = 0.25 + 0.2*math.cos(2*math.pi*count/4)
        skillButton = ImageButton(f"Skill{count}_Button", True, xPos, yPos, 0.08, 0.08, ["SkillMenu"], f"elements/{skill.element}.png", "showSkillDetails", [skill], True)

        skillLabel = TextEntity(f"Skill{count}_Name", True, xPos, yPos, 0.08, 0.08, ["SkillMenu"], skill.name, "mono", 16)
        skillButton.scale(screenX, screenY)
        skillLabel.scale(screenX, screenY)
        visualEntities.append(skillButton)
        visualEntities.append(skillLabel)
        buttons.append(skillButton)
        count += 1

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "inventory"): buttonFunc = inventory
                        if (entity.func == "showSkillDetails"): buttonFunc = showSkillDetails
                        print(entity)
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break

        refreshScreen(screen)
        if (leaveScreen):
            leaveScreen = False 
            break
    return gameData