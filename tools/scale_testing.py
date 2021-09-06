# finds the length between x,y,z for gt and estimation
import matplotlib.pyplot as plt
import numpy as np
import time
from params import par
import math

def scale_measure(method):
    scale_1 = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/straightGlass/{}_{}.txt'.format(method, video), "rt")
    scale_2 = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/straightGlass/{}_{}_scale.txt'.format(method, video), "wt")
    #
    print(gt[0], gt[1])
    for line in scale_1:
        #fout.write(line.replace(' ', ','))
        scale_2.write(line.replace(',', ' '))
    scale_1.close()
    scale_2.close()
    tx = []
    ty = []
    tz = []
    l1 = []
    l2 = []
    length = []
    count = 0
    scale = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/straightGlass/{}_{}_scale.txt'.format(method, video))
    #with open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/{}scale.txt'.format(video)) as scale1, open()
    for line in scale:
        t = []
        linei= line.split()
        t = [float(linei[3]), float(linei[4]), float(linei[5])]
        tx = np.append(tx,t[0])
        ty = np.append(ty,t[1])
        tz = np.append(tz,t[2])

        if len(tx) >= 2:
            x1 = tx[0]
            x2 = tx[1]
            y1 = ty[0]
            y2 = ty[1]
            z1 = tz[0]
            z2 = tz[1]
            l1.append(math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2))
            tx = np.delete(tx, 0)
            ty = np.delete(ty, 0)
            tz = np.delete(tz, 0)
            l2.append(math.sqrt((gt[count][3]-gt[count+1][3])**2 + (gt[count][4]-gt[count+1][4])**2 + (gt[count][5]-gt[count+1][5])**2))
            count += 1
        if count == 5:
            break
    for i in range(len(l1)):
        length.append(l1[i]/l2[i])
    avg = (sum(length)/len(length))/10
    scale.close()
    return avg
