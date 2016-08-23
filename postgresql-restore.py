#!/usr/bin/env python
# coding=utf-8
import time;

from misc import get_start_time, get_elapsed_time

root_dir = '/Data/psql_dump/data_dump_0/'


def get_database_name_list(startDate='01/15/2016', days=1):
    import datetime
    database_names = [];
    for i in range(0, days):
        d = datetime.datetime.strptime(startDate, '%m/%d/%Y') + datetime.timedelta(i);
        # s = "aero_%Y_%02m_%02d";
        s = 'r1508_%Y_%02m_%02d'
        name = d.strftime(s);
        database_names.append(name);
    return database_names;


def restore_database(database_list):
    import os
    for database in database_list:
        print(database)
        start = time.time();
        file_path = os.path.join(root_dir, database)
        if not os.path.isfile(file_path):
            continue
        """Create a database"""
        cmd = 'PGPASSWORD="isaisa" createdb -h localhost -U postgres %s' % database
        state = os.system(cmd)
        """Database already exists"""
        if state != 0:
            continue
        """Restore the database"""
        cmd = 'PGPASSWORD="isaisa" psql -h localhost -U postgres %s < %s' % (database, file_path)
        os.system(cmd)
        end = time.time();
        print("%s is restored. Elapsed Time = %.2fs" % (database, end - start))

if __name__ == '__main__':
    start_date = '01/06/2016'
    days = 28
    database_name_list = get_database_name_list(start_date, days)
    print(database_name_list)
    start_time = get_start_time()
    restore_database(database_name_list)
    elapsed_time = get_elapsed_time(start_time);
    print("Elapsed Time = %s" % elapsed_time)
    print("Task complete!")