import pygame, numpy, math, os, random, json
from model.visualentity.Tag import Tag
from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.DrawingEntity import DrawingEntity
from model.combat.Skill import Skill
from model.combat.Character import Character
from model.combat.Item import Item
import json

'''
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String
skilldata_engine = create_engine('sqlite:///skilldata.db', echo = True)

skilldata_meta = MetaData()

skilldata = Table(
   'skilldata', skilldata_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String),
   Column('img', String),
   Column('element', String),
   Column('singleTarget', Integer),
   Column('manaCost', Integer),
   Column('damage', Integer),
   Column('aoeDamage', Integer), 
   Column('healing', Integer),
   Column('aoeHealing', Integer))

skilldata_meta.create_all(skilldata_engine)
'''

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
         if (type(entity) == ImageEntity):
           if entity.isShowing:
             screen.blit(entity.img, (entity.xPosition, entity.yPosition))
         elif (type(entity) == DrawingEntity):
             if entity.isShowing:
                 pygame.draw.rect(screen,entity.color,(int(entity.xPosition), int(entity.yPosition),int(entity.width),int(entity.height)))

                # screen.blit(bar)

             '''
             if entity.entityType == 0:
                 screen.blit(entity.img, (entity.xPosition, entity.yPosition))
             elif entity.entityType == 1:
                    if entity.shape == "re  ctangle":
                    if entity.isBorder:
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.length), 2)
                    else:
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.length))
                if entity.shape == "ellipse":
                    if entity.isBorder:
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.length), 2)
                    else:
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.length))
            elif entity.entityType == 3:
                screen.blit(entity.textLabel, entity.textRect)
            '''
    pygame.display.flip()

# activeCharacter is an int showing which character in the party acted, enemies is an array of enemies, selectedEnemy is an int showing which enemy was selected, skill is the Skill that was used.
# Reminder that AoE effects do NOT include the target of an ability
# This does NOT verify that an ability can/should be used and simply executes the effects
def useSkill(enemies, selectedEnemy, activeCharacter, party, skill):
    if (len(enemies) == 0): return
    party[activeCharacter].mana = party[activeCharacter].mana - skill.manaCost

    party[activeCharacter].HP = party[activeCharacter].HP + skill.healing*party[activeCharacter].magic/100
    for character in range(0, len(party)):
        if (character != activeCharacter): party[character].HP = party[character].HP + skill.aoeHealing*party[activeCharacter].magic/100
    
    enemies[selectedEnemy].HP = enemies[selectedEnemy].HP - (skill.damage*party[activeCharacter].ATK/100)*math.pow(0.6, enemies[selectedEnemy].DEF/250)
    for enemy in range(0, len(enemies)):
        if (enemy != selectedEnemy): 
            enemies[enemy].HP = enemies[enemy].HP - ((skill.aoeDamage*party[activeCharacter].ATK/100)*math.pow(0.6, enemies[enemy].DEF/250))

    # Special code for individual skills with unique effects will go here
    if (skill.name == "Berserk"):
        party[activeCharacter].HP = party[activeCharacter].HP - ((skill.damage*party[activeCharacter].ATK/100)*math.pow(0.6, party[activeCharacter].DEF/250))


    for enemy in range(0, len(enemies)):
        if (enemies[enemy].HP < 0): enemies[enemy].HP = 0
        if (enemies[enemy].HP > enemies[enemy].maxHP): enemies[enemy].HP = enemies[enemy].maxHP
    for character in range(0, len(party)):
        if (party[character].HP < 0): party[character].HP = 0
        if (party[character].HP > party[character].maxHP): party[character].HP = party[character].maxHP
    party[activeCharacter].hasActed = True


