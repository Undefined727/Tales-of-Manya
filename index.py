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
HPBarFont = pygame.font.SysFont('mono', 10)
playerHPBarFont = pygame.font.SysFont('mono', 16)

background = pygame.image.load("dungeonbackground.png")
background = pygame.transform.scale(background, (screenX, screenY))

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

HPBar1Label =  HPBarFont.render('0/10', False, (0, 0, 0))
HPBar1LabelRect = HPBar1Label.get_rect()
HPBar1LabelRect.center = (HPBar1X + HPBarSizeX/5, HPBarY + HPBarSizeY/2)


HPBar2Label =  HPBarFont.render('0/10', False, (0, 0, 0))
HPBar2LabelRect = HPBar2Label.get_rect()
HPBar2LabelRect.center = (HPBar2X + HPBarSizeX/5, HPBarY + HPBarSizeY/2)


HPBar3Label =  HPBarFont.render('0/10', False, (0, 0, 0))
HPBar3LabelRect = HPBar3Label.get_rect()
HPBar3LabelRect.center = (HPBar3X + HPBarSizeX/5, HPBarY + HPBarSizeY/2)

HPBar4Label =  HPBarFont.render('0/10', False, (0, 0, 0))
HPBar4LabelRect = HPBar4Label.get_rect()
HPBar4LabelRect.center = (HPBar4X + HPBarSizeX/5, HPBarY + HPBarSizeY/2)

playerHPBarLabel = playerHPBarFont.render('0/10', False, (0, 0, 0))
playerHPBarLabelRect = playerHPBarLabel.get_rect()
playerHPBarLabelRect.center = (playerHPBarX + playerHPBarSizeX/10, playerHPBarY + playerHPBarSizeY/2)


catgirlImg = pygame.image.load("catgirl.png")
catgirlImg = pygame.transform.scale(catgirlImg, (catgirlSizeX, catgirlSizeY))

swordImg = pygame.image.load("sword.png")
swordImg = pygame.transform.scale(swordImg, (skillSizeX, skillSizeY))




# Set up the drawing window
screen = pygame.display.set_mode([screenX, screenY])




def RefreshSkillButtons(Player):
    # Add Skill Icons
    skill1Img = pygame.image.load(Player.skills[0].img)
    skill1Img = pygame.transform.scale(skill1Img, (skillSizeX, skillSizeY))
    skill2Img = pygame.image.load(Player.skills[1].img)
    skill2Img = pygame.transform.scale(skill2Img, (skillSizeX, skillSizeY))
    skill3Img = pygame.image.load(Player.skills[2].img)
    skill3Img = pygame.transform.scale(skill3Img, (skillSizeX, skillSizeY))

    screen.blit(skill1Img, (skill1X, skillY))
    screen.blit(skill2Img, (skill2X, skillY))
    screen.blit(skill3Img, (skill3X, skillY))

def RefreshEnemySelection():
    pygame.draw.ellipse(screen, "white", (enemy1X, enemyY, enemySizeX, enemySizeY), 2)
    pygame.draw.ellipse(screen, "white", (enemy2X, enemyY, enemySizeX, enemySizeY), 2)
    pygame.draw.ellipse(screen, "white", (enemy3X, enemyY, enemySizeX, enemySizeY), 2)
    pygame.draw.ellipse(screen, "white", (enemy4X, enemyY, enemySizeX, enemySizeY), 2)

