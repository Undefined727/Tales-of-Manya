import pygame, os, random, VisualEntity, Entity, Skill, Item
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String

#Initializes databases
'''
itemdata_engine = create_engine('sqlite:///itemdata.db', echo = True)

itemdata_meta = MetaData()

itemdata = Table(
   'itemdata', itemdata_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String),
   Column('type', String),
   Column('img', String), 
   Column('magicPercent', Integer),
   Column('manaPercent', Integer), 
   Column('DEFPercent', Integer),
   Column('ATKPercent', Integer),
   Column('HPPercent', Integer),
   Column('flatMagic', Integer), 
   Column('flatMana', Integer),
   Column('flatDEF', Integer),
   Column('flatATK', Integer),
   Column('flatHP', Integer))

itemdata_meta.create_all(itemdata_engine)
'''

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()
#screenX,screenY = info.current_w,info.current_h
screenX, screenY = 960, 600
pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('sprites/catgirl-icon.jpg'))
screen = pygame.display.set_mode([screenX, screenY])

visualEntities = []
inventory = []
party = []

party = [Entity.Entity("Catgirl", "catgirl.png", 20), Entity.Entity("Catgirl", "catgirl.png", 20), Entity.Entity("Catgirl", "catgirl.png", 20)]
party[1].skills[0] = Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0, 1)
party[1].skills[1] = Skill.Skill("Berserk", "sword.png", False, 0, 0, 0, 200, 0, 200, 0, 0, 0, 0, 0, 0, "Physical", 0, 1)
party[1].skills[2] = Skill.Skill("Spell of Healing", "wand.png", False, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Physical", 150, 1)

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
        if (entity.isShowing):
            if (entity.entityType == 0):
                screen.blit(entity.img, (entity.xPosition, entity.yPosition))
            elif (entity.entityType == 1):
                if (entity.shape == "rectangle"):
                    if (entity.isBorder):
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.length), 2)
                    else:
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.length))
                if (entity.shape == "ellipse"):
                    if (entity.isBorder):
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.length), 2)
                    else:
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.length))
            elif (entity.entityType == 3):
                screen.blit(entity.textLabel, entity.textRect)
    pygame.display.flip()
   
