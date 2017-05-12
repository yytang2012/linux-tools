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


def run_ssh_command(host, user='yutang'):
    cmd = 'ssh -X {user}@{host}'.format(user=user, host=host)
    os.system(cmd)


def start_ssh_to_host(host):
    host_dict = {
        'amsec13-01': ('amsec13-01', 'yutang'),
        'amsec12-05': ('amsec12-05', 'yutang'),
        'intern16-02': ('138.15.172.198', 'yutang'),
        'th101a-4': ('th101a-4.cs.wm.edu', 'yytang'),
    }
    try:
        host_name, user_name = host_dict[host]
        run_ssh_command(host=host_name, user=user_name)
    except:
        print('Unsupported host')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--remote_host", help='ip address or host name').completer = \
        ChoicesCompleter(('amsec13-01', 'amsec12-05', 'intern16-02', 'th101a-4'))
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    start_ssh_to_host(args.remote_host)
