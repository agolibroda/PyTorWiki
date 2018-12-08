#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda

# 
# 
# ProfileControl.py
# 
#  Набор контроллеров для работы с профилями пользоватеоей
 

import bcrypt
import concurrent.futures

import os.path
import re
import subprocess

import copy

# import torndb
import tornado.escape
from tornado import gen
# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
# import tornado.web

from torndsession.sessionhandler import SessionBaseHandler

import unicodedata

import logging

import json
import pickle

import config

import core.models

from core.models.author         import Author

from core.BaseHandler           import *
from core.WikiException         import *

from core.models.article import Article

from core.helpers.template import Template, TemplateParams


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class AuthCreateHandler(BaseHandler):
    """
    содать нового автора 
    - страница регистрации пользователя
    """
    def get(self):

        tplControl = TemplateParams()
#         tplControl.make(self.autor)
        tplControl.page_name='Регистрация нового Автора'
        tplControl.link='auth/create'
        tplControl.error=None
        
        self.render("create_author.html", parameters=tplControl)

    @gen.coroutine
    def post(self):
        """
        Обработка формы создания нового пользователя.
        
        """
        try:
#             if self.any_author_exists():
#                 raise tornado.web.HTTPError(400, "author already created")
     
            passwd = self.get_argument("pass")
            passwd2 = self.get_argument("pass_conf")
            if passwd != passwd2: 
#  надо добавить сообщение о том,что пароли не совпадают, и вывести эти сообщеия в правильном месте!!!!                
                error = Error ('500', 'Пароли не совпадают! ')
                raise WikiException(error ) 
                
            authorLoc =  Author()
            authorLoc.author_role = 'volunteer'
            
            authorLoc.author_login = self.get_argument("login")
            authorLoc.author_email = self.get_argument("email")
            authorLoc.author_pass = passwd
            
            authorLoc.author_name = self.get_argument("name")
            authorLoc.author_surname = self.get_argument("surname")
            authorLoc.author_phon = self.get_argument("phon")

            logging.info( 'AuthCreateHandler  post authorLoc = ' + str(authorLoc))
            
            rez = yield executor.submit( authorLoc.save )
            logging.info( 'AuthCreateHandler  post rez = ' + str(rez))
            logging.info( 'AuthCreateHandler  post self.get_secure_cookie("wiki_author") = ' + str(self.get_secure_cookie("wiki_author")))
            
            self.set_secure_cookie("wiki_author", authorLoc.serializationAuthor())
            
            self.redirect(self.get_argument("next", "/personal_desk_top"))
        except Exception as e:
            logging.info( 'AuthCreateHandler:: post Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')

            tplControl = TemplateParams()
    #         tplControl.make(self.autor)
            tplControl.page_name='Регистрация нового Автора'
            tplControl.link='auth/create'
            tplControl.error=str(error)
            
            self.render("create_author.html", parameters=tplControl)


class AuthLoginHandler(BaseHandler):
    """
    Контроллер обработки формы логина 
    
    """
    
    def get(self):
        
        isLogin = self.get_current_user()
#         logging.info( 'AuthLoginHandler  get isLogin = ' + str(isLogin))
#         logging.info( 'AuthLoginHandler  get self.current_user = ' + str(self.current_user))
        if isLogin:
            self.redirect("/personal_desk_top")
        tplControl = TemplateParams()
#         tplControl.make(self.autor)
        tplControl.page_name='Страница входа'
        tplControl.link='auth/login'
        tplControl.error=None
        
        self.render("login.html", parameters=tplControl)

    @gen.coroutine
    def post(self):
        try:
            authorloginLoad =  Author()
    
            rezult = yield executor.submit( authorloginLoad.login, self.get_argument("login"), self.get_argument("password") )
            if rezult:
#                 logging.info( 'AuthLoginHandler  post authorloginLoad = ' + str(authorloginLoad))
                
                self.current_user = authorloginLoad
#                 logging.info( 'AuthLoginHandler  post 1 authorloginLoad.serializationAuthor() = ' + str(authorloginLoad.serializationAuthor()))
                self.session['author'] = authorloginLoad.serializationAuthor()
                self.redirect(self.get_argument("next", "/personal_desk_top"))
            else:
                raise WikiException( 'incorrect login/password' )
            
        except Exception as e:
            logging.info( 'AuthLoginHandler:: POST Exception as et = ' + str(e))

            tplControl = TemplateParams()
            tplControl.error="incorrect login/password"
            tplControl.link='auth/login'
            tplControl.page_name='Страница входа'
            self.render('login.html', parameters = tplControl )

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.current_user = None # Author()
#         logging.info( 'AuthLogoutHandler get!!! ')
        self.session.delete("author")
        self.redirect(self.get_argument("next", "/"))


