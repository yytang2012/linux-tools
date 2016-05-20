#!/usr/bin/env python
# coding=utf-8

import os;


def ssh_wm_th101a_4():
    cmd = 'ssh -X yytang@th101a-4.cs.wm.edu'
    os.system(cmd);


if __name__ == '__main__':
    ssh_wm_th101a_4();
