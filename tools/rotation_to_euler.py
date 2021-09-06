# For changing SC-SfMLearner and DF-VO to euler form
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

# set directory
fin = open('/home/jaun/Downloads/SC-SfMLearner-Release-master/scripts/vo_results/17.txt')
fout = open('/home/jaun/glass_straight_SC.txt', "wt")



def to_4x4(pose3x4):
    pose4D = np.eye(4, dtype = np.float64)
    pose4D[:3,:] =  pose3x4
    return np.matrix(pose4D)

def SE2se(SE_data):
    """
    Converts a relative pose matrix (4x4)
    to euler format (1x6)
    """
    def SO2so(SO_data):
        return R.from_dcm(SO_data).as_rotvec()

    result = np.zeros((6))
    result[0:3] = SO2so(SE_data[0:3,0:3]).T
    result[3:6] = np.array(SE_data[0:3,3].T)
    return result

def rel_snips2abs(poses):
    output_poses = []
    pose = np.matrix(np.eye(4))
    kate = 0
    for i, snippet in enumerate(poses):  # for every snippet,
        kate += 1
        #multiply second relpose in snippet with prevpose
        pose = pose * to_4x4(snippet[1])
        pose1x6 = SE2se(pose)
        output_poses.append(pose1x6)
    return np.array(output_poses)
    print(kate)

for line in fin:
    linei = line.split()
    line_i = np.array(linei).reshape(3,4)
    a = to_4x4(line_i)
    b = SE2se(a)
    b = ["%1.19f" % member for member in b]
    print(*b, sep=', ', file=fout)

fout.close()

