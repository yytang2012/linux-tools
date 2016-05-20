#!/usr/bin/env python
# coding=utf-8
import os


def ubuntu_system_update():
    cmd1 = 'sudo apt-get update';        # Fetches the list of available updates
    os.system(cmd1);
    cmd2 = 'sudo apt-get upgrade';       # Strictly upgrades the current packages
    os.system(cmd2);
    cmd3 = 'sudo apt-get dist-upgrade';  # Installs updates (new ones)
    os.system(cmd3);


if __name__ == '__main__':
    ubuntu_system_update();
