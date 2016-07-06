"""
Cut videos that contains a number of persons
"""


import os
import sys
import numpy as np
import os.path
import pymongo
from pymongo import MongoClient
import time
import argparse, logging
from datetime import datetime

logger = logging.getLogger(__name__)

######################################################################
        
if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s')
    
    parser = argparse.ArgumentParser(description='Cut videos that contains a number of persons')
    parser.add_argument('--video_dir', type=str, default='/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m', help='root video directory')
    parser.add_argument('--output_dir', type=str, default='/net/per920a/export/das14a/satoh-lab/plsang/yfcc10k', help='Directory to save cut video')
    parser.add_argument('--dbname', type=str, default='yfcc100m', help='Name of the mongodb datbase')
    parser.add_argument('--meta_collection', type=str, default='metadata', help='Name of mongodb collection')
    parser.add_argument('--person_collection', type=str, default='persons', help='Name of mongodb collection that will be saved person info')
    parser.add_argument('--min_person', dest='min_person', help='Minimum number of person', default=0, type=int)
    parser.add_argument('--max_person', dest='max_person', help='Minimum number of person', default=sys.maxint, type=int)
    parser.add_argument('--duration', dest='duration', help='duration of the cut video in seconds', default=5, type=int)
    parser.add_argument('--num_cpu', dest='num_cpu', help='duration of the cut video in seconds', default=1, type=int)
    parser.add_argument('--fps', dest='fps', help='frame rate', default=25, type=int)
    
    args = parser.parse_args()
    logger.info('Command-line arguments: %s', args)
    
    start = datetime.now()
    
    logger.info('Starting mongodb client')
    client = MongoClient()
    db = client[args.dbname]
    meta_collection = db[args.meta_collection]
    person_collection = db[args.person_collection]

    videos = person_collection.find({"$and": [{'num_person':{'$gt':(args.min_person-1)}},{'num_person':{'$lt':(args.max_person+1)}}]})
    
    videos = {v['id']:{'fps':v['fps'], \
                       'frame_count':v['frame_count'], \
                       'persons':v['persons'], \
                       'frames':v['frames']} for v in videos}
    
    for count, (k, v) in enumerate(videos.iteritems(), 1):
        logger.info('[%d/%d] Cutting video %s', count, len(videos), k)
        max_person = max(v['persons'])
        max_idx = v['persons'].index(max_person)
        start_frame = v['frames'][max_idx]
        start_time = start_frame/v['fps']

        end_time = start_time + args.duration
        total_duration = v['frame_count']/v['fps']
        if end_time > total_duration:
            logger.warning('Cut video is too short! Skipped!')
            continue
                           
        meta_info = meta_collection.find({'id': k})
        assert(meta_info.count() == 1)
        part_id = meta_info[0]['part_id']

        video_file = os.path.join(args.video_dir, 'yfcc100m_dataset-' + str(part_id), k + '.mp4')
        if not os.path.isfile(video_file):
            logger.warning('File not exist: %s', video_file)
            continue
            
        output_mp4_file = os.path.join(args.output_dir, k + '_' + str(start_frame) + '.mp4')
        if os.path.isfile(output_mp4_file):
            logger.warning('File exist: %s. Skipped!', output_mp4_file)
            continue
        
        output_webm_file = os.path.join(args.output_dir, k + '.webm')
        
        try:
            start_time = time.strftime('%H:%M:%S', time.gmtime(start_time))
            cmd = 'ffmpeg -i {} -r {} -loglevel quiet -ss {} -t {} -async 1 {}'.format(
                video_file, args.fps, start_time, args.duration, output_mp4_file)
            logger.info('Cutting video: %s', cmd)
            os.system(cmd)

            cmd = 'ffmpeg -i {} -r {} -loglevel quiet -vcodec libvpx -cpu-used {} {}'.format(
                output_mp4_file, args.fps, args.num_cpu, output_webm_file)
            logger.info('Convert to webm format: %s', cmd)
            os.system(cmd)

            logger.info('Remove old mp4 file: %s', output_mp4_file)
            os.remove(output_mp4_file)

            cmd = 'ffmpeg -fflags +genpts -i {} -r {} -loglevel quiet -cpu-used {} {}'.format(
                output_webm_file, args.fps, args.num_cpu, output_mp4_file)
            logger.info('Convert to mp4 format: %s', cmd)
            os.system(cmd)

            logger.info('Remove webm file: %s', output_webm_file)
            os.remove(output_webm_file)
            
        except:
            logger.warning("Unexpected error: %s", sys.exc_info()[0])

    logger.info('Time: %s', datetime.now() - start)
