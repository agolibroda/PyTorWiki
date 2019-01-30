#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda


# список Групп GroupHandler.py 


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


import core.models

from core.models.author     import Author
from core.models.group      import Group

from core.helpers.template import Template, TemplateParams


from core.BaseHandlers import *
from core.WikiException import *

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)



class GroupListHandler(BaseHandler):
    """
    Показать список Групп - просто список
    Это ответ на запрос 
    r"/groups"
    
    показываем только Название + картинку. 
    
    """
    @gen.coroutine
    def get(self):
        """
        Получить список Групп
        
        
        """
        try:
        
            self.get_current_user()
            spectatorAuthor = self.current_user
            
            groupModel = Group()
    
            tplControl = TemplateParams()
            if spectatorAuthor != None:
                tplControl.make(spectatorAuthor)
                
            tplControl.groupsList = yield executor.submit( groupModel.list )

            logging.info(" GroupHandler get  tplControl.groupsList = " + str(tplControl.groupsList))             

            tplControl.page_name='Список Групп '
#             tplControl.link='profile'
            tplControl.error=None
            
            # ПОдготовить  к публикации шаблон  
            # получить его имя, и с те именем, которое получено, уже играть в список Авторов. 
             
            #
            logging.info(" GroupHandler get  tplControl = " + str(tplControl))             
            self.render("groupsList.html", parameters=tplControl)

        except Exception as e:
            logging.info( 'GroupHandler:: GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            
            tplControl = TemplateParams()
            tplControl.error=error
            tplControl.link='profile'
            tplControl.page_name='Error Page'
            self.render('error.html', parameters = tplControl )





class GroupProfile(BaseHandler):
    """
    Показать список Групп - просто список
    Это ответ на запрос 
    r"/groups"
    
    показываем только Название + картинку. 
    
    """
    @gen.coroutine
    def get(self):

        try:
        
            self.get_current_user()
            spectatorAuthor = self.current_user
            
            groupModel = Group()
    
            tplControl = TemplateParams()
            tplControl.make(spectatorAuthor)
            tplControl.groupsList = yield executor.submit( groupModel.list )

            tplControl.page_name='Список Групп '
#             tplControl.link='profile'
            tplControl.error=None
            
            # ПОдготовить  к публикации шаблон  
            # получить его имя, и с те именем, которое получено, уже играть в список Авторов. 
             
            #
            logging.info(" GroupHandler get  tplControl = " + str(tplControl))             
            self.render("groupsList.html", parameters=tplControl)

        except Exception as e:
            logging.info( 'GroupHandler:: GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            
            tplControl = TemplateParams()
            tplControl.error=error
            tplControl.link='profile'
            tplControl.page_name='Error Page'
            self.render('error.html', parameters = tplControl )



