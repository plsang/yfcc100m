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

import argparse

class Video(IsDescription):
    id              = StringCol(16)   # 16-character String
    title           = StringCol(256)   # 16-character String
    description     = StringCol(512)   # 16-character String
    user_tags       = StringCol(128)   # 16-character String
    machine_tags    = StringCol(128)   # 16-character String
    
        
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Read YFCC100M tables')
    parser.add_argument('--id', dest='vid', help='video id')
    
    args = parser.parse_args()
    return args
    
if __name__ == '__main__':
    
    args = parse_args()
    
    #parts = ['yfcc100m_dataset-'+str(i) for i in range(0,10)]
    
    h5file = open_file("/net/per610a/export/das11f/plsang/codes/yfcc100m/view/data/metadata/yfcc100m.h5", mode = "r")    
    
    table = h5file.root.video.yfcc100m
    
    #rows = [x['title'] for x in table.where('contains(title,"park")') \
    #    or x in table.where('contains(description,"park")') \
    #    or x in table.where('contains(user_tags,"park")') \
    #    or x in table.where('contains(machine_tags,"park")') ]
    
    condition = 'id == "' + args.vid + '"';
    rows = [(x['title'], x['description'], x['user_tags'], x['machine_tags']) for x in table.where(condition)]    
    
    if len(rows) > 0:
        for el in rows[0]:
            print el
        
        