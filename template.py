#!/usr/bin/env python3
# coding=utf-8

"""Comic Crawler
Usage:
    comiccrawler domains
    comiccrawler download (URL... | [--dest SAVE_FOLDER])
    comiccrawler  -t TYPE [-p PATH]
    comiccrawler (--help | --version)

Options:
    --dest SAVE_FOLDER  Set download save path. [default: .]
    --help              Show help message.
    --version           Show current version.
"""
from docopt import docopt
if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    print(arguments)