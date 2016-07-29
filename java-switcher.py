#!/usr/bin/env python
# coding=utf-8
import os


def switch_java_version():
    cmd = 'sudo update-alternatives --config java';
    os.system(cmd);
    cmd = 'sudo update-alternatives --config javac';
    os.system(cmd);


if __name__ == '__main__':
    switch_java_version();
