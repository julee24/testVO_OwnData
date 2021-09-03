# testVO_OwnData
Codes to help prepare your own datasets for testing VO algorithms.

This was made to test and evaluate specifically four VO algorithms: DeepVO, SfMLearner, SC-SfMLearner, DF-VO\
Run on Ubuntu 18.04

# Collect datasets:
You can use ios_logger by Varvar to collect datasets using ARKit VIO algorithms.

Change the video Frames.m4v to continuous images using\
``` ffmpeg -i Frames.m4v image_2/%06d.png -hide_banner ```

Run ```resize_image.py``` to resize the images according to the KITTI dataset.

With the ARposes.txt created from ios_logger run the file ```groundTruth.py```to get the txt file of\
ground truth in rotation matrix format:
```r11, r12, r13, tx, r21, r22, r23, ty, r31, r32, r33, tz```

