import numpy as np

class Rectangle:
    corner1 = np.array((0, 0))
    corner2 = np.array((0, 1))
    corner3 = np.array((1, 0))
    corner4 = np.array((1, 1))
    center = 0.5*(corner1+corner4)

    def __init__(self, corners):
        self.corner1 = np.array(corners[0])
        self.corner2 = np.array(corners[1])
        self.corner3 = np.array(corners[2])
        self.corner4 = np.array(corners[3])
        self.center = 0.5*(self.corner1+self.corner4)
    

    def pointIn(self, point): 
        #Triangle 1
        v0 = self.corner3 - self.corner1
        v1 = self.corner2 - self.corner1
        v2 = point - self.corner1

        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom
        if (u >= 0 and v >= 0 and (u + v) < 1): return True
        
        #Triangle 2
        v0 = self.corner2 - self.corner4
        v1 = self.corner3 - self.corner4
        v2 = point - self.corner4

        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom
        return (u >= 0 and v >= 0 and (u + v) < 1)


    def getCenter(self):
        return self.center
    
    def getCorners(self):
        return [self.corner1, self.corner2, self.corner3, self.corner4]
    
    def getImagePosition(self):
        xPos = self.corner1[0]
        if (self.corner2[0] < xPos): xPos = self.corner2[0]
        if (self.corner3[0] < xPos): xPos = self.corner3[0]
        if (self.corner4[0] < xPos): xPos = self.corner4[0]
        yPos = self.corner1[1]
        if (self.corner2[1] < yPos): yPos = self.corner2[1]
        if (self.corner3[1] < yPos): yPos = self.corner3[1]
        if (self.corner4[1] < yPos): yPos = self.corner4[1]
        return (xPos, yPos)
    
    def getImageSize(self):
        return tuple(abs(self.corner1-self.corner4))
    
    def setCenter(self, newCenter):
        newCenter = np.array(newCenter)
        diff = newCenter - self.center
        self.corner1 = self.corner1 + diff
        self.corner2 = self.corner2 + diff
        self.corner3 = self.corner3 + diff
        self.corner4 = self.corner4 + diff
        self.center = self.center + diff

    def move(self, diff):
        diff = np.array(diff)
        self.corner1 = self.corner1 + diff
        self.corner2 = self.corner2 + diff
        self.corner3 = self.corner3 + diff
        self.corner4 = self.corner4 + diff
        self.center = self.center + diff
