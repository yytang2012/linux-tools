#!/usr/bin/env python
# coding=utf-8
import contextlib
import os
import time


def get_absolute_path(original_path):
    absolute_path = os.path.expanduser(original_path)
    absolute_path = os.path.abspath(absolute_path)
    return absolute_path


def get_start_time():
    _start_time = time.time();
    return _start_time;


def get_elapsed_time(_start_time):
    _stop_time = time.time();
    # elapsedTime = time.strftime("%H hours %M minutes %S seconds", time.gmtime(end - start));
    seconds = _stop_time - _start_time;
    hours = seconds // (60 * 60);
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    if hours > 0:
        _elapsed_time = '%d hours %d minutes %.2f seconds' % (hours, minutes, seconds);
    elif minutes > 0:
        _elapsed_time = '%d minutes %.2f seconds' % (minutes, seconds);
    else:
        _elapsed_time = '%.2f seconds' % seconds;

    return _elapsed_time;


def get_current_time():
    import datetime;
    currentTime = str(datetime.datetime.now());
    return currentTime;


def get_percentage(num, total):
    import math;
    bits = 2;
    top = abs(100 * num);
    bottom = abs(total);
    percent = top / bottom;
    if percent == 0:
        percent_string = '0%';
        return percent_string
    scale = int(-math.floor(math.log10(percent)));
    if scale <= 0:
        scale = 1
    scale = scale + bits - 1;
    factor = 10 ** scale
    new_percent = math.floor(percent * factor) / factor
    # print(percent);
    percent_string = '%.12f' % new_percent;
    percent_string = '%s%%' % (percent_string.rstrip('0').rstrip('.'));
    return percent_string;


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))
