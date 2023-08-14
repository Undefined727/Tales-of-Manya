from model.openworld.Rectangle import Rectangle
from model.openworld.Circle import Circle
from model.openworld.openWorldEntity import openWorldEntity
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

swordEntity = openWorldEntity("sprites/sample_sword.png", Rectangle([(275, 175),  (325, 175),  (275, 275), (325, 275)]))
sword2Entity = openWorldEntity("sprites/sample_sword.png", Rectangle([(275, 175),  (325, 175),  (275, 275), (325, 275)]))
sword3Entity = openWorldEntity("sprites/sample_sword.png", Rectangle([(275, 175),  (325, 175),  (275, 275), (325, 275)]))
sword4Entity = openWorldEntity("sprites/sample_sword.png", Rectangle([(275, 175),  (325, 175),  (275, 275), (325, 275)]))
playerEntity = openWorldEntity("sprites/catgirl_head.png", Circle((300, 300), 25))
enemyEntity = openWorldEntity("sprites/frog.png", Circle((425, 300), 25))

sword2Entity.rotate(90, playerEntity.shape.getCenter())
sword3Entity.rotate(180, playerEntity.shape.getCenter())
sword4Entity.rotate(270, playerEntity.shape.getCenter())
while(True):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    swordEntity.rotate(2, playerEntity.shape.getCenter())
    sword2Entity.rotate(2, playerEntity.shape.getCenter())
    sword3Entity.rotate(2, playerEntity.shape.getCenter())
    sword4Entity.rotate(2, playerEntity.shape.getCenter())

    screen.blit(swordEntity.getSprite(), swordEntity.shape.getImagePosition())
    screen.blit(sword2Entity.getSprite(), sword2Entity.shape.getImagePosition())
    screen.blit(sword3Entity.getSprite(), sword3Entity.shape.getImagePosition())
    screen.blit(sword4Entity.getSprite(), sword4Entity.shape.getImagePosition())
    screen.blit(playerEntity.getSprite(), playerEntity.shape.getImagePosition())
    screen.blit(enemyEntity.getSprite(), enemyEntity.shape.getImagePosition())

    pygame.display.flip()
    if (swordEntity.shape.collidesWith(enemyEntity.shape)): screen.fill((255, 0, 0))
    elif (sword2Entity.shape.collidesWith(enemyEntity.shape)): screen.fill((0, 255, 0))
    elif (sword3Entity.shape.collidesWith(enemyEntity.shape)): screen.fill((0, 0, 255))
    elif (sword4Entity.shape.collidesWith(enemyEntity.shape)): screen.fill((255, 255, 0))
    else: screen.fill((0, 0, 0))

    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    sleep_time = (1. / FPS) - dt
    if sleep_time > 0:
        time.sleep(sleep_time)