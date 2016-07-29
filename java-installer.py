#!/usr/bin/env python
# coding=utf-8
import os


def java_install():
    cmd = 'sudo add-apt-repository ppa:openjdk-r/ppa';
    os.system(cmd);
    cmd = 'sudo apt-get update';
    os.system(cmd);
    cmd = 'sudo apt-get install openjdk-8-jdk';
    os.system(cmd);


if __name__ == '__main__':
    java_install();
