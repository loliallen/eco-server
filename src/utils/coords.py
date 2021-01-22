from math import degrees
import numpy as np


def coords(dot, coords):
    print("coords")
    print(coords[0])
    print(coords[1])
    print(coords[2])
    print(coords[3])
    lu = np.array(coords[0]) 
    ru = np.array(coords[1]) 
    rd = np.array(coords[2]) 
    ld = np.array(coords[3])
    
    dot = np.array(dot)
    print("dot", dot)
    if(pre_check(dot, lu, ru, rd, ld)):
        return True

    angles = [
        angle_between_points(lu, dot, ru),
        angle_between_points(ru, dot, rd),
        angle_between_points(rd, dot, ld),
        angle_between_points(ld, dot, lu)
    ]
    
    _sum = np.sum(angles)
    return  _sum == 360.0

def angle_between_points(a, b, c):
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    
    return degrees(angle)

def pre_check(dot, lu, ru, rd, ld):
    if(np.array_equal(dot, lu) or np.array_equal(dot, ru) or np.array_equal(dot, rd) or np.array_equal(dot, ld)):
        return True
    return False