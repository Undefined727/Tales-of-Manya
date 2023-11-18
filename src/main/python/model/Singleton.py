from model.character.Character import Character
from model.player.Player import Player
from model.database.DBElementFactory import DBElementFactory
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
        self.player = Player()
        self.screenOpen = "Welcome"
        self.currentMap = None
        self.currentEnemies = None
        self.renderedMapEntities = None
        self.database_factory = DBElementFactory()

global_states = Singleton()