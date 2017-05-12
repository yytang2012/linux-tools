#!/usr/bin/env python
# coding=utf-8
import time

from misc import stopwatch

data_dir = '/Data/psql_dump/data_dump_0/'

host_to_password_dict = {
    'amsec13-02': ('postgres', "isa-REL-aero"),
    'amsec13-03': ('postgres', "isaisa"),
    'amsec12-05': ('postgres', "isaisa"),
    'asi-stable': ('asi', "isa-REL-crimson"),

}


def get_database_name_list(startDate='01/15/2016', days=1):
    import datetime
    database_names = []
    for i in range(0, days):
        d = datetime.datetime.strptime(startDate, '%m/%d/%Y') + datetime.timedelta(i)
        s = "crimson_%Y_%02m_%02d"
        # s = "beige_%Y_%02m_%02d"
        # s = "aero_%Y_%02m_%02d"
        # s = 'r1508_%Y_%02m_%02d'
        name = d.strftime(s)
        database_names.append(name)
    return database_names


def dump_database(host_name, database_name):
    import os
    user, password = host_to_password_dict[host_name]
    print(user, password)
    cmd_template = 'PGPASSWORD="{password}" pg_dump -C -h {host_name} -U  {user} {db_name} > ' \
                   '/Data/psql_dump/data_dump_0/{db_name}'
    # cmd = 'PGPASSWORD="isa-REL-aero" pg_dump -C -h amsec13-02 -U  postgres %s > /Data/psql_dump/data_dump_0/%s'
    for db in database_name:
        path = os.path.join(data_dir, db)
        if not os.path.isfile(path):
            print("dumping {db_name}".format(db_name=db))
            cmd = cmd_template.format(password=password, host_name=host_name, user=user, db_name=db)
            os.system(cmd)
        else:
            print("{0} was downloaded".format(db))


if __name__ == '__main__':
    host_name = 'asi-stable'
    database_name_list = get_database_name_list('05/01/2017', 3)
    print(database_name_list)
    with stopwatch('Database dump'):
        dump_database(host_name, database_name_list)
    print("Task complete!")
