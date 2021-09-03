# code for creating KITTI format Groundtruth file from ios_logger ARposes.txt (changes format from quaternion to rotation matrix)
import numpy as np

f = open('/home/eunju/Downloads/ARposes.txt', "rt")
fout = open('/home/eunju/Downloads/ARposes1.txt', "wt")

for line in f:
    fout.write(line.replace(',', ' '))

f.close()
fout.close()

def quaternion_rotation_matrix(Q):
    """
    Covert a quaternion into a full three-dimensional rotation matrix.

    Input
    :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3)

    Output
    :return: A 3x3 element matrix representing the full 3D rotation matrix.
             This rotation matrix converts a point in the local reference
             frame to a point in the global reference frame.
    """
    # Extract the values from Q
    q0 = Q[0]
    q1 = Q[1]
    q2 = Q[2]
    q3 = Q[3]

    # First row of the rotation matrix
    r00 = 2 * (q0 * q0 + q1 * q1) - 1
    r01 = 2 * (q1 * q2 - q0 * q3)
    r02 = 2 * (q1 * q3 + q0 * q2)

    # Second row of the rotation matrix
    r10 = 2 * (q1 * q2 + q0 * q3)
    r11 = 2 * (q0 * q0 + q2 * q2) - 1
    r12 = 2 * (q2 * q3 - q0 * q1)

    # Third row of the rotation matrix
    r20 = 2 * (q1 * q3 - q0 * q2)
    r21 = 2 * (q2 * q3 + q0 * q1)
    r22 = 2 * (q0 * q0 + q3 * q3) - 1

    # 3x3 rotation matrix
    rot_matrix = np.array([[r00, r01, r02],
                           [r10, r11, r12],
                           [r20, r21, r22]])

    return rot_matrix

input = open('/home/eunju/Downloads/ARposes1.txt', "rt")
output = open('/home/eunju/Downloads/ARposes_half.txt', "wt")
i = 0
count = 1

for line in input:

    t = []
    Q = []
    out = []

    linei = line.split()

# aligns x, y, z to (0,0,0)
    if count == 1:
        key = [float(linei[1]), float(linei[2]), float(linei[3])]
    count = 2

    t = [float(linei[1])-key[0], float(linei[2])-key[1], float(linei[3])-key[2]]
    Q = [float(linei[4]), float(linei[5]), float(linei[6]), float(linei[7])]

    matrix = quaternion_rotation_matrix(Q)
    out = matrix[0]
    out = np.append(out, t[0])
    out = np.append(out, matrix[1])
    out = np.append(out, t[1])
    out = np.append(out, matrix[2])
    out = np.append(out, t[2])
    out = ["%1.6e" % member for member in out]
    #print(str(out) + '\n')
    i += 1

#ios_logger (30hz), need to divide by half
    if i%2 != 0:
        print(*out, sep=' ', file = output)
        output.write('')

input.close()
output.close()
