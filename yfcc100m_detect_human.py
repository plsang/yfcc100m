#!/usr/bin/env python

# --------------------------------------------------------
# Copyright (c) 2015 NII
# Written by Sang Phan
# --------------------------------------------------------

import os
import sys
import os.path
import tables
from tables import *
import subprocess

import argparse

class Video(IsDescription):
    id              = StringCol(16)   # 16-character String
    title           = StringCol(256)   # 16-character String
    description     = StringCol(512)   # 16-character String
    user_tags       = StringCol(128)   # 16-character String
    machine_tags    = StringCol(128)   # 16-character String
    part_id         = Int8Col()
    
        
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Read YFCC100M tables')
    parser.add_argument('--s', dest='start', help='search by keyword', default=0, type=int)
    parser.add_argument('--e', dest='end', help='search by video id', default=sys.maxint, type=int)
    
    args = parser.parse_args()
    return args
    
if __name__ == '__main__':
    
    args = parse_args()
    
    h5file = open_file("/net/per610a/export/das11f/plsang/codes/yfcc100m/view/data/metadata/yfcc100m.h5", mode = "r")    
    
    table = h5file.root.video.yfcc100m
    
    key = 'park'
    
    if key is not None:
        rows = [(x['id'],x['part_id']) for x in table.where('contains(title,"' + key + '")') \
            or x in table.where('contains(description,"' + key + '")') \
            or x in table.where('contains(user_tags,"' + key + '")') \
            or x in table.where('contains(machine_tags,"' + key + '")') ]
    
    h5file.close()    
    
    root_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m'
    
    start_video = args.start
    end_video = args.end
    
    print start_video, end_video, len(rows)
    
    if start_video < 0:
        start_video = 0
        
    if end_video > len(rows):
        end_video = len(rows)
    
    for ii in range(start_video, end_video):
    #for row in rows:
        row = rows[ii]
        print row
        
        video_file = root_dir + '/yfcc100m_dataset-' + str(row[1]) + '/' + row[0] + '.mp4';
        if not os.path.isfile(video_file):
            print 'File not exist', video_file
            continue
        
        print 'Detecting human in video', video_file
        cmd = 'matlab -nodisplay -r "cd /net/per610a/export/das11f/plsang/codes/opensource/ped_detector_RELEASE/ped-demo-fast-8x8x1.1; ped_demo_video(\'{}\'); quit;"'.format(video_file);
        
        subprocess.check_output(cmd, shell=True, stderr=True)       
    

    
        