def mouseInRegion(mouse, shape, xPosition, yPosition, width, length):
    if (shape == "rectangle"):
        return (xPosition <= mouse[0] <= xPosition+width and yPosition <= mouse[1] <= yPosition+length)
    elif (shape == "ellipse"):
        return ((mouse[0]-(xPosition+width/2))*(mouse[0]-(xPosition+width/2)) + (width/length)*(width/length)*(mouse[1]-(yPosition+length/2))*(mouse[1]-(yPosition+length/2)) < ((width/2)*(width/2)))

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


    catgirlX = screenX/3
    catgirlY = screenY/3
    catgirlSizeX = screenX/3
    catgirlSizeY = 2*screenY/3
    playerHPBarX = catgirlX
    playerHPBarY = catgirlY + catgirlSizeY - screenY/12
    playerHPBarSizeX = catgirlSizeX
    playerHPBarSizeY = screenY/25
    playerHPBarBorderWidthX = playerHPBarSizeY/2
    playerHPBarBorderWidthY = playerHPBarSizeY/2
    playerManaBarX = catgirlX
    playerManaBarY = playerHPBarY - 2*playerHPBarSizeY
    playerManaBarSizeX = 3*catgirlSizeX/4
    playerManaBarSizeY = screenY/25
    exitButtonX = 11*screenX/16
    exitButtonY = 5*screenY/6
    glossaryButtonX = 11*screenX/16
    glossaryButtonY = 4*screenY/6
    bagButtonX = screenX/16
    bagButtonY = 5*screenY/6
    skillButtonX = screenX/16
    skillButtonY = 4*screenY/6
    buttonSizeX = 4*screenX/16
    buttonSizeY = screenY/8
    skillSizeX = buttonSizeX/3
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
            if (party[activeCharacter-1].skills[skillSelected].singleTarget):
                enemySelectionShowing = True
                for entity in visualEntities:
                    if ("Enemy Selection" in entity.tags):
                        entity.isShowing = True
            else: 
                party[activeCharacter-1].useSkill(enemies[0], enemies, skillSelected)
                updateEnemies()
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
        if enemySelectionShowing:
            party[activeCharacter-1].useSkill(enemies[enemySelected], enemies, skillSelected)
            party[activeCharacter-1].hasActed = True
            updateEnemies()
            for entity in visualEntities:
                if (("Enemy Selection" in entity.tags) or ("Skill Selection" in entity.tags)):
                    entity.isShowing = False
            skillsShowing = False
            enemySelectionShowing = False

    def updateEnemies():
        nonlocal enemies
        global visualEntities
        global party
        enemyY = screenY/20
        enemySizeX = screenX/9
        enemySizeY = screenY/5
        HPBarY = enemyY + enemySizeY + screenY/100
        HPBarSizeX = enemySizeX
        HPBarSizeY = screenY/35
        HPBarBorderWidthX = HPBarSizeY
        HPBarBorderWidthY = HPBarSizeY
        playerHPBarSizeX = screenX/3
        playerHPBarSizeY = screenY/25
        playerManaBarSizeX = screenX/4

        for item in visualEntities[:]:
            if ("Enemy" in item.tags): visualEntities.remove(item)
            if (item.name == "PlayerHPText"): item.updateText(str(int(party[activeCharacter-1].HP)) + "/" + str(party[activeCharacter-1].maxHP), "mono", 12, "black", None)
            if (item.name == "PlayerHPGreen"): item.width = playerHPBarSizeX*party[activeCharacter-1].HP/party[activeCharacter-1].maxHP
            if (item.name == "PlayerManaText"): item.updateText(str(int(party[activeCharacter-1].mana)) + "/" + str(party[activeCharacter-1].maxMana), "mono", 12, "black", None)
            if (item.name == "PlayerManaBlue"): item.width = playerManaBarSizeX*party[activeCharacter-1].mana/party[activeCharacter-1].maxMana
        for enemy in enemies[:]:
            if (enemy.HP == 0):
                enemies.remove(enemy)

        count = 0
        for enemy in enemies:
            currEnemyX = (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1), 0, True, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy"], enemy.img))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "SelectionButton", 2, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], enemySelectionButtonFunction, (count), "ellipse"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "Selection", 1, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], "white", True, "ellipse"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "HPRed", 1, True, currEnemyX, HPBarY, HPBarSizeX, HPBarSizeY, ["Enemy"], "red", False, "rectangle"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "HPGreen", 1, True, currEnemyX, HPBarY, HPBarSizeX*enemy.HP/enemy.maxHP, HPBarSizeY, ["Enemy"], "green", False, "rectangle"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy" + str(count+1) + "HPBorder", 0, True, currEnemyX, HPBarY, HPBarSizeX, HPBarSizeY, ["Enemy"], "HPBarBorder.png"))
            visualEntities.append(VisualEntity.VisualEntity("Enemy"+ str(count+1) + "HPText", 3, True, currEnemyX, HPBarY, HPBarSizeX/2, HPBarSizeY, ["Enemy"], str(int(enemy.HP)) + "/" + str(enemy.maxHP), "mono", 8, "black", None))
            count = count+1

        skillsShowing = False
        enemySelectionShowing = False


    visualEntities.clear()
    visualEntities.append(VisualEntity.VisualEntity("Background", 0, True, 0, 0, screenX, screenY, ["Background"], "dungeonbackground.png"))
    visualEntities.append(VisualEntity.VisualEntity("Player", 0, True, catgirlX, catgirlY, catgirlSizeX, catgirlSizeY, ["Player"], "catgirl.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPRed", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPGreen", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX*party[activeCharacter-1].HP/party[activeCharacter-1].maxHP, playerHPBarSizeY, ["Player"], "green", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPBorder1", 0, True, playerHPBarX, playerHPBarY-playerHPBarBorderWidthY, playerHPBarSizeX, playerHPBarBorderWidthY, ["Player"], "HPBarBorder1.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPBorder2", 0, True, playerHPBarX-playerHPBarBorderWidthX, playerHPBarY, playerHPBarBorderWidthX, playerHPBarSizeY, ["Player"], "HPBarBorder2.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPBorder3", 0, True, playerHPBarX+playerHPBarSizeX, playerHPBarY, playerHPBarBorderWidthX, playerHPBarSizeY, ["Player"], "HPBarBorder3.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPBorder4", 0, True, playerHPBarX, playerHPBarY+playerHPBarSizeY, playerHPBarSizeX, playerHPBarBorderWidthY, ["Player"], "HPBarBorder4.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerHPText", 3, True, playerHPBarX, playerHPBarY, playerHPBarSizeX/2, playerHPBarSizeY, ["Player"], str(int(party[activeCharacter-1].HP)) + "/" + str(party[activeCharacter-1].maxHP), "mono", 8, "black", None))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaRed", 1, True, playerManaBarX, playerManaBarY, playerManaBarSizeX, playerManaBarSizeY, ["Player"], "red", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaBlue", 1, True, playerManaBarX, playerManaBarY, playerManaBarSizeX*party[activeCharacter-1].mana/party[activeCharacter-1].maxMana, playerManaBarSizeY, ["Player"], "blue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaBorder", 0, True, playerManaBarX, playerManaBarY, playerManaBarSizeX, playerManaBarSizeY, ["Player"], "HPBarBorder.png"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaText", 3, True, playerManaBarX, playerManaBarY, playerManaBarSizeX/2, playerManaBarSizeY, ["Player"], str(int(party[activeCharacter-1].mana)) + "/" + str(party[activeCharacter-1].maxMana), "mono", 8, "black", None))
    visualEntities.append(VisualEntity.VisualEntity("Exit", 0, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], "ExitButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("ExitButton", 2, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], exitButtonFunction, None, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill", 0, True, skillButtonX, skillButtonY, buttonSizeX, buttonSizeY, ["Menu"], "SkillButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("SkillButton", 2, True, skillButtonX, skillButtonY, buttonSizeX, buttonSizeY, ["Menu"], skillButtonFunction, None, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Bag", 0, True, bagButtonX, bagButtonY, buttonSizeX, buttonSizeY, ["Menu"], "BagButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("BagButton", 2, True, bagButtonX, bagButtonY, buttonSizeX, buttonSizeY, ["Menu"], bagButtonFunction, None, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Glossary", 0, True, glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY, ["Menu"], "GlossaryButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("GlossaryButton", 2, True, glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY, ["Menu"], pygame.quit, None, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill1", 0, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[0].img))
    visualEntities.append(VisualEntity.VisualEntity("Skill1Button", 2, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 0, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill1Text", 3, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[0].skillName, "mono", 8, "black", "yellow"))
    visualEntities.append(VisualEntity.VisualEntity("Skill1APText", 3, False, skill1X, skillY+skillSizeY/4, skillSizeX, skillSizeY, ["Skill Selection"], str(party[activeCharacter-1].skills[0].actionPointCost) + " AP", "mono", 12, "black", "yellow"))
    visualEntities.append(VisualEntity.VisualEntity("Skill2", 0, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[1].img))
    visualEntities.append(VisualEntity.VisualEntity("Skill2Button", 2, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 1, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill2Text", 3, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[1].skillName, "mono", 8, "black", "yellow"))
    visualEntities.append(VisualEntity.VisualEntity("Skill2APText", 3, False, skill2X, skillY+skillSizeY/4, skillSizeX, skillSizeY, ["Skill Selection"], str(party[activeCharacter-1].skills[1].actionPointCost) + " AP", "mono", 12, "black", "yellow"))
    visualEntities.append(VisualEntity.VisualEntity("Skill3", 0, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[2].img))
    visualEntities.append(VisualEntity.VisualEntity("Skill3Button", 2, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 2, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Skill3Text", 3, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], party[activeCharacter-1].skills[2].skillName, "mono", 8, "black", "yellow"))
    visualEntities.append(VisualEntity.VisualEntity("Skill3APText", 3, False, skill3X, skillY+skillSizeY/4, skillSizeX, skillSizeY, ["Skill Selection"], str(party[activeCharacter-1].skills[2].actionPointCost) + " AP", "mono", 12, "black", "yellow"))
    updateEnemies()

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


        if (party[activeCharacter-1].hasActed): 
            for enemy in enemies:
                enemy.useSkill(party[activeCharacter-1], enemies, 0)
            party[activeCharacter-1].hasActed = False
            updateEnemies()
              
        if (party[activeCharacter-1].HP == 0 or len(enemies) == 0):
            party[activeCharacter-1].HP = party[activeCharacter-1].maxHP
            party[activeCharacter-1].mana = party[activeCharacter-1].maxMana
            enemies = [Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30)), Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30))]
            updateEnemies()
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
            if (item.name == "PlayerHPText"): item.updateText("HP: " + str(int(party[0].maxHP)), "mono", 11, "black", None)
            if (item.name == "PlayerManaText"): item.updateText("Mana: " + str(int(party[0].maxMana)), "mono", 11, "black", None)
            if (item.name == "PlayerMagicText"): item.updateText("Magic Strength: " + str(int(party[0].magic)), "mono", 11, "black", None)
            if (item.name == "PlayerATKText"): item.updateText("ATK: " + str(int(party[0].ATK)), "mono", 11, "black", None)
            if (item.name == "PlayerDEFText"): item.updateText("DEF: " + str(int(party[0].DEF)), "mono", 11, "black", None)

    visualEntities.clear()
    visualEntities.append(VisualEntity.VisualEntity("Background", 0, True, 0, 0, screenX, screenY, ["Background"], "inventorybackground.png"))
    visualEntities.append(VisualEntity.VisualEntity("Player", 0, True, catgirlX, catgirlY, catgirlSizeX, catgirlSizeY, ["Player"], "catgirl.png"))
    visualEntities.append(VisualEntity.VisualEntity("HelmetBackground", 1, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Helmet", 0, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], party[0].helmet.img))
    visualEntities.append(VisualEntity.VisualEntity("ChestplateBackground", 1, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Chestplate", 0, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate"], party[0].chestplate.img))
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

    visualEntities.append(VisualEntity.VisualEntity("PlayerHPText", 3, True, statX, stat1Y, itemSizeX, itemSizeY, ["Stat"], "HP: " + str(int(party[0].maxHP)), "mono", 11, "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaText", 3, True, statX, stat2Y, itemSizeX, itemSizeY, ["Stat"], "Mana: " + str(int(party[0].maxMana)), "mono", 11, "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerMagicText", 3, True, statX, stat3Y, itemSizeX, itemSizeY, ["Stat"], "Magic Strength: " + str(int(party[0].magic)), "mono", 11, "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerATKText", 3, True, statX, stat4Y, itemSizeX, itemSizeY, ["Stat"], "ATK: " + str(int(party[0].ATK)), "mono", 11, "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerDEFText", 3, True, statX, stat5Y, itemSizeX, itemSizeY, ["Stat"], "DEF: " + str(int(party[0].DEF)), "mono", 11, "black", "green"))
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