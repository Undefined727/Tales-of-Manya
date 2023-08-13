import numpy as np

def rotate(point, pivot, degrees=0):
        angle = np.deg2rad(degrees)
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle),  np.cos(angle)]])
        pivot = np.atleast_2d(pivot)
        rotated = np.atleast_2d(point)
        return np.squeeze((rotation_matrix @ (rotated.T-pivot.T) + pivot.T).T)