#!/usr/bin/env python
# coding=utf-8
from misc import *;


def vimrc_setup():
    undo_directory = '~/.vim/undo'
    undo_directory = os.path.expanduser(undo_directory)
    if not os.path.isdir(undo_directory):
        os.mkdir(undo_directory)

    vimrc_path = '~/.vimrc'
    config = 'set undodir={0}'.format(undo_directory)

    if not is_defined(config, vimrc_path):
        current_time = get_current_time()
        cmd = 'echo "\\\" {0}\nset undofile \nset undodir={1} \n" >> {2}'.format(current_time, undo_directory, vimrc_path)
        os.system(cmd)


def is_defined(config, file_path):
    abs_path = get_absolute_path(file_path)
    with open(abs_path) as f:
        for line in f.readlines():
            if config in line:
                return True
    return False


def bashrc_setup():
    bashrc_path = '~/.bashrc'
    linux_tools_directory = os.path.dirname(os.path.abspath(__file__))
    config = 'export PATH={0}'.format(linux_tools_directory)
    if not is_defined(config, bashrc_path):
        current_time = get_current_time()
        cmd = 'echo "# {0} \n{1}:\$PATH\n" >> {2}'.format(current_time, config, bashrc_path)
        os.system(cmd)


def main():
    vimrc_setup();
    bashrc_setup()


if __name__ == '__main__':
    main()
