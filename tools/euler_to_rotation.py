import math
import numpy as np

#set directory
fin = open('/home/jaun/Downloads/kitti-odom-eval-master/result/glassStraight/deep_17.txt', "rt")
fout = open('/home/jaun/Downloads/kitti-odom-eval-master/result/glassStraight/deep_17_nocomma.txt', "wt")

#for pose files(+rotation matrix) with ','
for line in fin:
    fout.write(line.replace(',', ''))
fin.close()
fout.close()

fin = open('/home/jaun/Downloads/kitti-odom-eval-master/result/glassStraight/deep_17_nocomma.txt', "rt")
fout = open('/home/jaun/Downloads/kitti-odom-eval-master/result/glassStraight/deep_17_error.txt', "wt")


# Calculates Rotation Matrix given euler angles.
def eulerAnglesToRotationMatrix(theta):

    R_x = np.array([[1, 0, 0],
                [0, math.cos(theta[0]), -math.sin(theta[0])],
                [0, math.sin(theta[0]), math.cos(theta[0])]
                ])
    R_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
                    [0, 1, 0],
                    [-math.sin(theta[1]), 0, math.cos(theta[1])]
                    ])

    R_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0],
                [math.sin(theta[2]), math.cos(theta[2]), 0],
                [0, 0, 1]
                ])


    R = np.dot(R_z, np.dot(R_y, R_x))
    return R

#makes a 3x4 text file for pose
out = 0
for line in fin:
    linei = line.split()
    theta = [float(linei[0]), float(linei[1]), float(linei[2])]
    tx = float(linei[3])
    ty = float(linei[4])
    tz = float(linei[5])
    
    cake = eulerAnglesToRotationMatrix(theta)
    
    out = cake[0]
    out = np.append(out, tx)
    out = np.append(out, cake[1])
    out = np.append(out, ty)
    out = np.append(out, cake[2])
    out = np.append(out, tz)
    out = ["%1.6e" % member for member in out]
    
    #print(out)
    print(*out, sep=' ', file= fout)
    fout.write('')
