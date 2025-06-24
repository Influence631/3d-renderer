import numpy as np
from math import sin, cos

projection_matrix = np.array([[1,0,0],
                             [0,1,0],
                             [0,0,0]])

def rotate_x(angle):
    return np.array([[1, 0, 0], [0, cos(angle), -sin(angle)], [0, sin(angle), cos (angle)]])

def rotate_y(angle):
    return np.array([[cos(angle), 0, sin(angle)], [0, 1, 0], [-sin(angle), 0, cos (angle)]])

def rotate_z(angle):
    return np.array([[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]])

def rot_mat(angle):
    return rotate_z(angle).dot(rotate_y(angle).dot(rotate_x(angle)))

def map(value, i_min, i_max, o_min, o_max):
    return (value - i_min) / (i_max - i_min) * (o_max - o_min) + o_min
     
def v3_v2(vector3):
    return [vector3[0], vector3[1]]