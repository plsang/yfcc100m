"""Set up paths """

import os.path
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

this_dir = os.path.dirname(__file__)

# Add caffe to PYTHONPATH
caffe_path = os.path.join(this_dir, '..', 'py-faster-rcnn', 'caffe-fast-rcnn', 'python')
add_path(caffe_path)

# Add lib to PYTHONPATH
lib_path = os.path.join(this_dir, '..', 'py-faster-rcnn', 'lib')
add_path(lib_path)
