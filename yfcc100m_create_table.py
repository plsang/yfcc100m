"""
Read the YFCC100M metadata and insert them into a MongoDB database
"""

import os
import sys
import os.path
import urllib
from pymongo import MongoClient
import argparse, json
import logging
from datetime import datetime

from HTMLParser import HTMLParser

logger = logging.getLogger(__name__)

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

######################################################################

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', type=str, default='/net/per610a/export/das11f/plsang/dataset/YFCC100M', help='Path to the input directory!')
    parser.add_argument('--dbname', type=str, default='yfcc100m', help='Name of the mongodb datbase')
    parser.add_argument('--collection', type=str, default='metadata', help='Name of mongodb collection')
    
    args = parser.parse_args()
    logger.info('Command-line arguments: %s', args)
    
    logger.info('Starting mongodb client')
    client = MongoClient()
    db = client[args.dbname]
    collection = db[args.collection]
        
    start = datetime.now()
    
    parts = ['yfcc100m_dataset-'+str(i) for i in range(0,10)]
        
    for part in parts:
        logger.info('Inserting metadata for part: %s', part)
        meta_file = os.path.join(args.input_dir, part)
        
        with open(meta_file) as f:
            for line in f:
                info = line.rstrip('\n').split('\t');
                if info[-1] == '1':
                    video = {}
                    video['id'] = info[0]
                    video['title'] = strip_tags(urllib.unquote_plus(info[6]))
                    video['description'] = strip_tags(urllib.unquote_plus(info[7]))
                    video['user_tags'] = strip_tags(urllib.unquote_plus(info[8]))
                    video['machine_tags'] = strip_tags(urllib.unquote_plus(info[9]))
                    video['part_id'] = parts.index(part)
                    collection.insert_one(video)
                    
    logger.info('Time: %s', datetime.now() - start)