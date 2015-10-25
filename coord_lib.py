from math import cos, sin, pi
import numpy as np

def ang2cartezian(axis,distance):
    k = len(distance)
    if(len(axis) == len(distance)):
        pass
    else:
        print "Error: inputs has different lengths"
        print len(axis), len(distance)
        return 0,0
    x = np.zeros(k,np.int16)
    y = np.copy(x)
    for j in range(k):
        x[j] = cos(axis[j]/180.0*pi)*distance[j]
        y[j] = sin(axis[j]/180.0*pi)*distance[j]
    return x,y
