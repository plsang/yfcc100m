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
    part_id         = Int8Col()
    
        
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Read YFCC100M tables')
    parser.add_argument('--key', dest='key', help='search by keyword')
    parser.add_argument('--vid', dest='vid', help='search by video id')
    
    args = parser.parse_args()
    return args
    
if __name__ == '__main__':
    
    args = parse_args()
    
    h5file = open_file("/net/per610a/export/das11f/plsang/codes/yfcc100m/view/data/metadata/yfcc100m.h5", mode = "r")    
    
    table = h5file.root.video.yfcc100m
    
    if args.key is not None:
        rows = [(x['id'],x['part_id']) for x in table.where('contains(title,"' + args.key + '")') \
            or x in table.where('contains(description,"' + args.key + '")') \
            or x in table.where('contains(user_tags,"' + args.key + '")') \
            or x in table.where('contains(machine_tags,"' + args.key + '")') ]
    elif args.vid is not None:
        rows = [(x['part_id']) for x in table.where('id=="' + args.vid + '"')]
    
    if len(rows) > 0:
        for row in rows:
            print row
        
        