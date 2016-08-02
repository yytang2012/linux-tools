#!/usr/bin/env python
# coding=utf-8

import os;


def ssh_nec_dock_ubuntu():
    cmd = 'ssh -X yutang@138.15.172.198'
    os.system(cmd);


if __name__ == '__main__':
    ssh_nec_dock_ubuntu();
