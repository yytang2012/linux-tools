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
    _start_time = time.time()
    return _start_time


def get_elapsed_time(_start_time):
    _stop_time = time.time()
    # elapsedTime = time.strftime("%H hours %M minutes %S seconds", time.gmtime(end - start))
    seconds = _stop_time - _start_time
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    if hours > 0:
        _elapsed_time = '%d hours %d minutes %.2f seconds' % (hours, minutes, seconds)
    elif minutes > 0:
        _elapsed_time = '%d minutes %.2f seconds' % (minutes, seconds)
    else:
        _elapsed_time = '%.2f seconds' % seconds

    return _elapsed_time


def get_current_time():
    import datetime
    currentTime = str(datetime.datetime.now())
    return currentTime


def get_percentage(num, total):
    import math
    bits = 2
    top = abs(100 * num)
    bottom = abs(total)
    if bottom == 0:
        return "0%"
    percent = top / bottom
    if percent == 0:
        percent_string = '0%'
        return percent_string
    scale = int(-math.floor(math.log10(percent)))
    if scale <= 0:
        scale = 1
    scale = scale + bits - 1
    factor = 10 ** scale
    new_percent = math.floor(percent * factor) / factor
    # print(percent)
    percent_string = '%.12f' % new_percent
    percent_string = '%s%%' % (percent_string.rstrip('0').rstrip('.'))
    return percent_string


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


def get_database_names(start_date='02/01/2017', days=1):
    """ Used for operations related to postgres """
    import datetime
    threshold1 = '03/01/2016'
    t_date1 = datetime.datetime.strptime(threshold1, '%m/%d/%Y')
    threshold2 = '01/01/2017'
    t_date2 = datetime.datetime.strptime(threshold2, '%m/%d/%Y')
    database_names = []
    for i in range(0, days):
        d = datetime.datetime.strptime(start_date, '%m/%d/%Y') + datetime.timedelta(i)
        if d < t_date1:
            database_template = 'r1508_%Y_%02m_%02d'
        elif d < t_date2:
            database_template = 'aero_%Y_%02m_%02d'
        else:
            database_template = 'beige_%Y_%02m_%02d'
        name = d.strftime(database_template)
        database_names.append(name)
    return database_names


if __name__ == '__main__':
    start_date = '12/20/2016'
    days = 17
    database_names = get_database_names(start_date, days)
    print(database_names)
