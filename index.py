import pygame, Entity, Skill
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



# Initialize Visual Object Details

font = pygame.font.SysFont('mono', 32)


exitButtonLabel = font.render('Exit', False, (0, 0, 0))
exitButtonLabelRect = exitButtonLabel.get_rect()
exitButtonLabelRect.center = (exitButtonX + buttonSizeX/2, exitButtonY + buttonSizeY/2)

skillButtonLabel = font.render('Skill', False, (0, 0, 0))
skillButtonLabelRect = skillButtonLabel.get_rect()
skillButtonLabelRect.center = (skillButtonX + buttonSizeX/2, skillButtonY + buttonSizeY/2)

bagButtonLabel = font.render('Bag', False, (0, 0, 0))
bagButtonLabelRect = bagButtonLabel.get_rect()
bagButtonLabelRect.center = (bagButtonX + buttonSizeX/2, bagButtonY + buttonSizeY/2)

glossaryButtonLabel = font.render('Glossary', False, (0, 0, 0))
glossaryButtonLabelRect = glossaryButtonLabel.get_rect()
glossaryButtonLabelRect.center = (glossaryButtonX + buttonSizeX/2, glossaryButtonY + buttonSizeY/2)


swordImg = pygame.image.load("sword.png")
swordImg = pygame.transform.scale(swordImg, (skillSizeX, skillSizeY))




# Set up the drawing window
screen = pygame.display.set_mode([screenX, screenY])

#imgPath = "null" for no image, shapes are "null", "rectangle" and "ellipse", if border is True then it will be a border, if font is "null" no text
def visualEntity(imgPath, xPosition, yPosition, width, length, shape, color, border, text, textX, textY, font, fontSize, fontColor, highlightColor):
    if (shape == "rectangle"):
        if (border):
            pygame.draw.rect(screen,color,pygame.Rect(xPosition,yPosition,width,length), 2)
        else:
            pygame.draw.rect(screen,color,pygame.Rect(xPosition,yPosition,width,length))
    if (shape == "ellipse"):
        if (border):
            pygame.draw.ellipse(screen, color, (xPosition, yPosition, width, length), 2)
        else:
            pygame.draw.ellipse(screen, color, (xPosition, yPosition, width, length))
    if (imgPath != "null"):
        img = pygame.image.load(imgPath)
        img = pygame.transform.scale(img, (width, length))
        screen.blit(img, (xPosition, yPosition))
    if (font != "null"):
        textFont = pygame.font.SysFont(font, fontSize)
        if (highlightColor != "null"):
            label = textFont.render(text, True, fontColor, highlightColor)
        else:
            label = textFont.render(text, False, fontColor)
        labelRect = label.get_rect()
        labelRect.center = (textX, textY)
        screen.blit(label, labelRect)

def mouseInRegion(mouse, shape, xPosition, yPosition, width, length):
    if (shape == "rectangle"):
        return (xPosition <= mouse[0] <= xPosition+width and yPosition <= mouse[1] <= yPosition+length)
    elif (shape == "ellipse"):
        return ((mouse[0]-(xPosition+width/2))*(mouse[0]-(xPosition+width/2)) + (width/length)*(width/length)*(mouse[1]-(yPosition+length/2))*(mouse[1]-(yPosition+length/2)) < ((width/2)*(width/2)))



def RefreshSkillButtons(Player):
    # Add Skill Icons
    visualEntity(Player.skills[0].img, skill1X, skillY, skillSizeX, skillSizeY, "null", "null", False, Player.skills[0].skillName, skill1X + skillSizeX/2, skillY + 2*skillSizeY/3, "mono", 10, (0, 0, 0), "green")
    visualEntity(Player.skills[1].img, skill2X, skillY, skillSizeX, skillSizeY, "null", "null", False, Player.skills[1].skillName, skill2X + skillSizeX/2, skillY + 2*skillSizeY/3, "mono", 10, (0, 0, 0), "green")
    visualEntity(Player.skills[2].img, skill3X, skillY, skillSizeX, skillSizeY, "null", "null", False, Player.skills[2].skillName, skill3X + skillSizeX/2, skillY + 2*skillSizeY/3, "mono", 10, (0, 0, 0), "green")

def RefreshEnemySelection(enemies):
    count = 0
    for enemy in enemies:
        visualEntity("null", (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), enemyY, enemySizeX, enemySizeY, "ellipse", "white", True, "null", 0, 0, "null", 0, (0, 0, 0), "null")
        count = count + 1

