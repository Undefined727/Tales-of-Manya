import pygame, random, Entity, Skill

pygame.init()
pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('catgirl-icon.jpg'))



# Set up the drawing window
screenX = 960
screenY = 600
screen = pygame.display.set_mode([screenX, screenY])
visualEntities = []

# Initialize Screen Object Positions
enemy1X = screenX/9
enemy2X = 3*screenX/9
enemy3X = 5*screenX/9
enemy4X = 7*screenX/9
enemyY = screenY/20
enemySizeX = screenX/9
enemySizeY = screenY/5
HPBarY = enemyY + enemySizeY + screenY/100
HPBarSizeX = enemySizeX
HPBarSizeY = screenY/35
HPBarBorderWidthX = HPBarSizeY
HPBarBorderWidthY = HPBarSizeY
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
playerSkillPointSizeX = playerHPBarSizeX/16
playerSkillPointSizeY = playerHPBarSizeX/16
playerSkillPoint1X = playerManaBarX + playerManaBarSizeX + (playerHPBarSizeX/4 - 3*playerSkillPointSizeX)/4
playerSkillPoint2X = playerSkillPoint1X + playerSkillPointSizeX + (playerHPBarSizeX/4 - 3*playerSkillPointSizeX)/4
playerSkillPoint3X = playerSkillPoint2X + playerSkillPointSizeX + (playerHPBarSizeX/4 - 3*playerSkillPointSizeX)/4
playerSkillPointY = playerManaBarY + (playerManaBarSizeY - playerSkillPointSizeY)/2


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






class VisualEntity:
    name = "Default_Name"
    isShowing = True
    # Image = 0, Drawing = 1, Button = 2, Text = 3
    entityType = 0
    # Example tags: "Enemy", "Skill"
    tags = []
    img = None
    xPosition = 0
    yPosition = 0
    width = 0
    length = 0
    shape = "rectangle"
    color = None
    func = None
    args = None
    isBorder = False
    textLabel = None
    textRect = None
    
    #Args listings are formatted as follows; Image: imgPath. Drawing: color, isBorder, shape. Button: func, args, shape. Text: text, font, fontSize, fontColor, highlightColor
    def __init__(self, name, entityType, isShowing, xPosition, yPosition, width, length, tags, *args):
        self.name = name
        self.entityType = entityType
        self.isShowing = isShowing
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.width = width
        self.length = length
        self.tags = tags

        if (entityType == 0):
            self.img = pygame.image.load(args[0])
            self.img = pygame.transform.scale(self.img, (self.width, self.length))
        elif (entityType == 1):
            self.color = args[0]
            self.isBorder = args[1]
            self.shape = args[2]
        elif (entityType == 2):
            self.func = args[0]
            self.args = args[1]
            self.shape = args[2]
        else: self.updateText(args[0], args[1], args[2], args[3], args[4])
        
    def updateText(self, text, font, fontSize, fontColor, highlightColor):
        textFont = pygame.font.SysFont(font, fontSize)
        if (highlightColor != None):
            self.textLabel = textFont.render(text, True, fontColor, highlightColor)
        else:
            self.textLabel = textFont.render(text, False, fontColor)
        self.textRect = self.textLabel.get_rect()
        self.textRect.center = (self.xPosition + self.width/2, self.yPosition + self.length/2)
   
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
   

skillsShowing = False
enemySelectionShowing = False


# Temporary Manual Character Creation
enemies = []


