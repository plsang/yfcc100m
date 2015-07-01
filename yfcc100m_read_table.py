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

class Video(IsDescription):
    id              = StringCol(16)   # 16-character String
    title           = StringCol(256)   # 16-character String
    description     = StringCol(512)   # 16-character String
    user_tags       = StringCol(128)   # 16-character String
    machine_tags    = StringCol(128)   # 16-character String
    
    
            
if __name__ == '__main__':

    parts = ['yfcc100m_dataset-'+str(i) for i in range(0,10)]
    
    input_dir = '/net/per610a/export/das11f/plsang/dataset/YFCC100M'
    output_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata'

    h5file = open_file("/net/per610a/export/das11f/plsang/codes/yfcc100m/view/data/metadata/yfcc100m.h5", mode = "r")    
    
    table = h5file.root.video.yfcc100m_dataset_1
    
    rows = [x['title'] for x in table.where('contains(title,"park")')]
    for row in rows:
        print row
        
        