#!/usr/bin/env python3
# coding=utf-8
# PYTHON_ARGCOMPLETE_OK

from misc import stopwatch
import argcomplete
import argparse


class ChoicesCompleter(object):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self, **kwargs):
        return self.choices


class Postgres(object):
    # data_dir = '/Data/psql_dump/data_dump_0/'
    data_dir = '/Data/psql_dump/data_dump_0/'
    host_to_password_dict = {
        'amsec13-02': ('postgres', "isa-REL-aero"),
        'amsec13-03': ('postgres', "isaisa"),
        'amsec12-05': ('postgres', "isaisa"),
        'asi-stable': ('asi', "isa-REL-crimson"),
        'localhost': ('postgres', "isaisa"),
    }

    def __init__(self, start_date='01/15/2016', days=1, host_name='amsec12-05'):
        self.host_name = host_name
        self.user, self.password = self.host_to_password_dict[host_name]
        self.database_names = self.get_database_names(start_date, days)

    def get_database_names(self, start_date='01/15/2016', days=1):
        import datetime
        database_names = []
        for i in range(0, days):
            d = datetime.datetime.strptime(start_date, '%m/%d/%Y') + datetime.timedelta(i)
            # s = "crimson_%Y_%02m_%02d"
            # s = "beige_%Y_%02m_%02d"
            s = "aero_%Y_%02m_%02d"
            # s = 'r1508_%Y_%02m_%02d'
            name = d.strftime(s)
            database_names.append(name)
        print(database_names)
        return database_names

    def dump_database(self):
        import os
        cmd_template = 'PGPASSWORD="{password}" pg_dump -C -h {host_name} -U  {user} {db_name} > ' \
                       '{data_directory}/{db_name}'
        for db in self.database_names:
            path = os.path.join(self.data_dir, db)
            if not os.path.isfile(path):
                print("dumping {db_name}".format(db_name=db))
                cmd = cmd_template.format(password=self.password, host_name=self.host_name, user=self.user,
                                          data_directory=self.data_dir, db_name=db)
                os.system(cmd)
            else:
                print("{db_name} was downloaded".format(db_name=db))

    def restore_database(self):
        import os
        for db_name in self.database_names:
            print("Start to restore {db_name}".format(db_name=db_name))
            with stopwatch("{0}".format(db_name)):
                file_path = os.path.join(self.data_dir, db_name)
                if not os.path.isfile(file_path):
                    continue
                """Create a database"""
                cmd = 'PGPASSWORD="isaisa" createdb -h localhost -U postgres {db_name}'.format(db_name=db_name)
                state = os.system(cmd)
                """Database already exists"""
                if state != 0:
                    continue
                """Restore the database"""
                # cmd = 'PGPASSWORD="isaisa" psql -h localhost -U postgres %s < %s' % (database, file_path)
                cmd = 'PGPASSWORD="isaisa" psql -h localhost -U postgres {db_name} < {file_path}'.format(
                    db_name=db_name, file_path=file_path)
                os.system(cmd)

    def test(self):
        print('this is a test')


if __name__ == '__main__':
    host_name = 'localhost'
    start_date = '07/01/2017'
    days = 28
    postgres = Postgres(host_name=host_name, start_date=start_date, days=days)

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help='type your postgres commands').completer = \
        ChoicesCompleter(('dump', 'restore', 'drop', 'test'))
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with stopwatch('Database dump'):
        if args.type == 'dump':
            postgres.dump_database()
        elif args.type == 'restore':
            postgres.restore_database()
        elif 'test':
            postgres.test()
    print("Task complete!")
