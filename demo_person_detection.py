"""
Read an input video, do person detection,
and save the detection outputs (e.g., bounding boxes) as a video.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms

from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
import argparse

import json, h5py
import logging
from datetime import datetime
import io
import PIL

logger = logging.getLogger(__name__)

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel')}

def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
            )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                  fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()

def detect_person(net, im):
    """Detect object classes in an image using pre-computed object proposals."""

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.5
    NMS_THRESH = 0.3
    
    cls_ind = 15 # person
    cls = CLASSES[cls_ind]
    
    cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
    cls_scores = scores[:, cls_ind]
    dets = np.hstack((cls_boxes,
                      cls_scores[:, np.newaxis])).astype(np.float32)
    keep = nms(dets, NMS_THRESH)
    dets = dets[keep, :]
    vis_detections(im, cls, dets, thresh=CONF_THRESH)
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('input_video', type=str, default='', help='Path to the input video!')
    parser.add_argument('output_video', type=str, default='', help='Path to the output video')
    parser.add_argument('--gid', dest='gid', help='GPU device id to use [-1]',
                        default=-1, type=int)
    parser.add_argument('--net', dest='net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='vgg16')
    
    args = parser.parse_args()
    start = datetime.now()
    
    if args.gid >= 0:
        caffe.set_mode_gpu()
        caffe.set_device(args.gid)
        cfg.GPU_ID = args.gid
    else:
        caffe.set_mode_cpu()
    
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals
    prototxt = os.path.join(cfg.MODELS_DIR, NETS[args.net][0],
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
    caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              NETS[args.net][1])
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    
    video_reader = cv2.VideoCapture(args.input_video)
    
    if video_reader.isOpened():
        fourcc = int(video_reader.get(cv2.cv.CV_CAP_PROP_FOURCC))
        fps = video_reader.get(cv2.cv.CV_CAP_PROP_FPS)
        width = int(video_reader.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(video_reader.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

        # MP4 codec does not work with OpenCV 2.4
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        video_writer = cv2.VideoWriter(args.output_video, fourcc, fps, (width, height))
        if not video_writer.isOpened():
            logger.error('Cannot open file for writing: %s', args.output_video)
            
        while(video_reader.isOpened()):
            ret, frame = video_reader.read()

            if ret==True:
                #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                detect_person(net, frame)
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                im = PIL.Image.open(buf).convert('RGB') 
                im = np.array(im) 
                # Convert RGB to BGR 
                im = im[:, :, ::-1].copy()
                im = cv2.resize(im, (width, height)) 
                cv2.imshow('frame', im)
                video_writer.write(im)
                buf.close()
                plt.close()
            else:
                break
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        
        video_writer.release()
        video_reader.release()
        cv2.destroyAllWindows()
        
    else:
        logger.error('Cannot open video file: %s', args.input_video)
    
    logger.info('Time: %s', datetime.now() - start)