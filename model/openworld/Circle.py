import numpy as np

class Circle:
    center = np.array((0, 0))
    radius = 5

    def __init__(self, center, radius):
        self.center = np.array(center)
        self.radius = radius

    def getCenter(self):
        return self.center
    
    def pointIn(self, point):
        point = np.array(point)
        return (np.linalg.norm(point-self.center) <= self.radius)
    
    def getImagePosition(self):
        return tuple(self.center - np.array((self.radius, self.radius)))
    
    def getImageSize(self):
        return (2*self.radius, 2*self.radius)