class MyProfileHandler(BaseHandler):
    """
    показать и отредектировать собственный профиль :-) 
    - поменять пароль.... 
    
    """
    
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        """
        и шаблон должен быть что - то типа "АдминДома" -) 
        и набирать его... 
        или, набирать тот шаблон через вызовы реста? 
        ну да, тут  - просто шаблон (и проверку рав - а можно ли какретному пользователю Админить, и тогда  ))
        или 403  - нету правов, или шаблон "автозаполнялку..." 

        """
        try:

            self.get_current_user()
            curentAuthor = self.current_user
            
            logging.info( 'MyProfileHandler GET :: curentAuthor = ' + str(curentAuthor))

            if not curentAuthor.dt_header_id: raise tornado.web.HTTPError(404, "author not found")

            tplControl = TemplateParams()
            tplControl.make(curentAuthor)
            tplControl.page_name= curentAuthor.author_name + ' '+ curentAuthor.author_surname
            tplControl.link='profile'
            tplControl.error=None
            tplControl.anyAuthor=curentAuthor
            
            self.render("my_profile.html", parameters=tplControl)
            
        except Exception as e:
            logging.info( 'MyProfileHandler::GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            
            tplControl.error=error
            tplControl.link='/profile'
            tplControl.page_name=' Error Page '+ curentAuthor.author_name + ' '+ curentAuthor.author_surname
#             self.render('error.html', parameters = tplControl )
            self.render("my_profile.html", parameters=tplControl)

    @gen.coroutine
    def post(self):

        try:
            self.get_current_user()
            authorLoc = self.current_user

            passwd = self.get_argument("pass")
            passwd2 = self.get_argument("pass_conf")
#             old_passwd = self.get_argument("pass_conf")
            if passwd != passwd2: 
#  надо добавить сообщение о том,что пароли не совпадают, и вывести эти сообщеия в правильном месте!!!!                
                raise WikiException( 'Пароли не совпадают! ' )  # Exception # 
            
            authorLoc.author_login = self.get_argument("login")
            authorLoc.author_email = self.get_argument("email")

            authorLoc.password_entered = passwd
            authorLoc.author_old_pass = self.get_argument("old_pass")
            
            authorLoc.author_name = self.get_argument("name")
            authorLoc.author_surname = self.get_argument("surname")
            authorLoc.author_phon = self.get_argument("phon")
            
            rez = yield executor.submit( authorLoc.save )
            logging.info( 'MyProfileHandler  post rez = ' + str(rez))
            logging.info( 'MyProfileHandler  post authorLoc = ' + str(authorLoc))
            self.current_user = authorLoc

            logging.info( 'MyProfileHandler  post authorLoc.serializationAuthor() = ' + str(authorLoc.serializationAuthor()))

            self.session['author'] = authorLoc.serializationAuthor()
            
            tplControl = TemplateParams()
            tplControl.make(authorLoc)
            tplControl.page_name = authorLoc.author_name + ' '+ authorLoc.author_surname
            tplControl.link='profile'
            tplControl.error=None
            tplControl.autor=authorLoc
            
            self.render("my_profile.html", parameters = tplControl)
        except Exception as e:
            logging.info( 'MyProfileHandler Post:: Exception as et = ' + str(e))
            logging.info( 'MyProfileHandler Post:: Exception as authorLoc = ' + str(authorLoc))
            
            tplControl = TemplateParams()
            tplControl.error=str(e)
            tplControl.link='/profile'
            tplControl.page_name = authorLoc.author_name + ' '+ authorLoc.author_surname
            tplControl.error=str(e)
            tplControl.autor=authorLoc
            self.render('my_profile.html', parameters = tplControl )


class AuthorProfile(BaseHandler):
    """
    показать профиль любого пользователя
    Это надо показать и профиль пользователя (открытую часть)
    и список его статей (ПУБЛИЧНУЮ часть!!!!!)
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, presentAuthorId = 0):
        """
        и шаблон должен быть что - то типа "просмотр данных пользователя" -) 

        presentAuthorId - ИД автора, которого рассматриваем!
        
        """
        try:
            # от его имени ведутся все расмотреня.... 
            self.get_current_user()
            spectatorAuthor = self.current_user
            
            logging.info( 'AdminHomeHandler:: get ')
            logging.info( 'AdminHomeHandler:: get presentAuthorId = ' + str (presentAuthorId))
            # Надо загрузить описание пользователя по его ИД.... 
            
            authorControl = Author()
    
            tplControl = TemplateParams()
            tplControl.make(spectatorAuthor)
            tplControl.anyAuthor = yield executor.submit( authorControl.get, int(presentAuthorId) )
            artControl = Article()
            articles = yield executor.submit( artControl.listByAutorId, int(presentAuthorId), spectatorAuthor.dt_header_id )
            tplControl.articlesList = articles
            groupModel = Group()
            tplControl.allGroupsList = yield executor.submit( groupModel.list )
#             да, надо найти пользователя по его ИД, и вот тут его передать в шаблон!
#             да и список пользовательских статей надо показать!!!!!!
#             падение черного ястреба
            
            tplControl.page_name='Page of Author ' + tplControl.autor.author_name + ' ' + tplControl.autor.author_surname
            tplControl.link='profile'
            tplControl.error=None
            
            self.render("any_profile.html", parameters=tplControl)

        except Exception as e:
            logging.info( 'AuthorProfile:: GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            
            tplControl = TemplateParams()
            tplControl.error=error
            tplControl.link='profile'
            tplControl.page_name='Error Page'
            self.render('error.html', parameters = tplControl )

# 
# class ProfileHandler(BaseHandler):
#     pass


