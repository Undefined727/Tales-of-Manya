import pygame, numpy, math, os, random, json
from src.main.python.model.visualentity.Tag import Tag
from src.main.python.model.visualentity.ImageEntity import ImageEntity
from src.main.python.model.visualentity.DrawingEntity import DrawingEntity
from src.main.python.model.visualentity.TextEntity import TextEntity
from src.main.python.model.visualentity.ButtonEntity import ButtonEntity
from src.main.python.model.visualentity.TransparentButtonEntity import TransparentButtonEntity
from src.main.python.model.skill.Skill import Skill
from src.main.python.model.character.Character import Character
from src.main.python.model.item.Item import Item
from src.main.python.model.visualentity.CombatEnemyEntity import CombatEnemyEntity
import json

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
inventory = []
party = [Character("Catgirl", "catgirl.png", 10), Character("Catgirl", "catgirl.png", 10)]
party.append(Character("lmao", "catgirl.png", 20))
party[0].skills[0] = Skill(1)
party[0].skills[1] = Skill(2)
party[0].skills[2] = Skill(3)

inventory.append(Item(9))
inventory.append(Item(9))
inventory.append(Item(7))

party[0].helmet = Item(2)

def refreshScreen():
    # Fill the background
    global visualEntities
    for entity in visualEntities:
         print(entity.name)
         print(type(entity))
         if entity.isShowing:
            if (type(entity) == ImageEntity):
                screen.blit(entity.img, (entity.xPosition, entity.yPosition))
            elif (type(entity) == DrawingEntity):
                if entity.shape == "rectangle":
                    if entity.isBorder:
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.height), 2)
                    else:
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.height))
                if entity.shape == "ellipse":
                    if entity.isBorder:
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.height), 2)
                    else:
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.height))
            elif (type(entity) == TextEntity):
                print(entity.name)
                screen.blit(entity.textLabel, entity.textRect)
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