Player = Entity.Entity("Catgirl", "catgirl.png", 20)
Player.skills[0] = Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0, 1)
Player.skills[1] = Skill.Skill("Berserk", "sword.png", False, 0, 0, 0, 200, 0, 200, 0, 0, 0, 0, 0, 0, "Physical", 0, 1)
Player.skills[2] = Skill.Skill("Spell of Healing", "wand.png", False, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Physical", 150, 1)
skillSelected = 0
actionPoints = 3






def mouseInRegion(mouse, shape, xPosition, yPosition, width, length):
    if (shape == "rectangle"):
        return (xPosition <= mouse[0] <= xPosition+width and yPosition <= mouse[1] <= yPosition+length)
    elif (shape == "ellipse"):
        return ((mouse[0]-(xPosition+width/2))*(mouse[0]-(xPosition+width/2)) + (width/length)*(width/length)*(mouse[1]-(yPosition+length/2))*(mouse[1]-(yPosition+length/2)) < ((width/2)*(width/2)))

# Is called when an enemy dies or something, handles drops and buttons and sprites
def updateEnemies():
    global enemies
    global visualEntities
    global Player
    global playerHPBarSizeX
    for item in visualEntities[:]:
        if ("Enemy" in item.tags): visualEntities.remove(item)
        if (item.name == "PlayerHPText"): item.updateText(str(int(Player.HP)) + "/" + str(Player.maxHP), "mono", 12, "black", None)
        if (item.name == "PlayerHPGreen"): item.width = playerHPBarSizeX*Player.HP/Player.maxHP
        if (item.name == "PlayerManaText"): item.updateText(str(int(Player.mana)) + "/" + str(Player.maxMana), "mono", 12, "black", None)
        if (item.name == "PlayerManaBlue"): item.width = playerManaBarSizeX*Player.mana/Player.maxMana
    for enemy in enemies[:]:
        if (enemy.HP == 0):
            enemies.remove(enemy)

    count = 0
    for enemy in enemies:
        currEnemyX = (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2))
        visualEntities.append(VisualEntity("Enemy" + str(count+1), 0, True, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy"], enemy.img))
        visualEntities.append(VisualEntity("Enemy" + str(count+1) + "SelectionButton", 2, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], enemySelectionButtonFunction, (count), "ellipse"))
        visualEntities.append(VisualEntity("Enemy" + str(count+1) + "Selection", 1, False, currEnemyX, enemyY, enemySizeX, enemySizeY, ["Enemy", "Enemy Selection"], "white", True, "ellipse"))
        visualEntities.append(VisualEntity("Enemy" + str(count+1) + "HPRed", 1, True, currEnemyX, HPBarY, HPBarSizeX, HPBarSizeY, ["Enemy"], "red", False, "rectangle"))
        visualEntities.append(VisualEntity("Enemy" + str(count+1) + "HPGreen", 1, True, currEnemyX, HPBarY, HPBarSizeX*enemy.HP/enemy.maxHP, HPBarSizeY, ["Enemy"], "green", False, "rectangle"))
        visualEntities.append(VisualEntity("Enemy" + str(count+1) + "HPBorder", 0, True, currEnemyX, HPBarY, HPBarSizeX, HPBarSizeY, ["Enemy"], "HPBarBorder.png"))
        visualEntities.append(VisualEntity("Enemy"+ str(count+1) + "HPText", 3, True, currEnemyX, HPBarY, HPBarSizeX/2, HPBarSizeY, ["Enemy"], str(int(enemy.HP)) + "/" + str(enemy.maxHP), "mono", 8, "black", None))
        count = count+1

# Button Functions
def skillButtonFunction(*args):
    global skillsShowing
    global visualEntities
    skillsShowing = not skillsShowing
    for entity in visualEntities:
        if ("Skill Selection" in entity.tags):
            entity.isShowing = not entity.isShowing

def individualSkillButtonFunction(*args):
    global skillsShowing
    skillSelected = args[0]
    global visualEntities
    global Player
    global enemies
    global enemySelectionShowing
    global actionPoints
    if (skillsShowing and (Player.skills[skillSelected].actionPointCost <= actionPoints) and (Player.skills[skillSelected].manaCost <= Player.mana)): 
        if (Player.skills[skillSelected].singleTarget):
            enemySelectionShowing = True
            for entity in visualEntities:
                if ("Enemy Selection" in entity.tags):
                    entity.isShowing = True
        else: 
            Player.useSkill(enemies[0], enemies, skillSelected)
            actionPoints = actionPoints - Player.skills[skillSelected].actionPointCost
            for entity in visualEntities:
                if(actionPoints < 3 and entity.name == "PlayerSkillPoint3"): entity.isBorder = True
                if(actionPoints < 2 and entity.name == "PlayerSkillPoint2"): entity.isBorder = True
                if(actionPoints < 1 and entity.name == "PlayerSkillPoint1"): entity.isBorder = True
            updateEnemies()
            for entity in visualEntities:
                if ("Skill Selection" in entity.tags):
                    entity.isShowing = False
            skillsShowing = False

def enemySelectionButtonFunction(*args):
    global skillSelected
    enemySelected = args[0]
    global visualEntities
    global enemies
    global enemySelectionShowing
    global skillsShowing
    global actionPoints
    if enemySelectionShowing:
        Player.useSkill(enemies[enemySelected], enemies, skillSelected)
        actionPoints = actionPoints - Player.skills[skillSelected].actionPointCost
        for entity in visualEntities:
            if(actionPoints < 3 and entity.name == "PlayerSkillPoint3"): entity.isBorder = True
            if(actionPoints < 2 and entity.name == "PlayerSkillPoint2"): entity.isBorder = True
            if(actionPoints < 1 and entity.name == "PlayerSkillPoint1"): entity.isBorder = True
        updateEnemies()
        for entity in visualEntities:
            if (("Enemy Selection" in entity.tags) or ("Skill Selection" in entity.tags)):
                entity.isShowing = False
        skillsShowing = False
        enemySelectionShowing = False












# This would normally be called from a file, this is where the buttons/visuals for the scene are imported into the program
#y = json.loads(open("combat.json"))
#file = open("combat.txt", "r")
#for line in file:
#  lineread = line
 # visualEntities.append(VisualEntity(*lineread))

#for obj in visualEntities:
#    print(obj.name)

visualEntities.append(VisualEntity("Background", 0, True, 0, 0, screenX, screenY, ["Background"], "dungeonbackground.png"))
visualEntities.append(VisualEntity("Player", 0, True, catgirlX, catgirlY, catgirlSizeX, catgirlSizeY, ["Player"], "catgirl.png"))
visualEntities.append(VisualEntity("PlayerHPRed", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, ["Player"], "red", False, "rectangle"))
visualEntities.append(VisualEntity("PlayerHPGreen", 1, True, playerHPBarX, playerHPBarY, playerHPBarSizeX*Player.HP/Player.maxHP, playerHPBarSizeY, ["Player"], "green", False, "rectangle"))
visualEntities.append(VisualEntity("PlayerHPBorder1", 0, True, playerHPBarX, playerHPBarY-playerHPBarBorderWidthY, playerHPBarSizeX, playerHPBarBorderWidthY, ["Player"], "HPBarBorder1.png"))
visualEntities.append(VisualEntity("PlayerHPBorder2", 0, True, playerHPBarX-playerHPBarBorderWidthX, playerHPBarY, playerHPBarBorderWidthX, playerHPBarSizeY, ["Player"], "HPBarBorder2.png"))
visualEntities.append(VisualEntity("PlayerHPBorder3", 0, True, playerHPBarX+playerHPBarSizeX, playerHPBarY, playerHPBarBorderWidthX, playerHPBarSizeY, ["Player"], "HPBarBorder3.png"))
visualEntities.append(VisualEntity("PlayerHPBorder4", 0, True, playerHPBarX, playerHPBarY+playerHPBarSizeY, playerHPBarSizeX, playerHPBarBorderWidthY, ["Player"], "HPBarBorder4.png"))
visualEntities.append(VisualEntity("PlayerHPText", 3, True, playerHPBarX, playerHPBarY, playerHPBarSizeX/2, playerHPBarSizeY, ["Player"], str(int(Player.HP)) + "/" + str(Player.maxHP), "mono", 8, "black", None))
visualEntities.append(VisualEntity("PlayerManaRed", 1, True, playerManaBarX, playerManaBarY, playerManaBarSizeX, playerManaBarSizeY, ["Player"], "red", False, "rectangle"))
visualEntities.append(VisualEntity("PlayerManaBlue", 1, True, playerManaBarX, playerManaBarY, playerManaBarSizeX*Player.mana/Player.maxMana, playerManaBarSizeY, ["Player"], "blue", False, "rectangle"))
visualEntities.append(VisualEntity("PlayerManaBorder", 0, True, playerManaBarX, playerManaBarY, playerManaBarSizeX, playerManaBarSizeY, ["Player"], "HPBarBorder.png"))
visualEntities.append(VisualEntity("PlayerManaText", 3, True, playerManaBarX, playerManaBarY, playerManaBarSizeX/2, playerManaBarSizeY, ["Player"], str(int(Player.mana)) + "/" + str(Player.maxMana), "mono", 8, "black", None))
visualEntities.append(VisualEntity("PlayerSkillPoint1", 1, True, playerSkillPoint1X, playerSkillPointY, playerSkillPointSizeX, playerSkillPointSizeY, ["Player", "Skill Point"], "white", False, "ellipse"))
visualEntities.append(VisualEntity("PlayerSkillPoint2", 1, True, playerSkillPoint2X, playerSkillPointY, playerSkillPointSizeX, playerSkillPointSizeY, ["Player", "Skill Point"], "white", False, "ellipse"))
visualEntities.append(VisualEntity("PlayerSkillPoint3", 1, True, playerSkillPoint3X, playerSkillPointY, playerSkillPointSizeX, playerSkillPointSizeY, ["Player", "Skill Point"], "white", False, "ellipse"))
visualEntities.append(VisualEntity("Exit", 0, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], "ExitButton.png"))
visualEntities.append(VisualEntity("ExitButton", 2, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], pygame.quit, None, "rectangle"))
visualEntities.append(VisualEntity("Skill", 0, True, skillButtonX, skillButtonY, buttonSizeX, buttonSizeY, ["Menu"], "SkillButton.png"))
visualEntities.append(VisualEntity("SkillButton", 2, True, skillButtonX, skillButtonY, buttonSizeX, buttonSizeY, ["Menu"], skillButtonFunction, None, "rectangle"))
visualEntities.append(VisualEntity("Bag", 0, True, bagButtonX, bagButtonY, buttonSizeX, buttonSizeY, ["Menu"], "BagButton.png"))
visualEntities.append(VisualEntity("BagButton", 2, True, bagButtonX, bagButtonY, buttonSizeX, buttonSizeY, ["Menu"], pygame.quit, None, "rectangle"))
visualEntities.append(VisualEntity("Glossary", 0, True, glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY, ["Menu"], "GlossaryButton.png"))
visualEntities.append(VisualEntity("GlossaryButton", 2, True, glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY, ["Menu"], pygame.quit, None, "rectangle"))
visualEntities.append(VisualEntity("Skill1", 0, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], Player.skills[0].img))
visualEntities.append(VisualEntity("Skill1Button", 2, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 0, "rectangle"))
visualEntities.append(VisualEntity("Skill1Text", 3, False, skill1X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], Player.skills[0].skillName, "mono", 8, "black", "yellow"))
visualEntities.append(VisualEntity("Skill1APText", 3, False, skill1X, skillY+skillSizeY/4, skillSizeX, skillSizeY, ["Skill Selection"], str(Player.skills[0].actionPointCost) + " AP", "mono", 12, "black", "yellow"))
visualEntities.append(VisualEntity("Skill2", 0, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], Player.skills[1].img))
visualEntities.append(VisualEntity("Skill2Button", 2, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 1, "rectangle"))
visualEntities.append(VisualEntity("Skill2Text", 3, False, skill2X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], Player.skills[1].skillName, "mono", 8, "black", "yellow"))
visualEntities.append(VisualEntity("Skill2APText", 3, False, skill2X, skillY+skillSizeY/4, skillSizeX, skillSizeY, ["Skill Selection"], str(Player.skills[1].actionPointCost) + " AP", "mono", 12, "black", "yellow"))
visualEntities.append(VisualEntity("Skill3", 0, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], Player.skills[2].img))
visualEntities.append(VisualEntity("Skill3Button", 2, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], individualSkillButtonFunction, 2, "rectangle"))
visualEntities.append(VisualEntity("Skill3Text", 3, False, skill3X, skillY, skillSizeX, skillSizeY, ["Skill Selection"], Player.skills[2].skillName, "mono", 8, "black", "yellow"))
visualEntities.append(VisualEntity("Skill3APText", 3, False, skill3X, skillY+skillSizeY/4, skillSizeX, skillSizeY, ["Skill Selection"], str(Player.skills[2].actionPointCost) + " AP", "mono", 12, "black", "yellow"))


enemies = [Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30)), Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30))]
updateEnemies()

while True:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for entity in visualEntities:
                if (entity.entityType == 2):
                    if mouseInRegion(mouse, entity.shape, entity.xPosition, entity.yPosition, entity.width, entity.length):
                        entity.func(entity.args)



    if (actionPoints == 0): 
        for enemy in enemies:
            enemy.useSkill(Player, enemies, 0)
        actionPoints = 3
        for entity in visualEntities:
            if("Skill Point" in entity.tags): entity.isBorder = False
        updateEnemies()
              
    if (Player.HP == 0 or len(enemies) == 0):
        Player.HP = Player.maxHP
        Player.mana = Player.maxMana
        enemies = [Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30)), Entity.Entity("Wizard", "wizard.png", random.randint(5, 30)), Entity.Entity("Frog", "frog.png", random.randint(5, 30))]
        updateEnemies()
        actionPoints = 3
        for entity in visualEntities:
            if("Skill Point" in entity.tags): entity.isBorder = False
    
    refreshScreen()
    

# Done! Time to quit.
pygame.quit()