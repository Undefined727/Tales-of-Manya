import pygame, json
from model.visualentity.ImageEntity import ImageEntity

pygame.init()
screenX, screenY = 960, 600
screen = pygame.display.set_mode([screenX, screenY])
img = pygame.image.load("sprites/" + "catgirl.png")

visualEntities = []
file = open("screens/combatScreen.json", 'r')
data = json.load(file)
for item in data:
    imageEntity = ImageEntity.createFrom(item)
    imageEntity.resize(imageEntity.width*screen.get_width(), imageEntity.height*screen.get_height())
    imageEntity.reposition(imageEntity.xPosition*screen.get_width(), imageEntity.yPosition*screen.get_height())
    visualEntities.append(imageEntity)

count = 1
while True:
    count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    for entity in visualEntities:
        screen.blit(entity.img, (entity.xPosition, entity.yPosition))
        
    pygame.display.flip()
    if count > 100: count = 0