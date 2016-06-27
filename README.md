# YFCC100M Project

## Download YFCC100M dataset

## Installation
* [Faster RCNN](https://github.com/rbgirshick/py-faster-rcnn)
* OpenCV (built with ffmpeg and Python binding)
* PyMongo

## Demo
* Detect human in video and output a video file with annotated bounding boxes of detected person
```
python read_video.py $(YFCC_ROOT)/park_1_5_split_selected-webm-mp4/2956592867-1.mp4 out.avi --gid 0
```

## Person detection
* Create a mongodb table
```
python yfcc100m_create_table.py /path/to/video/directory --dbname yfcc100m --collection metadata
```

* Running person detection, and store the output in the `persons` collection
```
python yfcc100m_person_detection.py --person_collection persons --gid=3 2>&1 | tee log/yfcc100m_person_detection.log
```
