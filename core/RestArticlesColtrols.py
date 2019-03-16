#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


# RestArticlesColtrols

# Copyright 2019 Alec Golibroda

# from core.RestArticlesColtrols       import *



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

from core.BaseRestHandler       import *
from core.WikiException     import *

from core.models.article import Article
# from core.models.article import Article
# from core.models.file import File
# from core.models.group      import Group
# 
# 

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

#  пока  - затычка, потом включу базу данных.
souList = [
          { "article_id": "info", "article_id": 1, "article_title": "Статья о Rest Data  Детский отдых", "article_annotation": "Статья о Rest Data  Все возможности досуга с детьми", "article_source": "1111tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 1},
          { "color": "info", "article_id": 2, "article_title": "Статья о Rest Data  Пляжное Время", "article_annotation": "Статья о Rest Data  Досуг на пляже - где, когда, с кем, зачем" , "article_source": "22222 tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 13},
          { "color": "info", "article_id": 3, "article_title": "Статья о Rest Data  Вечером", "article_annotation": "Статья о Rest Data  Вечерние досуговые мероприятия - культурно, спортивно.." , "article_source": "3333 tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling. ", "article_permissions": "pbl", "group_count": 2},
          { "color": "info", "article_id": 4, "article_title": "Статья о Rest Data  Театральности", "article_annotation": "Статья о Rest Data  Походы в Театры - и себя показать, на других посмотреть, и самими выйти на сцену.." , "article_source": "4444444 tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 4},
          { "color": "info", "article_id": 5, "article_title": "Статья о Rest Data  Танцевальности", "article_annotation": "Статья о Rest Data  Танцы. Спортивные, Rest Data  " , "article_source": "345345345 tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 13},
          { "color": "info", "article_id": 6, "article_title": "Статья о Rest Data  Умничаем", "article_annotation": "Статья о Rest Data  Клубы по интересам - Шахматы, Лото... да мало ли что ещеRest Data " , "article_source": "sdfsdfsdf tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 3},
          { "color": "info", "article_id": 7, "article_title": "Статья о Rest Data  Путешествуем", "article_annotation": "Статья о Rest Data  Путешествия, естественно, самый знакомый метод организовать собственный досуг" , "article_source": "34534534 btornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 5},
          { "color": "info", "article_id": 8, "article_title": "Статья о Rest Data  Где поесть", "article_annotation": "Статья о Rest Data  'Праздник живота', что может быть прекраснее? :-) " , "article_source": "sdfsdfsdf tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 13},
          { "color": "info", "article_id": 9, "article_title": "Статья о Rest Data  Экскурсии", "article_annotation": "Статья о Rest Data  Знать даже то место, где живём, и то, куда попали 'случайно' - как  много не известного нам ожидает нас за поворотом..." , "article_source": "sdfsdfsdf tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 1},
          { "color": "info", "article_id": 10, "article_title": "Статья о Rest Data  Спрот", "article_annotation": "Статья о Rest Data  Спортивные секции, участи е соревнованиях, посещение соревнований как зритель... " , "article_source": "dsasdas tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 6},
          { "color": "info", "article_id": 11, "article_title": "Статья о Rest Data  Туризм в Дземброни", "article_annotation": "Статья о Rest Data  Туризм и отдых в Дземброни ... " , "article_source": "tornado.web provides a simple web framework with asynchronous features that allow it to scale to large numbers of open connections, making it ideal for long polling.", "article_permissions": "pbl", "group_count": 2}
        ]



class RestArticlesListColtrolHandler(BaseRestHandler):
# class RestArticlesListColtrolHandler(BaseHandler):
    """
    Сервис о получении списка Авторов
    
    """

    @gen.coroutine
    def get(self):
 
        self.get_current_user()
        self.curentAuthor = self.current_user
 
        logging.info( 'RestArticlesListColtrolHandler:: get self.curentAuthor = ' + str(self.curentAuthor))
        
        groupId = self.get_argument("groupId", False)
         
        logging.info( 'RestArticlesListColtrolHandler:: get groupId = ' + str(groupId)) 
        #  можно придумать, что делать для загрузки списка статей группы 
        
        # /rest/articles?groupId=3 
        try:
                 
#             label=self.get_argument('label')
#             selector=self.get_argument('selector')
             
#             if int(curentParameter) == 0:
#                 curentParameter = config.options.main_info_template
#                 articles = [Article(0, 'Выберите значение ')]
#             else:
#                 articles = []
#             
#             artHelper = HelperArticle()
#             articles += yield executor.submit(artHelper.getListArticles, config.options.tpl_categofy_id)
     
#             self.set_default_headers()
            
            self.write(json.dumps(souList))
#             self.get()

            

        except Exception as e:
            logging.info( 'cRestArticlesListColtrolHandler get ommandName:: '+ str(commandName)+' Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))



class RestArticleColtrolHandler(BaseRestHandler):
# class RestArticlesListColtrolHandler(BaseHandler):
    """
    Сервис для работы со статьями
    - поучить данные одного, 
    - создать
    - отредактировать
    
    """

    @gen.coroutine
    def get(self, articleTitle):
 
        # , commandName, curentParameter, label="" 
#         logging.info('RestArticlesListColtrolHandler:: commandName '+ str(commandName))
#         logging.info('RestArticlesListColtrolHandler:: curentParameter '+ str(curentParameter))
# 
#         link=self.get_argument('link', '')
#         logging.info('RestArticlesListColtrolHandler:: link = '+ str(link))
        
        logging.info( 'RestArticleColtrolHandler:: articleTitle = ' + str(articleTitle))
         
        self.get_current_user()
        self.curentAuthor = self.current_user
 
        logging.info( 'RestArticleColtrolHandler:: get self.curentAuthor = ' + str(self.curentAuthor))
         
         
        try:
                 
#             label=self.get_argument('label')
#             selector=self.get_argument('selector')
             
#             if int(curentParameter) == 0:
#                 curentParameter = config.options.main_info_template
#                 articles = [Article(0, 'Выберите значение ')]
#             else:
#                 articles = []
#             
#             artHelper = HelperArticle()
#             articles += yield executor.submit(artHelper.getListArticles, config.options.tpl_categofy_id)
#             id = articleId 

#             for item in souList:
#                 if int(item["article_id"]) == int(articleId) :
#                     foundValue = item
#                     break
# 
#             logging.info( 'RestArticleColtrolHandler:: foundValue = ' + str(foundValue))
            
#             if foundValue == None:
#                 self.write(dict({}))
#             else:
            self.write(souList[3])

        except Exception as e:
            logging.info( ' RestArticleColtrolHandler get  Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))

#             self.write({"error_message": error})
    
