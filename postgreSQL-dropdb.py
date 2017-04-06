#!/usr/bin/env python
# coding=utf-8
import time;

from misc import get_start_time, get_elapsed_time, stopwatch

root_dir = '/Data/psql_dump/data_dump_0/'
password = "isaisa"


def get_database_name_list(startDate='01/16/2016', days=1):
    import datetime
    database_names = []
    for i in range(0, days):
        d = datetime.datetime.strptime(startDate, '%m/%d/%Y') + datetime.timedelta(i)
        # s = "aero_%Y_%02m_%02d"
        # s = "beige_%Y_%02m_%02d"
        s = 'r1508_%Y_%02m_%02d'

        name = d.strftime(s)
        database_names.append(name)
    return database_names


def drop_database(database_list):
    import os
    for database in database_list:
        print("Start to restore {0}".format(database))
        with stopwatch("{0}".format(database)):
            """Drop a database"""
            cmd = 'PGPASSWORD="{0}" dropdb -h localhost -U postgres {1}'.format(password, database)
            state = os.system(cmd)
            """Database already exists"""
            if state != 0:
                print("{0} does not exist".format(database))
                continue


if __name__ == '__main__':
    start_date = '01/16/2016'
    days = 1
    database_name_list = get_database_name_list(start_date, days)
    print(database_name_list)
    with stopwatch("Main"):
        drop_database(database_name_list)
    print("Task complete!")
