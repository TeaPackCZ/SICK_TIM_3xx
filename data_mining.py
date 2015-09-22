
import matplotlib.pyplot as plt
import numpy as np
import math
from coord_lib import ang2cartezian

base_src = "measurements/Measurement_"
max_dif = 150
number_of_files = 5

ang_values = np.zeros(271,np.int16)
axis_x = np.arange(-135,136,1,np.float)

first_run = True

for i in range(number_of_files):
    name = base_src + str(i)
    files = open(name,"r")
    str_data = files.readline().replace(" ","").replace("[","").replace("]","").split(",")
    for j in range(len(str_data)):
        ang_values[j] = int(str_data[j])
    files.close()

    [x,y] = ang2cartezian(axis_x,ang_values)

    ## shift previous data to old ones:
    if(not first_run):
        try:
            del old_angle, old_x, old_y, old_segments, old_segm_len, old_segm_start
            del old_np_data
        except:
            pass
        old_angle = new_angle
        old_x = new_x
        old_y = new_y
        old_segments = new_segments
        old_segm_len = new_segm_len
        old_segm_start = new_segm_start
        old_np_data = np.copy(new_np_data)
        del new_angle, new_x, new_y, new_segments, new_segm_len, new_segm_start
        del new_np_data
    else:
        first_run = False

    new_angle = np.asarray(ang_values).astype(np.int16)
    [new_x,new_y]=ang2cartezian(axis_x,new_angle)
    
    ## Segmentation:
    new_segments = []
    new_segm_len = []
    new_segm_start = []

    new_segm_start.append(0)
    start_segm = 0
    for j in range(270):
        diff = abs(new_angle[j]-new_angle[j+1])
        if diff > max_dif:
            if(start_segm == j):
                # throw out single points
                start_segm = j+1
                pass
            else:
                end_segm = j
                new_segments.append(new_angle[start_segm:end_segm+1])
                new_segm_start.append(j)
                new_segm_len.append(len(new_angle[start_segm:end_segm+1]))
                start_segm = j+1

    new_segments.append(new_angle[start_segm:-1])
    new_segm_start.append(start_segm)
    new_segm_len.append(len(new_angle[start_segm:-1]))

    ## convert to np array
    new_np_data = np.asarray(new_segments)

    ## TODO: script for finding human legs near [0,3500] +-[500,500]
    
    ## Show data:
    plt.figure(0)
    for j in range(len(new_segm_start)-1):
        if(new_segm_len[j] > 1):
            plt.plot(axis_x[new_segm_start[j]:new_segm_start[j]+new_segm_len[j]],new_segments[j])
        else:
            plt.plot(axis_x[segm_start[j]:segm_start[j]+segm_len[j]],segments[j],"*")
    plt.show()
    




