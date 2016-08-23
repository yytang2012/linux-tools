#!/usr/bin/env python
# coding=utf-8
import time;


def get_database_name_list(startDate='01/15/2016', days=1):
    import datetime
    database_names = [];
    for i in range(0, days):
        d = datetime.datetime.strptime(startDate, '%m/%d/%Y') + datetime.timedelta(i);
        # s = "aero_%Y_%02m_%02d"
        s = 'r1508_%Y_%02m_%02d'
        name = d.strftime(s);
        database_names.append(name);
    return database_names;


def dump_database(database_name):
    import os
    cmd = 'PGPASSWORD="isaisa" pg_dump -C -h amsec12-05 -U  postgres %s > /Data/psql_dump/data_dump_0/%s'
    dir = os.getcwd();
    for db in database_name:
        path = os.path.join(dir, db);
        if not os.path.isfile(path):
            print("dumping %s" % db);
            os.system(cmd % (db, db));
        else:
            print("%s was downloaded" % db);


if __name__ == '__main__':
    database_name_list = get_database_name_list('01/06/2016', 28);
    print(database_name_list);
    start = time.time();
    dump_database(database_name_list);
    end = time.time();
    print("Elapsed Time = %.2fs" % (end - start));
    print("Task complete!")
