import pygame, math, random
from model.visualentity.Tag import Tag
from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.ShapeEntity import ShapeEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ShapeButton import ShapeButton
from model.visualentity.ImageButton import ImageButton
from model.visualentity.DynamicStatEntity import DynamicStatEntity
from model.visualentity.CombatCharacterEntity import CharacterEntities
from model.skill.Skill import Skill
from model.character.Character import Character
from model.item.Item import Item
from model.visualentity.CombatEnemyEntity import CombatEnemyEntity
from displayHandler import displayEntity
from JSONParser import loadJson


visualEntities = []
partyVisuals = []
buttons = []
quit = False
nextScreen = "Quit"


inventory = []

party = [Character("Catgirl", "catgirl.png", "catgirl_head.png", 10), Character("Catgirl", "catgirl.png", "catgirl_head.png", 10)]
party.append(Character("lmao", "catgirl.png", "catgirl_head.png", 20))

party[0].skills[0] = Skill(1)
party[0].skills[1] = Skill(2)
party[0].skills[2] = Skill(3)

inventory.append(Item(9))
inventory.append(Item(9))
inventory.append(Item(7))

party[0].helmet = Item(2)

def openWorldButton():
    global quit
    global nextScreen
    quit = True
    nextScreen = "Open World"

def inventoryButton():
    global quit
    global nextScreen
    quit = True
    nextScreen = "Inventory"
    print("test")


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
def useSkill(enemies, selectedEnemy, activeCharacter, party, skill):
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

def loadCombat(screen, screenX, screenY):
    global visualEntities
    global party
    global partyVisuals
    global quit
    enemies = [Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30)), Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30))]
    activeCharacter = 1
    skillSelected = 0
    skillsShowing = False
    enemySelectionShowing = False

    visualEntities = []
    partyVisuals = [CharacterEntities(party[0]), CharacterEntities(party[1]), CharacterEntities(party[2])]
    loadJson("combatScreen.json", screenX, screenY, [visualEntities, buttons, partyVisuals, party])

    def buttonExit():
        pygame.quit()

    def bagButtonFunction():
        global quit
        global nextScreen
        nextScreen = "Inventory"
        leaveScreen = True

    def changeCharacter(*args):
        nonlocal activeCharacter
        if (args[0] == "Right"): activeCharacter = ((activeCharacter)%len(party))+1
        else: activeCharacter = ((activeCharacter-2)%len(party))+1

        partyVisuals[0].changeCharacter(party[(activeCharacter-2) % len(party)])
        partyVisuals[1].changeCharacter(party[(activeCharacter-1) % len(party)])
        partyVisuals[2].changeCharacter(party[(activeCharacter) % len(party)])
        updateCharacters()

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
                updateEnemies()
                updateCharacters()
                for entity in visualEntities:
                    if ("Skill Selection" in entity.tags):
                        entity.isShowing = False
                skillsShowing = False

    def enemySelectionButtonFunction(*args):
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
            updateEnemies()
            updateCharacters()
            for entity in visualEntities:
                if (("Enemy Selection" in entity.tags) or ("Skill Selection" in entity.tags)):
                    entity.isShowing = False
            skillsShowing = False
            enemySelectionShowing = False

    def updateCharacters():
        global partyVisuals
        global party
        global screenX
        global screenY
        nonlocal activeCharacter

        partyVisuals[0].updateCharacter()
        partyVisuals[1].updateCharacter()
        partyVisuals[2].updateCharacter()

        if (len(party)<3) : partyVisuals[2].changeCharacter(None)
        if (len(party)<2) : partyVisuals[0].changeCharacter(None)

        for item in visualEntities:
            if (item.name == "Skill1"): item.updateImg(party[(activeCharacter-1)%len(party)].skills[0].img)
            if (item.name == "Skill2"): item.updateImg(party[(activeCharacter-1)%len(party)].skills[1].img)
            if (item.name == "Skill3"): item.updateImg(party[(activeCharacter-1)%len(party)].skills[2].img)
            if (item.name == "Skill1Text"): item.updateText(party[(activeCharacter-1)%len(party)].skills[0].name, "mono", int(screenX*0.5/15), "black", "yellow")
            if (item.name == "Skill2Text"): item.updateText(party[(activeCharacter-1)%len(party)].skills[1].name, "mono", int(screenX*0.5/15), "black", "yellow")
            if (item.name == "Skill3Text"): item.updateText(party[(activeCharacter-1)%len(party)].skills[2].name, "mono", int(screenX*0.5/15), "black", "yellow")


    def updateEnemies():
        nonlocal enemies
        enemySpacing = 1/(1+len(enemies)*2)
        
        for entity in visualEntities[:]:
            if (Tag.ENEMY in entity.tags):
                visualEntities.remove(entity)
        for enemy in enemies[:]:
            if (enemy.getCurrentHP() <= 0):
                enemies.remove(enemy)

        count = 0
        for enemy in enemies:
            currEnemyX = enemySpacing*(2*count+1)
            displayedEnemy = CombatEnemyEntity(currEnemyX, 1/10, enemySpacing, 1/3, enemy)
            displayedEnemy.scale(screenX, screenY)
            visualEntities.append(displayedEnemy.enemyImg)
            visualEntities.append(displayedEnemy.enemyHPBarBorder)
            visualEntities.append(displayedEnemy.enemyHPBarRed)
            visualEntities.append(displayedEnemy.enemyHPBarGreen)
            visualEntities.append(displayedEnemy.enemyHPBarText)
            count = count+1


    updateEnemies()
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
                        elif (entity.func == "openWorld"): buttonFunc = openWorldButton
                        elif (entity.func == "changeCharacter"): buttonFunc = changeCharacter
                        elif (entity.func == "inventory"): buttonFunc = inventoryButton
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break

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
            quit = False 
            break
    return nextScreen