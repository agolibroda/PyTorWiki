#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda
#
#
# from core.BaseHandler       import *
#


import bcrypt
import concurrent.futures

import os.path
import re
import subprocess
import unicodedata
import logging
import json
import pickle

from datetime import datetime


# import torndb
import tornado.escape
from tornado import gen
# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
import tornado.web
# from torndsession.sessionhandler import SessionBaseHandler


##################

import traceback


#####################################

import config

from core.WikiException     import *

from core.Helpers           import *
# 
import core.models

from core.models.author     import Author

from core.models.token      import Token


@singleton
class SingletonAuthor(Author):
    pass



class BaseHandler(tornado.web.RequestHandler):
    """
    нужен классный токен 
    его как впердолим... 
    и буду п этому токену доставать из редиски всякие данные  - во всяком случае - 
    профиль Автора. что еще? - чо - то еще было, надо вспомнить!!!!

    СекОверФлоу говорит, что правильно бороться с ошибкой 
    "has been blocked by CORS policy" 
    надо так:
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    
    """

    token = 'классный токен'

    def __init__(self, *args, **kwargs):        
        super(BaseHandler, self).__init__(*args, **kwargs)


        logging.info( ' BaseHandler __init__ args:: '+ str(args))

        # for line in traceback.format_stack():
        #     print(line.strip())

       


        self.tokenControl = Token()

#         self.set_header("access-control-allow-origin", "http://localhost:4200")
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        # HEADERS!
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 
#         self.set_header("Access-Control-Allow-Headers", "X-Requested-With,content-type") 

        self.set_header("Access-Control-Allow-Credentials", True) 


    def options(self):
        # no body
        self.set_status(204)
        self.finish()


#     def get(self):
#         """
#         Надо забрать ТОКЕН - на всякий случай, вдруг ОН есть, а если нету, тогда 
#         надо создать  
#         """
#         logging.info('BaseHandler:: get:: self.get_query_argument '+ str(self.get_query_argument('token', False)))
#         self.token = self.get_query_argument('token', False)
#              
        


#     @gen.coroutine
    def get_current_user(self):
        """
        Это Стандартный торнадовский функций, про получение данных о пользователе
        
        """
        try:
            self.current_user = SingletonAuthor()
            # logging.info('BaseHandler:: get_current_user:: START self.author = '+ str(self.author))
            isLogin = True
            if self.token != '':
                
                pickleAuthor = self.tokenControl.get('currentAuthor')
                logging.info('BaseHandler:: get_current_user:: pickleAuthor'+ str(pickleAuthor))
                author = Author()
                author.unSerializationAuthor(picledAutor)
                self.current_user = author
                logging.info('BaseHandler:: get_current_user:: self.current_user '+ str(self.current_user))
            
                if self.current_user.dt_header_id == 0:
                    isLogin = False
                    self.current_user = None
            return isLogin
        except Exception as e:
            logging.info('BaseHandler:: get_current_user:: Have Error!!! '+ str(e))
            return False


    def any_author_exists(self):
        return bool(self.get_current_user())



        
