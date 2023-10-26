import pygame, math, random, json
from view.visualentity.CombatCharacterEntity import CombatCharacterEntity
from view.visualentity.HoverShapeButton import HoverShapeButton
from model.skill.Skill import Skill
from model.character.Character import Character
from model.player.Player import Player
from model.item.Item import Item
from model.Singleton import Singleton
from view.displayHandler import displayEntity
from view.JSONParser import loadJson


visualEntities = []
partyVisuals = []
buttons = []
quit = False
newSceneData = []
inventory = []

playerData:Player
screen:pygame.surface
gameData:Singleton

party:list



def openWorld():
    global quit
    global gameData
    quit = True
    gameData.screenOpen = "Open World"

def inventoryButton():
    global quit
    global gameData
    quit = True
    gameData.screenOpen = "Inventory"


def refreshScreen(screen):
    # Fill the background
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    for entity in partyVisuals:
        ls = entity.getItems()
        for item in ls:
            if item.isShowing:
                displayEntity(item, screen)

    pygame.display.flip()

# activeCharacter is an int showing which character in the party acted, enemies is an array of enemies, selectedEnemy is an int showing which enemy was selected, skill is the Skill that was used.
# Reminder that AoE effects do NOT include the target of an ability
# This does NOT verify that an ability can/should be used and simply executes the effects
def useSkill(enemies, selectedEnemy, activeCharacter, skill):
    global party
    if (len(enemies) == 0): return
    party[activeCharacter].mana = party[activeCharacter].mana - skill.manaCost

    party[activeCharacter].setCurrentHP(party[activeCharacter].getCurrentHP() + skill.healing*party[activeCharacter].magic/100)
    for character in range(0, len(party)):
        if (character != activeCharacter): party[character].setCurrentHP(party[character].getCurrentHP() + skill.aoeHealing*party[activeCharacter].magic/100)
    
    enemies[selectedEnemy].setCurrentHP(enemies[selectedEnemy].getCurrentHP() - (skill.damage*party[activeCharacter].ATK/100)*math.pow(0.6, enemies[selectedEnemy].DEF/250))
    for enemy in range(0, len(enemies)):
        if (enemy != selectedEnemy): 
            enemies[enemy].setCurrentHP(enemies[enemy].getCurrentHP() - ((skill.aoeDamage*party[activeCharacter].ATK/100)*math.pow(0.6, enemies[enemy].DEF/250)))

    # Special code for individual skills with unique effects will go here
    if (skill.name == "Berserk"):
        party[activeCharacter].setCurrentHP(party[activeCharacter].getCurrentHP() - ((skill.damage*party[activeCharacter].ATK/100)*math.pow(0.6, party[activeCharacter].DEF/250)))


    party[activeCharacter].hasActed = True

