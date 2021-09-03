import matplotlib.pyplot as plt
import numpy as np
import time
from params import par
import math
from collections import OrderedDict

#change directory accordingly
pose_GT_dir = 'KITTI/pose_GT/'
#predicted_result_dir = '/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/'
predicted_result_dir = '/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/straightGlass_final/'
gradient_color = False

#you can choose out of these linestyles
linestyles_dict = OrderedDict(
    [('solid',               (0, ())),
     ('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     ('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 1))),

     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])

# plotting all the VO trajectories
def plot_route(gt, deep, sfm, sc, dfvo, c_gt='g', c_deep='r', c_sfm='b', c_sc='c', c_dfvo = 'k', avg1=None, avg2=None, avg3=None, avg4 = None):
    #plot ground truth
    x_idx = 3
    y_idx = 5
    x = [v for v in gt[:, x_idx]]
    y = [v for v in gt[:, y_idx]]
    plt.plot(x, y, color=c_gt, label='Ground Truth')
    # plt.scatter(x, y, color='b')

    #plot DeepVO
    x = [v for v in deep[:, x_idx]]
    y = [v for v in deep[:, y_idx]]
    plt.plot(x, y, color=c_deep, linestyle=':', label='DeepVO')
    # plt.scatter(x, y, color='b')
    plt.gca().set_aspect('equal', adjustable='datalim')

    #plot SfMLearner
    x = [v*1.9 for v in sfm[:, x_idx]]
    y = [v*1.9 for v in sfm[:, y_idx]]
    plt.plot(x, y, color=c_sfm, linestyle='--', label='SfMLearner')
    # plt.scatter(x, y, color='b')
    plt.gca().set_aspect('equal', adjustable='datalim')

    #plot SC-SfMLearner
    x = [v*9 for v in sc[:, x_idx]]
    y = [v*9 for v in sc[:, y_idx]]
    plt.plot(x, y, color=c_sc, linestyle='-.', label='SC-SfMLearner')
    # plt.scatter(x, y, color='b')
    plt.gca().set_aspect('equal', adjustable='datalim')

    #plot DF-VO
    x = [v for v in dfvo[:, x_idx]]
    y = [v for v in dfvo[:, y_idx]]
    plt.plot(x, y, color=c_dfvo, linestyle=linestyles_dict['densely dashdotted'], label='DF-VO')
    # plt.scatter(x, y, color='b')
    plt.gca().set_aspect('equal', adjustable='datalim')

    
# the scaling factor still needs to be fixed
def scale_measure(method):
    scale_1 = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/straightGlass_final/{}_{}.txt'.format(method, video), "rt")
    scale_2 = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/straightGlass_final/{}_{}_scale.txt'.format(method, video), "wt")
    #
    for line in scale_1:
        #fout.write(line.replace(' ', ','))
        scale_2.write(line.replace(',', ''))
    scale_1.close()
    scale_2.close()
    tx = []
    ty = []
    tz = []
    l1 = []
    l2 = []
    length = []
    count = 0
    scale = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/straightGlass_final/{}_{}_scale.txt'.format(method, video))
    #with open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/{}scale.txt'.format(video)) as scale1, open()
    for line in scale:
        t = []
        linei = line.split()
        t = [float(linei[3]), float(linei[4]), float(linei[5])]
        tx = np.append(tx, t[0])
        ty = np.append(ty, t[1])
        tz = np.append(tz, t[2])
            #
        a = np.array([tx, ty])
        t_xyz = np.append(a, [tz], axis=0)

    gt_x = gt[:, 3]
    gt_y = gt[:, 4]
    gt_z = gt[:, 5]
    b = np.array([gt_x, gt_y])
    gt_xyz = np.append(b, [gt_z], axis=0)
    avg = np.sum(gt_xyz * t_xyz) / np.sum(t_xyz ** 2)

    return avg

video_list = ['17']
#choose your video sequence number

#method_list = ['deep','sc','sfm']

for video in video_list:
    print('=' * 50)
    print('Video {}'.format(video))

    GT_pose_path = '{}{}.npy'.format(pose_GT_dir, video)
    gt = np.load(GT_pose_path)
    pose_result_path_deep = '{}deep_{}.txt'.format(predicted_result_dir, video)
    pose_result_path_sfm = '{}sfm_{}.txt'.format(predicted_result_dir, video)
    pose_result_path_sc = '{}sc_{}.txt'.format(predicted_result_dir, video)
    pose_result_path_dfvo = '{}dfvo_{}.txt'.format(predicted_result_dir, video)

    # outputs error results: RMSE(rotation, translation)
    with open(pose_result_path_deep) as f_out_1:
        out = [l.split('\n')[0] for l in f_out_1.readlines()]
        for i, line in enumerate(out):
            out[i] = [float(v) for v in line.split(',')]
        deep = np.array(out)
        mse_rotate = 100 * np.mean((deep[:, :3] - gt[:, :3]) ** 2)
        mse_translate = np.mean((deep[:, 3:]*0.8 - gt[:, 3:6]) ** 2)
        print('DeepVO_mse_rotate: ', mse_rotate)
        print('DeepVO_mse_translate: ', mse_translate)
        print("------------")

    with open(pose_result_path_sfm) as f_out_2:
        out = [l.split('\n')[0] for l in f_out_2.readlines()]
        for i, line in enumerate(out):
            out[i] = [float(v) for v in line.split(',')]
        sfm = np.array(out)
        mse_rotate = 100 * np.mean((sfm[:, :3] - gt[:, :3]) ** 2)
        mse_translate = np.mean((sfm[:, 3:]*7 - gt[:, 3:6]) ** 2)
        print('SfMLearner_mse_rotate: ', mse_rotate)
        print('SfMLearner_mse_translate: ', mse_translate)
        print("------------")

    with open(pose_result_path_sc) as f_out_3:
        out = [l.split('\n')[0] for l in f_out_3.readlines()]
        for i, line in enumerate(out):
            out[i] = [float(v) for v in line.split(',')]
        sc = np.array(out)
        mse_rotate = 100 * np.mean((sc[:, :3] - gt[:, :3]) ** 2)
        mse_translate = np.mean((sc[:, 3:]*16 - gt[:, 3:6]) ** 2)
        print('SC-SfMLearner_mse_rotate: ', mse_rotate)
        print('SC-SfMLearner_mse_translate: ', mse_translate)
        print("------------")

    with open(pose_result_path_dfvo) as f_out_3:
        out = [l.split('\n')[0] for l in f_out_3.readlines()]
        for i, line in enumerate(out):
            out[i] = [float(v) for v in line.split(',')]
        dfvo = np.array(out)
        mse_rotate = 100 * np.mean((dfvo[:, :3] - gt[:, :3]) ** 2)
        mse_translate = np.mean((dfvo[:, 3:] * 7 - gt[:, 3:6]) ** 2)
        print('DFVO_mse_rotate: ', mse_rotate)
        print('DFVO_mse_translate: ', mse_translate)
        print("------------")
     
    plt.clf()
    plt.scatter([gt[0][3]], [gt[0][5]], label='sequence start', marker='s', color='k')
    plot_route(gt, deep, sfm, sc, dfvo,  'g', 'r', 'b', 'c', 'k', scale_measure('deep'),scale_measure('sfm'),scale_measure('sc'), scale_measure('dfvo'))
    plt.legend()
    save_name = '{}route_{}.png'.format(predicted_result_dir, video)
    plt.savefig(save_name)
