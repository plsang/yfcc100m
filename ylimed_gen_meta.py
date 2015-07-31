#!/usr/bin/env python

# --------------------------------------------------------
# Copyright (c) 2015 NII
# Written by Sang Phan
# --------------------------------------------------------

import os
import sys
import os.path
import hashlib
import pickle
import tables
from tables import *
      
if __name__ == '__main__':

    md5_dict_file = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/md5dict.pickle'
    
    yli_med_meta_file = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/yli-med/YLI-MED_v.1.2.0/YLI-MED_Corpus_v.1.2.txt'
    
    print 'loading md5 dict...'
    with open(md5_dict_file, 'rb') as handle:
        dict = pickle.load(handle)
    
    events = ['Ev'+str(i) for i in range(100, 111)]
    labels = ['Positive', 'Negative', 'Near_Miss', 'Related']
    
    yli_meta = {}
    for event in events:
        yli_meta[event] = {};
        
        for label in labels:
            yli_meta[event][label] = []
            
    error_md5 = 0;
    with open(yli_med_meta_file) as f:
        for line in f:
            info = line.rstrip('\n').split('\t');
            md5 = info[0]
            if md5 not in dict:
                error_md5 += 1
                continue
                
            id = dict[md5]
            event = info[7]
            assert event in events
            label = info[9]
            assert label in labels
            
            yli_meta[event][label].append(id)
            
    print 'total error_md5', error_md5
    
    print 'load location meta'
    h5file = open_file("/net/per610a/export/das11f/plsang/codes/yfcc100m/view/data/metadata/yfcc100m.h5", mode = "r")    
    table = h5file.root.video.yfcc100m
    
    print 'printing metadata'
    output_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/yli-med/YLI-MED_v.1.2.0/events'
    
    for event in events[::-1]:
        print event
        output_event_dir = os.path.join(output_dir, event)
        
        if not os.path.exists(output_event_dir):
            os.makedirs(output_event_dir)
        
        for label in labels:
            output_file = os.path.join(output_event_dir, event + '.' + label + '.txt')
            with open(output_file, 'w') as f:
                for id in yli_meta[event][label]:
                    rows = [(x['part_id']) for x in table.where('id=="' + id + '"')]
                    part_id = rows[0]
                    f.write('{0} {1}\n'.format(id, part_id))
        
        
    
    
    