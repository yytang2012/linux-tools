#!/usr/bin/env python3
# coding=utf-8
""" PYTHON_ARGCOMPLETE_OK """

from misc import stopwatch, get_database_names
import argcomplete
import argparse


class ChoicesCompleter(object):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self, **kwargs):
        return self.choices


class Postgres(object):
    host_to_password_dict = {
        'amsec13-02': ('postgres', "isa-REL-aero"),
        'amsec13-03': ('postgres', "isaisa"),
        'amsec12-05': ('postgres', "isaisa"),
        'asi-stable': ('asi', "isa-REL-crimson"),
        'localhost': ('postgres', "isaisa"),
    }

    def __init__(self, start_date='01/15/2016', days=1, host_name='amsec12-05',
                 root_dir='/Data/psql_dump/data_dump_0/'):
        self.host_name = host_name
        self.user, self.password = self.host_to_password_dict[host_name]
        self.database_names = get_database_names(start_date, days)
        self.root_dir = root_dir

    def dump_database(self):
        import os
        cmd_template = 'PGPASSWORD="{password}" pg_dump -C -h {host_name} -U  {user} {db_name} > {root_dir}/{db_name}'
        for db in self.database_names:
            path = os.path.join(self.root_dir, db)
            if not os.path.isfile(path):
                print("dumping {db_name}".format(db_name=db))
                cmd = cmd_template.format(password=self.password, host_name=self.host_name, user=self.user, db_name=db,
                                          root_dir=self.root_dir)
                os.system(cmd)
            else:
                print("{db_name} was downloaded".format(db_name=db))

    def restore_database(self):
        import os
        for db_name in self.database_names:
            print("Start to restore {db_name}".format(db_name=db_name))
            with stopwatch("{0}".format(db_name)):
                file_path = os.path.join(self.root_dir, db_name)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help='type your postgres commands').completer = \
        ChoicesCompleter(('dump', 'restore', 'drop', 'test'))
    parser.add_argument("-H", "--Host_name", help='specify the host name').completer = \
        ChoicesCompleter(('localhost', 'amsec13-02', 'amsec13-03', 'amsec12-05', 'asi-stable'))
    parser.add_argument("-d", "--days", help='specify how many days')
    parser.add_argument("-s", "--start_date", help='specify the start date')
    parser.add_argument("-r", "--root_dir", help='specify the root directory')
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with stopwatch('Database dump'):
        """ Get the host_name """
        if args.Host_name is None:
            host_name = 'localhost'
        else:
            host_name = args.Host_name

        """ Get the start_date """
        if args.start_date is None:
            start_date = '07/01/2016'
        else:
            start_date = args.start_date

        """ Get the days """
        if args.days is None:
            days = 28
        else:
            days = int(args.days)

        """ Get the root directory """
        if args.root_dir is None:
            root_dir = '/Migration/psql_dump/'
        else:
            root_dir = args.root_dir

        print(" host_name: {host_name}\n start_data: {start_date}\n days: {days}\n root_dir: {root_dir}".format(
            host_name=host_name, start_date=start_date, days=days, root_dir=root_dir
        ))
        postgres = Postgres(host_name=host_name, start_date=start_date, days=days, root_dir=root_dir)

        """ extract host_name, start_date, days """
        if args.type == 'dump':
            postgres.dump_database()
        elif args.type == 'restore':
            postgres.restore_database()
        elif 'test':
            postgres.test()
    print("Task complete!")
