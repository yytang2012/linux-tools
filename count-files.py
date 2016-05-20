#!/usr/bin/env python
# coding=utf-8

import os;
import sys;

from misc import get_absolute_path


def count_files(root_directory, file_type='.java'):
    localCnt = 0;
    childCnt = 0;
    for file in os.listdir(root_directory):
        file_path = os.path.join(root_directory, file);
        if os.path.isfile(file_path):
            if file[-len(file_type):] == file_type:
                localCnt += 1;
        elif os.path.isdir(file_path):
            childCnt += count_files(file_path, file_type=file_type);
        else:
            pass;
    if localCnt != 0:
        print("%-3d: %s" % (localCnt, root_directory));
    return childCnt + localCnt;


def main():
    fileType = '.java';
    if len(sys.argv) > 3:
        print("usage: %s /path/to/file .java" % sys.argv[0]);
        sys.exit(-1);
    if len(sys.argv) == 1:
        rootDir = os.getcwd();
    else:
        rootDir = get_absolute_path(sys.argv[1]);

    if not os.path.isdir(rootDir):
        print("%s does not exist!" % rootDir);
        sys.exit(-1);
    if len(sys.argv) == 3:
        fileType = sys.argv[2];
    count = count_files(rootDir, file_type=fileType);
    print("%-3d: %s" % (count, rootDir));


if __name__ == '__main__':
    main();