def combatScreen():
    global visualEntities
    enemies = []
    enemies = [Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30)), Character("Wizard", "wizard.png", random.randint(5, 30)), Character("Frog", "frog.png", random.randint(5, 30))]
    activeCharacter = 1
    skillSelected = 0
    skillsShowing = False
    enemySelectionShowing = False
    leaveScreen = False
    nextScreen = None

    visualEntities = []
    file = open("screens/combatScreen.json", 'r')
    data = json.load(file)
    for item in data:
        if item["entityType"] == "Image":
             imageEntity = ImageEntity.createFrom(item)
             imageEntity.resize(imageEntity.width*screen.get_width(), imageEntity.height*screen.get_height())
             imageEntity.reposition(imageEntity.xPosition*screen.get_width(), imageEntity.yPosition*screen.get_height())
             visualEntities.append(imageEntity)
        elif item["entityType"] == "Drawing":
            drawingEntity = DrawingEntity.createFrom(item)
            drawingEntity.resize(drawingEntity.width*screen.get_width(), drawingEntity.height*screen.get_height())
            drawingEntity.reposition(drawingEntity.xPosition * screen.get_width(),drawingEntity.yPosition * screen.get_height())

            visualEntities.append(drawingEntity)

    

    def exitButtonFunction(*args):
        pygame.quit()

    def bagButtonFunction(*args):
        nonlocal nextScreen
        nonlocal leaveScreen
        nextScreen = "Inventory"
        leaveScreen = True

    def changeCharacterFunction(*args):
        nonlocal activeCharacter
        if (args[0] == "Left"): activeCharacter = ((activeCharacter)%len(party))+1
        else: activeCharacter = ((activeCharacter-2)%len(party))+1
        updateCharacters()

    def skillButtonFunction(*args):
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
            if (item.name == "PlayerHPText"): item.updateText(str(int(party[activeCharacter-1].HP)) + "/" + str(int(party[activeCharacter-1].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "PlayerHPGreen"): item.width = screenX*0.5*party[activeCharacter-1].HP/party[activeCharacter-1].maxHP
            if (item.name == "PlayerManaText"): item.updateText(str(int(party[activeCharacter-1].mana)) + "/" + str(int(party[activeCharacter-1].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "PlayerManaBlue"): item.width = screenX*0.5*party[activeCharacter-1].mana/party[activeCharacter-1].maxMana
            if (item.name == "InactiveCharacter1Img"): item.updateImg(str(party[(activeCharacter-2)%len(party)].headImg))
            if (item.name == "InactiveCharacter1HPText"): item.updateText(str(int(party[(activeCharacter-2)%len(party)].HP)) + "/" + str(int(party[(activeCharacter-2)%len(party)].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "InactiveCharacter1HPGreen"): item.width = screenX*0.5*party[activeCharacter-2].HP/party[activeCharacter-2].maxHP
            if (item.name == "InactiveCharacter1ManaText"): item.updateText(str(int(party[(activeCharacter-2)%len(party)].mana)) + "/" + str(int(party[(activeCharacter-2)%len(party)].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "InactiveCharacter1ManaBlue"): item.width = screenX*0.5*party[(activeCharacter-2)%len(party)].mana/party[(activeCharacter-2)%len(party)].maxMana
            if (item.name == "PlayerCheckmark"): item.isShowing = party[(activeCharacter - 1) % len(party)].hasActed
            if (item.name == "InactiveCharacter1Checkmark" ): item.isShowing = party[(activeCharacter-2) % len(party)].hasActed
            if (item.name == "InactiveCharacter2Checkmark"): item.isShowing = party[(activeCharacter) % len(party)].hasActed
            if (item.name == "InactiveCharacter2Img"): item.updateImg(str(party[(activeCharacter)%len(party)].headImg))
            if (item.name == "InactiveCharacter2HPText"): item.updateText(str(int(party[(activeCharacter)%len(party)].HP)) + "/" + str(int(party[(activeCharacter)%len(party)].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "InactiveCharacter2HPGreen"): item.width = screenX*0.5*party[(activeCharacter)%len(party)].HP/party[(activeCharacter)%len(party)].maxHP
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
        global visualEntities
        enemyY = screenY/20
        enemySizeX = screenX/9
        enemySizeY = screenY/5
        HPBarY = enemyY + enemySizeY + screenY/100
        HPBarSizeX = 2*enemySizeX/3
        HPBarSizeY = enemySizeY/15
        HPBarBorderWidthX = HPBarSizeX/3
        HPBarBorderWidthY = 3*HPBarSizeY/2

        for item in visualEntities[:]:
            if (Tag.ENEMY in item.tags): visualEntities.remove(item)
        for enemy in enemies[:]:
            if (enemy.HP <= 0):
                enemies.remove(enemy)

        count = 0
        for enemy in enemies:

            currEnemyX = (((1.5 + 2*count))/(len(enemies)*2+1) - (enemySizeX/2))
            currEnemyHPBarX = currEnemyX + enemySizeX/6
            print(currEnemyX)
            #visualEntities.append(ImageEntity("Enemy" + str(count+1), True, currEnemyX, enemyY, enemySizeX, enemySizeY, [Tag.ENEMY], enemy.img))

            #visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "SelectionButton", 2, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], enemySelectionButtonFunction, (count), "ellipse"))
            #visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "Selection", 1, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], "white", True, "ellipse"))
            visualEntities.append(ImageEntity("Enemy" + str(count + 1) + "enemyImg", True, currEnemyX/100, enemyY/100,enemySizeX, enemySizeY, [Tag.ENEMY], enemy.img))
            #visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "HPRed", 1, True, currEnemyHPBarX, HPBarY, HPBarSizeX, HPBarSizeY, ["Enemy"], "red", False, "rectangle"))
            #visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "HPGreen", 1, True, currEnemyHPBarX, HPBarY, HPBarSizeX*enemy.HP/enemy.maxHP, HPBarSizeY, ["Enemy"], "green", False, "rectangle"))
            #visualEntities.append(VisualEntity.VisualEntity("Enemy"+ str(count+1) + "HPText", 3, True, currEnemyHPBarX+HPBarSizeX/2, HPBarY+HPBarSizeY/2, HPBarSizeX/2, HPBarSizeY, ["Enemy"], str(int(enemy.HP)) + "/" + str(int(enemy.maxHP)), "mono", int(HPBarSizeX/10), "black", None))
            count = count+1

    '''
    activeCharacterX = 38
    activeCharacterY = 5
    activeCharacterSizeX = 22
    activeCharacterSizeY = 44
    inactiveCharacterSizeX = 4
    inactiveCharacterSizeY = 8
    inactiveCharacter1X = 27
    inactiveCharacter2X = 67
    inactiveCharacterY = 67
    playerHPBarSizeX = 11
    playerHPBarSizeY = 2
    playerManaBarX = 44
    playerManaBarY = 45
    playerHPBarX = 44
    playerHPBarY = 35
    playerHPBarBorderWidthX = 4
    playerHPBarBorderWidthY = 3
    inactiveCharacter1HPBarX = 25
    inactiveCharacter1HPBarY = 83
    inactiveCharacter1HPBarSizeX = 8
    inactiveCharacter1HPBarSizeY = 2
    inactiveCharacter1HPBarBorderWidthX = 3
    inactiveCharacter1HPBarBorderWidthY = 2.4
    inactiveCharacter1ManaBarX = 25
    inactiveCharacter1ManaBarY = 91
    inactiveCharacter2HPBarX = 65
    inactiveCharacter2HPBarY = 83
    inactiveCharacter2HPBarSizeX = 8
    inactiveCharacter2HPBarSizeY = 2
    inactiveCharacter2HPBarBorderWidthX = 3
    inactiveCharacter2HPBarBorderWidthY = 3
    inactiveCharacter2ManaBarX = 65
    inactiveCharacter2ManaBarY = 91
    changeCharacterLX = 27
    changeCharacterLY = 5
    changeCharacterRX = 67
    changeCharacterRY = 5
    changeCharacterSizeX = 4
    changeCharacterSizeY = 3
    exitButtonX = 84
    exitButtonY = 83
    glossaryButtonX = 84
    glossaryButtonY = 67
    bagButtonX = 3
    bagButtonY = 83
    skillButtonX = 3
    skillButtonY = 67
    buttonSizeX = 13
    buttonSizeY = 13
    skillSizeX = 7
    skillSizeY = 13
    skill1X = 3
    skill2X = 10
    skill3X = 17
    skillY = 54
    
   # 1 = drawing
   # 3 = text
   # 2 = button
   # 0 = image
   # 4 = transparent
   
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPRed", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPGreen", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX*party[activeCharacter-1].HP/party[activeCharacter-1].maxHP, playerHPBarSizeY, ["Player"], "green", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPText", 3, True, playerHPBarX+playerHPBarSizeX/2, playerHPBarY+playerHPBarSizeY/2, playerHPBarSizeX/2, playerHPBarSizeY, ["Player"], str(int(party[activeCharacter-1].HP)) + "/" + str(int(party[activeCharacter-1].maxHP)), "mono", int(playerHPBarSizeX/10), "black", None))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaRed", 1, True, playerManaBarX, playerManaBarY, playerHPBarSizeX, playerHPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaBlue", 1, True, playerManaBarX, playerManaBarY, playerHPBarSizeX*party[activeCharacter-1].mana/party[activeCharacter-1].maxMana, playerHPBarSizeY, ["Player"], "blue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaText", 3, True, playerManaBarX+playerHPBarSizeX/2, playerManaBarY+playerHPBarSizeY/2, playerHPBarSizeX/2, playerHPBarSizeY, ["Player"], str(int(party[activeCharacter-1].mana)) + "/" + str(int(party[activeCharacter-1].maxMana)), "mono", int(playerHPBarSizeX/10), "black", None))
    

    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1HPRed", 1, True, inactiveCharacter1HPBarX, inactiveCharacter1HPBarY, inactiveCharacter1HPBarSizeX, inactiveCharacter1HPBarSizeY, ["InactiveCharacter1"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1HPGreen", 1, True, inactiveCharacter1HPBarX, inactiveCharacter1HPBarY, inactiveCharacter1HPBarSizeX*party[(activeCharacter-2)%len(party)].HP/party[(activeCharacter-2)%len(party)].maxHP, inactiveCharacter1HPBarSizeY, ["InactiveCharacter1"], "green", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1HPText", 3, True, inactiveCharacter1HPBarX+inactiveCharacter1HPBarSizeX/2, inactiveCharacter1HPBarY+inactiveCharacter1HPBarSizeY/2, inactiveCharacter1HPBarSizeX/2, inactiveCharacter1HPBarSizeY, ["InactiveCharacter1"], str(int(party[(activeCharacter-2)%len(party)].HP)) + "/" + str(int(party[(activeCharacter-2)%len(party)].maxHP)), "mono", int(inactiveCharacter1HPBarSizeX/10), "black", None))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1ManaRed", 1, True, inactiveCharacter1ManaBarX, inactiveCharacter1ManaBarY, inactiveCharacter1HPBarSizeX, inactiveCharacter1HPBarSizeY, ["InactiveCharacter1"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1ManaBlue", 1, True, inactiveCharacter1ManaBarX, inactiveCharacter1ManaBarY, inactiveCharacter1HPBarSizeX*party[(activeCharacter-2)%len(party)].mana/party[(activeCharacter-2)%len(party)].maxMana, inactiveCharacter1HPBarSizeY, ["InactiveCharacter1"], "blue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1ManaText", 3, True, inactiveCharacter1ManaBarX+inactiveCharacter1HPBarSizeX/2, inactiveCharacter1ManaBarY+inactiveCharacter1HPBarSizeY/2, inactiveCharacter1HPBarSizeX/2, inactiveCharacter1HPBarSizeY, ["InactiveCharacter1"], str(int(party[(activeCharacter-2)%len(party)].mana)) + "/" + str(int(party[(activeCharacter-2)%len(party)].maxMana)), "mono", int(inactiveCharacter1HPBarSizeX/10), "black", None))

    
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2HPRed", 1, True, inactiveCharacter2HPBarX, inactiveCharacter2HPBarY, inactiveCharacter2HPBarSizeX, inactiveCharacter2HPBarSizeY, ["InactiveCharacter2"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2HPGreen", 1, True, inactiveCharacter2HPBarX, inactiveCharacter2HPBarY, inactiveCharacter2HPBarSizeX*party[(activeCharacter)%len(party)].HP/party[(activeCharacter)%len(party)].maxHP, inactiveCharacter2HPBarSizeY, ["InactiveCharacter2"], "green", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2HPText", 3, True, inactiveCharacter2HPBarX+inactiveCharacter2HPBarSizeX/2, inactiveCharacter2HPBarY+inactiveCharacter2HPBarSizeY/2, inactiveCharacter2HPBarSizeX/2, inactiveCharacter2HPBarSizeY, ["InactiveCharacter2"], str(int(party[(activeCharacter)%len(party)].HP)) + "/" + str(int(party[(activeCharacter)%len(party)].maxHP)), "mono", int(inactiveCharacter2HPBarSizeX/10), "black", None))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2ManaRed", 1, True, inactiveCharacter2ManaBarX, inactiveCharacter2ManaBarY, inactiveCharacter2HPBarSizeX, inactiveCharacter2HPBarSizeY, ["InactiveCharacter2"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2ManaBlue", 1, True, inactiveCharacter2ManaBarX, inactiveCharacter2ManaBarY, inactiveCharacter2HPBarSizeX*party[(activeCharacter)%len(party)].mana/party[(activeCharacter)%len(party)].maxMana, inactiveCharacter2HPBarSizeY, ["InactiveCharacter2"], "blue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2ManaText", 3, True, inactiveCharacter2ManaBarX+inactiveCharacter2HPBarSizeX/2, inactiveCharacter2ManaBarY+inactiveCharacter2HPBarSizeY/2, inactiveCharacter2HPBarSizeX/2, inactiveCharacter2HPBarSizeY, ["InactiveCharacter2"], str(int(party[(activeCharacter)%len(party)].mana)) + "/" + str(int(party[(activeCharacter)%len(party)].maxMana)), "mono", int(inactiveCharacter2HPBarSizeX/10), "black", None))

    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterRight", 4, True, changeCharacterRX, changeCharacterRY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], changeCharacterFunction, "Right", "change_active_right.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterRightImg", 0, True, changeCharacterRX, changeCharacterRY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], "change_active_right.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterLeft", 4, True, changeCharacterLX, changeCharacterLY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], changeCharacterFunction, "Left", "change_active_left.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterLeftImg", 0, True, changeCharacterLX, changeCharacterLY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], "change_active_left.png"))

    visualEntities.append(VisualEntity.VisualEntity("Exit", 0, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], "ExitButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("ExitButton", 2, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], exitButtonFunction, None, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill", 0, True, skillButtonX, skillButtonY, buttonSizeX, buttonSizeY, ["Menu"], "SkillButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("SkillButton", 2, True, skillButtonX, skillButtonY, buttonSizeX, buttonSizeY, ["Menu"], skillButtonFunction, None, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Bag", 0, True, bagButtonX, bagButtonY, buttonSizeX, buttonSizeY, ["Menu"], "BagButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("BagButton", 4, True, bagButtonX, bagButtonY, buttonSizeX, buttonSizeY, ["Menu"], bagButtonFunction, None, "BagButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("Glossary", 0, True, glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY, ["Menu"], "GlossaryButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("GlossaryButton", 2, True, glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY, ["Menu"], pygame.quit, None, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill1", 0, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[0].img))
    visualEntities.append(VisualEntity.VisualEntity("Skill1Button", 2, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 0, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill1Text", 3, False, skill1X+skillSizeX/2, skillY+skillSizeY/2, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[0].name, "mono", int(skill1X/3), "black", "yellow"))
    visualEntities.append(VisualEntity.VisualEntity("Skill2", 0, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[1].img))
    visualEntities.append(VisualEntity.VisualEntity("Skill2Button", 2, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 1, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill2Text", 3, False, skill2X+skillSizeX/2, skillY+skillSizeY/2, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[1].name, "mono", int(skill2X/10), "black", "yellow"))
    visualEntities.append(VisualEntity.VisualEntity("Skill3", 0, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[2].img))
    visualEntities.append(VisualEntity.VisualEntity("Skill3Button", 2, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 2, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill3Text", 3, False, skill3X+skillSizeX/2, skillY+skillSizeY/2, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[2].name, "mono", int(skill3X/20), "black", "yellow"))
    
    '''

    updateEnemies()
    updateCharacters()

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        entity.func(entity.args)
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
              
        if (party[activeCharacter-1].HP == 0 or len(enemies) == 0):
            party[activeCharacter-1].HP = party[activeCharacter-1].maxHP
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
                for entity in visualEntities:
                    if (entity.entityType == 2):
                        if mouseInRegion(mouse, entity.shape, entity.xPosition, entity.yPosition, entity.width, entity.length):
                            entity.func(entity.args)
                            break
                    if (entity.entityType == 4):
                        array = entity.npArray
                        x = int(mouse[0]-entity.xPosition)
                        y = int(mouse[1]-entity.yPosition)
                        if (x >= 0 and x < int(entity.width) and y >= 0 and y < int(entity.length)): 
                            transparency = array[y, x, 3]
                            if (transparency != 0):
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

combatScreen()
pygame.quit()