3# Yolov7 + StrongSORT with OSNet





<div align="center">
<p>
<img src="MOT16_eval/track_pedestrians.gif" width="400"/> <img src="MOT16_eval/track_all.gif" width="400"/> 
</p>
<br>  
<a href="https://colab.research.google.com/drive/101f0PNBPx3245Hu710QAf2LXpf3E2uIk?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
 
 [![CI CPU testing](https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet/actions/workflows/ci-testing.yml/badge.svg)](https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet/actions/workflows/ci-testing.yml)
</div>

</div>


## Introduction

This repository contains a highly configurable two-stage-tracker that adjusts to different deployment scenarios. The detections generated by [YOLOv7](https://github.com/WongKinYiu/yolov7), a family of object detection architectures and models pretrained on the COCO dataset, are passed to [StrongSORT](https://github.com/dyhBUPT/StrongSORT)[](https://arxiv.org/pdf/2202.13514.pdf) which combines motion and appearance information based on [OSNet](https://github.com/KaiyangZhou/deep-person-reid)[](https://arxiv.org/abs/1905.00953) in order to tracks the objects. It can track any object that your Yolov7 model was trained to detect.

## Before you run the tracker

1. Clone the repository recursively:

`git clone --recurse-submodules https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet.git`

If you already cloned and forgot to use `--recurse-submodules` you can run `git submodule update --init`

2. Make sure that you fulfill all the requirements: Python 3.8 or later with all [requirements.txt](https://github.com/mikel-brostrom/Yolov7_DeepSort_Pytorch/blob/master/requirements.txt) dependencies installed, including torch>=1.7. To install, run:

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

By default the tracker tracks all MS COCO classes.

If you want to track a subset of the MS COCO classes, add their corresponding index after the classes flag

```bash
python track.py --source 0 --yolo-weights yolov7.pt --classes 16 17  # tracks cats and dogs, only
```

[Here](https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/) is a list of all the possible objects that a Yolov7 model trained on MS COCO can detect. Notice that the indexing for the classes in this repo starts at zero.

## Implementation Steps for inference in google colab

1. Clone the repository, navigate into its directory, install dependencies via `pip` or `requirements.txt`, check PyTorch installation using `import torch`, and verify GPU availability with `torch.cuda.is_available()`.

```bash
!git clone --recurse-submodules https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet.git  # clone repo
%pip install -qr requirements.txt  # install dependencies

import torch
from IPython.display import Image, clear_output  # to display images

clear_output()
print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")
```

2. Retrieve the test video from the repository and utilize a video processing library, such as OpenCV, to extract the first 2 seconds of it.

```bash
%cd /content/Yolov7_StrongSORT_OSNet

# get yolov5m model trained on the crowd-human dataset
!wget -nc https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt -O /content/Yolov7_StrongSORT_OSNet/yolov7.pt

# get the test video from the repo
!wget -nc https://github.com/mikel-brostrom/Yolov5_StrongSORT_OSNet/releases/download/v.2.0/test.avi
# extract 3 seconds worth of video frames of it
!yes | ffmpeg -ss 00:00:00 -i test.avi -t 00:00:02 -c copy out.avi
```

3. Download the test video from the repository, then use OpenCV to extract the initial 2 seconds, saving it to a file due to incompatibility with displaying in a Jupyter notebook, though local viewing with real-time tracking visualization is possible using the --show-vid flag.

```bash
!python track.py --yolo-weights /content/Yolov7_StrongSORT_OSNet/yolov7.pt --strong-sort-weights osnet_x0_25_msmt17.pt --source out.avi --save-vid --conf-thres 0.15 --device 0
```

4. Convert the extracted video from avi to mp4.

```bash
!ffmpeg -i /content/Yolov7_StrongSORT_OSNet/runs/track/exp/out.mp4 output.mp4
```

5. Get the file content into a data url.

```bash
from IPython.display import HTML
from base64 import b64encode
mp4 = open('output.mp4','rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
```

  Display the results with HTML

```bash
HTML("""
<video controls>
      <source src="%s" type="video/mp4">
</video>
""" % data_url)
```

## Replicate the Streamlit Application as shown in the sample output video. 
# Please note that this replication is done locally to ease the complexity of real time execution
# You might first want to install these dependencies and requirements

1. Create a new folder and clone the repository
```bash
git clone --recurse-submodules https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet.git
```

2. cd into the cloned folder and install the requirements using

```bash
 pip install -r requirements.txt
```

# IMPORTANT: Make sure to install the following packages before proceeding with the next steps
```bash
1. brew install pipx
2. pipx install streamlit
3. brew install torchvision
4. brew install wget
5. brew install ffmpeg
6. pipx install moviepy -include-deps
```

3. Install the weights for yolo

```bash
 wget -nc https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt

```

4. Download a sample video using

```bash
    wget -nc https://github.com/mikel-brostrom/Yolov5_StrongSORT_OSNet/releases/download/v.2.0/test.avi

```

5. Copy a small duration of this sample test video

```bash
    yes | ffmpeg -ss 00:00:00 -i test.avi -t 00:00:02 -c copy out.avi

```

6. Now, run the track.py on this sample video

```bash
    python track.py --yolo-weights yolov7.pt --strong-sort-weights osnet_x0_25_msmt17.pt --source out.avi --save-vid --conf-thres 0.15
```

7. Convert the avi file to an mp4

```bash
   ffmpeg -i /content/Yolov7_StrongSORT_OSNet/runs/track/exp/out.mp4 output.mp4
````

8. Now, download the app.py file in the code and store it inside the current "Yolov7_StrongSORT_OSNet". Then, run the command

```bash
     streamlit run app.py

```

## MOT compliant results

Can be saved to your experiment folder `runs/track/<yolo_model>_<deep_sort_model>/` by 

```bash
python track.py --source ... --save-txt
```


## Cite

If you find this project useful in your research, please consider cite:

```latex
@misc{yolov7-strongsort-osnet-2022,
    title={Real-time multi-camera multi-object tracker using YOLOv7 and StrongSORT with OSNet},
    author={Mikel Broström},
    howpublished = {\url{https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet}},
    year={2022}
}
```

## Contact 

For Yolov7 DeepSort OSNet bugs and feature requests please visit [GitHub Issues](https://github.com/mikel-brostrom/Yolov7_StrongSORT_OSNet/issues). For business inquiries or professional support requests please send an email to: yolov5.deepsort.pytorch@gmail.com
