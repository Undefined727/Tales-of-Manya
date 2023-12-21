import pygame, math, random, json
from view.visualentity.Battlefield import Battlefield
from view.visualentity.CombatCharacterEntity import CombatCharacterEntity
from view.visualentity.ImageButton import ImageButton
from view.visualentity.Animation import Animation
from view.visualentity.TextEntity import TextEntity
from view.visualentity.HoverShapeButton import HoverShapeButton
from model.character.Character import Character
from model.character.Skill import Skill
import model.character.SkillFunctions as SkillFunctions
from model.player.Player import Player
from model.item.Item import Item
from model.Singleton import Singleton
from view.displayHandler import displayEntity
from view.JSONParser import loadJson

visualEntities = []
buttons = []
quit = False
battlefield:Battlefield

playerData:Player
screen:pygame.surface
gameData:Singleton
party:list

def openWorld():
    global quit
    global gameData
    quit = True
    gameData.screenOpen = "Open World"

def refreshScreen(screen):
    # Fill the background
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    pygame.display.flip()

def loadCombat(transferredData):
    global visualEntities
    global party
    global quit
    global playerData
    global screen
    global gameData
    global buttons
    global battlefield
    gameData = transferredData
    screen = gameData.pygameWindow
    screenX, screenY = screen.get_size()
    enemies = gameData.currentEnemies
    playerData = gameData.player
    party = playerData.party
    skillsShowing = False
    currSelectedChar = None
    currSelectedEnemy = None

    for character in party:
        character.setCurrentMana(character.mana.max_value)
        character.hasActed = False

    visualEntities = []
    buttons = []
    loadJson("combatScreen.json", screenX, screenY, visualEntities, buttons)
    battlefield = Battlefield(gameData)
    visualEntities.append(battlefield)
    buttons.extend(battlefield.getButtons())

    pygame.mixer.init()
    randInt = random.randint(1, 200)
    if (randInt == 69): 
        song = "nyan_cat.mp3"
    else: 
        song = "zelda_lost_woods.mp3"
    pygame.mixer.music.load(f"src/main/python/audio/music/{song}")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    def skillMenu():
        global visualEntities
        global buttons
        nonlocal currSelectedChar
        nonlocal skillsShowing
        if(currSelectedChar == None): return

        # Add animation in the future
        if (not skillsShowing):
            count = 0
            for skill in currSelectedChar.character.skills:
                xPos = 0.61 + 0.1*math.sin(2*math.pi*count/len(currSelectedChar.character.skills))
                yPos = 0.45 + 0.1*math.cos(2*math.pi*count/len(currSelectedChar.character.skills))
                skillButton = ImageButton(f"Skill{count}_Button", True, xPos, yPos, 0.08, 0.08, ["SkillMenu"], "attackButton.png", "useSkill", [skill], True)
                skillLabel = TextEntity(f"Skill{count}_Name", True, xPos, yPos, 0.08, 0.08, ["SkillMenu"], skill.name, "mono", 16)
                skillButton.scale(screenX, screenY)
                skillLabel.scale(screenX, screenY)
                visualEntities.append(skillButton)
                visualEntities.append(skillLabel)
                buttons.append(skillButton)
                count += 1
        else:
            for entity in visualEntities[:]:
                if "SkillMenu" in entity.tags:
                    visualEntities.remove(entity)
            for entity in buttons[:]:
                if "SkillMenu" in entity.tags:
                    buttons.remove(entity)
        skillsShowing = not skillsShowing

    def buttonExit():
        pygame.quit()

    def characterSelection(selectedChar:CombatCharacterEntity):
        nonlocal currSelectedChar
        nonlocal currSelectedEnemy
        global battlefield
        print(selectedChar.isEnemy)
        if (selectedChar.isEnemy):
            if (currSelectedEnemy is not None): currSelectedEnemy.isSelected = False
            currSelectedEnemy = selectedChar
            currSelectedEnemy.isSelected = True
        else:
            if (currSelectedChar is not None): currSelectedChar.isSelected = False
            currSelectedChar = selectedChar
            currSelectedChar.isSelected = True
            if (skillsShowing): 
                skillMenu()
                skillMenu()
        battlefield.updateCharacters()

    def useSkill(skill):
        global gameData
        nonlocal currSelectedChar
        nonlocal currSelectedEnemy
        global battlefield
        if((currSelectedChar == None) or (currSelectedEnemy == None)): return
        if(currSelectedChar.character.hasActed): return

        SkillFunctions.useSkill(currSelectedChar.character, currSelectedEnemy.character, gameData, battlefield, skill)

        currSelectedChar.character.hasActed = True
        currSelectedEnemy.isSelected = False
        currSelectedEnemy = None
        currSelectedChar.isSelected = False
        currSelectedChar = None
        battlefield.updateCharacters()
        skillMenu()

    def attack():
        nonlocal currSelectedChar
        nonlocal currSelectedEnemy
        if((currSelectedChar == None) or (currSelectedEnemy == None)): return
        if(currSelectedChar.character.hasActed): return

        useSkill(currSelectedChar.character.skills[0])

    

    battlefield.updateCharacters()
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                buttonPressed = False
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        buttonPressed = True
                        if (entity.func == "exit"): buttonFunc = buttonExit
                        elif (entity.func == "openWorld"): buttonFunc = openWorld
                        elif (entity.func == "characterSelection"): buttonFunc = characterSelection
                        elif (entity.func == "attack"): buttonFunc = attack
                        elif (entity.func == "skillMenu"): buttonFunc = skillMenu
                        elif (entity.func == "useSkill"): buttonFunc = useSkill
                        else: break
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break
                if (not buttonPressed):
                    # Code for clicking out
                    if skillsShowing: skillMenu()
                    if (currSelectedChar is not None): 
                        currSelectedChar.isSelected = False
                        currSelectedChar = None
                    if (currSelectedEnemy is not None): 
                        currSelectedEnemy.isSelected = False
                        currSelectedEnemy = None   
            
        ### Make Hover Buttons shine funny color
        for button in buttons:
            if (type(button) == HoverShapeButton):
                button.mouseInRegion(mouse)

        isEnemyTurn = True
        for character in party:
            if (not character.hasActed and character.getCurrentHP() > 0):
                isEnemyTurn = False
        if (isEnemyTurn):
            for enemy in enemies:
                SkillFunctions.useSkill(enemy, party[random.randint(1, len(party))-1], gameData, battlefield, enemy.skills[0])
            for character in party:
                character.hasActed = False
            battlefield.updateCharacters()

        enemiesDead = True  
        for enemy in enemies:
            if (enemy.getCurrentHP() > 0):
                enemiesDead = False
                break
        
        if (enemiesDead):
            for enemy in enemies:
                enemy.setCurrentHP(character.getMaxHP())
            openWorld()

        refreshScreen(screen)
        if (quit):
            quit = False 
            break
    return gameData