#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_DB_210607

# Проверим коннект к базе данных и какие  - то элементарные операции.

# Вызов процедуры запуска тестера для начала вот такой:
# 
# Запускаем эту шнягу в консоли ВИРТУАЛЬНОЙ машины!!!!! 

# cd /home/alec/workhome/sites/vedogon.local/torWikiPy/test
# python3 -m tornado.test.runtests test_DB_210607





import logging

logging.basicConfig(filename='test.log', level=logging.INFO)
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)


from datetime import date
import time

# import tornado.httpserver 
import tornado.httpclient 
# import tornado.ioloop 
import tornado.web 

import sys, os


# http://initd.org/psycopg/docs/index.html
import psycopg2

# from somewhere import namedtuple
import collections
# collections.namedtuple = namedtuple
# from psycopg2.extras import NamedTupleConnection
from psycopg2.extras import DictCursor
# NamedTupleCursor



sys.path.append(os.path.dirname('./../'))
# from app import * 
import config
# import core.models

# from core.models.author         import Author

sys.path.pop()

import unittest 
         
class TestDB_connect(unittest.TestCase): 
    autor= None

    def setUp(self): 

        print( 'test_DB_210607::: config.options.postgreBase = ' + str(config.options.postgreBase) )
        print( 'test_DB_210607::: config.options.postgreHost = ' + str(config.options.postgreHost) )
        print( 'test_DB_210607::: config.options.postgrePort = ' + str(config.options.postgrePort) )
        print( 'test_DB_210607::: config.options.postgreUser = ' + str(config.options.postgreUser) )
        print( 'test_DB_210607::: config.options.postgrePwd = ' + str(config.options.postgrePwd) )

        self._connectInstans = psycopg2.connect(
                                                database= config.options.postgreBase, 
                                                host= config.options.postgreHost,
                                                port= config.options.postgrePort,
                                                user= config.options.postgreUser, 
                                                password= config.options.postgrePwd 
                                                )
        self._cursor = self._connectInstans.cursor(cursor_factory=DictCursor) 
        print( 'setUp::: self._cursor = ' + str(self._cursor) )
#         self._cursor = self._connectInstans.cursor(cursor_factory=NamedTupleCursor) DictCursor
        # self._cursor = self._connectInstans.cursor(cursor_factory=DictCursor) 

    # @gen_test
    def test_autor_list(self):
        # try:
        #     # self._cursor = self._connectInstans.getCursor() # служебные параметры (те, которые не будут отбражаться в )

        #     _loDb = self._cursor
        #     sqlStr= "SELECT * FROM articles "
        #     _loDb.execute(sqlStr)
        #     sourse = _loDb.fetchall()



        #     print( 'test_autor_list::: list = ' + str(sourse) )
        #     # for oneAuthor in list:
        #     #     print( 'test_autor_list::: oneAuthor = ' + str(oneAuthor) )

        # except Exception as e:
        #     logging.info( 'test_autor_list:: Exception as et = ' + str(e))
        #     # error = Error ('500', 'что - то пошло не так :-( ')
        _loDb = self._cursor
        # sqlStr= "SELECT * FROM articles "
        # _loDb.execute(sqlStr)
        # sourse = _loDb.fetchall()

        # print( 'test_articles_list::: list = ' + str(sourse) )

        sqlStr= "SELECT dt_headers.dt_header_id,  author_login, author_name, author_surname, author_role, author_phon, author_email, author_create, dt_headers.public_key  FROM authors, dt_headers WHERE   dt_headers.dt_header_id = authors.dt_header_id  AND actual_flag = 'A'  ORDER BY  dt_header_id "
        _loDb.execute(sqlStr)
        sourse = _loDb.fetchall()

        print( 'test_autor_list::: list = ' + str(sourse) )




        
if __name__ == '__main__': 
    unittest.main() 