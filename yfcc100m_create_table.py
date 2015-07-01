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
import urllib

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

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

    h5file = open_file("/net/per610a/export/das11f/plsang/codes/yfcc100m/view/data/metadata/yfcc100m.h5", mode = "w", title = "YFCC100M")    
    
    group = h5file.create_group("/", 'video', 'Yfcc100m video')
    
    for part in parts:
        
        print 'Gen table for part', part
        
        table_name = 'yfcc100m_dataset_' + str(parts.index(part))
        
        table = h5file.create_table(group, table_name, Video, "Yfcc100m part")
        
        video = table.row
        
        meta_file = os.path.join(input_dir, part)
        
        with open(meta_file) as f:
            for line in f:
                info = line.rstrip('\n').split('\t');
                if info[-1] == '1':
                    video['id'] = info[0]
                    video['title'] = strip_tags(urllib.unquote_plus(info[6]))
                    video['description'] = strip_tags(urllib.unquote_plus(info[7]))
                    video['user_tags'] = strip_tags(urllib.unquote_plus(info[8]))
                    video['machine_tags'] = strip_tags(urllib.unquote_plus(info[9]))
                    video.append()
                    
        table.flush()
        #print table[0]['id'], table[0]['title'], table[0]['description'], table[0]['user_tags'], table[0]['machine_tags'], 
        #print '-- ID:', table[0]['id']
        #print '-- Title:', table[0]['title']
        #print '-- Description:', table[0]['description']
        #print '-- User tags:', table[0]['user_tags']
        #print '-- Machine tags:', table[0]['machine_tags']
        