#visualization of the pose estimations in 3D
import matplotlib.pyplot as plt
import numpy as np
import time
from params import par
import math
from collections import OrderedDict
import matplotlib.ticker as mticker
from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')

pose_GT_dir = par.pose_dir  # 'KITTI/pose_GT/'

#change the directory accordingly
#predicted_result_dir = '/home/jaun/Downloads/DeepVO-pytorch-master/KITTI/result/'
predicted_result_dir = '/home/jaun/Downloads/result/dynamic_11_1/'
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


def plot_route(gt, deep, sfm, sc, dfvo, c_gt='g', c_deep='r', c_sfm='b', c_sc='c', c_dfvo = 'k', avg1=None,avg2=None,avg3=None, avg4 = None):
    x_idx = 3
    y_idx = 4
    z_idx = 5
    x = [v for v in gt[:, x_idx]]
    y = [v for v in gt[:, y_idx]]
    z = [v for v in gt[:, z_idx]]
    ax.plot3D(x, y, z, color=c_gt, label='Ground Truth')
    # plt.scatter(x, y, color='b')

    x = [v for v in deep[:, x_idx]]
    y = [v for v in deep[:, y_idx]]
    z = [v for v in deep[:, z_idx]]
    ax.plot3D(x, y,z, color=c_deep, linestyle=':', label='DeepVO')
    # plt.scatter(x, y, color='b')


    x = [v for v in sfm[:, x_idx]]
    y = [v for v in sfm[:, y_idx]]
    z = [v for v in sfm[:, z_idx]]
    ax.plot3D(x, y, z, color=c_sfm, linestyle='--', label='SfMLearner')
    # plt.scatter(x, y, color='b')

    x = [v for v in sc[:, x_idx]]
    y = [v for v in sc[:, y_idx]]
    z = [v for v in sc[:, z_idx]]
    ax.plot3D(x, y, z, color=c_sc, linestyle='-.', label='SC-SfMLearner')
    # plt.scatter(x, y, color='b')


    x = [v for v in dfvo[:, x_idx]]
    y = [v for v in dfvo[:, y_idx]]
    z = [v for v in dfvo[:, z_idx]]
    ax.plot3D(x, y, z, color=c_dfvo, linestyle=linestyles_dict['densely dashdotted'], label='DF-VO')
    # plt.scatter(x, y, color='b')


def scale_measure(method):
    scale_1 = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/dynamic_11_1/{}_{}.txt'.format(method, video), "rt")
    scale_2 = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/dynamic_11_1/{}_{}_scale.txt'.format(method, video), "wt")
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
    scale = open('/media/jaun/로컬 디스크/DeepVO-pytorch-master/KITTI/result/dynamic_11_1/{}_{}_scale.txt'.format(method, video))
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

            # if len(tx) >= 2:
            # x1 = tx[0]
            # x2 = tx[1]
            # y1 = ty[0]
            # y2 = ty[1]
            # z1 = tz[0]
            # z2 = tz[1]
            # l1.append(math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2))
            # tx = np.delete(tx, 0)
            # ty = np.delete(ty, 0)
            # tz = np.delete(tz, 0)
            # print(count)
            # l2.append(math.sqrt((gt[count][3]-gt[count+1][3])**2 + (gt[count][4]-gt[count+1][4])**2 + (gt[count][5]-gt[count+1][5])**2))
            # count += 1
            # print(l1)
            # print(l2)
            # print(len(l1))
            # print(len(l2))

            # if count == 5000:
            #
            # break
        # for i in range(len(l1)):
        # length.append(l1[i]/l2[i])
        # print(length)
        # avg = (sum(length)/len(length))
        # scale.close()
        # print(avg)

        # print(t_xyz)

    gt_x = gt[:, 3]
    gt_y = gt[:, 4]
    gt_z = gt[:, 5]
    b = np.array([gt_x, gt_y])
    gt_xyz = np.append(b, [gt_z], axis=0)
    avg = np.sum(gt_xyz * t_xyz) / np.sum(t_xyz ** 2)

    return avg

# Load in GT and predicted pose
#video_list = ['00', '02', '08']
#video_list += ['01', '04', '05', '06', '07']
video_list = ['20']
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

    if gradient_color:
        # plot gradient color
        step = 200
        plt.clf()
        plt.scatter([gt[0][3]], [gt[0][5]], label='sequence start', marker='s', color='k')
        for st in range(0, len(out), step):
            end = st + step
            g = max(0.2, st / len(out))
            c_gt = (0, g, 0)
            c_out = (1, g, 0)
            plot_route(gt[st:end], out[st:end], c_gt, c_out, avg)
            if st == 0:
                plt.legend()
            plt.title('Video {}'.format(video))
            save_name = '{}route_{}_gradient.png'.format(predicted_result_dir, video)
        plt.savefig(save_name)
    else:
        # plot one color
        #plt.clf()
        ax.scatter3D([gt[0][3]], [gt[0][4]], [gt[0][5]], label='sequence start', marker='s', color='k')
        plot_route(gt, deep, sfm, sc, dfvo, 'g', 'r', 'b', 'c', 'k')
        #ax.legend()
        save_name = '{}route_{}.png'.format(predicted_result_dir, video)
        plt.savefig(save_name)
