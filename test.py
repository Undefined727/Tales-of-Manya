from model.openworld.Rectangle import Rectangle
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

entity = openWorldEntity("sprites/change_active_right.png", Rectangle([(100, 100), (100, 300), (200, 100), (200, 300)]))
img = pygame.image.load("sprites/catgirl_head.png")
img = pygame.transform.scale(img, (50, 50))
entity.rotate(292, entity.shape.center)
while(True):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    entity.rotate(1, (300, 300))
    screen.blit(img, (275, 275))
    screen.blit(img, (500, 275))
    screen.blit(*entity.getSprite())

    pygame.display.flip()
    if (entity.shape.pointIn((500, 275))): screen.fill((0, 255, 0))
    elif (entity.shape.pointIn((500, 325))): screen.fill((0, 255, 0))
    else: screen.fill((0, 0, 0))

    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    sleep_time = (1. / FPS) - dt
    if sleep_time > 0:
        time.sleep(sleep_time)