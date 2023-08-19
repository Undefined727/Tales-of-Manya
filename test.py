from model.openworld.Rectangle import Rectangle
from model.openworld.Circle import Circle
from model.openworld.OpenWorldEntity import OpenWorldEntity
from model.character.Character import Character
import model.openworld.ShapeMath as ShapeMath
import pygame, numpy, time

pygame.init()
info = pygame.display.Info()
#screenX,screenY = info.current_w,info.current_h
screenX, screenY = 960, 600
pygame.display.set_caption('Catgirl Dungeon')
pygame.display.set_icon(pygame.image.load('sprites/catgirl_head.png'))
screen = pygame.display.set_mode([screenX, screenY])
FPS = 60
prev_time = time.time()

# To be replaced with database or something somewhere in the future
# Probably a defined size and you just give it the name of the item and position
swordEntity = OpenWorldEntity("sample_sword.png", Rectangle([(275, 175),  (325, 175),  (275, 275), (325, 275)]), "attack", None, None)
playerEntity = OpenWorldEntity("catgirl_head.png", Circle((300, 300), 25), "player", None, None)
enemy = Character("Wizard", "wizard.png", 5)
enemyEntity = OpenWorldEntity(enemy.img, Circle((425, 300), 25), "enemy", enemy, "attack")
swordEntity.rotate(350, playerEntity.getCenter())

entities = []
entities.append(playerEntity)
entities.append(enemyEntity)

swordSwinging = 0

while(True):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if (swordSwinging <= 0):
            swordSwinging = 30
            if keys[pygame.K_RIGHT]:
                if keys[pygame.K_UP]:
                    swordEntity.rotate(15, playerEntity.getCenter())
                elif keys[pygame.K_DOWN]:
                    swordEntity.rotate(105, playerEntity.getCenter())
                else:
                    swordEntity.rotate(55, playerEntity.getCenter())
            elif keys[pygame.K_LEFT]:
                if keys[pygame.K_UP]:
                    swordEntity.rotate(285, playerEntity.getCenter())
                elif keys[pygame.K_DOWN]:
                    swordEntity.rotate(195, playerEntity.getCenter())
                else: swordEntity.rotate(235, playerEntity.getCenter())
            elif keys[pygame.K_UP]: 
                swordEntity.rotate(330, playerEntity.getCenter())
            elif keys[pygame.K_DOWN]: 
                swordEntity.rotate(150, playerEntity.getCenter())
            else: swordEntity.rotate(55, playerEntity.getCenter())
            entities.append(swordEntity)
    
    if (swordSwinging > 0):
        swordSwinging -=1
        swordEntity.rotate(2, playerEntity.getCenter())
        if (swordSwinging == 0):
            if (swordEntity in entities):
                entities.remove(swordEntity)
            swordEntity = OpenWorldEntity("sample_sword.png", Rectangle([(275, 175),  (325, 175),  (275, 275), (325, 275)]), "attack", None, None)
    


    for item in entities:
        screen.blit(item.getSprite(), item.getImagePosition())
    pygame.display.flip()



    for item in entities:
         if (not item.trigger == None):
              for trigger in entities:
                   if (trigger.entityType == item.trigger):
                        if (ShapeMath.collides(trigger.shape, item.shape)):
                             if (item.entityType == "enemy"):
                                  item.data.health.setCurrentValue(item.data.health.getCurrentValue()-10)
                                  print(str(item.data.health.getCurrentValue()) + "/" + str(item.data.health.getMaxValue()))

    
    screen.fill((0, 0, 0))

    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    sleep_time = (1. / FPS) - dt
    if sleep_time > 0:
        time.sleep(sleep_time)