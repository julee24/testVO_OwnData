# For manually changing scale of groundtruth
import numpy as np

#Eliminate comma
f = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/pose_GT/04.txt', "rt")
fout = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/pose_GT/04_change1.txt', "wt")

for line in f:
    fout.write(line.replace(',', ' '))
fout.close()
f.close()

input = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/pose_GT/04_change1.txt', "rt")
output = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/pose_GT/04_change_end.txt', "wt")
for line in input:
    out = []
    theta_change = []
    translation_change = []

    linei = line.split()
    
    '''
    r11 r12 r13 tx r21 r22 r23 ty r31 r32 r33 tz
    multiply or divide the elements. float(linei[3]) is x, float(linei[7]) is y, float(linei[11]) is z
    mostly only have to change x and z
    '''
    translation_change = [float(linei[0]), float(linei[1]), float(linei[2]), float(linei[3]), float(linei[4]),
                          float(linei[5]), float(linei[6]), float(linei[7]), float(linei[8]), float(linei[9]),
                          float(linei[10]), float(linei[11])]
    out = np.append(out, translation_change)
    out = ["%1.6e" % member for member in out]

    print(*out, sep=' ', file=output)
    output.write('')


input.close()
output.close()
