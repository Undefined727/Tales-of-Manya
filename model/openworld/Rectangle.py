import numpy as np
import model.openworld.ShapeMath as ShapeMath
from model.openworld.Circle import Circle
import pygame

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

    def rotate(self, angle, pivot):
        self.corner1 = np.array(ShapeMath.rotate(self.corner1, pivot, angle))
        self.corner2 = np.array(ShapeMath.rotate(self.corner2, pivot, angle))
        self.corner3 = np.array(ShapeMath.rotate(self.corner3, pivot, angle))
        self.corner4 = np.array(ShapeMath.rotate(self.corner4, pivot, angle))
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
    

    def collidesWith(self, shape):
        if (type(shape) == Circle):
            # Finds point on each side of the rectangle that's closest to the center of the circle, if distance to point from center of circle
            # less than radius, collides.
            # Also checks if center of circle is in rectangle incase it's fully inside
            if (self.pointIn(shape.center)): return True

            side1 = self.corner1 - self.corner2
            side2 = self.corner1 - self.corner3
            side3 = self.corner4 - self.corner2
            side4 = self.corner4 - self.corner3
            # Side 1
            t = np.dot(shape.center-self.corner2, side1) / np.dot(side1, side1)
            
            if (t < 0): t = 0
            if (t > 1): t = 1
            point1 = self.corner2 + t*side1
            if (shape.pointIn(point1)): return True
            # Side 2
            t = np.dot(shape.center-self.corner3, side2) / np.dot(side2, side2)
            if (t < 0): t = 0
            if (t > 1): t = 1
            point2 = self.corner3 + t*side2
            if (shape.pointIn(point2)): return True
            # Side 3
            t = np.dot(shape.center-self.corner2, side3) / np.dot(side3, side3)
            if (t < 0): t = 0
            if (t > 1): t = 1
            point3 = self.corner2 + t*side3
            if (shape.pointIn(point3)): return True
            # Side 4
            t = np.dot(shape.center-self.corner3, side4) / np.dot(side4, side4)
            if (t < 0): t = 0
            if (t > 1): t = 1
            point4 = self.corner3 + t*side4
            if (shape.pointIn(point4)): return True
            return False
        return False


    def getCenter(self):
        return self.center
    
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
