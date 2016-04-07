#!/usr/bin/env python
# coding=utf-8

import os;
import sys;

def countFiles(rootDir, relativeDir = './', fileType = '.java'):
    localCnt = 0;
    childCnt = 0;
    for file in os.listdir(rootDir):        
        filePath = os.path.join(rootDir, file);   
        if(os.path.isfile(filePath) == True):
            if file[-len(fileType):] == fileType:
                localCnt += 1;
        elif(os.path.isdir(filePath) == True):
            localDir =  os.path.join(relativeDir, file);
            childCnt += countFiles(filePath, localDir, fileType = fileType);
        else:
            pass;
    if(localCnt != 0):
        print("%s: %d" %(relativeDir, localCnt));
    return childCnt + localCnt;

def validRootDir(rootDir):
    if rootDir[0] != '/':
        dir = os.getcwd();
        rootDirPath = os.path.join(dir, rootDir);
    elif rootDir[0:2] == '~/':
        rootDirPath = os.path.expanduser(rootDir);
    else:
        rootDirPath = rootDir;
    if os.path.isdir(rootDirPath) == True:
        return rootDirPath;
    else:
        return None;

if __name__ == '__main__':
    fileType = '.java';
    if len(sys.argv) > 3:
        print("usage: %s /path/to/file .java" % sys.argv[0]);
        sys.exit(-1);
    if len(sys.argv) == 1:
        rootDir = os.getcwd(); 
    else: 
        rootDir = validRootDir(sys.argv[1]);
    if rootDir == None:
        print("%s does not exist!" % rootDir);
        sys.exit(-1);
    if len(sys.argv) == 3:
        fileType = sys.argv[2];
    count = countFiles(rootDir, fileType = fileType);
    print(count);
