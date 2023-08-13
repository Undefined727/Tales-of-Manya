from model.openworld.Circle import Circle
from model.openworld.Rectangle import Rectangle
import pygame

class openWorldEntity:
    accX = 0
    accY = 0
    speedX = 0
    speedY = 0
    
    currentHeight = 0
    shape = Circle(0, 0, 0)
    imgPath = "nekoarc.png"
    img = pygame.image.load("sprites/nekoarc.png")
    rotImg = img
    currentRotation = 0

    def __init__(self, imgPath, shape):
        self.shape = shape
        self.imgPath = imgPath
        img = pygame.image.load(imgPath)
        imgSize = abs(shape.corner1-shape.corner4)
        self.img = pygame.transform.scale(img, tuple(imgSize))
        self.rotImg = self.img
        self.currentRotation = 0
    
    def rotate(self, angle, pivot):
        self.currentRotation -= angle
        self.currentRotation %= 360
        self.shape.rotate(angle, pivot)
        self.rotImg = pygame.transform.rotate(self.img, self.currentRotation)
    
    def getSprite(self):
        imgRect = self.rotImg.get_rect()
        imgRect.center = tuple(self.shape.center)
        return (self.rotImg, imgRect)

