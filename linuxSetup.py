#!/usr/bin/env python
# coding=utf-8
from misc import *;


def vimrc_setup():
    undo_directory = '~/.vim/undo'
    undo_directory = os.path.expanduser(undo_directory);
    if not os.path.isdir(undo_directory):
        os.mkdir(undo_directory);
    current_time = get_current_time();
    cmd = 'echo "\\\" %s\nset undofile \nset undodir=%s " >> ~/.vimrc' % (current_time, undo_directory);
    os.system(cmd);


def bashrc_setup():
    linux_tools_directory = os.path.dirname(os.path.abspath(__file__));
    current_time = get_current_time();
    cmd = 'echo "# %s \nexport PATH=%s:$PATH" >> ~/.bashrc' % (current_time, linux_tools_directory);
    os.system(cmd);


def main():
    vimrc_setup();
    bashrc_setup();


if __name__ == '__main__':
    main();
