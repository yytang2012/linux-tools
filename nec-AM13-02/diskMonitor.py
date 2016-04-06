#!/usr/bin/env python
# coding=utf-8
import os

def monitor():
    cmd = 'watch -n 1 df -m';
    os.system(cmd);

if __name__ == '__main__':
    monitor();

