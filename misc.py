#!/usr/bin/env python
# coding=utf-8
import os


def get_absolute_path(original_path):
    absolute_path = os.path.expanduser(original_path);
    absolute_path = os.path.abspath(absolute_path);
    return absolute_path;


def get_current_time():
    import datetime;
    currentTime = str(datetime.datetime.now());
    return currentTime;
