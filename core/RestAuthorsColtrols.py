#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
#
# RestAuthorsColtrols
#
# Copyright 2019 Alec Golibroda
#
# from core.RestAuthorsColtrols   import *
#
#


import bcrypt
import concurrent.futures

import os.path
import re
import subprocess

import json

# import tornado.escape
# from tornado import gen
# # import tornado.httpserver
# # import tornado.ioloop
# # import tornado.options
# # import tornado.web
# 
# from tornado.web import Application, RequestHandler
# from tornado.ioloop import IOLoop


import unicodedata

import logging

import config

import core.models

from core.BaseHandler   import *
from core.WikiException     import *

from core.models.author     import Author


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

#  пока  - затычка, потом включу базу данных.
souList = [
                { "color": "info", "author_id": 1, "author_name": "REST_DataВася", "author_surname": "Доллина", "article_count": 3, "group_count": 1, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 2, "author_name": "REST_DataДЭниз", "author_surname": "Замызгайло" , "article_count": 43, "group_count": 13,     "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 3, "author_name": "REST_DataМарфа", "author_surname": "Культурщикова" , "article_count": 89, "group_count": 2, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 4, "author_name": "REST_DataСрастена", "author_surname": "Печуркина-Фассо" , "article_count": 65, "group_count": 4, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 5, "author_name": "REST_DataМидора", "author_surname": "Грачёва" , "article_count": 99, "group_count": 13, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 6, "author_name": "REST_DataГамлет", "author_surname": "Стубебекеров" , "article_count": 23, "group_count": 3, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 7, "author_name": "REST_DataБуйвоша", "author_surname": "Статейщиков" , "article_count": 8, "group_count": 5, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 8, "author_name": "REST_DataПрэлесть", "author_surname": "Углов" , "article_count": 13, "group_count": 13, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 9, "author_name": "REST_DataИзя", "author_surname": "Поворотников" , "article_count": 9, "group_count": 1, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 10, "author_name": "REST_DataЛёха", "author_surname": "Венедиктович" , "article_count": 1, "group_count": 6, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "author_id": 11, "author_name": "REST_DataТрабзоний", "author_surname": "Олларионов" , "article_count": 0, "group_count": 2, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                ]


class RestAuthorsListColtrolHandler(BaseHandler):
# class RestAuthorsListColtrolHandler(BaseHandler):
    """
    Сервис о получении списка Авторов
    
    Это разбор ГЕТ - запроса вида:
    /rest/authors 
    ?groupId=123 - получить список Авторов в группе №№ ...
    да, и всякие остальные параметры выбоора - типа, страница, 
    количетсво на странице, сортировака, фильтрация...

    
    
    """

    @gen.coroutine
    def get(self):
        """
        Получим список Авторов, возможно, список прикрутим к Группе - 
        может, попробуем забрать ещё какие  - то параметры...
         
        """
 
        self.get_current_user()
        self.curentAuthor = self.current_user
  
        logging.info( 'getPersonalArticlesList:: get self.curentAuthor = ' + str(self.curentAuthor))
          
#         groupId=0 #None
         
        groupId = self.get_argument("groupId", False)
        logging.info( 'getPersonalArticlesList:: get groupId = ' + str(groupId))
         
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
            logging.info( 'commandName:: '+ str(commandName)+' Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))
        



class RestAuthorColtrolHandler(BaseHandler):
# class RestAuthorsListColtrolHandler(BaseHandler):
    """
    
    Сервис для работы с данными  Автора
    - поучить данные одного, 
    - создать
    - отредактировать
    - логин 
    
    """

    @gen.coroutine
    def get(self, authorId=None ): # 
        
        super().get()
        
        self.get_current_user()
        self.curentAuthor = self.current_user
 
        logging.info( 'RestAuthorColtrolHandler:: get self.curentAuthor = ' + str(self.curentAuthor))
        
        try:
                 
            id = authorId 
            logging.info( 'RestAuthorColtrolHandler:: authorId = ' + str(authorId))
            foundValue = None
            for item in souList:
                if int(item["author_id"]) == int(authorId) :
                    foundValue = item
                    break

            logging.info( 'RestAuthorColtrolHandler:: foundValue = ' + str(foundValue))
            
            if foundValue == None:
                self.write(dict({}))
            else:
                self.write(dict(foundValue))

        except Exception as e:
            logging.info( ' RestAuthorColtrolHandler get  Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))

#             self.write({"error_message": error})
    
