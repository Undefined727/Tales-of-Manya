from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.DrawingEntity import DrawingEntity
from model.visualentity.Tag import Tag
from model.character.Character import Character

class CombatEnemyEntity:
    xPosition = 0
    yPosition = 0
    width = 0
    height = 0

    enemyImg = ImageEntity
    enemyHPBarBorder = ImageEntity
    enemyHPBarGreen = DrawingEntity
    enemyHPBarRed = DrawingEntity
    enemyHPBarText = TextEntity

    positions = {
        "enemyImg" : [0.5, 0.3, 1, 0.6, True],
        "enemyHPBarBorder" : [0.5, 0.8, 1, 0.3, True],
        "enemyHPBarRed" : [0.5, 0.8, 0.6, 0.05, True],
        "enemyHPBarGreen" : [0.5, 0.8, 0.6, 0.05, True],
        "enemyHPBarText" : [0.5, 0.8, 0.6, 0.05, True]
    }

    enemy = Character


    def __init__(self, xPosition, yPosition, width, height, enemy):
       self.enemy = enemy
       self.xPosition = xPosition
       self.yPosition = yPosition
       self.width = width
       self.height = height
       self.enemyImg = ImageEntity(enemy.name + "Img", True, 0, 0, 0, 0, [Tag.ENEMY], enemy.img)
       self.enemyHPBarBorder = ImageEntity(enemy.name + "HPBorder", True, 0, 0, 0, 0, [Tag.ENEMY], "HPBar.png")
       self.enemyHPBarRed = DrawingEntity(enemy.name + "HPRed", True, 0, 0, 0, 0, [Tag.ENEMY], "red", False, "rectangle")
       self.enemyHPBarGreen = DrawingEntity(enemy.name + "HPGreen", True, 0, 0, 0, 0, [Tag.ENEMY], "green", False, "rectangle")
       self.enemyHPBarText = TextEntity(enemy.name + "HPText", True, 0, 0, 0, 0, [Tag.ENEMY], str(int(enemy.getCurrentHP())) + "/" + str(int(enemy.getMaxHP())), "mono", int(self.width/10), "black", None)
       self.resize()
       self.reposition()
       self.update()

    def resize(self):
        self.enemyImg.resize(self.positions["enemyImg"][2]*self.width, self.positions["enemyImg"][3]*self.height)
        self.enemyHPBarBorder.resize(self.positions["enemyHPBarBorder"][2]*self.width, self.positions["enemyHPBarBorder"][3]*self.height)
        self.enemyHPBarGreen.resize(self.positions["enemyHPBarRed"][2]*self.width, self.positions["enemyHPBarRed"][3]*self.height)
        self.enemyHPBarRed.resize(self.positions["enemyHPBarGreen"][2]*self.width, self.positions["enemyHPBarGreen"][3]*self.height)
        self.enemyHPBarText.resize(self.positions["enemyHPBarText"][2]*self.width, self.positions["enemyHPBarText"][3]*self.height)
    
    def reposition(self):
        self.enemyImg.reposition(self.xPosition + self.positions["enemyImg"][0]*self.width - self.positions["enemyImg"][2]*self.width/2, self.yPosition + self.positions["enemyImg"][1]*self.height - self.positions["enemyImg"][3]*self.height/2)
        self.enemyHPBarBorder.reposition(self.xPosition + self.positions["enemyHPBarBorder"][0]*self.width - self.positions["enemyHPBarBorder"][2]*self.width/2, self.yPosition + self.positions["enemyHPBarBorder"][1]*self.height - self.positions["enemyHPBarBorder"][3]*self.height/2)
        self.enemyHPBarGreen.reposition(self.xPosition + self.positions["enemyHPBarRed"][0]*self.width - self.positions["enemyHPBarRed"][2]*self.width/2, self.yPosition + self.positions["enemyHPBarRed"][1]*self.height - self.positions["enemyHPBarRed"][3]*self.height/2)
        self.enemyHPBarRed.reposition(self.xPosition + self.positions["enemyHPBarGreen"][0]*self.width - self.positions["enemyHPBarGreen"][2]*self.width/2, self.yPosition + self.positions["enemyHPBarGreen"][1]*self.height - self.positions["enemyHPBarGreen"][3]*self.height/2)
        self.enemyHPBarText.reposition(self.xPosition + self.positions["enemyHPBarText"][0]*self.width, self.yPosition + self.positions["enemyHPBarText"][1]*self.height)

    def scale(self, screenX, screenY):
        self.enemyImg.scale(screenX, screenY)
        self.enemyHPBarBorder.scale(screenX, screenY)
        self.enemyHPBarGreen.scale(screenX, screenY)
        self.enemyHPBarRed.scale(screenX, screenY)
        self.enemyHPBarText.scale(screenX, screenY)

    def update(self):
        self.enemyHPBarGreen.resize(self.enemyHPBarGreen.width * (self.enemy.getMaxHP()/self.enemy.getCurrentHP()), self.enemyHPBarGreen.height)
        self.enemyHPBarText.updateText(str(int(self.enemy.getCurrentHP())) + "/" + str(int(self.enemy.getMaxHP())), "mono", int(self.width/10), "black", None)
