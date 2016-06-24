"""
Perform person detection in videos
"""


import os
import sys
import numpy as np
import os.path
import pymongo
from pymongo import MongoClient
import re
import argparse, logging
from datetime import datetime

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import caffe, cv2


logger = logging.getLogger(__name__)

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel')}

def detect_person(net, im, opt):
    """Detect object classes in an image using pre-computed object proposals."""

    # Detect all object classes and regress object bounds
    
    scores, boxes = im_detect(net, im)
    cls_boxes = boxes[:, 4*opt['cls_ind']:4*(opt['cls_ind'] + 1)]
    cls_scores = scores[:, opt['cls_ind']]
    dets = np.hstack((cls_boxes,
                      cls_scores[:, np.newaxis])).astype(np.float32)
    keep = nms(dets, opt['tnms'])
    dets = dets[keep, :]
    inds = np.where(dets[:, -1] >= opt['tconf'])[0]
    sel_dets = dets[inds, :]
    return sel_dets

######################################################################
        
if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s')
    
    parser = argparse.ArgumentParser(description='Perform person detection for video selection')
    parser.add_argument('--video_dir', type=str, default='/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m', help='root video directory')
    parser.add_argument('--dbname', type=str, default='yfcc100m', help='Name of the mongodb datbase')
    parser.add_argument('--collection', type=str, default='metadata', help='Name of mongodb collection')
    parser.add_argument('--person_collection', type=str, default='persons', help='Name of mongodb collection that will be saved person info')
    parser.add_argument('--s', dest='start', help='search by keyword', default=0, type=int)
    parser.add_argument('--e', dest='end', help='search by video id', default=sys.maxint, type=int)
    parser.add_argument('--gid', dest='gid', help='GPU device id to use [-1]',
                        default=0, type=int)
    parser.add_argument('--net', dest='net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='vgg16')
    parser.add_argument('--cls_ind', dest='cls_ind', help='Class index in PASCAL VOC, set to 15 for person',
                        default=15, type=int)
    parser.add_argument('--tconf', dest='tconf', help='Confident threshold',
                        default=0.5, type=float)
    parser.add_argument('--tnms', dest='tnms', help='Non-maximum suppression threshold',
                        default=0.3, type=float)
    parser.add_argument('--detect_interval', dest='detect_interval', help='number of seconds between two consecutive detections',
                        default=1.0, type=float)
    
    args = parser.parse_args()
    logger.info('Command-line arguments: %s', args)
    
    logger.info('Starting mongodb client')
    client = MongoClient()
    db = client[args.dbname]
    collection = db[args.collection]
    person_collection = db[args.person_collection]
    person_collection.create_index([('id', pymongo.ASCENDING)], unique=True)
    
    #logger.info('search for videos that contain `park` in their descriptions')
    #regex = re.compile("park", re.IGNORECASE)
    
    logger.info('Search for videos where descriptions are non-empty')
    regex = re.compile(".+")
    
    # rows = collection.find({"description": regex}).sort('id') # 237,602 videos, failed to sort
    rows = collection.find({"description": regex}) # 237,602 videos
    videos = [(row['id'], row['part_id']) for row in rows]
    
    start_video = args.start
    end_video = args.end
    num_video = len(videos)
    
    if start_video < 0:
        start_video = 0
        
    if end_video > num_video:
        end_video = num_video
    
    logger.info('Loading RCNN model...')
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
    
    logger.info('Processing videos: %d, Start video: %d, End video: %d', num_video, start_video, end_video)
    start = datetime.now()
    
    det_opt = {'tconf': args.tconf, 'tnms': args.tnms, 'cls_ind': args.cls_ind}
    
    for ii in range(start_video, end_video):
        info = videos[ii]
        
        video_file = args.video_dir + '/yfcc100m_dataset-' + str(info[1]) + '/' + info[0] + '.mp4';
        if not os.path.isfile(video_file):
            logger.warning('File not exist: %s', video_file)
            continue
        
        logger.info('[%d/%d] Detecting human in video: %s', ii-start_video, end_video-start_video, video_file)
        
        video_reader = cv2.VideoCapture(video_file)
    
        if video_reader.isOpened():
            timer = Timer()
            timer.tic()
            fps = video_reader.get(cv2.cv.CV_CAP_PROP_FPS)
            frame_count = video_reader.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            frame_interval = int(round(fps * args.detect_interval))
            
            frames = []
            persons = []
            boxes = []
            while(video_reader.isOpened()):
                frame_number = int(round(video_reader.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)))
                ret, frame = video_reader.read()
                if ret==True:
                    if frame_number % frame_interval == 0:
                        dets = detect_person(net, frame, det_opt)
                        frames.append(frame_number)
                        persons.append(dets.shape[0])
                        boxes.append(dets.tolist())
                else:
                    break
            video_reader.release()
            
            video = {}
            video['id'] = info[0]
            video['fps'] = fps
            video['frame_count'] = frame_count
            video['num_person'] = max(persons)
            video['frames'] = frames
            video['persons'] = persons
            video['boxes'] = boxes
            person_collection.insert_one(video)
            
            timer.toc()
            logger.info('Detected (max) {:d} person(s) in {:.3f}s'.format(video['num_person'], timer.total_time))
        else:
            logger.warning('Cannot open video file: %s', args.input_video)

    logger.info('Time: %s', datetime.now() - start)
        