def combatScreen():
    global visualEntities
    enemies = [Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30)), Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30))]
    activeCharacter = 1
    skillSelected = 0
    skillsShowing = False
    enemySelectionShowing = False
    leaveScreen = False
    nextScreen = None

    visualEntities = []
    file = open("./src/main/python/screens/combatScreen.json", 'r')
    data = json.load(file)
    for item in data:
        if item["entityType"] == "Image":
             entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Drawing":
            entity = DrawingEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "Button":
            entity = ButtonEntity.createFrom(item)
        elif item["entityType"] == "TransparentButton":
            entity = TransparentButtonEntity.createFrom(item)
            
        entity.resize(entity.width*screen.get_width(), entity.height*screen.get_height())
        entity.reposition(entity.xPosition * screen.get_width(),entity.yPosition * screen.get_height())
        if (item["entityType"] == "TransparentButton" or item["entityType"] == "Button"): buttons.append(entity)
        else: visualEntities.append(entity)

    

    def buttonExit():
        pygame.quit()

    def bagButtonFunction():
        nonlocal nextScreen
        nonlocal leaveScreen
        nextScreen = "Inventory"
        leaveScreen = True
    
    def buttonOpenWorld():
        nonlocal nextScreen
        nonlocal leaveScreen
        nextScreen = "Open World"
        leaveScreen = True

    def changeCharacterFunction(*args):
        nonlocal activeCharacter
        if (args[0] == "Left"): activeCharacter = ((activeCharacter)%len(party))+1
        else: activeCharacter = ((activeCharacter-2)%len(party))+1
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
        global visualEntities
        global party
        global screenX
        global screenY
        nonlocal activeCharacter

        for item in visualEntities:
            if (item.name == "Player"): item.updateImg(str(party[activeCharacter-1].img))
            if (item.name == "PlayerHPText"): item.updateText(str(int(party[activeCharacter-1].getCurrentHP())) + "/" + str(int(party[activeCharacter-1].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "PlayerHPGreen"): item.width = screenX*0.5*party[activeCharacter-1].getCurrentHP()/party[activeCharacter-1].maxHP
            if (item.name == "PlayerManaText"): item.updateText(str(int(party[activeCharacter-1].mana)) + "/" + str(int(party[activeCharacter-1].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "PlayerManaBlue"): item.width = screenX*0.5*party[activeCharacter-1].mana/party[activeCharacter-1].maxMana
            if (item.name == "InactiveCharacter1Img"): item.updateImg(str(party[(activeCharacter-2)%len(party)].headImg))
            if (item.name == "InactiveCharacter1HPText"): item.updateText(str(int(party[(activeCharacter-2)%len(party)].getCurrentHP())) + "/" + str(int(party[(activeCharacter-2)%len(party)].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "InactiveCharacter1HPGreen"): item.width = screenX*0.5*party[activeCharacter-2].getCurrentHP()/party[activeCharacter-2].maxHP
            if (item.name == "InactiveCharacter1ManaText"): item.updateText(str(int(party[(activeCharacter-2)%len(party)].mana)) + "/" + str(int(party[(activeCharacter-2)%len(party)].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "InactiveCharacter1ManaBlue"): item.width = screenX*0.5*party[(activeCharacter-2)%len(party)].mana/party[(activeCharacter-2)%len(party)].maxMana
            if (item.name == "PlayerCheckmark"): item.isShowing = party[(activeCharacter - 1) % len(party)].hasActed
            if (item.name == "InactiveCharacter1Checkmark" ): item.isShowing = party[(activeCharacter-2) % len(party)].hasActed
            if (item.name == "InactiveCharacter2Checkmark"): item.isShowing = party[(activeCharacter) % len(party)].hasActed
            if (item.name == "InactiveCharacter2Img"): item.updateImg(str(party[(activeCharacter)%len(party)].headImg))
            if (item.name == "InactiveCharacter2HPText"): item.updateText(str(int(party[(activeCharacter)%len(party)].getCurrentHP())) + "/" + str(int(party[(activeCharacter)%len(party)].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "InactiveCharacter2HPGreen"): item.width = screenX*0.5*party[(activeCharacter)%len(party)].getCurrentHP()/party[(activeCharacter)%len(party)].maxHP
            if (item.name == "InactiveCharacter2ManaText"): item.updateText(str(int(party[(activeCharacter)%len(party)].mana)) + "/" + str(int(party[(activeCharacter)%len(party)].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "InactiveCharacter2ManaBlue"): item.width = screenX*0.5*party[(activeCharacter)%len(party)].mana/party[(activeCharacter)%len(party)].maxMana
            if (item.name == "Skill1"): item.updateImg(party[(activeCharacter-1)%len(party)].skills[0].img)
            if (item.name == "Skill2"): item.updateImg(party[(activeCharacter-1)%len(party)].skills[1].img)
            if (item.name == "Skill3"): item.updateImg(party[(activeCharacter-1)%len(party)].skills[2].img)
            if (item.name == "Skill1Text"): item.updateText(party[(activeCharacter-1)%len(party)].skills[0].name, "mono", int(screenX*0.5/15), "black", "yellow")
            if (item.name == "Skill2Text"): item.updateText(party[(activeCharacter-1)%len(party)].skills[1].name, "mono", int(screenX*0.5/15), "black", "yellow")
            if (item.name == "Skill3Text"): item.updateText(party[(activeCharacter-1)%len(party)].skills[2].name, "mono", int(screenX*0.5/15), "black", "yellow")
            
            if ((Tag.INACTIVE_CHARACTER2 in item.tags) and (len(party)<3)) : item.isShowing = False
            if ((Tag.INACTIVE_CHARACTER1 in item.tags) and (len(party) < 2)): item.isShowing = False


    def updateEnemies():
        nonlocal enemies
        enemySpacing = screenX/(1+len(enemies)*2)
        
        for entity in visualEntities[:]:
            if (Tag.ENEMY in entity.tags):
                visualEntities.remove(entity)
        for enemy in enemies[:]:
            if (enemy.getCurrentHP() <= 0):
                enemies.remove(enemy)

        count = 0
        for enemy in enemies:
            currEnemyX = enemySpacing*(2*count+1)
            displayedEnemy = CombatEnemyEntity(currEnemyX, screenY/10, enemySpacing, screenY/3, enemy)
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
                        elif (entity.func == "openWorld"): buttonFunc = openWorldScreen
                        if (len(entity.args) == 0): buttonFunc()
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
    



        refreshScreen()
        if (leaveScreen): break
    if (nextScreen == "Inventory"):
        inventoryScreen()
    elif (nextScreen == "Open World"):
        openWorldScreen()
    elif (nextScreen == "Quit"):
        pygame.quit()
    else:
        print("Screen Not Found")
        combatScreen()

def inventoryScreen():
    global visualEntities
    global party
    global inventory
    leaveScreen = False
    nextScreen = None
    attachedItem = None
    attachedItemEquipped = None
    attachedItemVisual = VisualEntity.VisualEntity("AttachedItem", 0, False, 0, 0, screenX/12, screenX/12, ["Item"], "catgirl.png")

    activeCharacter = 1

    exitButtonX = screenX/16
    exitButtonY = 5*screenY/6
    buttonSizeX = 4*screenX/16
    buttonSizeY = screenY/8
    catgirlX = 29*screenX/48
    catgirlY = 3*screenY/12
    catgirlSizeX = screenX/3
    catgirlSizeY = 2*screenY/3
    nameX = 29*screenX/48
    nameY = 6*screenY/48
    levelX = 36*screenX/48
    itemSizeX = screenX/12
    itemSizeY = screenX/12
    helmetX = 21*screenX/24
    helmetY = 4*screenY/24
    chestplateX = 21*screenX/24
    chestplateY = 8*screenY/24
    leggingsX = 21*screenX/24
    leggingsY = 12*screenY/24
    bootsX = 21*screenX/24
    bootsY = 16*screenY/24
    accessory1X = 16*screenX/24
    accessory1Y = 19*screenY/24
    accessory2X = 37*screenX/48
    accessory2Y = 19*screenY/24
    weaponX = 29*screenX/48
    weaponY = 10*screenY/24
    statFontSize = screenX/100
    nameFontSize = screenX/40

    changeCharacterRX = 22*screenX/24
    changeCharacterRY = 4*screenY/48
    changeCharacterLX = 20*screenX/24
    changeCharacterLY = 4*screenY/48
    changeCharacterSizeX = screenX/24
    changeCharacterSizeY = 3*screenY/48


    def itemClickFunction(*args):
        nonlocal attachedItem
        nonlocal attachedItemEquipped
        attachedItem = args[0][0]
        if (attachedItem == None): return
        if (len(args[0]) > 1): attachedItemEquipped = args[0][1]
        else: attachedItemEquipped = None
        attachedItemVisual.updateImg(attachedItem.img)
        attachedItemVisual.isShowing = True


    def exitButtonFunction(*args):
        nonlocal leaveScreen
        nonlocal nextScreen
        leaveScreen = True
        nextScreen = "Combat"
    
    def changeCharacterFunction(*args):
        nonlocal activeCharacter
        global party
        if (args[0] == "Left"): activeCharacter = ((activeCharacter)%len(party))+1
        else: activeCharacter = ((activeCharacter-2)%len(party))+1
        updateCharacter()

    def updateCharacter():
        global visualEntities
        global party
        nonlocal activeCharacter
        updateStats()
        for entity in visualEntities:
            if (entity.name == "CharacterName"): entity.updateText(party[activeCharacter-1].name, "mono", int(nameFontSize), "black", "green")
            elif (entity.name == "CharacterLevel"): entity.updateText("Level " + str(party[activeCharacter-1].level), "mono", int(nameFontSize), "black", "green")
            elif ("Equipped Item" in entity.tags):
                if (entity.name == "Helmet"):
                    if (party[activeCharacter-1].helmet == None): entity.updateImg("helmet_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].helmet.img)
                elif (entity.name == "Chestplate"):
                    if (party[activeCharacter-1].chestplate == None): entity.updateImg("chestplate_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].chestplate.img)
                elif (entity.name == "Leggings"):
                    if (party[activeCharacter-1].leggings == None): entity.updateImg("leggings_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].leggings.img)
                elif (entity.name == "Boots"):
                    if (party[activeCharacter-1].boots == None): entity.updateImg("boots_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].boots.img)
                elif (entity.name == "Accessory1"):
                    if (party[activeCharacter-1].accessory1 == None): entity.updateImg("accessory_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].accessory1.img)
                elif (entity.name == "Accessory2"):
                    if (party[activeCharacter-1].accessory2 == None): entity.updateImg("accessory_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].accessory2.img)
                elif (entity.name == "Weapon"):
                    if (party[activeCharacter-1].weapon == None): entity.updateImg("weapon_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].weapon.img)
                elif (entity.entityType == 2):
                    if (entity.name == "HelmetButton"): entity.args = [party[activeCharacter-1].helmet, "Helmet"]
                    elif (entity.name == "ChestplateButton"): entity.args = [party[activeCharacter-1].chestplate, "Chestplate"]
                    elif (entity.name == "LeggingsButton"): entity.args = [party[activeCharacter-1].leggings, "Leggings"]
                    elif (entity.name == "BootsButton"): entity.args = [party[activeCharacter-1].boots, "Boots"]
                    elif (entity.name == "Accessory1Button"): entity.args = [party[activeCharacter-1].accessory1, "Accessory1"]
                    elif (entity.name == "Accessory2Button"): entity.args = [party[activeCharacter-1].accessory2, "Accessory2"]
                    elif (entity.name == "WeaponButton"): entity.args = [party[activeCharacter-1].weapon, "Weapon"]

    def updateStats():
        global visualEntities
        global party
        nonlocal activeCharacter
        party[activeCharacter-1].updateItems()
        for item in visualEntities:
            if (item.name == "PlayerHPText"): item.updateText("HP: " + str(int(party[activeCharacter-1].maxHP)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerManaText"): item.updateText("Mana: " + str(int(party[activeCharacter-1].maxMana)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerMagicText"): item.updateText("Magic Strength: " + str(int(party[activeCharacter-1].magic)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerATKText"): item.updateText("ATK: " + str(int(party[activeCharacter-1].ATK)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerDEFText"): item.updateText("DEF: " + str(int(party[activeCharacter-1].DEF)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearHPText"): item.updateText("HP: +" + str(int(party[activeCharacter-1].maxHP - (party[activeCharacter-1].level*100))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearManaText"): item.updateText("Mana: +" + str(int(party[activeCharacter-1].maxMana - (1000 + party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearMagicText"): item.updateText("Magic Strength: +" + str(int(party[activeCharacter-1].magic - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearATKText"): item.updateText("ATK: +" + str(int(party[activeCharacter-1].ATK - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearDEFText"): item.updateText("DEF: +" + str(int(party[activeCharacter-1].DEF - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")

    def updateInventory():
        global visualEntities
        for entity in visualEntities[:]:
            if ("Inventory" in entity.tags):
                    visualEntities.remove(entity)
        
        count = 0
        itemrow = 0
        bufferX = screenX/24
        bufferY = screenY/20

        for item in inventory:
            curritemX = count * (itemSizeX + bufferX) + bufferX
            curritemY = itemrow * (itemSizeY + bufferY) + bufferY

            visualEntities.append(VisualEntity.VisualEntity(item.name, 0, True, curritemX, curritemY, itemSizeX, itemSizeY, ["Item", "Inventory"], item.img))
            visualEntities.append(VisualEntity.VisualEntity("Item" + str(count + itemrow*4) + "Button", 2, True, curritemX, curritemY, itemSizeX, itemSizeY, ["Button","Item", "Inventory"], itemClickFunction, [item], "rectangle"))
            count += 1
            if count >= 4:
                count = 0
                itemrow +=1

    visualEntities.clear()
    visualEntities.append(VisualEntity.VisualEntity("Background", 0, True, 0, 0, screenX, screenY, ["Background"], "inventorybackground.png"))
    visualEntities.append(VisualEntity.VisualEntity("Character", 0, True, catgirlX, catgirlY, catgirlSizeX, catgirlSizeY, ["Character"], party[activeCharacter-1].img))
    visualEntities.append(VisualEntity.VisualEntity("CharacterName", 3, True, nameX, nameY, itemSizeX, itemSizeY, ["Stat"], party[activeCharacter-1].name, "mono", int(nameFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("CharacterLevel", 3, True, levelX, nameY, itemSizeX, itemSizeY, ["Stat"], "Level " + str(party[activeCharacter-1].level), "mono", int(nameFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("HelmetBackground", 1, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet", "Item Background"], "cadetblue", False, "rectangle"))
    if (party[activeCharacter-1].helmet == None): visualEntities.append(VisualEntity.VisualEntity("Helmet", 0, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], "helmet_transparent.png"))
    else: visualEntities.append(VisualEntity.VisualEntity("Helmet", 0, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], party[activeCharacter-1].helmet.img))
    visualEntities.append(VisualEntity.VisualEntity("ChestplateBackground", 1, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate", "Item Background"], "cadetblue", False, "rectangle"))
    if (party[activeCharacter-1].chestplate == None): visualEntities.append(VisualEntity.VisualEntity("Chestplate", 0, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], "chestplate_transparent.png"))
    else: visualEntities.append(VisualEntity.VisualEntity("Chestplate", 0, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate"], party[activeCharacter-1].chestplate.img))
    visualEntities.append(VisualEntity.VisualEntity("LeggingsBackground", 1, True, leggingsX, leggingsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Leggings", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Leggings", 0, True, leggingsX, leggingsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Leggings"], party[activeCharacter-1].leggings.img))
    visualEntities.append(VisualEntity.VisualEntity("BootsBackground", 1, True, bootsX, bootsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Boots", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Boots", 0, True, bootsX, bootsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Boots"], party[activeCharacter-1].boots.img))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1Background", 1, True, accessory1X, accessory1Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory1", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1", 0, True, accessory1X, accessory1Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory1"], party[activeCharacter-1].accessory1.img))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2Background", 1, True, accessory2X, accessory2Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory2", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2", 0, True, accessory2X, accessory2Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory2"], party[activeCharacter-1].accessory2.img))
    visualEntities.append(VisualEntity.VisualEntity("WeaponBackground", 1, True, weaponX, weaponY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Weapon", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Weapon", 0, True, weaponX, weaponY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Weapon"], party[activeCharacter-1].weapon.img))

    visualEntities.append(VisualEntity.VisualEntity("HelmetButton", 2, True, helmetX, helmetY, itemSizeX, itemSizeY,["Button", "Helmet","Item","Equipped Item"], itemClickFunction, [party[activeCharacter-1].helmet, "Helmet"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("ChestplateButton", 2, True, chestplateX, chestplateY, itemSizeX, itemSizeY,["Button", "Chestplate","Item","Equipped Item"], itemClickFunction, [party[activeCharacter-1].chestplate, "Chestplate"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("LeggingsButton", 2, True, leggingsX, leggingsY, itemSizeX, itemSizeY,["Button", "Item","Leggings","Equipped Item"], itemClickFunction, [party[activeCharacter-1].leggings, "Leggings"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("BootsButton", 2, True, bootsX, bootsY, itemSizeX, itemSizeY,["Button", "Item", "Boots","Equipped Item"], itemClickFunction, [party[activeCharacter-1].boots, "Boots"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1Button", 2, True, accessory1X, accessory1Y, itemSizeX, itemSizeY,["Button", "Item", "Accessory1","Equipped Item"], itemClickFunction, [party[activeCharacter-1].accessory1, "Accessory1"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2Button", 2, True, accessory2X, accessory2Y, itemSizeX, itemSizeY,["Button", "Item", "Accessory2","Equipped Item"], itemClickFunction, [party[activeCharacter-1].accessory2, "Accessory2"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("WeaponButton", 2, True, weaponX, weaponY, itemSizeX, itemSizeY,["Item", "Equipped Item", "Button", "Weapon"], itemClickFunction, [party[activeCharacter-1].weapon, "Weapon"], "rectangle"))

    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterRight", 4, True, changeCharacterRX, changeCharacterRY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], changeCharacterFunction, "Right", "change_active_right.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterRightImg", 0, True, changeCharacterRX, changeCharacterRY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], "change_active_right.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterLeft", 4, True, changeCharacterLX, changeCharacterLY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], changeCharacterFunction, "Left", "change_active_left.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterLeftImg", 0, True, changeCharacterLX, changeCharacterLY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], "change_active_left.png"))


    updateInventory()

    statX = 29*screenX/48
    stat1Y = 9*screenY/48
    stat2Y = 11*screenY/48
    stat3Y = 13*screenY/48
    stat4Y = 15*screenY/48
    stat5Y = 17*screenY/48
    gearStatBuffer = 20*screenY/48

    visualEntities.append(VisualEntity.VisualEntity("PlayerHPText", 3, True, statX, stat1Y, itemSizeX, itemSizeY, ["Stat"], "HP: " + str(int(party[activeCharacter-1].maxHP)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaText", 3, True, statX, stat2Y, itemSizeX, itemSizeY, ["Stat"], "Mana: " + str(int(party[activeCharacter-1].maxMana)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerMagicText", 3, True, statX, stat3Y, itemSizeX, itemSizeY, ["Stat"], "Magic Strength: " + str(int(party[activeCharacter-1].magic)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerATKText", 3, True, statX, stat4Y, itemSizeX, itemSizeY, ["Stat"], "ATK: " + str(int(party[activeCharacter-1].ATK)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerDEFText", 3, True, statX, stat5Y, itemSizeX, itemSizeY, ["Stat"], "DEF: " + str(int(party[activeCharacter-1].DEF)), "mono", int(statFontSize), "black", "green"))

    visualEntities.append(VisualEntity.VisualEntity("PlayerGearText", 3, True, statX, stat1Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "Gear Stats", "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearHPText", 3, True, statX, stat2Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "HP: +" + str(int(party[activeCharacter-1].maxHP - (party[activeCharacter-1].level*100))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearManaText", 3, True, statX, stat3Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "Mana: +" + str(int(party[activeCharacter-1].maxMana - (1000 + party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearMagicText", 3, True, statX, stat4Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "Magic Strength: +" + str(int(party[activeCharacter-1].magic - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearATKText", 3, True, statX, stat5Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "ATK: +" + str(int(party[activeCharacter-1].ATK - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearDEFText", 3, True, statX, stat5Y + gearStatBuffer + 2*screenY/48, itemSizeX, itemSizeY, ["Stat"], "DEF: +" + str(int(party[activeCharacter-1].DEF - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))


    visualEntities.append(VisualEntity.VisualEntity("ExitImg", 0, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], "ExitButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("ExitButton", 2, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], exitButtonFunction, None, "rectangle"))

    visualEntities.append(attachedItemVisual)
    

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                        if entity.mouseInRegion(mouse, entity.shape, entity.xPosition, entity.yPosition, entity.width, entity.length):
                            entity.func(entity.args)
                            break
            if (event.type == pygame.MOUSEBUTTONUP):
                for entity in visualEntities:
                    if (entity.entityType == 2 and "Equipped Item" in entity.tags):
                        if mouseInRegion(mouse, entity.shape, entity.xPosition, entity.yPosition, entity.width, entity.length):
                            if ("Helmet" in entity.tags and attachedItem.type == "helmet"):
                                if (party[activeCharacter-1].helmet == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].helmet == None): inventory.append(party[activeCharacter-1].helmet)   
                                party[activeCharacter-1].helmet = attachedItem
                            elif ("Chestplate" in entity.tags and attachedItem.type == "chestplate"):
                                if (party[activeCharacter-1].chestplate == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].chestplate == None): inventory.append(party[activeCharacter-1].chestplate)   
                                party[activeCharacter-1].chestplate = attachedItem
                            elif ("Leggings" in entity.tags and attachedItem.type == "leggings"):
                                if (party[activeCharacter-1].leggings == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].leggings == None): inventory.append(party[activeCharacter-1].leggings)   
                                party[activeCharacter-1].leggings = attachedItem
                            elif ("Boots" in entity.tags and attachedItem.type == "boots"):
                                if (party[activeCharacter-1].boots == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].boots == None): inventory.append(party[activeCharacter-1].boots)   
                                party[activeCharacter-1].boots = attachedItem
                            elif ("Accessory1" in entity.tags and attachedItem.type == "accessory"):
                                if (party[activeCharacter-1].accessory1 == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].accessory1 == None): inventory.append(party[activeCharacter-1].accessory1)   
                                party[activeCharacter-1].accessory1 = attachedItem
                            elif ("Accessory2" in entity.tags and attachedItem.type == "accessory"):
                                if (party[activeCharacter-1].accessory2 == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].accessory2 == None): inventory.append(party[activeCharacter-1].accessory2)   
                                party[activeCharacter-1].accessory2 = attachedItem
                            elif ("Weapon" in entity.tags and attachedItem.type == "weapon"):
                                if (party[activeCharacter-1].weapon == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].weapon == None): inventory.append(party[activeCharacter-1].weapon)   
                                party[activeCharacter-1].weapon = attachedItem
                            updateInventory()
                            updateCharacter()
                            attachedItem = None
                            attachedItemVisual.isShowing = False
                            break
                if (not attachedItem == None):
                    if (not attachedItemEquipped == None):
                        if (attachedItemEquipped == "Helmet"):
                            party[activeCharacter-1].helmet = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Chestplate"):
                            party[activeCharacter-1].chestplate = None
                            inventory.append(attachedItem) 
                        elif (attachedItemEquipped == "Leggings"):
                            print(attachedItemEquipped)
                            party[activeCharacter-1].leggings = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Boots"):
                            party[activeCharacter-1].boots = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Accessory1"):
                            party[activeCharacter-1].accessory1 = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Accessory2"):
                            party[activeCharacter-1].accessory2 = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Weapon"):
                            party[activeCharacter-1].weapon = None
                            inventory.append(attachedItem)  
                    attachedItem = None
                    attachedItemVisual.isShowing = False
                    updateInventory()
                    updateCharacter()
    
        if (not attachedItem == None):
            attachedItemVisual.xPosition = mouse[0] - attachedItemVisual.width/2
            attachedItemVisual.yPosition = mouse[1] - attachedItemVisual.length/2
        refreshScreen()
        if (leaveScreen): break
    if (nextScreen == "Combat"):
        combatScreen()
    elif (nextScreen == "Quit"):
        pygame.quit()
    else:
        print("Screen Not Found")
        combatScreen()

def openWorldScreen():
    global visualEntities
    visualEntities = []
    screen.fill((0, 0, 0))
    file = open("screens/loadingScreen.json", 'r')
    data = json.load(file)
    for item in data:
        if item["entityType"] == "Image":
             entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Drawing":
            entity = DrawingEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "Button":
            entity = ButtonEntity.createFrom(item)
        elif item["entityType"] == "TransparentButton":
            entity = TransparentButtonEntity.createFrom(item)
            
        entity.resize(entity.width*screen.get_width(), entity.height*screen.get_height())
        entity.reposition(entity.xPosition * screen.get_width(),entity.yPosition * screen.get_height())
        if (item["entityType"] == "TransparentButton" or item["entityType"] == "Button"): buttons.append(entity)
        else: visualEntities.append(entity)
    
    refreshScreen()
    run(screen, screenX, screenY)
    pygame.quit()















combatScreen()
pygame.quit()