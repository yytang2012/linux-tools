#!/usr/bin/env python
# coding=utf-8

import os;
def sshToDockUbuntu():
    cmd = 'ssh -X root@138.15.172.114 -p 10322'
    os.system(cmd);

if __name__ == '__main__':
    sshToDockUbuntu();