def RefreshMenu(enemies, Player):
    # Fill the background
    visualEntity("dungeonbackground.png", 0, 0, screenX, screenY, "null", "null", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")

    # Add Enemies
    count = 0
    for enemy in enemies:
        visualEntity(enemy.img, (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), enemyY, enemySizeX, enemySizeY, "null", "null", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
        visualEntity("null", (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), HPBarY, HPBarSizeX, HPBarSizeY, "rectangle", "red", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
        visualEntity("null", (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), HPBarY, HPBarSizeX*enemy.HP/enemy.maxHP, HPBarSizeY, "rectangle", "green", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
        visualEntity("null", (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), HPBarY, HPBarSizeX, HPBarSizeY, "rectangle", "black", True, str(int(enemy.HP)) + '/' + str(int(enemy.maxHP)), (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)) + HPBarSizeX/3, HPBarY + HPBarSizeY/2, "mono", 10, (0, 0, 0), "null")
        count = count+1


    # Add Player
    visualEntity(Player.img, catgirlX, catgirlY, catgirlSizeX, catgirlSizeY, "null", "null", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")

    #Add Player HP Bar and Label
    visualEntity("null", playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, "rectangle", "red", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
    visualEntity("null", playerHPBarX, playerHPBarY, playerHPBarSizeX*Player.HP/Player.maxHP, playerHPBarSizeY, "rectangle", "green", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
    visualEntity("null", playerHPBarX, playerHPBarY, playerHPBarSizeX, playerHPBarSizeY, "rectangle", "black", True, str(int(Player.HP)) + '/' + str(int(Player.maxHP)), playerHPBarX + playerHPBarSizeX/5, playerHPBarY + playerHPBarSizeY/2, "mono", 16, (0, 0, 0), "null")


    # Add Menu
    visualEntity("null", exitButtonX,exitButtonY,buttonSizeX,buttonSizeY, "rectangle", "white", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
    visualEntity("null", exitButtonX,exitButtonY,buttonSizeX,buttonSizeY, "rectangle", "black", True, "Exit", exitButtonX + buttonSizeX/2, exitButtonY + buttonSizeY/2, "mono", 32, (0, 0, 0), "null")

    visualEntity("null", glossaryButtonX,glossaryButtonY, buttonSizeX,buttonSizeY, "rectangle", "white", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
    visualEntity("null", glossaryButtonX,glossaryButtonY, buttonSizeX,buttonSizeY, "rectangle", "black", True, "Glossary", glossaryButtonX + buttonSizeX/2, glossaryButtonY + buttonSizeY/2, "mono", 32, (0, 0, 0), "null")

    visualEntity("null", bagButtonX,bagButtonY,buttonSizeX,buttonSizeY, "rectangle", "white", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
    visualEntity("null", bagButtonX,bagButtonY,buttonSizeX,buttonSizeY, "rectangle", "black", True, "Bag", bagButtonX + buttonSizeX/2, bagButtonY + buttonSizeY/2, "mono", 32, (0, 0, 0), "null")

    visualEntity("null", skillButtonX,skillButtonY, buttonSizeX,buttonSizeY, "rectangle", "white", False, "null", 0, 0, "null", 0, (0, 0, 0), "null")
    visualEntity("null", skillButtonX,skillButtonY, buttonSizeX,buttonSizeY, "rectangle", "black", True, "Skill", skillButtonX + buttonSizeX/2, skillButtonY + buttonSizeY/2, "mono", 32, (0, 0, 0), "null")


# Temporary Manual Character Creation
enemies = [Entity.Entity("Wizard", "wizard.png", 10), Entity.Entity("Frog", "frog.png", 10), Entity.Entity("Wizard", "wizard.png", 10), Entity.Entity("Frog", "frog.png", 10)]


Player = Entity.Entity("Catgirl", "catgirl.png", 20)
Player.skills[0] = Skill.Skill("Basic Attack", "sword.png", True, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, "Physical", 0)
Player.skills[1] = Skill.Skill("Berserk", "sword.png", False, 0, 0, 0, 200, 0, 200, 0, 0, 0, 0, 0, 0, "Physical", 0)
Player.skills[2] = Skill.Skill("Spell of Healing", "wand.png", False, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "Physical", 0)
skillSelected = 0



skillsShowing = False
enemySelectionShowing = False
while True:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouseInRegion(mouse, "rectangle", exitButtonX, exitButtonY, buttonSizeX, buttonSizeY):
                pygame.quit()
            elif mouseInRegion(mouse, "rectangle", skillButtonX, skillButtonY, buttonSizeX, buttonSizeY):
                skillsShowing = not skillsShowing
            elif mouseInRegion(mouse, "rectangle", bagButtonX, bagButtonY, buttonSizeX, buttonSizeY):
                pygame.quit()
            elif mouseInRegion(mouse, "rectangle", glossaryButtonX, glossaryButtonY, buttonSizeX, buttonSizeY):
                pygame.quit()
            elif mouseInRegion(mouse, "rectangle", skill1X, skillY, skillSizeX, skillSizeY):
                if skillsShowing: 
                    skillSelected = 0
                    if (Player.skills[skillSelected].singleTarget):
                        enemySelectionShowing = True
                    else: Player.useSkill(enemies[0], enemies, skillSelected)
            elif mouseInRegion(mouse, "rectangle", skill2X, skillY, skillSizeX, skillSizeY):
                if skillsShowing: 
                    skillSelected = 1
                    if (Player.skills[skillSelected].singleTarget):
                        enemySelectionShowing = True
                    else: Player.useSkill(enemies[0], enemies, skillSelected)
            elif mouseInRegion(mouse, "rectangle", skill3X, skillY, skillSizeX, skillSizeY):
                if skillsShowing: 
                    skillSelected = 2
                    if (Player.skills[skillSelected].singleTarget):
                        enemySelectionShowing = True
                    else: Player.useSkill(enemies[0], enemies, skillSelected)
            else:
                count = 0
                for enemy in enemies:
                    if mouseInRegion(mouse, "ellipse", (((1.5 + 2*count)*screenX)/(len(enemies)*2+1) - (enemySizeX/2)), enemyY, enemySizeX, enemySizeY):
                        if enemySelectionShowing:
                            Player.useSkill(enemy, enemies, skillSelected)
                            enemySelectionShowing = False
                    count = count+1



              
    
    
    RefreshMenu(enemies, Player)
    if (skillsShowing): RefreshSkillButtons(Player)
    if (enemySelectionShowing): RefreshEnemySelection(enemies)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()