#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda


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

import core.Helpers
from core.Helpers           import *
# from core.Helpers           import SingletonDecorator

import core.models
from core.models.author     import Author
from core.models.article    import Article
from core.models.file       import File

from core.models.group      import Group

from core.helpers.article   import HelperArticle 


from core.helpers.template  import Template, TemplateParams

from core.BaseHandlers       import *
from core.WikiException     import *



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)



    


class PersonalDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол пользователя.
    
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
            author = self.current_user
    
            logging.info( 'PersonalDeskTop get:: author = ' + str(author))
    
            tplControl = TemplateParams()
            tplControl.make(author)

            tplControl.page_name = 'Рабочий стол ' + author.author_name
            tplControl.link='personal_desk_top'

            # Выбрать все Статьи одного автора.
            artHelper = HelperArticle()
            tplControl.personalArticlesList = yield executor.submit( artHelper.getListArticlesByAutorId, author.dt_header_id, 0 )

#             logging.info( 'PersonalDeskTop get:: tplControl.personalArticlesList = ' + toStr(tplControl.personalArticlesList))

            # Выбрать все статьи в системе. 
            tplControl.allArticlesList = yield executor.submit( artHelper.getListArticlesAll, author.dt_header_id )

#             logging.info( 'PersonalDeskTop get:: tplControl.allArticlesList = ' + toStr(tplControl.allArticlesList))

            # выберем все группы в Автора.
            groupModel = Group()
            tplControl.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, author.dt_header_id )
            tplControl.allGroupsList = yield executor.submit( groupModel.list )

#             logging.info( 'PersonalDeskTop get:: tplControl.autorGroupList = ' + toStr(tplControl.autorGroupList))
#             logging.info( 'PersonalDeskTop get:: tplControl.allGroupsList = ' + toStr(tplControl.allGroupsList))

            # Выьерем всех Авторов в системе.
            authorModel = Author()
            tplControl.allAuthorsList = yield executor.submit( authorModel.list )

#             logging.info( 'PersonalDeskTop get:: tplControl.allAuthorsList = ' + toStr(tplControl.allAuthorsList))
#             logging.info( 'PersonalDeskTop get:: tplControl = ' + toStr(tplControl))

            self.render("personal_dt.html", parameters= tplControl ) 

        except Exception as e:
            logging.info( 'PersonalDeskTop get:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error, page_name= 'Рабочий стол ', link='personal_desk_top')


class GroupDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол уастника группы.
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, dt_header_id=0):
        """
        и шаблон должен быть что - то типа "АдминДома" -) 
        и набирать его... 
        или, набирать тот шаблон через вызовы реста? 
        ну да, тут  - просто шаблон (и проверку рав - а можно ли какретному пользователю Админить, и тогда  ))
        или 403  - нету правов, или шаблон "автозаполнялку..." 

        """
        try:

            logging.info( 'GroupDeskTop Get:: dt_header_id = ' + str(dt_header_id))
            self.get_current_user()
            author = self.current_user

            if not author.dt_header_id: return None

            groupModel = Group()
    
            if dt_header_id==0:
                groupName = 'Create New Group'
                groupData = groupModel
            else:
                groupData = yield executor.submit( groupModel.get, dt_header_id )
                groupName = groupData.group_title 

            tplControl = TemplateParams()
            tplControl.make(author)
            tplControl.page_name = groupName 
            tplControl.groupData = groupData

            articles = yield executor.submit( groupModel.getGroupArticleList, dt_header_id )
            tplControl.articlesList = articles 
            logging.info( 'GroupDeskTop Get:: dt_header_id = ' + str(dt_header_id))
            logging.info( 'GroupDeskTop Get:: groupModel = ' + str(groupModel))
            members = yield executor.submit( groupModel.getGroupMembersleList, dt_header_id )
            tplControl.groupMembersList = members 
            logging.info( 'GroupDeskTop Get:: members = ' + str(members))

            if int(dt_header_id) == 0:
                tplControl.link = 'group_desk_top'
            else:
                tplControl.link='group_desk_top/' + str(dt_header_id)   

            logging.info( 'GroupDeskTop Get:: 4 = ' + str(True))

            self.render("group_dt.html", parameters= tplControl)
        except Exception as e:
            logging.info( 'GroupDeskTop Get:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


    @tornado.web.authenticated
    @gen.coroutine
    def post(self, dt_header_id=0):
        try:
            self.get_current_user()
            author = self.current_user
    
            groupModel = Group()
    
            groupModel.dt_header_id = int(self.get_argument("id", 0))
            groupModel.group_title = self.get_argument("title")
            groupModel.group_annotation = self.get_argument("annotation")
            groupModel.group_status = self.get_argument("status", 'pbl')                                
            
            rez = yield executor.submit( groupModel.save, author.dt_header_id )
            
            self.redirect("/group_desk_top/" + str(groupModel.dt_header_id))
        except Exception as e:
            logging.info( 'GroupDeskTop POST!!! (Save):: Exception as et = ' + str(e))
#             error = Error ('500', 'что - то пошло не так :-( ')
#             self.render('error.html', error=error, link='/compose', page_name='')
            pageName = 'Редактирование ' + groupModel.group_title
            self.render("group_dt.html", group=group, page_name= pageName, link='group_dt')



class GroupAdmDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол админа группы.
    
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
            author = self.current_user
#             self.render(config.options.adminTplPath+"admin_home.html", articles=articles, tplCategory=config.options.tpl_categofy_id )
            self.render(config.options.adminTplPath+"admin_home.html" )
        except Exception as e:
            logging.info( 'GroupAdmDeskTop:: GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)



class SysAdmDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол админа системы.
    
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
            author = self.current_user

            if not author.dt_header_id: return None

            tplControl = TemplateParams()
            tplControl.make(author)
            tplControl.page_name = 'Страница Супер Администратора' 
            tplControl.link='sys_adm_desk_top'

            # Выбрать все Статьи одного автора.
            artHelper = HelperArticle()

            # Выбрать все статьи в системе. 
            tplControl.allArticlesList = yield executor.submit( artHelper.getListArticlesAll, author.dt_header_id )

#             logging.info( 'PersonalDeskTop get:: tplControl.allArticlesList = ' + toStr(tplControl.allArticlesList))

            # выберем все группы в Автора.
            groupModel = Group()
            tplControl.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, author.dt_header_id )
            tplControl.allGroupsList = yield executor.submit( groupModel.list )

#             logging.info( 'PersonalDeskTop get:: tplControl.autorGroupList = ' + toStr(tplControl.autorGroupList))
#             logging.info( 'PersonalDeskTop get:: tplControl.allGroupsList = ' + toStr(tplControl.allGroupsList))

            # Выьерем всех Авторов в системе.
            authorModel = Author()
            tplControl.allAuthorsList = yield executor.submit( authorModel.list )
            
            self.render(config.options.adminTplPath+"admin_home.html", parameters= tplControl )
        except Exception as e:
            logging.info( 'SysAdmDeskTop:: GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)

