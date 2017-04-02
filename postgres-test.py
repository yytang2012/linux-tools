#!/usr/bin/env python
# coding=utf-8
import psycopg2


class Postgres:

    def __init__(self, dbname='aero_2016_08_08', host='138.15.172.198', user='postgres', password='isaisa'):
        info = 'dbname={0} user={1} host={2} password={3} port={4}'.format(dbname, user, host, password, port)
        try:
            self.conn = psycopg2.connect(info)
        except:
            print('I cannot connect to database, are you sure the login information is correct? {0}'.format(info))
            self.conn = -1

    def exe_statement(self, statement):
        if self.conn != -1:
            cur = self.conn.cursor()
            cur.execute(statement)
            res = cur.fetchall()
            print(res)

if __name__ == '__main__':
    postgres = Postgres(dbname='postgres', host='138.15.172.198', user='postgres', password='isaisa')
    statement = 'select * from fileevent limit 10'
    postgres.exe_statement(statement=statement)