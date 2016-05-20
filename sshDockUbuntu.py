#!/usr/bin/env python
# coding=utf-8

import os;


def ssh_nec_dock_ubuntu():
    cmd = 'ssh -X root@138.15.172.114 -p 10322'
    os.system(cmd);


if __name__ == '__main__':
    ssh_nec_dock_ubuntu();
