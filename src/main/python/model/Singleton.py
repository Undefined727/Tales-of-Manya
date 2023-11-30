from src.main.python.model.character.Character import Character
from src.main.python.model.player.Player import Player
from src.main.python.model.database.DBElementFactory import DBElementFactory
import pygame

class Singleton:
    currentEnemies:list[Character]
    player : Player
    currentMap : str
    screenOpen : str
    pygameWindow : pygame.surface
    renderedMapEntities : list
    database_factory : DBElementFactory

    def __init__(self, screen, dataFile):
        self.pygameWindow = screen
        self.database_factory = DBElementFactory()
        self.player = Player(self.database_factory)
        self.screenOpen = "Welcome"
        self.currentMap = None
        self.currentEnemies = None
        self.renderedMapEntities = None
        

#global_states = Singleton()