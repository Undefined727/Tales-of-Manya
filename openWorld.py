from model.openworld.Tile import Tile
import numpy
from PIL import Image
import pygame

npArray = numpy.zeros((50,50, 3), dtype=numpy.uint8)

for y in range(0, 50):
    for x in range(0, 50):
        if (x%3 == 1): npArray[y, x, 1] = 255
        if (y%3 == 2): npArray[y, x, 2] = 255
        #else: npArray[y, x] = (255, 0, 0)

image = Image.fromarray(npArray, "RGB")
image.save("maps/test.png")





img = Image.open("maps/" + "test.png")
npArray = numpy.array(img)
height, width, dim = npArray.shape


image = Image.fromarray(npArray, "RGB")
image.save("maps/convert.png")


pygame.init()
screenX, screenY = 1000, 1000
screen = pygame.display.set_mode([screenX, screenY])
img = pygame.image.load("sprites/tiles/grass.png")
img2 = pygame.image.load("sprites/tiles/grass2.png")
img3 = pygame.image.load("sprites/tiles/grass3.png")

tiles = []

for y in range(0, height):
    for x in range(0, width):
        if (npArray[y, x, 1] == 255): tiles.append(img)
        elif (npArray[y, x, 2] == 255): tiles.append(img2)
        else: tiles.append(img3)


cameraX = width/2
cameraY = height/2
cameraWidth = int(width/2)
cameraHeight = int(height/2)
speed = 0.05
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cameraX -= speed
        if (cameraX < 0): cameraX = 0
    if keys[pygame.K_RIGHT]:
        cameraX += speed
        if (cameraX > width): cameraX = width
    if keys[pygame.K_UP]:
        cameraY -= speed
        if (cameraY < 0): cameraY = 0
    if keys[pygame.K_DOWN]:
        cameraY += speed
        if (cameraY > height): cameraY = height
    screen.fill((0, 0, 0))
    for x in range(0, width):
        for y in range(0, height):
            screen.blit(tiles[width*y + x], ((screenX/2-(cameraX-x)*48), (screenY/2-(cameraY-y)*48)))
    pygame.display.flip()





