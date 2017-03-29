#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "nagracks"
__date__      = "15-07-2016"
__license__   = "MIT"
__copyright__ = "Copyright © 2016 nagracks"

import argparse
import collections
import hashlib
import os
import sys

def get_filesize(filepath):
    """
        Get size of file as bytes
        :filepath: path to file
        :returns: int, file size in bytes
    """
    return os.stat(filepath).st_size

def get_hash_md5(filepath):
    """
        Get md5 hash of a file
        :filepath: path of file
        :returns: md5 hash
    """
    # md5 hash object #
    m = hashlib.md5()
    try:
        # Don't read at once #
        # Because it will be inefficient if file is large #
        # Read in 1024 chunks #
        with open(filepath, 'rb', 1024) as f:
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


def get_filesize_dict(path):
    """
        Make size:file dictionary, {key=size:value=files}
        :path: full path of file
        :returns: dictionary
    """
    filesize_dict = collections.defaultdict(list)
    for base_dir, dirs, files in os.walk(path):
        for filename in files:
            full_path = os.path.join(base_dir, filename)
            filesize_dict[get_filesize(full_path)].append(full_path)
    return filesize_dict


def hash_dict_from_filesize_dict(filesize_dict):
    """
        Make hash:file dictionary from filesize:file dictionary
        Note: only includes files which have duplicate filesizes.
        :filesize_dict: dictionary, contains filesize:files
        returns: hash_file_dict {key=hash, value=filepath}
    """

    hash_file_dict = collections.defaultdict(list)
    for size, files in filesize_dict.items():
        if len(files) < 2:
            continue
        for filepath in files:
            hash_file_dict[get_hash_md5(filepath)].append(filepath)
    return hash_file_dict

def print_duplicates(hash_file_dict):
    """
        Print duplicate files
        :hash_file_dict: dictionary, contains hash:files
        :returns: None
    """
    for k, v in hash_file_dict.items():
        # If it contain duplicates #
        # Print them #
        if len(v) > 1:
            print ("Duplicate Files => {}".format(', '.join(v)))


def summarize_duplicates(hash_file_dict):
    """
        Summarize file duplicate searching
        :hash_file_dict: dictionary, contains hash:files
        :returns: dictionary containing the search summary
    """
    summary = { 'dupcount' : 0,     # number of unique files with duplicates
                'empty' : 0,        # number of empty files
                'duptotal' : 0 }    # overall number of duplicate files
    for k, v in hash_file_dict.items():
        if len(v) > 1:
            summary['dupcount'] += 1
            summary['duptotal'] += len(v)
            if os.stat(v[0]).st_size == 0:
                summary['empty'] += len(v)
    return summary


def delete_all_duplicates(hash_file_dict):
    """
        Delete all files with duplicates
        :hash_file_dict: dictionary, contains hash:files
        :returns: None
    """
    for k, v in hash_file_dict.items():
        if len(v) > 1:
            for dup in v:
                os.remove(dup)
    print ("All duplicate files are deleted.")


def move_duplicates(hash_file_dict, dirname):
    """
        Move duplicates to location specified by parameter dirname
        :hash_file_dict: dictionary, contains hash:files
        :dirname: location on where to transfer duplicates
        :returns: None
    """
    if not os.path.isdir(dirname):
        print("Invalid Directory {}. Aborted.".format(dirname))
        return

    for k, v in hash_file_dict.items():
        if len(v) > 1:
            for dup in v:
                os.rename(dup, os.path.join(dirname, os.path.basename(dup)))
    print ("All duplicate files are moved to {}.".format(dirname))


def open_file(filepath):
    """
        Opens file using default programs
        :filepath: filepath of the file to be openned
        :returns: None
    """
    if sys.platform.startswith('darwin'):   # mac
        os.system("open {}".format(filepath))
    elif os.name == 'nt':                   # windows
        os.system("start {}".format(filepath))
    elif os.name == 'posix':                # unix
        os.system("xdg-open {}".format(filepath))


def interactive_mode(hash_file_dict):
    """
        Interactively go through each of the duplicate files to choose action.
        Interactive actions on individual files include:
            [d]eleting duplicate
            [v]iew file contents
        :hash_file_dict: dictionary, contains hash:files
        :returns: None
    """
    print("=" * 80)
    for k, v in hash_file_dict.items():
        if len(v) > 1:
            print ("Duplicate Files => {}".format(', '.join(v)))
            while True:
                action = input("[s]kip, take [a]ction > ").lower()
                if action in "sa" and len(action) == 1:
                    break
            if action == "s":
                continue
            # action == "a", choose action for each of the duplicates
            for i, dup in enumerate(v):
                print("Duplicate {}: {}".format(i, dup))
                while True:
                    action = input("[s]kip [d]elete [o]pen [r]ename [m]ove > ")\
                        .lower()
                    if action in "sdorm" and len(action) == 1:
                        if action == "s":
                            break
                        elif action == "d":
                            os.remove(dup)
                            break
                        elif action == "o":
                            open_file(dup)
                            # after opening, it is assumed that the user
                            # might want to take another action
                        elif action == "r":
                            newname = input("new name > ")
                            os.rename(dup,
                                os.path.join(os.path.dirname(dup), newname))
                            break
                        elif action == "m":
                            while True:
                                destdir = input("directory name > ")
                                if os.path.isdir(destdir):
                                    break
                            os.rename(dup,
                                os.path.join(destdir, os.path.basename(dup)))
                            break

def get_duplicates(path):
    """
        From a specific path, returns duplicates path dictionnary
        returns:{key:hash, value:filepath}
    """
    filesize_dict = get_filesize_dict(path)
    hash_file_dict = hash_dict_from_filesize_dict(filesize_dict)
    return hash_file_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Python Duplicates - Find duplicates"
            )
    parser.add_argument(
            'paths',
            nargs='+',
            help="paths where to find duplicates")
    parser.add_argument(
            '-d',
            '--delete',
            action='store_true',
            help="delete all files with duplicates"
            )
    parser.add_argument(
            '-i',
            '--interactive',
            action='store_true',
            help="interactively manage duplicates"
            )
    parser.add_argument(
            '-s',
            '--summary',
            action='store_true',
            help="display summary of duplicate search"
            )
    parser.add_argument(
            '-m',
            '--move',
            metavar='DIR',
            help="move all duplicates to another directory"
            )
    args = parser.parse_args()

    if len(args.paths) in (1, 2):
        path = args.paths[0]

    duplicates_dict = get_duplicates(path)
    print_duplicates(duplicates_dict)

    if args.delete:
        delete_all_duplicates(duplicates_dict)
    elif args.interactive:
        interactive_mode(duplicates_dict)
    elif args.summary:
        summary = summarize_duplicates(hash_file_dict)
        print("** summary **")
        print(
            "{dupcount} files have duplicates, having a total of {duptotal}"
            " duplicate files.\n{empty} files are empty.".format(**summary)
            )
    elif args.move:
        move_duplicates(hash_file_dict, args.move)
