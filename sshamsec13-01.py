#!/usr/bin/env python
# coding=utf-8

import os;


def ssh_nec_amsec1301():
    cmd = 'ssh -X amsec13-01'
    os.system(cmd);


if __name__ == '__main__':
    ssh_nec_amsec1301();
