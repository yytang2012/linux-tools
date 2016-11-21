#!/usr/bin/env python
# coding=utf-8
import time

host_name = 'amsec13-02'
data_dir = '/Data/psql_dump/data_dump_0/'


def db_configuration(host_name='amsec13-02'):
    if host_name == 'amsec13-02':
        password = "isa-REL-aero"
    elif host_name == 'amsec12-05':
        password = "isaisa"
    else:
        password = ''
    return password


def get_database_name_list(startDate='01/15/2016', days=1):
    import datetime
    database_names = []
    for i in range(0, days):
        d = datetime.datetime.strptime(startDate, '%m/%d/%Y') + datetime.timedelta(i)
        s = "aero_%Y_%02m_%02d"
        # s = 'r1508_%Y_%02m_%02d'
        name = d.strftime(s)
        database_names.append(name)
    return database_names


def dump_database(database_name):
    import os
    password = db_configuration(host_name)
    cmd_template = 'PGPASSWORD="{0}" pg_dump -C -h {1} -U  postgres {2} > /Data/psql_dump/data_dump_0/{2}'
    # cmd = 'PGPASSWORD="isa-REL-aero" pg_dump -C -h amsec13-02 -U  postgres %s > /Data/psql_dump/data_dump_0/%s'
    for db in database_name:
        path = os.path.join(data_dir, db)
        if not os.path.isfile(path):
            print("dumping %s" % db)
            cmd = cmd_template.format(password, host_name, db)
            os.system(cmd)
        else:
            print("%s was downloaded".format(db))


if __name__ == '__main__':
    database_name_list = get_database_name_list('08/07/2016', 1)
    print(database_name_list)
    start = time.time()
    dump_database(database_name_list)
    end = time.time()
    print("Elapsed Time = %.2fs" % (end - start))
    print("Task complete!")
