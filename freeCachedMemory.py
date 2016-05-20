#!/usr/bin/env python
# coding=utf-8
import os

# To free pagecache:
#         echo 1 > /proc/sys/vm/drop_caches
# To free dentries and inodes:
#         echo 2 > /proc/sys/vm/drop_caches
# To free pagecache, dentries and inodes:
#         echo 3 > /proc/sys/vm/drop_caches


def free_cached_memory():
    cmd = 'sudo sync && sudo sysctl -w vm.drop_caches=3'
    os.system(cmd);

if __name__ == '__main__':
    free_cached_memory();

