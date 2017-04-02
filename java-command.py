#!/usr/bin/env python3
# coding=utf-8

"""
usage:
    java.py install [JAVA_VERSION]
    java.py switch
"""
__version__ = '2016-08-22'

import os


def java_install(java_version='openjdk-8-jdk'):
    cmd = 'sudo add-apt-repository ppa:openjdk-r/ppa'
    os.system(cmd)
    cmd = 'sudo apt-get update'
    os.system(cmd)
    cmd = 'sudo apt-get install {0}'.format(java_version)
    os.system(cmd)


def switch_java_version():
    cmd = 'sudo update-alternatives --config java'
    os.system(cmd)
    cmd = 'sudo update-alternatives --config javac'
    os.system(cmd)


def main():
    from docopt import docopt
    arguments = docopt(__doc__, version=__version__)
    if arguments['install']:
        if not arguments['JAVA_VERSION']:
            java_install()
        else:
            java_version = arguments['JAVA_VERSION']
            java_install(java_version)
    elif arguments['switch']:
        switch_java_version()


if __name__ == '__main__':
    main()
