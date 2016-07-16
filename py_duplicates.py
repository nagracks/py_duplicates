#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "nagracks"
__date__      = "15-07-2016"
__license__   = "GPL3"
__copyright__ = "Copyright © 2016 nagracks"

import argparse
import collections
import hashlib
import os
 
def parse_args():
    """Parse args with argparse
    :returns: args

    """
    parser = argparse.ArgumentParser(description="Python Duplicates"
                                                 " - Find duplicate")
    parser.add_argument('path',
                        action='store',
                        help="path where to find duplicates")

    args = parser.parse_args()
    return args

def get_hash_md5(filename):
    """Get md5 hash of filename

    :filename: name of file
    :returns: md5 hash
    """
    # md5 hash object #
    m = hashlib.md5()
    try:
        # Don't read at once #
        # Because it will be inefficient if file is large #
        # Read in 1024 chunks #
        with open(filename, 'rb', 1024) as f:
            # Read data until there is no data #
            while True:
                data = f.read(1024)
                if not data:
                    break
                # Update hash object #
                m.update(data)
    except (FileNotFoundError, OSError) as e:
        print(e)
    # Return hexadecimal digits #
    return m.hexdigest()

def hash_file_dict(path):
    """Make hash:file dictionary, {key=hash:value=files}

    :path: full path in which to find duplicates 
    :returns: dictionary

    """
    # Make defaultdict with list #
    hash_file_dict = collections.defaultdict(list)

    # Walk recursively on path #
    for base_dirs, dirs, files in os.walk(path):
        for filename in files:
            # Make full path #
            full_path = os.path.join(base_dirs, filename)
            # Make hash:files pair #
            hash_file_dict[get_hash_md5(full_path)].append(full_path)
    return hash_file_dict

def get_duplicates(hash_file_dict):
    """Get duplicate files

    :hash_file_dict: dictionary, contains hash:files
    :returns: None

    """
    for k, v in hash_file_dict.items():
        # If it contain duplicates #
        # Print them #
        if len(v) > 1:
            print ("Duplicate Files => {}".format(', '.join(v)))

if __name__ == "__main__":
    # Commandline args #
    args = parse_args()

    hash_file_dict = hash_file_dict(args.path)
    get_duplicates(hash_file_dict)
