# for resizing all the images in selected file
import PIL
import os
import os.path
from PIL import Image

# change the directory accordingly
f = r'/home/jaun/Downloads/SC-SfMLearner-Release-master/Dataset/kitti_odom_test/sequences/11/image_2'

for file in os.listdir(f):
    f_img = f + "/" + file
    img = Image.open(f_img)
    
    # resizes image to KITTI dataset size
    img = img.resize((1226,370))
    img.save(f_img)
