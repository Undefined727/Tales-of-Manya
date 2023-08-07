import pygame

class Tile:
    tileSize = 48
    height = 0
    img = "grass.png"
    solid = False

    def __init__(self, img, height):
        self.height = height
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (self.tileSize, self.tileSize))
    
    def isSolid(self):
        return self.solid

    def canPass(self, tile):
        return (not ((self.height-tile.height > 1) or (self.height-tile.height < -1) or tile.isSolid()))