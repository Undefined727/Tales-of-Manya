from PIL import Image
import pygame, numpy

class VisualEntity:
    name = "Default_Name"
    isShowing = True
    # Image = 0, Drawing = 1, Button = 2, Text = 3
    entityType = 0
    # Example tags: "Enemy", "Skill"
    tags = []
    img = None
    xPosition = 0
    yPosition = 0
    width = 0
    length = 0
    shape = "rectangle"
    color = None
    func = None
    args = None
    isBorder = False
    textLabel = None
    textRect = None
    npArray = None
    
    #Args listings are formatted as follows; Image: imgPath. Drawing: color, isBorder, shape. Button: func, args, shape. Text: text, font, fontSize, fontColor, highlightColor. Custom Button: func, args, imgPath
    def __init__(self, name, entityType, isShowing, xPosition, yPosition, width, length, tags, *args):
        self.name = name
        self.entityType = entityType
        self.isShowing = isShowing
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.width = width
        self.length = length
        self.tags = tags

        if (entityType == 0):
            self.img = pygame.image.load("sprites/" + args[0])
            self.img = pygame.transform.scale(self.img, (self.width, self.length))
        elif (entityType == 1):
            self.color = args[0]
            self.isBorder = args[1]
            self.shape = args[2]
        elif (entityType == 2):
            self.func = args[0]
            self.args = args[1]
            self.shape = args[2]
        elif (entityType == 3):
            self.updateText(args[0], args[1], args[2], args[3], args[4])
        elif (entityType == 4):
            self.func = args[0]
            self.args = args[1]
            img = Image.open("sprites/" + args[2])
            img = img.resize((int(width), int(length)))
            self.npArray = numpy.asarray(img)
        else:
            print("bruh moment")
        
    def updateText(self, text, font, fontSize, fontColor, highlightColor):
        textFont = pygame.font.SysFont(font, fontSize)
        if (highlightColor != None):
            self.textLabel = textFont.render(text, True, fontColor, highlightColor)
        else:
            self.textLabel = textFont.render(text, False, fontColor)
        self.textRect = self.textLabel.get_rect()
        self.textRect.center = (self.xPosition, self.yPosition)
    
    def updateImg(self, imgPath):
        self.img = pygame.image.load("sprites/" + imgPath)
        self.img = pygame.transform.scale(self.img, (self.width, self.length))