#change the scales of the estimated poses
import numpy as np

#Eliminate comma

f = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/straightGlass/sc_04.txt', "rt")
fout = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/straightGlass/sc_04_change1.txt', "wt")

for line in f:
    fout.write(line.replace(',', ' '))
fout.close()
f.close()

input = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/straightGlass/sc_04_change1.txt', "rt")
output = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/straightGlass/sc_04_change2.txt', "wt")
for line in input:
    out = []
    theta_change = []
    translation_change = []

    linei = line.split()
    
    
    #divide or multipy correct scale to the elements, x:float(linei[3]), y:float(linei[4]), z:float(linei[5])
    
    translation_change = [float(linei[0]), float(linei[1]), float(linei[2]), float(linei[3]), float(linei[4]), float(linei[5])]
    #theta_change = [float(linei[2]), float(linei[1]),float(linei[0]), float(linei[3]), float(linei[4]), float(linei[5])]

    out = np.append(out, translation_change)
    out = ["%1.9f" % member for member in out]

    print(*out, sep=' ', file=output)
    output.write('')


input.close()
output.close()

f = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/straightGlass/sc_04_change2.txt', "rt")
fout = open('/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/straightGlass/sc_04_change_end.txt', "wt")

#put commas in again
for line in f:
    fout.write(line.replace(' ', ', '))

f.close()
fout.close()
