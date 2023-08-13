import numpy as np
import model.openworld.ShapeMath as ShapeMath
import pygame

class Rectangle:
    corner1 = np.array((0, 0))
    corner2 = np.array((0, 1))
    corner3 = np.array((1, 0))
    corner4 = np.array((1, 1))
    center = 0.5*(corner1+corner4)
    a = 0.5*np.linalg.norm(corner1 - corner4)
    b = 0.5*np.linalg.norm(corner2 - corner3)
    U = (corner1-corner4)/(2*a)
    V = (corner2-corner3)/(2*b)

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
        v0 = self.corner4 - self.corner1
        v1 = self.corner3 - self.corner1
        v2 = point - self.corner1

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
