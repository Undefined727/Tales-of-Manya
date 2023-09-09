import pygame

class Tile:
    height = 0
    name = "grass.png"
    solid = False

    def __init__(self, name, height, solid = False):
        self.height = height
        self.name = name
        self.solid = solid
    
    def isSolid(self):
        return self.solid

    def canPass(self, tile):
        return (not ((self.height-tile.height > 1) or (self.height-tile.height < -1) or tile.isSolid()))