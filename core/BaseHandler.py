#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda


#  Впринцепе, Это "тулБокс" - ящик с инструментами просто пользователя 
# надо сюда добавить 
# список ПОльзователей
# список Групп 


import bcrypt
import concurrent.futures

import os.path
import re
import subprocess
# import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

import logging
import json

import pickle

import config


from core.Helpers           import *


import core.models

from core.models.author     import Author

# from core.models.article import Article
# from core.models.article import Revision
# from core.models.file import File
# from core.models.template import Template
# 
# from core.control.article import ControlArticle 



@singleton
class SingletonAuthor(Author):
    pass

class BaseHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         return self.application.db
#     x = OnlyOne('sausage')

#     @singleton
#     class __Autor:
#         def __init__(self):
#             self.locAuthor = self.__Autor()
        
#     @gen.coroutine
    def get_current_user(self):
        """
        Это Стандартный торнадовский функций, про получение данных о пользователе
        
        """
# походу, это какая  - то не правильная версия одиночки!!!!
# надо проверить - то, что лежит в модеи!!!!

        self.author = SingletonAuthor()
#         logging.info('BaseHandler:: get_current_user:: START self.author = '+ str(self.author))
        try:
            if self.author.dt_header_id == 0:
                picledAutor = self.get_secure_cookie("wiki_author")
                if not picledAutor:
                    return None
                self.author.unSerializationAuthor(picledAutor)
#                 logging.info('BaseHandler:: get_current_user:: END self.author = '+ str(self.author))
            return self.author
        except Exception as e:
            logging.info('BaseHandler:: get_current_user:: Have Error!!! '+ str(e))
            return None


    def any_author_exists(self):
        return bool(self.get_current_user())




