#!/usr/bin/env python
# coding=utf-8
import os
import sys

def getLineNumber(filename):
    if filename[0] != '/':
        dir = os.getcwd();
        filePath = os.path.join(dir, filename);
    elif filename[0:2] == '~/':
        filePath = os.path.expanduser(filename);
    else:
        filePath = filename;
    
    if os.path.isfile(filePath) == True:
        cmd = 'awk "END { print NR  }" %s' %filePath;
        os.system(cmd);
    else:
        print("%s doesn't exist" % filePath);

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: %s /path/to/file" % sys.argv[0]);
    else: 
        filename = sys.argv[1];
        getLineNumber(filename);




