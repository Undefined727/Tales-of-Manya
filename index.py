import pygame, numpy, os, random, VisualEntity, Entity, Skill, Item
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String

'''
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
pygame.display.set_icon(pygame.image.load('sprites/catgirl-icon.jpg'))
screen = pygame.display.set_mode([screenX, screenY])

visualEntities = []
inventory = []
party = []

party = [Entity.Entity("Catgirl", "catgirl.png", 10), Entity.Entity("Catgirl", "catgirl.png", 20), Entity.Entity("Catgirl", "catgirl.png", 15)]
party[1].skills[0] = Skill.Skill(1)
party[1].skills[1] = Skill.Skill(2)
party[1].skills[2] = Skill.Skill(3)

inventory.append(Item.Item(9))
inventory.append(Item.Item(9))
inventory.append(Item.Item(7))
inventory.append(Item.Item(2))
inventory.append(Item.Item(5))
inventory.append(Item.Item(9))
inventory.append(Item.Item(9))
inventory.append(Item.Item(9))
inventory.append(Item.Item(9))
inventory.append(Item.Item(9))



   
def refreshScreen():
    # Fill the background
    global visualEntities
    for entity in visualEntities:
        if entity.isShowing:
            if entity.entityType == 0:
                screen.blit(entity.img, (entity.xPosition, entity.yPosition))
            elif entity.entityType == 1:
                if entity.shape == "rectangle":
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

    pygame.display.flip()
   
def mouseInRegion(mouse, shape, xPosition, yPosition, width, length):
    if (shape == "rectangle"):
        return (xPosition <= mouse[0] <= xPosition+width and yPosition <= mouse[1] <= yPosition+length)
    elif (shape == "ellipse"):
        return ((mouse[0]-(xPosition+width/2))*(mouse[0]-(xPosition+width/2)) + (width/length)*(width/length)*(mouse[1]-(yPosition+length/2))*(mouse[1]-(yPosition+length/2)) < ((width/2)*(width/2)))

# activeCharacter is an int showing which character in the party acted, enemies is an array of enemies, selectedEnemy is an int showing which enemy was selected, skill is the Skill that was used.
# Reminder that AoE effects do NOT include the target of an ability
# This does NOT verify that an ability can/should be used and simply executes the effects
def useSkill(enemies, selectedEnemy, activeCharacter, party, skill):
    if (len(enemies) == 0): return
    party[activeCharacter].mana = party[activeCharacter].mana - skill.manaCost

    party[activeCharacter].HP = party[activeCharacter].HP + skill.healing*party[activeCharacter].magic/100
    for character in range(0, len(party)):
        if (character != activeCharacter): party[character].HP = party[character].HP + skill.aoeHealing*party[activeCharacter].magic/100
    
    enemies[selectedEnemy].HP = enemies[selectedEnemy].HP - skill.damage*party[activeCharacter].ATK/100
    for enemy in range(0, len(enemies)):
        if (enemy != selectedEnemy): 
            enemies[enemy].HP = enemies[enemy].HP - skill.aoeDamage*party[activeCharacter].ATK/100

    # Special code for individual skills with unique effects will go here
    if (skill.name == "Berserk"):
        party[activeCharacter].HP = party[activeCharacter].HP - skill.damage*party[activeCharacter].ATK/100


    for enemy in range(0, len(enemies)):
        if (enemies[enemy].HP < 0): enemies[enemy].HP = 0
        if (enemies[enemy].HP > enemies[enemy].maxHP): enemies[enemy].HP = enemies[enemy].maxHP
    for character in range(0, len(party)):
        if (party[character].HP < 0): party[character].HP = 0
        if (party[character].HP > party[character].maxHP): party[character].HP = party[character].maxHP


def combatScreen():
    global visualEntities
    enemies = []
    enemies = [Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30)), Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30))]
    activeCharacter = 2
    skillSelected = 0
    skillsShowing = False
    enemySelectionShowing = False
    leaveScreen = False
    nextScreen = None


    activeCharacterX = 7*screenX/18
    activeCharacterY = 9*screenY/18
    activeCharacterSizeX = 2*screenX/9
    activeCharacterSizeY = 4*screenY/9
    inactiveCharacterSizeX = screenX/24
    inactiveCharacterSizeY = screenY/12
    inactiveCharacter1X = activeCharacterX-activeCharacterSizeX/2
    inactiveCharacter2X = activeCharacterX+3*activeCharacterSizeX/2-inactiveCharacterSizeX
    inactiveCharacterY = 4*screenY/6
    playerHPBarSizeX = activeCharacterSizeX/2
    playerHPBarSizeY = screenY/40
    playerManaBarX = activeCharacterX+activeCharacterSizeX/4
    playerManaBarY = activeCharacterY + activeCharacterSizeY - screenY/24
    playerHPBarX = playerManaBarX
    playerHPBarY = playerManaBarY - 5*playerHPBarSizeY
    playerHPBarBorderWidthX = playerHPBarSizeX/3
    playerHPBarBorderWidthY = 3*playerHPBarSizeY/2
    

    inactiveCharacter1HPBarX = inactiveCharacter1X - inactiveCharacterSizeX/2
    inactiveCharacter1HPBarY = inactiveCharacterY + 2*inactiveCharacterSizeY
    inactiveCharacter1HPBarSizeX = 2 * inactiveCharacterSizeX
    inactiveCharacter1HPBarSizeY = inactiveCharacterSizeY/5
    inactiveCharacter1HPBarBorderWidthX = inactiveCharacter1HPBarSizeX/3
    inactiveCharacter1HPBarBorderWidthY = 3*inactiveCharacter1HPBarSizeY/2
    inactiveCharacter1ManaBarX = inactiveCharacter1HPBarX
    inactiveCharacter1ManaBarY = inactiveCharacter1HPBarY + inactiveCharacterSizeY

    inactiveCharacter2HPBarX = inactiveCharacter2X - inactiveCharacterSizeX/2
    inactiveCharacter2HPBarY = inactiveCharacterY + 2*inactiveCharacterSizeY
    inactiveCharacter2HPBarSizeX = 2 * inactiveCharacterSizeX
    inactiveCharacter2HPBarSizeY = inactiveCharacterSizeY/5
    inactiveCharacter2HPBarBorderWidthX = inactiveCharacter2HPBarSizeX/3
    inactiveCharacter2HPBarBorderWidthY = 3*inactiveCharacter2HPBarSizeY/2
    inactiveCharacter2ManaBarX = inactiveCharacter2HPBarX
    inactiveCharacter2ManaBarY = inactiveCharacter2HPBarY + inactiveCharacterSizeY

    changeCharacterLX = inactiveCharacter1X
    changeCharacterLY = activeCharacterY
    changeCharacterRX = inactiveCharacter2X
    changeCharacterRY = activeCharacterY
    changeCharacterSizeX = playerHPBarBorderWidthX
    changeCharacterSizeY = playerHPBarBorderWidthX
    
    exitButtonX = 27*screenX/32
    exitButtonY = 5*screenY/6
    glossaryButtonX = 27*screenX/32
    glossaryButtonY = 4*screenY/6
    bagButtonX = screenX/32
    bagButtonY = 5*screenY/6
    skillButtonX = screenX/32
    skillButtonY = 4*screenY/6
    buttonSizeX = 2*screenX/16
    buttonSizeY = screenY/8
    skillSizeX = buttonSizeX/2
    skillSizeY = buttonSizeY
    skill1X = skillButtonX
    skill2X = skillButtonX + skillSizeX
    skill3X = skillButtonX + 2*skillSizeX
    skillY = skillButtonY-skillSizeY


    def exitButtonFunction(*args):
        pygame.quit()

    def bagButtonFunction(*args):
        nonlocal nextScreen
        nonlocal leaveScreen
        nextScreen = "Inventory"
        leaveScreen = True

    def changeCharacterFunction(*args):
        nonlocal activeCharacter
        print(args[0])
        if (args[0] == "Left"): activeCharacter = ((activeCharacter)%3)+1
        else: activeCharacter = ((activeCharacter-2)%3)+1
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
        nonlocal playerHPBarSizeX
        nonlocal inactiveCharacter1HPBarSizeX
        nonlocal inactiveCharacter2HPBarSizeX
        for item in visualEntities:
            if (item.name == "Player"): item.updateImg(str(party[activeCharacter-1].img))
            if (item.name == "PlayerHPText"): item.updateText(str(int(party[activeCharacter-1].HP)) + "/" + str(int(party[activeCharacter-1].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "PlayerHPGreen"): item.width = playerHPBarSizeX*party[activeCharacter-1].HP/party[activeCharacter-1].maxHP
            if (item.name == "PlayerManaText"): item.updateText(str(int(party[activeCharacter-1].mana)) + "/" + str(int(party[activeCharacter-1].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "PlayerManaBlue"): item.width = playerHPBarSizeX*party[activeCharacter-1].mana/party[activeCharacter-1].maxMana
            if (item.name == "InactiveCharacter1Img"): item.updateImg(str(party[(activeCharacter-2)%3].headImg))
            if (item.name == "InactiveCharacter1HPText"): item.updateText(str(int(party[(activeCharacter-2)%3].HP)) + "/" + str(int(party[(activeCharacter-2)%3].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "InactiveCharacter1HPGreen"): item.width = inactiveCharacter1HPBarSizeX*party[activeCharacter-2].HP/party[activeCharacter-2].maxHP
            if (item.name == "InactiveCharacter1ManaText"): item.updateText(str(int(party[(activeCharacter-2)%3].mana)) + "/" + str(int(party[(activeCharacter-2)%3].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "InactiveCharacter1ManaBlue"): item.width = inactiveCharacter1HPBarSizeX*party[(activeCharacter-2)%3].mana/party[(activeCharacter-2)%3].maxMana
            if (item.name == "InactiveCharacter2Img"): item.updateImg(str(party[(activeCharacter)%3].headImg))
            if (item.name == "InactiveCharacter2HPText"): item.updateText(str(int(party[(activeCharacter)%3].HP)) + "/" + str(int(party[(activeCharacter)%3].maxHP)), "mono", int(playerHPBarX/40), "black", None)
            if (item.name == "InactiveCharacter2HPGreen"): item.width = inactiveCharacter2HPBarSizeX*party[(activeCharacter)%3].HP/party[(activeCharacter)%3].maxHP
            if (item.name == "InactiveCharacter2ManaText"): item.updateText(str(int(party[(activeCharacter)%3].mana)) + "/" + str(int(party[(activeCharacter)%3].maxMana)), "mono", int(playerManaBarX/40), "black", None)
            if (item.name == "InactiveCharacter2ManaBlue"): item.width = inactiveCharacter2HPBarSizeX*party[(activeCharacter)%3].mana/party[(activeCharacter)%3].maxMana

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
            if ("Enemy" in item.tags): visualEntities.remove(item)
        for enemy in enemies[:]:
            if (enemy.HP <= 0):
                enemies.remove(enemy)

        count = 0
        for enemy in enemies:
            currEnemyX = (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2))
            currEnemyHPBarX = currEnemyX + enemySizeX/6
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1), 0, True, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy"], enemy.img))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "SelectionButton", 2, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], enemySelectionButtonFunction, (count), "ellipse"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "Selection", 1, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], "white", True, "ellipse"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count + 1) + "HPBorder", 0, True, currEnemyHPBarX-HPBarBorderWidthX, HPBarY-HPBarBorderWidthY, HPBarSizeX + 2*HPBarBorderWidthX, HPBarSizeY + 2*HPBarBorderWidthY, ["Enemy"], "HPBar.png"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "HPRed", 1, True, currEnemyHPBarX, HPBarY, HPBarSizeX, HPBarSizeY, ["Enemy"], "red", False, "rectangle"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "HPGreen", 1, True, currEnemyHPBarX, HPBarY, HPBarSizeX*enemy.HP/enemy.maxHP, HPBarSizeY, ["Enemy"], "green", False, "rectangle"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy"+ str(count+1) + "HPText", 3, True, currEnemyHPBarX+HPBarSizeX/2, HPBarY+HPBarSizeY/2, HPBarSizeX/2, HPBarSizeY, ["Enemy"], str(int(enemy.HP)) + "/" + str(int(enemy.maxHP)), "mono", int(HPBarSizeX/10), "black", None))
            count = count+1


    visualEntities.clear()
    visualEntities.append(VisualEntity.VisualEntity("Background", 0, True, 0, 0, screenX, screenY, ["Background"], "dungeonbackground.png"))
    
    visualEntities.append(VisualEntity.VisualEntity("Player", 0, True, activeCharacterX, activeCharacterY, activeCharacterSizeX, activeCharacterSizeY, ["Player"], str(party[activeCharacter-1].img)))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPBorder", 0, True, playerHPBarX-playerHPBarBorderWidthX, playerHPBarY-playerHPBarBorderWidthY, playerHPBarSizeX+2*playerHPBarBorderWidthX, playerHPBarSizeY+2*playerHPBarBorderWidthY, ["Player"], "HPBar.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPRed", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPGreen", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX*party[activeCharacter-1].HP/party[activeCharacter-1].maxHP, playerHPBarSizeY, ["Player"], "green", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPText", 3, True, playerHPBarX+playerHPBarSizeX/2, playerHPBarY+playerHPBarSizeY/2, playerHPBarSizeX/2, playerHPBarSizeY, ["Player"], str(int(party[activeCharacter-1].HP)) + "/" + str(int(party[activeCharacter-1].maxHP)), "mono", int(playerHPBarSizeX/10), "black", None))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaBorder", 0, True, playerManaBarX-playerHPBarBorderWidthX, playerManaBarY-playerHPBarBorderWidthY, playerHPBarSizeX+2*playerHPBarBorderWidthX, playerHPBarSizeY+2*playerHPBarBorderWidthY, ["Player"], "ManaBar.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaRed", 1, True, playerManaBarX, playerManaBarY, playerHPBarSizeX, playerHPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaBlue", 1, True, playerManaBarX, playerManaBarY, playerHPBarSizeX*party[activeCharacter-1].mana/party[activeCharacter-1].maxMana, playerHPBarSizeY, ["Player"], "blue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaText", 3, True, playerManaBarX+playerHPBarSizeX/2, playerManaBarY+playerHPBarSizeY/2, playerHPBarSizeX/2, playerHPBarSizeY, ["Player"], str(int(party[activeCharacter-1].mana)) + "/" + str(int(party[activeCharacter-1].maxMana)), "mono", int(playerHPBarSizeX/10), "black", None))
    
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1Img", 0, True, inactiveCharacter1X, inactiveCharacterY, inactiveCharacterSizeX, inactiveCharacterSizeY, ["Player"], str(party[(activeCharacter-2)%3].headImg)))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1HPBorder", 0, True, inactiveCharacter1HPBarX-inactiveCharacter1HPBarBorderWidthX, inactiveCharacter1HPBarY-inactiveCharacter1HPBarBorderWidthY, inactiveCharacter1HPBarSizeX+2*inactiveCharacter1HPBarBorderWidthX, inactiveCharacter1HPBarSizeY+2*inactiveCharacter1HPBarBorderWidthY, ["Player"], "HPBar.png"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1HPRed", 1, True, inactiveCharacter1HPBarX, inactiveCharacter1HPBarY, inactiveCharacter1HPBarSizeX, inactiveCharacter1HPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1HPGreen", 1, True, inactiveCharacter1HPBarX, inactiveCharacter1HPBarY, inactiveCharacter1HPBarSizeX*party[(activeCharacter-2)%3].HP/party[(activeCharacter-2)%3].maxHP, inactiveCharacter1HPBarSizeY, ["Player"], "green", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1HPText", 3, True, inactiveCharacter1HPBarX+inactiveCharacter1HPBarSizeX/2, inactiveCharacter1HPBarY+inactiveCharacter1HPBarSizeY/2, inactiveCharacter1HPBarSizeX/2, inactiveCharacter1HPBarSizeY, ["Player"], str(int(party[(activeCharacter-2)%3].HP)) + "/" + str(int(party[(activeCharacter-2)%3].maxHP)), "mono", int(inactiveCharacter1HPBarSizeX/10), "black", None))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1ManaBorder", 0, True, inactiveCharacter1ManaBarX-inactiveCharacter1HPBarBorderWidthX, inactiveCharacter1ManaBarY-inactiveCharacter1HPBarBorderWidthY, inactiveCharacter1HPBarSizeX+2*inactiveCharacter1HPBarBorderWidthX, inactiveCharacter1HPBarSizeY+2*inactiveCharacter1HPBarBorderWidthY, ["Player"], "ManaBar.png"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1ManaRed", 1, True, inactiveCharacter1ManaBarX, inactiveCharacter1ManaBarY, inactiveCharacter1HPBarSizeX, inactiveCharacter1HPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1ManaBlue", 1, True, inactiveCharacter1ManaBarX, inactiveCharacter1ManaBarY, inactiveCharacter1HPBarSizeX*party[(activeCharacter-2)%3].mana/party[(activeCharacter-2)%3].maxMana, inactiveCharacter1HPBarSizeY, ["Player"], "blue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter1ManaText", 3, True, inactiveCharacter1ManaBarX+inactiveCharacter1HPBarSizeX/2, inactiveCharacter1ManaBarY+inactiveCharacter1HPBarSizeY/2, inactiveCharacter1HPBarSizeX/2, inactiveCharacter1HPBarSizeY, ["Player"], str(int(party[(activeCharacter-2)%3].mana)) + "/" + str(int(party[(activeCharacter-2)%3].maxMana)), "mono", int(inactiveCharacter1HPBarSizeX/10), "black", None))
    
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2Img", 0, True, inactiveCharacter2X, inactiveCharacterY, inactiveCharacterSizeX, inactiveCharacterSizeY, ["Player"], str(party[(activeCharacter)%3].headImg)))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2HPBorder", 0, True, inactiveCharacter2HPBarX-inactiveCharacter2HPBarBorderWidthX, inactiveCharacter2HPBarY-inactiveCharacter1HPBarBorderWidthY, inactiveCharacter2HPBarSizeX+2*inactiveCharacter2HPBarBorderWidthX, inactiveCharacter2HPBarSizeY+2*inactiveCharacter2HPBarBorderWidthY, ["Player"], "HPBar.png"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2HPRed", 1, True, inactiveCharacter2HPBarX, inactiveCharacter2HPBarY, inactiveCharacter2HPBarSizeX, inactiveCharacter2HPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2HPGreen", 1, True, inactiveCharacter2HPBarX, inactiveCharacter2HPBarY, inactiveCharacter2HPBarSizeX*party[(activeCharacter)%3].HP/party[(activeCharacter)%3].maxHP, inactiveCharacter2HPBarSizeY, ["Player"], "green", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2HPText", 3, True, inactiveCharacter2HPBarX+inactiveCharacter2HPBarSizeX/2, inactiveCharacter2HPBarY+inactiveCharacter2HPBarSizeY/2, inactiveCharacter2HPBarSizeX/2, inactiveCharacter2HPBarSizeY, ["Player"], str(int(party[(activeCharacter)%3].HP)) + "/" + str(int(party[(activeCharacter)%3].maxHP)), "mono", int(inactiveCharacter2HPBarSizeX/10), "black", None))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2ManaBorder", 0, True, inactiveCharacter2ManaBarX-inactiveCharacter2HPBarBorderWidthX, inactiveCharacter2ManaBarY-inactiveCharacter2HPBarBorderWidthY, inactiveCharacter2HPBarSizeX+2*inactiveCharacter2HPBarBorderWidthX, inactiveCharacter2HPBarSizeY+2*inactiveCharacter2HPBarBorderWidthY, ["Player"], "ManaBar.png"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2ManaRed", 1, True, inactiveCharacter2ManaBarX, inactiveCharacter2ManaBarY, inactiveCharacter2HPBarSizeX, inactiveCharacter2HPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2ManaBlue", 1, True, inactiveCharacter2ManaBarX, inactiveCharacter2ManaBarY, inactiveCharacter2HPBarSizeX*party[(activeCharacter)%3].mana/party[(activeCharacter)%3].maxMana, inactiveCharacter2HPBarSizeY, ["Player"], "blue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("InactiveCharacter2ManaText", 3, True, inactiveCharacter2ManaBarX+inactiveCharacter2HPBarSizeX/2, inactiveCharacter2ManaBarY+inactiveCharacter2HPBarSizeY/2, inactiveCharacter2HPBarSizeX/2, inactiveCharacter2HPBarSizeY, ["Player"], str(int(party[(activeCharacter)%3].mana)) + "/" + str(int(party[(activeCharacter)%3].maxMana)), "mono", int(inactiveCharacter2HPBarSizeX/10), "black", None))

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
    updateEnemies()
    updateCharacters()

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
                                print("test")
                                entity.func(entity.args)
                                break



        if (party[activeCharacter-1].hasActed): 
            count = 0
            for enemy in enemies:
                useSkill(party, activeCharacter-1, count, enemies, enemy.skills[0])
                count += 1
            party[activeCharacter-1].hasActed = False
            updateEnemies()
            updateCharacters()
              
        if (party[activeCharacter-1].HP == 0 or len(enemies) == 0):
            party[activeCharacter-1].HP = party[activeCharacter-1].maxHP
            party[activeCharacter-1].mana = party[activeCharacter-1].maxMana
            enemies = [Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30)), Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30))]
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

    exitButtonX = screenX/16
    exitButtonY = 5*screenY/6
    buttonSizeX = 4*screenX/16
    buttonSizeY = screenY/8
    catgirlX = 29*screenX/48
    catgirlY = 3*screenY/12
    catgirlSizeX = screenX/3
    catgirlSizeY = 2*screenY/3
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
    hpsizeX = screenX/100
    manasizeX = screenX / 100
    magicsizeX = screenX / 100
    atksizeX = screenX / 100
    defsizeX = screenX / 100

    def itemClickFunction(*args):
        print("lol")

    def exitButtonFunction(*args):
        nonlocal leaveScreen
        nonlocal nextScreen
        leaveScreen = True
        nextScreen = "Combat"

    def updateInventoryStats():
        global visualEntities
        global party
        for item in visualEntities:
            if (item.name == "PlayerHPText"): item.updateText("HP: " + str(int(party[0].maxHP)), "mono", int(hpsizeX), "black", None)
            if (item.name == "PlayerManaText"): item.updateText("Mana: " + str(int(party[0].maxMana)), "mono", int(manasizeX), "black", None)
            if (item.name == "PlayerMagicText"): item.updateText("Magic Strength: " + str(int(party[0].magic)), "mono", int(magicsizeX), "black", None)
            if (item.name == "PlayerATKText"): item.updateText("ATK: " + str(int(party[0].ATK)), "mono", int(atksizeX), "black", None)
            if (item.name == "PlayerDEFText"): item.updateText("DEF: " + str(int(party[0].DEF)), "mono", int(defsizeX), "black", None)

    visualEntities.clear()
    visualEntities.append(VisualEntity.VisualEntity("Background", 0, True, 0, 0, screenX, screenY, ["Background"], "inventorybackground.png"))
    visualEntities.append(VisualEntity.VisualEntity("Player", 0, True, catgirlX, catgirlY, catgirlSizeX, catgirlSizeY, ["Player"], "catgirl.png"))
    visualEntities.append(VisualEntity.VisualEntity("HelmetBackground", 1, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet", "Item Background"], "cadetblue", False, "rectangle"))
    if (party[0].helmet == None): visualEntities.append(VisualEntity.VisualEntity("Helmet", 0, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], "helmet_transparent.png"))
    else: visualEntities.append(VisualEntity.VisualEntity("Helmet", 0, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], party[0].helmet.img))
    visualEntities.append(VisualEntity.VisualEntity("ChestplateBackground", 1, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate", "Item Background"], "cadetblue", False, "rectangle"))
    if (party[0].chestplate == None): visualEntities.append(VisualEntity.VisualEntity("Chestplate", 0, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], "chestplate_transparent.png"))
    else: visualEntities.append(VisualEntity.VisualEntity("Chestplate", 0, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate"], party[0].chestplate.img))
    visualEntities.append(VisualEntity.VisualEntity("LeggingsBackground", 1, True, leggingsX, leggingsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Leggings", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Leggings", 0, True, leggingsX, leggingsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Leggings"], party[0].leggings.img))
    visualEntities.append(VisualEntity.VisualEntity("BootsBackground", 1, True, bootsX, bootsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Boots", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Boots", 0, True, bootsX, bootsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Boots"], party[0].boots.img))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1Background", 1, True, accessory1X, accessory1Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory1", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1", 0, True, accessory1X, accessory1Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory1"], party[0].accessory1.img))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2Background", 1, True, accessory2X, accessory2Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory2", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2", 0, True, accessory2X, accessory2Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory2"], party[0].accessory2.img))
    visualEntities.append(VisualEntity.VisualEntity("WeaponBackground", 1, True, weaponX, weaponY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Weapon", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Weapon", 0, True, weaponX, weaponY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Weapon"], party[0].weapon.img))

    visualEntities.append(VisualEntity.VisualEntity("HelmetButton", 2, True, helmetX, helmetY, itemSizeX, itemSizeY,["Button", "Helmet","Item","Equipped Item"], itemClickFunction, party[0].helmet, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("ChestplateButton", 2, True, chestplateX, chestplateY, itemSizeX, itemSizeY,["Button", "Chestplate","Item","Equipped Item"], itemClickFunction, party[0].chestplate, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("LeggingsButton", 2, True, leggingsX, leggingsY, itemSizeX, itemSizeY,["Button", "Item","Leggings","Equipped Item"], itemClickFunction, party[0].leggings, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("BootsButton", 2, True, bootsX, bootsY, itemSizeX, itemSizeY,["Button", "Item", "Boots","Equipped Item"], itemClickFunction, party[0].boots, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1Button", 2, True, accessory1X, accessory1Y, itemSizeX, itemSizeY,["Button", "Item", "Accessory1","Equipped Item"], itemClickFunction, party[0].accessory1, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2Button", 2, True, accessory2X, accessory2Y, itemSizeX, itemSizeY,["Button", "Item", "Accessory2","Equipped Item"], itemClickFunction, party[0].accessory2, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("WeaponButton", 2, True, weaponX, weaponY, itemSizeX, itemSizeY,["Item", "Equipped Item", "Button", "Weapon"], itemClickFunction, party[0].weapon, "rectangle"))


    count = 0
    itemrow = 0
    bufferX = screenX/24
    bufferY = screenY/10

    for item in inventory:
        curritemX = count * (itemSizeX + bufferX) + bufferX
        curritemY = itemrow * (itemSizeY + bufferY) + bufferY

        visualEntities.append(VisualEntity.VisualEntity(item.name, 0, True, curritemX, curritemY, itemSizeX, itemSizeY, ["Item"], item.img))
        visualEntities.append(VisualEntity.VisualEntity("Item" + str(count + itemrow*4) + "Button", 2, True, curritemX, curritemY, itemSizeX, itemSizeY, ["Button","Item"], itemClickFunction, item, "rectangle"))
        count += 1
        if count >= 4:
            count = 0
            itemrow +=1
        

    statWidth = itemSizeX
    statLength = itemSizeY/2
    statX = 28*screenX/48
    stat1Y = 7*screenY/48
    stat2Y = 9*screenY/48
    stat3Y = 11*screenY/48
    stat4Y = 13*screenY/48
    stat5Y = 15*screenY/48

    visualEntities.append(VisualEntity.VisualEntity("PlayerHPText", 3, True, statX, stat1Y, itemSizeX, itemSizeY, ["Stat"], "HP: " + str(int(party[0].maxHP)), "mono", int(hpsizeX), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaText", 3, True, statX, stat2Y, itemSizeX, itemSizeY, ["Stat"], "Mana: " + str(int(party[0].maxMana)), "mono", int(manasizeX), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerMagicText", 3, True, statX, stat3Y, itemSizeX, itemSizeY, ["Stat"], "Magic Strength: " + str(int(party[0].magic)), "mono", int(magicsizeX), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerATKText", 3, True, statX, stat4Y, itemSizeX, itemSizeY, ["Stat"], "ATK: " + str(int(party[0].ATK)), "mono", int(atksizeX), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerDEFText", 3, True, statX, stat5Y, itemSizeX, itemSizeY, ["Stat"], "DEF: " + str(int(party[0].DEF)), "mono", int(defsizeX), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("ExitImg", 0, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], "ExitButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("ExitButton", 2, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], exitButtonFunction, None, "rectangle"))

    

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
                                print("test")
                                entity.func(entity.args)
                                break
    
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