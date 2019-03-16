#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda


# from core.BaseHandler       import *


import bcrypt
import concurrent.futures

import os.path
import re
import subprocess
# import torndb
import tornado.escape
from tornado import gen
# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
import tornado.web
from torndsession.sessionhandler import SessionBaseHandler


import unicodedata


import logging
import json

import pickle

import config

from core.Helpers           import *
# 
import core.models

from core.models.author     import Author


@singleton
class SingletonAuthor(Author):
    pass


class BaseHandler(SessionBaseHandler):

#     @gen.coroutine
    def get_current_user(self):
        """
        Это Стандартный торнадовский функций, про получение данных о пользователе
        
        """
        self.current_user = SingletonAuthor()
#         logging.info('BaseHandler:: get_current_user:: START self.author = '+ str(self.author))
        try:
            if self.current_user.dt_header_id == 0:
                isLogin = False
                self.current_user = None
                if 'author' in self.session:
                    picledAutor = self.session['author']
                    author = Author()
                    author.unSerializationAuthor(picledAutor)
                    self.current_user = author
                    isLogin = True
#                     logging.info('BaseHandler:: get_current_user:: END self.current_user = '+ str(self.current_user))
            return isLogin
        except Exception as e:
            logging.info('BaseHandler:: get_current_user:: Have Error!!! '+ str(e))
            return None


    def any_author_exists(self):
        return bool(self.get_current_user())




