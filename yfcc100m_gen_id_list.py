#!/usr/bin/env python

# --------------------------------------------------------
# Copyright (c) 2015 NII
# Written by Sang Phan
# --------------------------------------------------------

import os
import sys
import os.path
            
if __name__ == '__main__':

    parts = ['yfcc100m_dataset-'+str(i) for i in range(0,10)]
    
    input_dir = '/net/per610a/export/das11f/plsang/dataset/YFCC100M'
    output_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata'
    
    for part in parts:
        
        print 'Gen video id list for part', part
        
        output_file = os.path.join(output_dir, part + '.txt')
        meta_file = os.path.join(input_dir, part)
        
        with open(output_file, "w") as fo:
            with open(meta_file) as f:
                for line in f:
                    info = line.rstrip('\n').split('\t');
                    if info[-1] == '1':
                        fo.write( "%s\n" % (info[0]) )
        
