# Introduction
Darknet python interface. Tested only in Python3.6, Jetpack4.4, Ubuntu 16.04 and Ubuntu 18.04.

# Pre-Installation
1. darknet: please set the DARKNET_PATH with libdarknet.so file in environmental varaible. If you don't know how to compile darknet to generate libdarknet.so, please refer to the following commands.
```
# in the darknet path
import os
import shutil
shutil.copyfile('Makefile', 'Makefile_copy')
with open('Makefile', 'w') as fw, open('Makefile_copy', 'r') as fr:
    for line in fr:
        if line in ['GPU=0\n', 'CUDA=0\n', 'CUDNN=0\n' , 'CUDNN_HALF=0\n', 'LIBSO=0\n', 'OPENCV=0\n']: # 'DEBUG=0\n'
           fw.write(line.replace('=0', '=1'))
        else:
            fw.write(line)
exit()
```


# Installation
```
pip3 install Yolov4Detector
```

# Usage
## image
```python3
import cv2
from Yolov4Detector import io, Detector
from Yolov4Detector.utils import plot_one_box

# initialize Detector
cfg_fp, names_fp, weights_fp= get_test_params()
detector = Detector(cfg_fp, names_fp, weights_fp)
img_fp = io.get_test_data('bus')

image_bgr = cv2.imread(img_fp)
boxes, confs, clses = detector.detect(image_bgr, conf_thres=0.15, iou_thres=0.6)
if len(boxes) != 0:
    for xyxy, conf, cls in zip(boxes, confs, clses):
        plot_one_box(xyxy, image_bgr, label=cls, color=(255, 0, 0))
        print(xyxy, conf, cls)

cv2.imshow('img', image_bgr) 
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## video
```python
import cv2
from datetime import datetime, timedelta
from Yolov4Detector import io, Detector
from Yolov4Detector.utils import plot_one_box

cfg_fp, names_fp, weights_fp= get_test_params()
detector = Detector(cfg_fp, names_fp, weights_fp)
img_fp = '<video_fp>'

cap = cv2.VideoCapture(img_fp)
count = 0
st = datetime.now()
while(True):
    ret, image_bgr = cap.read()

    conf_thres = 0.15
    iou_thres = 0.6
    boxes, confs, clses = detector.detect(image_bgr, conf_thres=conf_thres, iou_thres=iou_thres)
    if boxes is not None:
        for xyxy, conf, cls in zip(boxes, confs, clses):
            plot_one_box(xyxy, image_bgr, label=cls, color=(255, 0, 0))


    cv2.imshow('frame', image_bgr)
    count += 1
    if datetime.now()- st > timedelta(seconds=1):
        print("fps:", count)
        count = 0
        st = datetime.now()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
```