def loadCombat(transferredData):
    global visualEntities
    global party
    global partyVisuals
    global quit
    global playerData
    global screen
    global gameData
    global buttons
    gameData = transferredData
    screen = gameData.pygameWindow
    screenX, screenY = screen.get_size()
    enemies = gameData.currentEnemies
    playerData = gameData.player
    party = playerData.party
    activeCharacter = 1
    skillSelected = 0
    skillsShowing = False
    enemySelectionShowing = False

    
    visualEntities = []
    loadJson("combatScreen.json", screenX, screenY, visualEntities, buttons)
    counter = 0
    for entity in visualEntities:
        if type(entity) == CombatCharacterEntity:
            entity.changeCharacter(party[counter], False)
            counter += 1
            if (counter > len(party)): break


    pygame.mixer.init()
    randInt = random.randint(1, 200)
    if (randInt == 69): 
        song = "nyan_cat.mp3"
    else: 
        song = "zelda_lost_woods.mp3"
    pygame.mixer.music.load(f"src/main/python/audio/music/{song}")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    def buttonExit():
        pygame.quit()


    currSelectedChar = None
    def characterSelection(selectedChar:CombatCharacterEntity):
        nonlocal currSelectedChar
        
        if (currSelectedChar is not None): 
            currSelectedChar.selectionButton.activatesOnHover = True
        currSelectedChar = selectedChar
        print(currSelectedChar.selectionButton.activatesOnHover)
        currSelectedChar.selectionButton.activatesOnHover = False
        updateCharacters()

    def enemySelection(selectedChar:CombatCharacterEntity):
        nonlocal skillSelected
        enemySelected = args[0]
        global visualEntities
        nonlocal enemies
        nonlocal enemySelectionShowing
        nonlocal skillsShowing
        nonlocal activeCharacter
        if enemySelectionShowing:
            useSkill(enemies, enemySelected, activeCharacter-1, party, party[activeCharacter-1].skills[skillSelected])
            party[activeCharacter-1].hasActed = True
            updateCharacters()
            for entity in visualEntities:
                if (("Enemy Selection" in entity.tags) or ("Skill Selection" in entity.tags)):
                    entity.isShowing = False
            skillsShowing = False
            enemySelectionShowing = False

    def attack():
        nonlocal currSelectedChar
        if (currSelectedChar is not None):
            print(currSelectedChar.character.attack)

    def skillButtonFunction():
        nonlocal skillsShowing
        global visualEntities
        skillsShowing = not skillsShowing
        for entity in visualEntities:
            if ("Skill Selection" in entity.tags):
                entity.isShowing = not entity.isShowing

    def individualSkillButtonFunction(*args):
        global visualEntities
        global party
        nonlocal skillsShowing
        nonlocal skillSelected
        nonlocal activeCharacter
        nonlocal enemies
        nonlocal enemySelectionShowing
        
        skillSelected = args[0]

        if (skillsShowing and (not party[activeCharacter-1].hasActed) and (party[activeCharacter-1].skills[skillSelected].manaCost <= party[activeCharacter-1].mana)): 
            if (party[activeCharacter-1].skills[skillSelected].singleTarget == 1):
                enemySelectionShowing = True
                for entity in visualEntities:
                    if ("Enemy Selection" in entity.tags):
                        entity.isShowing = True
            else: 
                useSkill(enemies, 0, activeCharacter-1, party, party[activeCharacter-1].skills[skillSelected])
                updateCharacters()
                for entity in visualEntities:
                    if ("Skill Selection" in entity.tags):
                        entity.isShowing = False
                skillsShowing = False

    

    def updateCharacters():
        for entity in visualEntities[:]:
            if type(entity) == CombatCharacterEntity:
                if (entity.character is not None and entity.character.health.current_value <= 0):
                    visualEntities.remove(entity)
                else:
                    entity.updateCharacter()


    def addEnemies():
        nonlocal enemies
        enemyLeftPadding = 0.4
        enemyRightPadding = 0.1
        enemiesWidth = 1-(enemyLeftPadding+enemyRightPadding)
        enemySpacing = enemiesWidth/(1+len(enemies)*2)

        count = 0
        for enemy in enemies:
            currEnemyX = enemyLeftPadding + enemySpacing*(2*count+1)

            entityDetails = {
                "name": enemy.name,
                "HPBorderXPosition": 0.02,
                "HPBorderYPosition": 0.1,
                "ManaBorderXPosition": 0.02,
                "ManaBorderYPosition": 0.1,
                "imgXPosition": currEnemyX,
                "imgYPosition": 0.1,
                "imgWidth": 0.12,
                "imgHeight": 0.24,
                "checkmarkXPosition": 0.375,
                "checkmarkYPosition": 0.05,
            }
            entityDetails = json.loads(json.dumps(entityDetails))

            print(type(entityDetails))
            displayedEnemy = CombatCharacterEntity.createFrom(entityDetails)
            displayedEnemy.changeCharacter(enemy, True)
            displayedEnemy.scale(screenX, screenY)
            visualEntities.append(displayedEnemy)
            count = count+1


    addEnemies()
    updateCharacters()





    buttonFunc = updateCharacters
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "exit"): buttonFunc = buttonExit
                        elif (entity.func == "openWorld"): buttonFunc = openWorld
                        elif (entity.func == "characterSelection"): buttonFunc = characterSelection
                        elif (entity.func == "inventory"): buttonFunc = inventoryButton
                        elif (entity.func == "attack"): buttonFunc = attack
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break
            
        ### Make Hover Buttons shine funny color
        for button in buttons:
            if (type(button) == HoverShapeButton):
                button.mouseInRegion(mouse)

        isEnemyTurn = True
        for character in party:
            if not character.hasActed:
                isEnemyTurn = False
        if (isEnemyTurn):
            count = 0
            for enemy in enemies:
                useSkill(party, activeCharacter-1, count, enemies, enemy.skills[0])
                count += 1
            for character in party:
                character.hasActed = False
            updateEnemies()
            updateCharacters()
              
        if (party[activeCharacter-1].getCurrentHP() == 0 or len(enemies) == 0):
            party[activeCharacter-1].setCurrentHP(party[activeCharacter-1].maxHP)
            party[activeCharacter-1].mana = party[activeCharacter-1].maxMana
            enemies = [Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30)), Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30))]
            updateEnemies()
            updateCharacters()
            for entity in visualEntities:
                if("Skill Point" in entity.tags): entity.isBorder = False

        refreshScreen(screen)
        if (quit):
            currSelectedChar.selectionButton.activesOnHover = True
            quit = False 
            break
    return gameData