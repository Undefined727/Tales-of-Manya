from view.visualentity.ImageEntity import ImageEntity

class DamageNumber:
    timer:int
    numbers:list[ImageEntity]
    elementType:str
    xPos:float
    yPos:float
    isShowing:float


    def __init__(self, number, elementType, xPos, yPos, screenX, screenY):
        self.timer = 25
        self.xPos = xPos
        self.yPos = yPos
        self.elementType = elementType
        self.numbers = []
        self.isShowing = True

        digits = 0
        counter = number
        while(counter > 0):
            digits += 1
            counter -= counter%10
            counter /= 10

        for i in range(digits):
            digit = int((number/10**(digits-i-1))%10) 
            image = ImageEntity(f"Number{i}", True, xPos + i*0.05*screenX, yPos, 0.05*screenX, 0.05*screenY)
            image.updateImg(f"font/{digit}.png")
            self.numbers.append(image)

    def getItems(self):
        return self.numbers