def RefreshMenu(Enemy1, Enemy2, Enemy3, Enemy4, Player):
    # Fill the background
    screen.blit(background, (0, 0))

    # Add Enemies
    enemy1Img = pygame.image.load(Enemy1.img)
    enemy1Img = pygame.transform.scale(enemy1Img, (enemySizeX, enemySizeY))

    enemy2Img = pygame.image.load(Enemy2.img)
    enemy2Img = pygame.transform.scale(enemy2Img, (enemySizeX, enemySizeY))

    enemy3Img = pygame.image.load(Enemy3.img)
    enemy3Img = pygame.transform.scale(enemy3Img, (enemySizeX, enemySizeY))

    enemy4Img = pygame.image.load(Enemy4.img)
    enemy4Img = pygame.transform.scale(enemy4Img, (enemySizeX, enemySizeY))

    screen.blit(enemy1Img, (enemy1X, enemyY))
    screen.blit(enemy2Img, (enemy2X, enemyY))
    screen.blit(enemy3Img, (enemy3X, enemyY))
    screen.blit(enemy4Img, (enemy4X, enemyY))

    # Add Enemy HP Bars
    pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect(HPBar1X,HPBarY,HPBarSizeX,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(HPBar1X,HPBarY,HPBarSizeX*Enemy1.HP/Enemy1.maxHP,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(HPBar1X,HPBarY,HPBarSizeX,HPBarSizeY), 2)

    pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect(HPBar2X,HPBarY,HPBarSizeX,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(HPBar2X,HPBarY,HPBarSizeX*Enemy2.HP/Enemy2.maxHP,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(HPBar2X,HPBarY,HPBarSizeX,HPBarSizeY), 2)

    pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect(HPBar3X,HPBarY,HPBarSizeX,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(HPBar3X,HPBarY,HPBarSizeX*Enemy3.HP/Enemy3.maxHP,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(HPBar3X,HPBarY,HPBarSizeX,HPBarSizeY), 2)

    pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect(HPBar4X,HPBarY,HPBarSizeX,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(HPBar4X,HPBarY,HPBarSizeX*Enemy4.HP/Enemy4.maxHP,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(HPBar4X,HPBarY,HPBarSizeX,HPBarSizeY), 2)

    # Add Enemy HP Bar Label
    HPBar1Label =  HPBarFont.render(str(int(Enemy1.HP)) + '/' + str(int(Enemy1.maxHP)), False, (0, 0, 0))
    screen.blit(HPBar1Label, HPBar1LabelRect)

    HPBar2Label =  HPBarFont.render(str(int(Enemy2.HP)) + '/' + str(int(Enemy2.maxHP)), False, (0, 0, 0))
    screen.blit(HPBar2Label, HPBar2LabelRect)

    HPBar3Label =  HPBarFont.render(str(int(Enemy3.HP)) + '/' + str(int(Enemy3.maxHP)), False, (0, 0, 0))
    screen.blit(HPBar3Label, HPBar3LabelRect)

    HPBar4Label =  HPBarFont.render(str(int(Enemy4.HP)) + '/' + str(int(Enemy4.maxHP)), False, (0, 0, 0))
    screen.blit(HPBar4Label, HPBar4LabelRect)


    # Add Player
    screen.blit(catgirlImg, (catgirlX, catgirlY))

    #Add Player HP Bar and Label
    pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect(playerHPBarX,playerHPBarY,playerHPBarSizeX,playerHPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(playerHPBarX,playerHPBarY,playerHPBarSizeX*Player.HP/Player.maxHP,playerHPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(playerHPBarX,playerHPBarY,playerHPBarSizeX,playerHPBarSizeY), 2)

    playerHPBarLabel =  playerHPBarFont.render(str(int(Player.HP)) + '/' + str(int(Player.maxHP)), False, (0, 0, 0))
    screen.blit(playerHPBarLabel, playerHPBarLabelRect)

    # Add Menu
    pygame.draw.rect(screen,pygame.Color('aliceblue'),pygame.Rect(exitButtonX,exitButtonY,buttonSizeX,buttonSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(exitButtonX,exitButtonY,buttonSizeX,buttonSizeY), 2)

    pygame.draw.rect(screen, pygame.Color('aliceblue'), pygame.Rect(glossaryButtonX,glossaryButtonY, buttonSizeX,buttonSizeY))
    pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(glossaryButtonX,glossaryButtonY, buttonSizeX,buttonSizeY), 2)

    pygame.draw.rect(screen,pygame.Color('aliceblue'),pygame.Rect(bagButtonX,bagButtonY,buttonSizeX,buttonSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(bagButtonX,bagButtonY,buttonSizeX,buttonSizeY), 2)

    pygame.draw.rect(screen, pygame.Color('aliceblue'), pygame.Rect(skillButtonX,skillButtonY, buttonSizeX,buttonSizeY))
    pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(skillButtonX,skillButtonY, buttonSizeX,buttonSizeY), 2)

    #Label things
    screen.blit(exitButtonLabel, exitButtonLabelRect)
    screen.blit(skillButtonLabel, skillButtonLabelRect)
    screen.blit(bagButtonLabel, bagButtonLabelRect)
    screen.blit(glossaryButtonLabel, glossaryButtonLabelRect)


# Temporary Manual Character Creation
Enemy1 = Entity.Entity("Wizard", "wizard.png", 10)
Enemy2 = Entity.Entity("Frog", "frog.png", 10)
Enemy3 = Entity.Entity("Wizard", "wizard.png", 10)
Enemy4 = Entity.Entity("Frog", "frog.png", 10)


Player = Entity.Entity("Catgirl", "catgirl.png", 20)
Player.skills[0] = Skill.Skill("Basic Attack", "sword.png", 1, 0, 0, 0, 100, 0, 0, 0, "Physical", 0)
Player.skills[1] = Skill.Skill("Berserk", "sword.png", 2, 0, 0, 200, 200, 0, 0, 0, "Physical", 0)
Player.skills[2] = Skill.Skill("Spell of Healing", "wand.png", 1, 100, 0, 0, 0, 0, 0, 0, "Physical", 0)
skillSelected = 0



skillsShowing = False
enemySelectionShowing = False
while True:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if exitButtonX <= mouse[0] <= exitButtonX+buttonSizeX and exitButtonY <= mouse[1] <= exitButtonY+buttonSizeY:
                pygame.quit()
            elif skillButtonX <= mouse[0] <= skillButtonX+buttonSizeX and skillButtonY <= mouse[1] <= skillButtonY+buttonSizeY:
                skillsShowing = not skillsShowing
            elif bagButtonX <= mouse[0] <= bagButtonX+buttonSizeX and bagButtonY <= mouse[1] <= bagButtonY+buttonSizeY:
                pygame.quit()
            elif skill1X <= mouse[0] <= skill1X+skillSizeX and skillY <= mouse[1] <= skillY+skillSizeY:
                if skillsShowing: 
                    skillSelected = 0
                    if ((Player.skills[skillSelected].targetLevel == 2) or (Player.skills[skillSelected].healEnemy == 0 and Player.skills[skillSelected].damageEnemy == 0 and Player.skills[skillSelected].manaGiveEnemy == 0 and Player.skills[skillSelected].manaDrainEnemy == 0)):
                        Player.useSkill(Enemy1, Enemy2, Enemy3, Enemy4, skillSelected)
                    else: enemySelectionShowing = True
            elif skill2X <= mouse[0] <= skill2X+skillSizeX and skillY <= mouse[1] <= skillY+skillSizeY:
                if skillsShowing: 
                    skillSelected = 1
                    if ((Player.skills[skillSelected].targetLevel == 2) or (Player.skills[skillSelected].healEnemy == 0 and Player.skills[skillSelected].damageEnemy == 0 and Player.skills[skillSelected].manaGiveEnemy == 0 and Player.skills[skillSelected].manaDrainEnemy == 0)):
                        Player.useSkill(Enemy1, Enemy2, Enemy3, Enemy4, skillSelected)
                    else: enemySelectionShowing = True
            elif skill3X <= mouse[0] <= skill3X+skillSizeX and skillY <= mouse[1] <= skillY+skillSizeY:
                if skillsShowing: 
                    skillSelected = 2
                    if ((Player.skills[skillSelected].targetLevel == 2) or (Player.skills[skillSelected].healEnemy == 0 and Player.skills[skillSelected].damageEnemy == 0 and Player.skills[skillSelected].manaGiveEnemy == 0 and Player.skills[skillSelected].manaDrainEnemy == 0)):
                        Player.useSkill(Enemy1, Enemy2, Enemy3, Enemy4, skillSelected)
                    else: enemySelectionShowing = True
            elif (mouse[0]-(enemy1X+enemySizeX/2))*(mouse[0]-(enemy1X+enemySizeX/2)) + (enemySizeX/enemySizeY)*(enemySizeX/enemySizeY)*(mouse[1]-(enemyY+enemySizeY/2))*(mouse[1]-(enemyY+enemySizeY/2)) < ((enemySizeX/2)*(enemySizeX/2)):
                if enemySelectionShowing:
                    Player.useSkill(Enemy1, Enemy2, Enemy3, Enemy4, skillSelected)
                    enemySelectionShowing = False
            elif (mouse[0]-(enemy2X+enemySizeX/2))*(mouse[0]-(enemy2X+enemySizeX/2)) + (enemySizeX/enemySizeY)*(enemySizeX/enemySizeY)*(mouse[1]-(enemyY+enemySizeY/2))*(mouse[1]-(enemyY+enemySizeY/2)) < ((enemySizeX/2)*(enemySizeX/2)):
                if enemySelectionShowing:
                    Player.useSkill(Enemy2, Enemy1, Enemy3, Enemy4, skillSelected)
                    enemySelectionShowing = False
            elif (mouse[0]-(enemy3X+enemySizeX/2))*(mouse[0]-(enemy3X+enemySizeX/2)) + (enemySizeX/enemySizeY)*(enemySizeX/enemySizeY)*(mouse[1]-(enemyY+enemySizeY/2))*(mouse[1]-(enemyY+enemySizeY/2)) < ((enemySizeX/2)*(enemySizeX/2)):
                if enemySelectionShowing:
                    Player.useSkill(Enemy3, Enemy1, Enemy2, Enemy4, skillSelected)
                    enemySelectionShowing = False
            elif (mouse[0]-(enemy4X+enemySizeX/2))*(mouse[0]-(enemy4X+enemySizeX/2)) + (enemySizeX/enemySizeY)*(enemySizeX/enemySizeY)*(mouse[1]-(enemyY+enemySizeY/2))*(mouse[1]-(enemyY+enemySizeY/2)) < ((enemySizeX/2)*(enemySizeX/2)):
                if enemySelectionShowing:
                    Player.useSkill(Enemy4, Enemy1, Enemy2, Enemy3, skillSelected)
                    enemySelectionShowing = False
            elif glossaryButtonX <= mouse[0] <= glossaryButtonX+buttonSizeX and glossaryButtonY <= mouse[1] <= glossaryButtonY+buttonSizeY:
                pygame.quit()



              
    
    
    RefreshMenu(Enemy1, Enemy2, Enemy3, Enemy4, Player)
    if (skillsShowing): RefreshSkillButtons(Player)
    if (enemySelectionShowing): RefreshEnemySelection()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()