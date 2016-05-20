#!/usr/bin/env python
# coding=utf-8
import sys

from misc import *;


def get_line_number(original_file_name):
    original_file_name = get_absolute_path(original_file_name);

    if os.path.isfile(original_file_name):
        cmd = 'awk "END { print NR  }" %s' % original_file_name;
        os.system(cmd);
    else:
        print("%s doesn't exist" % original_file_name);


def main():
    if len(sys.argv) != 2:
        print("usage: %s /path/to/file" % sys.argv[0]);
    else:
        filename = sys.argv[1];
        get_line_number(filename);

if __name__ == '__main__':
    main();
