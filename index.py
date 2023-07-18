import pygame, Entity, Skill, json
pygame.init()

pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('catgirl-icon.jpg'))

# Initialize Screen Object Positions

screenX = 960
screenY = 600


enemy1X = screenX/9
enemy2X = 3*screenX/9
enemy3X = 5*screenX/9
enemy4X = 7*screenX/9
enemyY = screenY/20

enemySizeX = screenX/9
enemySizeY = screenY/5


HPBar1X = enemy1X
HPBar2X = enemy2X
HPBar3X = enemy3X
HPBar4X = enemy4X

HPBarY = enemyY + enemySizeY + screenY/100

HPBarSizeX = enemySizeX
HPBarSizeY = screenY/35


catgirlX = screenX/3
catgirlY = screenY/3

catgirlSizeX = screenX/3
catgirlSizeY = 2*screenY/3

playerHPBarX = catgirlX
playerHPBarY = catgirlY + catgirlSizeY - screenY/10

playerHPBarSizeX = catgirlSizeX
playerHPBarSizeY = screenY/25


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



# Set up the drawing window
screen = pygame.display.set_mode([screenX, screenY])

def mouseInRegion(mouse, shape, xPosition, yPosition, width, length):
    if (shape == "rectangle"):
        return (xPosition <= mouse[0] <= xPosition+width and yPosition <= mouse[1] <= yPosition+length)
    elif (shape == "ellipse"):
        return ((mouse[0]-(xPosition+width/2))*(mouse[0]-(xPosition+width/2)) + (width/length)*(width/length)*(mouse[1]-(yPosition+length/2))*(mouse[1]-(yPosition+length/2)) < ((width/2)*(width/2)))

class VisualEntity:
    name = "Default_Name"
    # How the button is analyzed: 0 = not a button type, 1 = Menu Button, 2 = Enemy Selection Button
    # Example tags: "Enemy", "Skill"
    itemTags = []
    isButton = False

    imgPath = "catgirl.png"
    img = None
    xPosition = 0
    yPosition = 0
    width = 0
    length = 0
    shape = "rectangle"
    color = None
    func = None
    args = None
    border = False
    text = None
    textX = xPosition
    textY = yPosition
    font = None
    fontSize = 8
    fontColor = "black"
    highlightColor = None
    isShowing = True
    
    def __init__(self, *args):
        # Everything
        if (len(args) == 21):
            self.name = args[0]
            self.itemType = args[1]
            self.isButton = args[2]
            self.xPosition = args[3]
            self.yPosition = args[4]
            self.width = args[5]
            self.length = args[6]
            self.shape = args[7]
            self.color = args[8]
            self.func = args[9]
            self.args = args[10]
            self.imgPath = args[11]
            self.border = args[12]
            self.text = args[13]
            self.textX = args[14]
            self.textY = args[15]
            self.font = args[16]
            self.fontSize = args[17]
            self.fontColor = args[18]
            self.highlightColor = args[19]
            self.isShowing = args[20]

            if (self.imgPath != None):
                self.img = pygame.image.load(self.imgPath)
                self.img = pygame.transform.scale(self.img, (self.width, self.length))
        # No Text
        if (len(args) == 14):
            self.name = args[0]
            self.itemType = args[1]
            self.isButton = args[2]
            self.xPosition = args[3]
            self.yPosition = args[4]
            self.width = args[5]
            self.length = args[6]
            self.shape = args[7]
            self.color = args[8]
            self.func = args[9]
            self.args = args[10]
            self.imgPath = args[11]
            self.border = args[12]
            self.isShowing = args[13]

            if (self.imgPath != None):
                self.img = pygame.image.load(self.imgPath)
                self.img = pygame.transform.scale(self.img, (self.width, self.length))
        # Button Image
        # Order is the following: name, xPosition, yPosition, width, length, imgPath
        if (len(args) == 11):
            self.name = args[0]
            self.itemType = args[1]
            self.isButton = args[2]
            self.xPosition = args[3]
            self.yPosition = args[4]
            self.width = args[5]
            self.length = args[6]
            self.imgPath = args[7]
            self.func = args[8]
            self.args = args[9]
            self.isShowing = args[10]

            if (self.imgPath != None):
                self.img = pygame.image.load(self.imgPath)
                self.img = pygame.transform.scale(self.img, (self.width, self.length))
        #Image
        if (len(args) == 8):
            self.name = args[0]
            self.itemType = args[1]
            self.xPosition = args[2]
            self.yPosition = args[3]
            self.width = args[4]
            self.length = args[5]
            self.imgPath = args[6]
            self.isShowing = args[7]

            if (self.imgPath != None):
                self.img = pygame.image.load(self.imgPath)
                self.img = pygame.transform.scale(self.img, (self.width, self.length))
        
