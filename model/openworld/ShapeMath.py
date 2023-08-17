import numpy as np
from model.openworld.Circle import Circle
from model.openworld.Rectangle import Rectangle

### Rotation ###

def rotate(shape, angle, pivot):
        if (type(shape) == Circle):
                rotateCircle(shape, angle, pivot)
        elif(type(shape) == Rectangle):
               rotateRectangle(shape, angle, pivot)

def rotateCircle(shape, angle, pivot):
       pass

def rotateRectangle(shape, angle, pivot):
        shape.corner1 = np.array(rotatePoint(shape.corner1, pivot, angle))
        shape.corner2 = np.array(rotatePoint(shape.corner2, pivot, angle))
        shape.corner3 = np.array(rotatePoint(shape.corner3, pivot, angle))
        shape.corner4 = np.array(rotatePoint(shape.corner4, pivot, angle))
        shape.center = 0.5*(shape.corner1+shape.corner4)

def rotatePoint(point, pivot, degrees=0):
        angle = np.deg2rad(degrees)
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle),  np.cos(angle)]])
        pivot = np.atleast_2d(pivot)
        rotated = np.atleast_2d(point)
        return np.squeeze((rotation_matrix @ (rotated.T-pivot.T) + pivot.T).T)




### Collision ###

def collides(shape1, shape2):
        if (type(shape1) == Circle):
                if (type(shape2) == Circle):
                       return collidesCircleCircle(shape1, shape2)
                if (type(shape2) == Rectangle): 
                       return collidesCircleRect(shape1, shape2)
        elif (type(shape1) == Rectangle):
                if (type(shape2) == Circle): 
                     return collidesCircleRect(shape2, shape1)
                if (type(shape2) == Rectangle):
                       return collidesRectRect(shape1, shape2)
        else: print("bruh")

def collidesCircleCircle(circle1, circle2):
        distance = np.linalg.norm(circle1.getCenter()-circle2.getCenter())
        return ((distance <= circle1.radius) or (distance <= circle2.radius))

def collidesRectRect(rect1, rect2):
        rect1Corners = rect1.getCorners()
        rect2Corners = rect2.getCorners()
        for corner in rect2Corners:
                if (rect1.pointIn(corner)): return True
        for corner in rect1Corners:
              if (rect2.pointIn(corner)): return True
        if (rect1.pointIn(rect2.getCenter())): return True
        if (rect2.pointIn(rect1.getCenter())): return True
        return False

def collidesCircleRect(circle, rect):
        # Finds point on each side of the rectangle that's closest to the center of the circle, if distance to point from center of circle
        # less than radius, collides.
        # Also checks if center of circle is in rectangle incase it's fully inside
        if (rect.pointIn(circle.center)): return True

        side1 = rect.corner1 - rect.corner2
        side2 = rect.corner1 - rect.corner3
        side3 = rect.corner4 - rect.corner2
        side4 = rect.corner4 - rect.corner3
        # Side 1
        t = np.dot(circle.center-rect.corner2, side1) / np.dot(side1, side1)
            
        if (t < 0): t = 0
        if (t > 1): t = 1
        point1 = rect.corner2 + t*side1
        if (circle.pointIn(point1)): return True
        # Side 2
        t = np.dot(circle.center-rect.corner3, side2) / np.dot(side2, side2)
        if (t < 0): t = 0
        if (t > 1): t = 1
        point2 = rect.corner3 + t*side2
        if (circle.pointIn(point2)): return True
        # Side 3
        t = np.dot(circle.center-rect.corner2, side3) / np.dot(side3, side3)
        if (t < 0): t = 0
        if (t > 1): t = 1
        point3 = rect.corner2 + t*side3
        if (circle.pointIn(point3)): return True
        # Side 4
        t = np.dot(circle.center-rect.corner3, side4) / np.dot(side4, side4)
        if (t < 0): t = 0
        if (t > 1): t = 1
        point4 = rect.corner3 + t*side4
        if (circle.pointIn(point4)): return True
        return False