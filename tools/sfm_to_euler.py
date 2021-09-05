# file for changing sfmlearner pose estimation result(5-frame snippet) to euler form
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

data = np.load("/home/jaun/Downloads/SfmLearner-Pytorch-master/output/pose/17/predictions.npy")
fout = open('/home/jaun/21_1.txt', "wt")

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


a = rel_snips2abs(data)
for i in a:
    i = ["%1.19f" % member for member in i]
    print(*i, sep=', ', file=fout)
