#!/usr/bin/env python
# coding=utf-8
import os

vimrcStr = """
set undofile 
set undodir=%s
""";

def linuxSetup():
    undoDir = '~/.vim/undo'
    undoDir = os.path.expanduser(undoDir);
    if os.path.isdir(undoDir) == False:
        os.mkdir(undoDir);
    s = vimrcStr % undoDir;
    cmd = 'echo "%s" >> ~/.vimrc' %s;
    os.system(cmd);

if __name__ == '__main__':
    linuxSetup();

