#!/usr/bin/env python
# coding=utf-8
import os

def monitorMemory():
    cmd = 'watch -n 1 free -m';
    os.system(cmd);

if __name__ == '__main__':
    monitorMemory();

