"""
Create a thumbnail image for each video
"""

import os
import sys
import numpy as np
import os.path
import time
import argparse, logging
from datetime import datetime

logger = logging.getLogger(__name__)

######################################################################
        
if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s')
    
    parser = argparse.ArgumentParser(description='Create a thumbnail image for each video in a specified directory')
    parser.add_argument('--video_dir', type=str, default='/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/yfcc10k', help='root video directory')
    parser.add_argument('--output_dir', type=str, default='/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/yfcc10k_thumbnails', help='Directory to save thumbnail images')
    parser.add_argument('--video_ext', type=str, default='.mp4', help='extension of the input video files')
    parser.add_argument('--thumbnail_ext', type=str, default='.jpg', help='extension of the output thumbnail files')
    parser.add_argument('--cut_position', type=int, default=0, help='position (in second) to cut. Eg. 0 is the beginning of video.')
    
    args = parser.parse_args()
    logger.info('Command-line arguments: %s', args)
    
    start = datetime.now()
    
    for f in os.listdir(args.video_dir):
        if f.endswith(args.video_ext):
            o = f.replace(args.video_ext, args.thumbnail_ext)
            input_file = os.path.join(args.video_dir, f)
            output_file = os.path.join(args.output_dir, o)
            start_time = time.strftime('%H:%M:%S', time.gmtime(args.cut_position))
            
            cmd = 'ffmpeg -i {} -ss {} -vframes 1 {}'.format(input_file, start_time, output_file)
            logger.info(cmd)
            
            try:
                os.system(cmd)
            except:
                logger.warning("Unexpected error: %s", sys.exc_info()[0])
        
    logger.info('Time: %s', datetime.now() - start)
