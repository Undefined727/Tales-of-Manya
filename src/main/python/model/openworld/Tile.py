import pygame

class Tile:
    height = 0
    img = "grass.png"
    solid = False

    def __init__(self, img, height, solid = False):
        self.height = height
        self.img = img
        self.solid = solid
    
    def isSolid(self):
        return self.solid

    def canPass(self, tile):
        return (not ((self.height-tile.height > 1) or (self.height-tile.height < -1) or tile.isSolid()))