visualEntities = []        

skillsShowing = False
enemySelectionShowing = False


# Temporary Manual Character Creation
enemies = [Entity.Entity("Wizard", "wizard.png", 10), Entity.Entity("Frog", "frog.png", 30), Entity.Entity("Wizard", "wizard.png", 10), Entity.Entity("Frog", "frog.png", 10)]


Player = Entity.Entity("Catgirl", "catgirl.png", 20)
Player.skills[0] = Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0)
Player.skills[1] = Skill.Skill("Berserk", "sword.png", False, 0, 0, 0, 200, 0, 200, 0, 0, 0, 0, 0, 0, "Physical", 0)
Player.skills[2] = Skill.Skill("Spell of Healing", "wand.png", False, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Physical", 0)
skillSelected = 0



# Button Functions
def skillButtonFunction(*args):
    global skillsShowing
    global visualEntities
    skillsShowing = not skillsShowing
    for entity in visualEntities:
        if (entity.itemType == 2):
            entity.isShowing = not entity.isShowing

def individualSkillButtonFunction(*args):
    global skillsShowing
    skillSelected = args[0]
    global visualEntities
    global Player
    global enemies
    global enemySelectionShowing
    if skillsShowing: 
        if (Player.skills[skillSelected].singleTarget):
            enemySelectionShowing = True
        else: 
            Player.useSkill(enemies[0], enemies, skillSelected)
            updateEnemies()
            for entity in visualEntities:
                if (entity.itemType == 2):
                    entity.isShowing = False
            skillsShowing = False

def enemySelectionButtonFunction(*args):
    global skillSelected
    enemySelected = args[0]
    global visualEntities
    global enemies
    global enemySelectionShowing
    global skillsShowing
    if enemySelectionShowing:
        Player.useSkill(enemies[enemySelected], enemies, skillSelected)
        updateEnemies()
        for entity in visualEntities:
            if (entity.itemType == 2):
                entity.isShowing = False
        skillsShowing = False
        enemySelectionShowing = False


def RefreshScreen(enemies, Player, skillsShowing, enemySelectionShowing):
    # Fill the background
    global visualEntities
    for entity in visualEntities:
        if (entity.isShowing):
            if (entity.img != None):
                screen.blit(entity.img, (entity.xPosition, entity.yPosition))
            if (entity.color != None):
                if (entity.shape == "rectangle"):
                    if (entity.border):
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.length), 2)
                    else:
                        pygame.draw.rect(screen,entity.color,pygame.Rect(entity.xPosition,entity.yPosition,entity.width,entity.length))
                if (entity.shape == "ellipse"):
                    if (entity.border):
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.length), 2)
                    else:
                        pygame.draw.ellipse(screen, entity.color, (entity.xPosition, entity.yPosition, entity.width, entity.length))
            if (entity.text != None):
                textFont = pygame.font.SysFont(entity.font, entity.fontSize)
                if (entity.highlightColor != "null"):
                    label = textFont.render(entity.text, True, entity.fontColor, entity.highlightColor)
                else:
                    label = textFont.render(entity.text, False, entity.fontColor)
                labelRect = label.get_rect()
                labelRect.center = (entity.textX, entity.textY)
                screen.blit(label, labelRect)





