# -*- coding: utf-8 -*-

from threading import Lock
import MySQLdb

__author__ = 'luofei'


class DataSource(object):

    __host = '127.0.0.1'
    __user = 'luofei'
    __passwd = '16021incloud'
    __dbname = 'h5_game'

    @classmethod
    def setDbInfo(cls, db_conf):
        cls.__host = db_conf["host"]
        cls.__user = db_conf["user"]
        cls.__passwd = db_conf["passwd"]
        cls.__dbname = db_conf["dbname"]


    @classmethod
    def connect(cls):
        if not (cls.__host != None and cls.__user != None and cls.__passwd != None and cls.__dbname != None):
            raise RuntimeError("db information not set")
        return MySQLdb.connect(host=cls.__host,
                   user=cls.__user,
                   passwd=cls.__passwd,
                   db=cls.__dbname,
                   charset='utf8',
                   use_unicode=True)


    @classmethod
    def closeConnect(cls, db):
        db.close()

