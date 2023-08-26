import pygame

class Tile:
    tileSize = 48
    height = 0
    img = "grass.png"
    solid = False

    def __init__(self, img, height, solid = False):
        self.height = height
        self.img = pygame.image.load(f"src/main/python/sprites/tiles/{img}")
        self.img = pygame.transform.scale(self.img, (self.tileSize, self.tileSize))
        self.solid = solid
    
    def isSolid(self):
        return self.solid

    def canPass(self, tile):
        return (not ((self.height-tile.height > 1) or (self.height-tile.height < -1) or tile.isSolid()))