# Human Object Tracking 
## Yolov7 + StrongSORT with OSNet

<div align="center">
<p>
<img src="TrackingContent/Track_Horse.png" width="400" height="225"/> <img src="TrackingContent/track_all.gif" width="400" /> 
</p>
<br>  
</div>

</div>


## Introduction

In the realm of computer vision, object tracking stands as a crucial application, pivotal in realms ranging from surveillance to autonomous driving. This project harnesses the power of state-of-the-art models, integrating YOLOv7 for object detection with StrongSORT and OSNet for robust and precise object tracking. The integration aims to enhance tracking accuracy and real-time performance, making it particularly valuable in scenarios where human object tracking is critical.

Our approach leverages YOLOv7 for its exceptional capability in detecting objects with high accuracy and speed. For the tracking component, we employ StrongSORT, which enhances the SORT (Simple Online and Realtime Tracking) algorithm by integrating more powerful features and association metrics. To further boost the tracking performance, OSNet is utilized for its cutting-edge deep learning architecture designed for re-identifying objects, ensuring that the tracked subjects are followed accurately across different frames, even in challenging conditions.

## Before running the tracker

1. We can clone the repository recursively:

`git clone --recurse-submodules https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet.git`


2. Ensure you meet all prerequisites: 
   Python version 3.8 or newer with all dependencies listed in [requirements.txt], including torch>=1.7.
   To install them, execute the following command:
   
`pip install -r requirements.txt`


## Tracking sources

Tracking can be run on most video formats

```bash
$ python track.py --source 0  # webcam
                           img.jpg  # image
                           vid.mp4  # video
                           path/  # directory
                           path/*.jpg  # glob
                           'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                           'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream
```


## Select object detection and ReID model

### Yolov7

There is a clear trade-off between model inference speed and accuracy. In order to make it possible to fulfill your inference speed/accuracy needs
you can select a Yolov7 family model for automatic download

```bash


$ python track.py --source 0 --yolo-weights yolov7.pt --img 640
                                            yolov7x.pt --img 640
                                            yolov7-e6e.pt --img 1280
                                            ...
```

### StrongSORT

The above applies to StrongSORT models as well. Choose a ReID model based on your needs from this ReID [model zoo](https://kaiyangzhou.github.io/deep-person-reid/MODEL_ZOO)

```bash


$ python track.py --source 0 --strong-sort-weights osnet_x0_25_market1501.pt
                                                   osnet_x0_5_market1501.pt
                                                   osnet_x0_75_msmt17.pt
                                                   osnet_x1_0_msmt17.pt
                                                   ...
```


## Filter tracked classes

By default, the tracker monitors all MS COCO classes.

To track a specific subset of MS COCO classes, append their respective indices after the classes flag.


```bash
python track.py --source 0 --yolo-weights yolov7.pt --classes 16 17  # tracks cats and dogs, only
```

You can find a comprehensive list of all the objects detectable by a Yolov7 model trained on MS COCO here (https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/). 
Note that the indexing for classes in this repository begins at zero.


## Save Multiple Object Tracking Compliant Results
You can save MOT-compliant results to your experiment folder at `runs/track/<yolo_model>_<deep_sort_model>/` using the following command:

```bash
python track.py --source ... --save-txt
```
