from model.character.Character import Character
from model.player.Player import Player
import pygame

class Singleton:
    currentEnemies:list[Character]
    player:Player
    currentMap:str
    coords:(int, int)
    screenOpen:str
    pygameWindow:pygame.surface

    def __init__(self, screen, dataFile):
        self.pygameWindow = screen
        self.player = Player()
        self.screenOpen = "Welcome"
        self.currentMap = None
        self.coords = None
        self.currentEnemies = None