#!/usr/bin/env python3
""" PYTHON_ARGCOMPLETE_OK """
import os
import argcomplete
import argparse


class ChoicesCompleter(object):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self, **kwargs):
        return self.choices


def monitor_memory_usage():
    cmd = 'watch -n 1 free -m'
    os.system(cmd)


def monitor_disk_usage():
    cmd = 'watch -n 1 df -m'
    os.system(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help='Choose a device to monitor').completer = \
        ChoicesCompleter(('memory', 'disk'))
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.type == 'memory':
        monitor_memory_usage()
    elif args.type == 'disk':
        monitor_disk_usage()
