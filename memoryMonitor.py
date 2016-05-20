#!/usr/bin/env python
# coding=utf-8
import os


def monitor_memory_usage():
    cmd = 'watch -n 1 free -m';
    os.system(cmd);


if __name__ == '__main__':
    monitor_memory_usage();
