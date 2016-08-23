#!/usr/bin/env python3
# coding=utf-8

"""
Usage:
    dot-convert.py -t TYPE [-p PATH]
"""
import os

__version__ = '2016-08-22'


def main():
    from docopt import docopt
    arguments = docopt(__doc__, version=__version__)

    """ Default value is svg"""
    if arguments['TYPE'] == 'png':
        opts = '-Tpng'
        fig_type = 'png'
    else:
        opts = '-Tsvg'
        fig_type = 'svg'

    if arguments['PATH'] is not None:
        folder_path = arguments['PATH']
    else:
        folder_path = './'

    from misc import get_absolute_path
    folder_path = get_absolute_path(folder_path)
    file_path_list = [os.path.join(folder_path, file_item) for file_item in os.listdir(folder_path)]
    file_path_list = list(
        filter(lambda file_path: os.path.isfile(file_path) and file_path[-4:] == '.dot', file_path_list))

    for file_item in file_path_list:
        input_file = file_item
        output_file = file_item[:-4] + '.' + fig_type
        cmd = 'dot {0} {1} > {2}'.format(opts, input_file, output_file)
        print(cmd)
        os.system(cmd);


if __name__ == '__main__':
    main()
