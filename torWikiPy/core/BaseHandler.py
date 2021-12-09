#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda
#
#
# from core.BaseHandler       import *
#

import os
import os.path
################
import logging

dirModule = os.path.dirname(__file__)
nameModule = __file__
logger = logging.getLogger(nameModule)
logger.setLevel(logging.DEBUG)
###################################

import uuid

import bcrypt
import concurrent.futures

import re
import subprocess
import unicodedata
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

# from core.models.token      import Token

from core.systems.sessions import * #session, Session, SessionHandler


@singleton
class SingletonAuthor(Author):
    pass


class BaseHandler(tornado.web.RequestHandler):
# class BaseHandler(SessionHandler):
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

        # new_id = uuid.uuid4().hex
        # logger.info(" __init__ :: new_id = " + str(new_id) ) 
        # self.session = Session(new_id)

        setup_session(self) # Вот и создадим сессию. (или, прицепимся к существующей??)

        logger.info('BaseHandler:: __init__:: self.session = '+ str(self.session))


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
#         logger.info('BaseHandler:: get:: self.get_query_argument '+ str(self.get_query_argument('token', False)))
#         self.token = self.get_query_argument('token', False)
#              
    # @session
    # def get(self):
    #     logger.info( ' BaseHandler get config.options.cookieName :: '+ str(config.options.cookieName))
    #     if not self.get_secure_cookie(config.options.cookieName):
    #         new_id = uuid.uuid4().hex
    #         self.set_secure_cookie(config.options.cookieName, new_id)
    #         self.write("Your cookie was not set yet!")
    #     else:
    #         self.write("Your cookie was set!")        


#     @gen.coroutine
    # @session
    def get_current_user(self):
        """
        Это Стандартный торнадовский функций, про получение данных о пользователе
        Его мы немного поменяем, для того, что бы честно получать данные о Авторе!!!
        
        """
        try:
            self.current_user = SingletonAuthor()
            # logger.info('BaseHandler:: get_current_user:: START self.author = '+ str(self.author))
            isLogin = True
            if self.token != '':
                
                pickleAuthor = self.tokenControl.get('currentAuthor')
                logger.info('BaseHandler:: get_current_user:: pickleAuthor'+ str(pickleAuthor))
                author = Author()
                author.unSerializationAuthor(picledAutor)
                self.current_user = author
                logger.info('BaseHandler:: get_current_user:: self.current_user '+ str(self.current_user))
            
                if self.current_user.dt_header_id == 0:
                    isLogin = False
                    self.current_user = None
            return isLogin
        except Exception as e:
            logger.info('BaseHandler:: get_current_user:: Have Error!!! '+ str(e))
            return False

    # @session
    def any_author_exists(self):
        return bool(self.get_current_user())



        