# Is called when an enemy dies or something, handles drops and buttons and sprites
def updateEnemies():
    count = 0
    global enemies
    global visualEntities
    global Player
    for button in visualEntities:
        if (button.itemType == 3): visualEntities.remove(button)
    for enemy in enemies:
        visualEntities.append(VisualEntity("Enemy" + str(count+1), 3, True, (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), enemyY, enemySizeX, enemySizeY, enemy.img, enemySelectionButtonFunction, count, True))
        visualEntities.append(VisualEntity("Enemy"+ str(count+1) + "HPRed", 3, False, (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), HPBarY, HPBarSizeX, HPBarSizeY, "rectangle", "red", None, None, None, False, True))
        visualEntities.append(VisualEntity("Enemy"+ str(count+1) + "HPGreen", 3, False, (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), HPBarY, HPBarSizeX*enemy.HP/enemy.maxHP, HPBarSizeY, "rectangle", "green", None, None, None, False, True))
        visualEntities.append(VisualEntity("Enemy"+ str(count+1) + "HPBorderText", 3, False, (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), HPBarY, HPBarSizeX, HPBarSizeY, "rectangle", "black", None, None, None, True, str(int(enemy.HP)) + "/" + str(enemy.maxHP), (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)) + HPBarSizeX/4, HPBarY + HPBarSizeY/2, "mono", 8, "black", None, True))
        count = count+1
    visualEntities.append(VisualEntity("PlayerHPRed", 3, False, playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, "rectangle", "red", None, None, None, False, True))
    visualEntities.append(VisualEntity("PlayerHPGreen", 3, False, playerHPBarX, playerHPBarY, playerHPBarSizeX*Player.HP/Player.maxHP, playerHPBarSizeY, "rectangle", "green", None, None, None, False, True))
    visualEntities.append(VisualEntity("PlayerHPBorderText", 3, False, playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, "rectangle", "black", None, None, None, True, str(int(Player.HP)) + "/" + str(Player.maxHP), playerHPBarX + playerHPBarSizeX/5, playerHPBarY + playerHPBarSizeY/2, "mono", 12, "black", None, True))




# This would normally be called from a file, this is where the buttons/visuals for the scene are imported into the program
#y = json.loads(open("combat.json"))
#file = open("combat.txt", "r")
#for line in file:
#  lineread = line
 # visualEntities.append(VisualEntity(*lineread))

#for obj in visualEntities:
#    print(obj.name)
visualEntities.append(VisualEntity("Background", 0, 0, 0, screenX, screenY, "dungeonbackground.png", True))
visualEntities.append(VisualEntity("Player", 0, catgirlX, catgirlY, catgirlSizeX, catgirlSizeY, "catgirl.png", True))
visualEntities.append(VisualEntity("Exit", 1, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, "ExitButton.png", pygame.quit, None, True))
visualEntities.append(VisualEntity("Skill", 1, True, skillButtonX, skillButtonY, buttonSizeX, buttonSizeY, "SkillButton.png", skillButtonFunction, (), True))
visualEntities.append(VisualEntity("Bag", 1, True, bagButtonX, bagButtonY, buttonSizeX, buttonSizeY, "BagButton.png", pygame.quit, None, True))
visualEntities.append(VisualEntity("Glossary", 1, True, glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY, "GlossaryButton.png", pygame.quit, None, True))
visualEntities.append(VisualEntity("Skill1", 2, True, skill1X, skillY, skillSizeX, skillSizeY, Player.skills[0].img, individualSkillButtonFunction, 0, False))
visualEntities.append(VisualEntity("Skill2", 2, True, skill2X, skillY, skillSizeX, skillSizeY, Player.skills[1].img, individualSkillButtonFunction, 1, False))
visualEntities.append(VisualEntity("Skill3", 2, True, skill3X, skillY, skillSizeX, skillSizeY, Player.skills[2].img, individualSkillButtonFunction, 2, False))
updateEnemies()




while True:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in visualEntities:
                if (button.isButton):
                    if mouseInRegion(mouse, button.shape, button.xPosition, button.yPosition, button.width, button.length):
                        button.func(button.args)



              
    
    
    RefreshScreen(enemies, Player, skillsShowing, enemySelectionShowing)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()