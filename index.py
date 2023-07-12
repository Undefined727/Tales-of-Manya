import pygame
import Entity
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

HPBarY = enemyY + enemySizeY + screenX/100

HPBarSizeX = enemySizeX
HPBarSizeY = screenX/50


catgirlX = screenX/3
catgirlY = screenY/3

catgirlSizeX = screenX/3
catgirlSizeY = 2*screenY/3


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


skill1X = screenX/12


skillY = screenY/2

skillSizeX = screenX/10
skillSizeY = screenY/6

# Initialize Visual Object Details

font = pygame.font.SysFont('mono', 32)
HPBarFont = pygame.font.SysFont('mono', 10)

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




catgirlImg = pygame.image.load("catgirl.png")
catgirlImg = pygame.transform.scale(catgirlImg, (catgirlSizeX, catgirlSizeY))

swordImg = pygame.image.load("sword.png")
swordImg = pygame.transform.scale(swordImg, (skillSizeX, skillSizeY))




# Set up the drawing window
screen = pygame.display.set_mode([screenX, screenY])




def RefreshSkillButtons():
    # Add Skill Icons
    screen.blit(swordImg, (skill1X, skillY))


def RefreshMenu(Enemy1, Enemy2, Enemy3, Enemy4):
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
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(HPBar2X,HPBarY,HPBarSizeX*Enemy2.maxHP/Enemy2.HP,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(HPBar2X,HPBarY,HPBarSizeX,HPBarSizeY), 2)

    pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect(HPBar3X,HPBarY,HPBarSizeX,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(HPBar3X,HPBarY,HPBarSizeX*Enemy3.maxHP/Enemy3.HP,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(HPBar3X,HPBarY,HPBarSizeX,HPBarSizeY), 2)

    pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect(HPBar4X,HPBarY,HPBarSizeX,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('green'),pygame.Rect(HPBar4X,HPBarY,HPBarSizeX*Enemy4.maxHP/Enemy4.HP,HPBarSizeY))
    pygame.draw.rect(screen,pygame.Color('black'),pygame.Rect(HPBar4X,HPBarY,HPBarSizeX,HPBarSizeY), 2)

    # Add Enemy HP Bar Label
    HPBar1Label =  HPBarFont.render(str(int(Enemy1.HP)) + '/' + str(int(Enemy1.maxHP)), False, (0, 0, 0))
    screen.blit(HPBar1Label, HPBar1LabelRect)


    # Add Player
    screen.blit(catgirlImg, (catgirlX, catgirlY))

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
Enemy1 = Entity.Entity("Wizard", 10, "wizard.png")
Enemy2 = Entity.Entity("Frog", 10, "frog.png")
Enemy3 = Entity.Entity("Wizard", 10, "wizard.png")
Enemy4 = Entity.Entity("Frog", 10, "frog.png")


Player = Entity.Entity("Catgirl", 20, "catgirl.png")

skillsShowing = False
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
                Player.attack(Enemy1, 10)
            elif bagButtonX <= mouse[0] <= bagButtonX+buttonSizeX and bagButtonY <= mouse[1] <= bagButtonY+buttonSizeY:
                pygame.quit()
            elif glossaryButtonX <= mouse[0] <= glossaryButtonX+buttonSizeX and glossaryButtonY <= mouse[1] <= glossaryButtonY+buttonSizeY:
                pygame.quit()



              
    
    
    RefreshMenu(Enemy1, Enemy2, Enemy3, Enemy4)
    if (skillsShowing): RefreshSkillButtons()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()