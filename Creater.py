from typing import Any

import pymysql
from pymysql import Connection
from pymysql.cursors import Cursor


class Creater:

    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root', password='1111')
        self.create_sql_db()

    def create_sql_db(self):
        with self.connect.cursor() as cursor:
            cursor.execute("DROP DATABASE wiki")
            cursor.execute('CREATE DATABASE wiki')
            cursor.execute("USE wiki")
            sql = "create table wikiurl\n" + "(\n" + "id  int auto_increment\n" + "primary key,\n" + "url varchar(500) null,\n" + "constraint wikiUrl_id_uindex\n" + "unique (id),\n" + "constraint wikiUrl_url_uindex\n" + "unique (url)\n" + ")"
            cursor.execute(sql)
            sql = "create table rawwiki\n" + "(\n" + "id  int auto_increment\n" + "primary key,\n" + "url varchar(500) not null,\n" + "constraint rawwiki_id_uindex\n" + "unique (id),\n" + "constraint rawwiki_url_uindex\n" + "unique (url)\n" + ")"
            cursor.execute(sql)
            sql = "create table wikiaddiction\n" + "(\n" + "id  int auto_increment\n" + "primary key,\n" + "url varchar(500) null,\n" + "wikiId int           null,\n" + "constraint wikiaddiction_ibfk_1\n" + "foreign key (wikiId) references wiki.wikiurl (id)\n" + ")"
            cursor.execute(sql)
        self.connect.commit()

    def get_raw_url(self):
        with self.connect.cursor() as cursor:

            self.connect.ping()
            cursor.execute("SELECT url FROM rawwiki Order By id Limit 10")
            self.connect.commit()
            row = cursor.fetchall()
            cursor.execute("DELETE FROM rawwiki Order By id  Limit 10")
            cursor.close()
            ans = [-1]*10
            k = 0
            for i in row:
                ans[k] = i[0]
                k+=1
            return ans


