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

### gen md5 using python function
def gen_md5():

    parts = ['yfcc100m_dataset-'+str(i) for i in range(0,10)]
    
    input_dir = '/net/per610a/export/das11f/plsang/dataset/YFCC100M'
    output_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata'
    output_file = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/md5dict.pickle'
    
    dict = {};
    
    for part in parts:
        
        print 'Gen video id list for part', part
        
        id_list_file = os.path.join(output_dir, part + '.txt')
        
        with open(id_list_file, "r") as fid:            
            for line in fid:
                id = line.rstrip('\n')
                print id
                md5 = hashlib.md5(id).hexdigest()
                if md5 == '9d85ff792e4491aed52985d09a681b':
                    print 'found'
                dict[md5] = id;
        
    #with open(output_file, 'wb') as handle:
    #    pickle.dump(dict, handle)  

def get_video_id_list():
    parts = ['yfcc100m_dataset-'+str(i) for i in range(0,10)]
    
    input_dir = '/net/per610a/export/das11f/plsang/dataset/YFCC100M'
    output_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata'
    output_file = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/md5dict.pickle'
    
    #use set for searching/indexing, don't use list structure 
    video_ids = set();
    
    for part in parts:
        
        print 'Gen video id list for part', part
        
        id_list_file = os.path.join(output_dir, part + '.txt')
        
        with open(id_list_file, "r") as fid:            
            for line in fid:
                id = line.rstrip('\n')
                video_ids.add(id)
    
    return video_ids
    
if __name__ == '__main__':

    hash_file = '/net/per610a/export/das11f/plsang/dataset/YFCC100M/yfcc100m_hash'
    output_file = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/md5dict.pickle'
    
    dict = {};
    
    video_ids = get_video_id_list();
    
    print len(video_ids)
    
    count = 0
    with open(hash_file, "r") as fid:            
        for line in fid:
            count = count + 1;
            if count % 1000000 == 0:
                print count
                
            info = line.rstrip('\n').split('\t')
            id = info[0]
            md5 = info[1]
            if id in video_ids:
                dict[md5] = id;
                
    print 'saving dict'
    with open(output_file, 'wb') as handle:
        pickle.dump(dict, handle)  