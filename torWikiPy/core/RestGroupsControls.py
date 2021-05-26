#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# RestGroupss

# Copyright 2019 Alec Golibroda

# from core.RestGroupss       import *



import bcrypt
import concurrent.futures

import os.path
import re
import subprocess

import json

import tornado.escape
from tornado import gen
# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
# import tornado.web

from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop


import unicodedata

import logging
import json

import config

import core.models

from core.BaseHandler       import *
from core.WikiException         import *

from core.models.group          import Group
# from core.models.group import Article
# from core.models.file import File
# from core.models.group      import Group
# 
# 

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

#  пока  - затычка, потом включу базу данных.
souList = [
          { "article_count": 13, "color": "info", "group_id": 1, "group_title": "Rest Data Детский отдых", "group_annotation": "Rest Data Все возможности досуга с детьми" },
          { "article_count": 786, "color": "info", "group_id": 2, "group_title": "Rest Data Пляжное Время", "group_annotation": "Rest Data Досуг на пляже - где, когда, с кем, зачем" },
          { "article_count": 9, "color": "info", "group_id": 3, "group_title": "Rest Data Вечером", "group_annotation": "Rest Data Вечерние досуговые мероприятия - культурно, спортивно.." },
          { "article_count": 34, "color": "info", "group_id": 4, "group_title": "Rest Data Театральности", "group_annotation": "Rest Data Походы в Театры - и себя показать, на других посмотреть, и самими выйти на сцену.." },
          { "article_count": 123, "color": "info", "group_id": 5, "group_title": "Rest Data Танцевальности", "group_annotation": "Rest Data Танцы. Спортивные, .... " },
          { "article_count": 78, "color": "info", "group_id": 6, "group_title": "Rest Data Умничаем", "group_annotation": "Rest Data Клубы по интересам - Шахматы, Лото... да мало ли что еще...." },
          { "article_count": 67, "color": "info", "group_id": 7, "group_title": "Rest Data Путешествуем", "group_annotation": "Rest Data Путешествия, естественно, самый знакомый метод организовать собственный досуг" },
          { "article_count": 345, "color": "info", "group_id": 8, "group_title": "Rest Data Где поесть", "group_annotation": "Rest Data 'Праздник живота', что может быть прекраснее? :-) " },
          { "article_count": 9, "color": "info", "group_id": 9, "group_title": "ЭRest Data кскурсии", "group_annotation": "Rest Data Знать даже то место, где живём, и то, куда попали 'случайно' - как  много не известного нам ожидает нас за поворотом..." },
          { "article_count": 156, "color": "info", "group_id": 10, "group_title": "Rest Data Спрот", "group_annotation": "Rest Data Спортивные секции, участи е соревнованиях, посещение соревнований как зритель... " },
          { "article_count": 15, "color": "info", "group_id": 11, "group_title": "Rest Data Туризм в Дземброни", "group_annotation": "Rest Data Туризм и отдых в Дземброни ... " }
        ]



class RestGroupsListHandler(BaseHandler):
# class RestGroupsListHandler(BaseHandler):
    """
    Сервис о получении списка групп :-) 

    /rest/groups/ -то там - выбрать всех авторов, у которых в ФИО будет некая фраза.

    /rest/groups?serch=что -то там - выбрать всех авторов, у которых в ФИО будет некая фраза.
     
    
    """

    @gen.coroutine
    def get(self):

        # всегда можно получить список групп для одного автора :-) 
        athorId = self.get_argument("athorId", False)
        logging.info( 'RestGroupsListHandler get athorId = ' + str(athorId))
 
        self.get_current_user()
        self.curentAuthor = self.current_user
 
        logging.info( 'getPersonalGroupsList:: get self.curentAuthor = ' + str(self.curentAuthor))
         
        authorId = self.get_argument("authorId", False)
        #  усли есть АВТОР, тогда надо отдать все группы, где автор засветился.
                 
        try:
                 
#             label=self.get_argument('label')
#             selector=self.get_argument('selector')
             
#             if int(curentParameter) == 0:
#                 curentParameter = config.options.main_info_template
#                 groups = [Group(0, 'Выберите значение ')]
#             else:
#                 groups = []
#             
#             artHelper = HelperGroup()
#             groups += yield executor.submit(artHelper.getListGroups, config.options.tpl_categofy_id)
     
#             self.set_default_headers()
            
            self.write(json.dumps(souList))
#             self.get()

            

        except Exception as e:
            logging.info( 'commandName:: '+ str(commandName)+' Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))



class RestGroupHandler(BaseHandler):
# class RestGroupsListHandler(BaseHandler):
    """
    Сервис для работы с группами
    - поучить данные группы, 
    - создать
    - отредактировать
    - добавить новую статью (просмотреть список статей, выбрать статью, добавить в группу.)
    - пригласить Участника
    
    """

    @gen.coroutine
    def get(self, groupId):
 
        # , commandName, curentParameter, label="" 
#         logging.info('RestGroupsListHandler:: commandName '+ str(commandName))
#         logging.info('RestGroupsListHandler:: curentParameter '+ str(curentParameter))
# 
#         link=self.get_argument('link', '')
#         logging.info('RestGroupsListHandler:: link = '+ str(link))
        
         
        self.get_current_user()
        self.curentAuthor = self.current_user
 
        logging.info( 'RestGroupHandler:: get self.curentAuthor = ' + str(self.curentAuthor))
         
         
        try:
                 
#             label=self.get_argument('label')
#             selector=self.get_argument('selector')
             
#             if int(curentParameter) == 0:
#                 curentParameter = config.options.main_info_template
#                 groups = [Group(0, 'Выберите значение ')]
#             else:
#                 groups = []
#             
#             artHelper = HelperGroup()
#             groups += yield executor.submit(artHelper.getListGroups, config.options.tpl_categofy_id)
#             id = groupId 
            logging.info( 'RestGroupHandler:: groupId = ' + str(groupId))
            foundValue = None
            for item in souList:
                if int(item["group_id"]) == int(groupId) :
                    foundValue = item
                    break

            logging.info( 'RestGroupHandler:: foundValue = ' + str(foundValue))
            
            if foundValue == None:
                self.write(dict({}))
            else:
                self.write(dict(foundValue))

        except Exception as e:
            logging.info( ' RestGroupHandler get  Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))

#             self.write({"error_message": error})
    
