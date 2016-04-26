#!/usr/bin/env python
# coding=utf-8
import os


def vimrcSetup():
    vimrcStr = """ set undofile 
    set undodir=%s """;
    undoDir = '~/.vim/undo'
    undoDir = os.path.expanduser(undoDir);
    if os.path.isdir(undoDir) == False:
        os.mkdir(undoDir);
    s = vimrcStr % undoDir;
    cmd = 'echo "%s" >> ~/.vimrc' %s;
    os.system(cmd);

def bashrcSetup():
    bashrcPath = "~/.bashrc";
    bashrcPath = os.path.expanduser(bashrcPath);
    linuxToolsDir = "~/linux-tools/";
    linuxToolsDir = os.path.expanduser(linuxToolsDir);
    if os.path.isdir(linuxToolsDir) == False:
        linuxToolsDir = os.getcwd();
        if os.path.isdir(linuxToolsDir) == False:
            print("Cannot find the directory");
            return -1;
    path1 = os.path.join(linuxToolsDir, 'common');
    path2 = os.path.join(linuxToolsDir, 'sshconnection');
    cmd = 'echo "export PATH=%s:%s:$PATH" >> ~/.bashrc'%(path1, path2);
    os.system(cmd);
    

if __name__ == '__main__':
    vimrcSetup();
    bashrcSetup();

