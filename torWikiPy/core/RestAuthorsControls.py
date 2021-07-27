#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# 
# RestAuthorsControls
#
# Copyright 2019 Alec Golibroda
#
# from core.RestAuthorsControls   import *
#  
# Походу, всю работу с Авторами - 
#
# Список авторов,
# Карточка одного автора,
# Логин/Логаут
# Регистрация Автора в Системе
# Редактирование собственного профиля - 
# Все это должно быть в одном месте!!! (я пока так думаю!!!!)
# 
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

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


import unicodedata

import logging

import config

import core.models

from core.BaseHandler   import *
from core.WikiException     import *

from core.models.author     import Author

from core.models.token      import Token


MAX_WORKERS = 4

# A thread pool to be used for password hashing with bcrypt.
# executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
executor = concurrent.futures.ThreadPoolExecutor(MAX_WORKERS)

#  пока  - затычка, потом включу базу данных.
souList = [
                { "color": "info", "dt_header_id": 1, "author_name": "REST_DataВася", "author_surname": "Доллина", "article_count": 3, "group_count": 1, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 2, "author_name": "REST_DataДЭниз", "author_surname": "Замызгайло" , "article_count": 43, "group_count": 13,     "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 3, "author_name": "REST_DataМарфа", "author_surname": "Культурщикова" , "article_count": 89, "group_count": 2, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 4, "author_name": "REST_DataСрастена", "author_surname": "Печуркина-Фассо" , "article_count": 65, "group_count": 4, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 5, "author_name": "REST_DataМидора", "author_surname": "Грачёва" , "article_count": 99, "group_count": 13, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 6, "author_name": "REST_DataГамлет", "author_surname": "Стубебекеров" , "article_count": 23, "group_count": 3, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 7, "author_name": "REST_DataБуйвоша", "author_surname": "Статейщиков" , "article_count": 8, "group_count": 5, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 8, "author_name": "REST_DataПрэлесть", "author_surname": "Углов" , "article_count": 13, "group_count": 13, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 9, "author_name": "REST_DataИзя", "author_surname": "Поворотников" , "article_count": 9, "group_count": 1, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 10, "author_name": "REST_DataЛёха", "author_surname": "Венедиктович" , "article_count": 1, "group_count": 6, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                { "color": "info", "dt_header_id": 11, "author_name": "REST_DataТрабзоний", "author_surname": "Олларионов" , "article_count": 0, "group_count": 2, "author_yourself_story": "Прям в крутом ресте все заработло???? ну прям тАААКОГО понараскажем за себя, за любмого, что прям нувааааще!"},
                ]




class RestAnyBoduHandler(BaseHandler):
    """
    Сервис о пустом вызове.
    
    Это разбор ГЕТ - запроса вида:
    /
    /rest/

    
    
    """

    @gen.coroutine
    def get(self):
        """
        Пустой вызов не должен давать ошибку.
         
        """
 
        logging.info( 'RestAnyBoduHandler:: '+ str(self))

        # RestAnyBoduHandler
        # 
        #  
        try:
                  
            error = Error ('200', 'Вы ничего не хотели... :-( ')
            self.write(json.dumps(error))
 
             
 
        except Exception as e:
#             logging.info( 'commandName:: '+ str(commandName)+' Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error.message))
        



class RestAuthorsListHandler(BaseHandler):
# class RestAuthorsListHandler(BaseHandler):
    """
    Сервис о получении списка Авторов
    
    Это разбор ГЕТ - запроса вида:
    /rest/authors 
    /rest/authors?groupId=123 - получить список Авторов в группе №№ ...
    да, и всякие остальные параметры выбоора - типа, страница, 
    количетсво на странице, сортировака, фильтрация...
     и инй вариант
     /rest/authors?serch=что -то там - выбрать всех авторов, у которых в ФИО будет некая фраза.
     

    
    
    """

    # @gen.coroutine
    @tornado.gen.coroutine
    def get(self):
        """
        Получим список Авторов, возможно, список прикрутим к Группе - 
        может, попробуем забрать ещё какие  - то параметры...

        /rest/authors 
        /rest/authors?groupId=12
        /rest/authors?str=кусок_Имя-Фаилия 
        /rest/authors?authorId=123
        /rest/authors?authorHash=asda12amdasd89asd8as9d

        """
 
        try:
            
            # да, похоже, мне всегда надо знать, что за чел тут залогиненый, 
            # возможно с назными челами будет связана и область видимостей..
            # self.get_current_user()
            # self.curentAuthor = self.current_user
    
            # logging.info( 'RestAuthorsListHandler get self.curentAuthor = ' + str(self.curentAuthor))
            
#         groupId=0 #None
         
            _groupId = self.get_argument("groupId", False)
            logging.info( 'RestAuthorsListHandler get groupId = ' + str(_groupId))

            _serchStr = self.get_argument("str", '')
            logging.info( 'RestAuthorsListHandler get serchStr = ' + str(_serchStr))
            # если строка не нулевая, то стоит искать группу авторов по кусочку ИМЯРЕК ???

            _authorId = self.get_argument("authorId", '')
            logging.info( 'RestAuthorsListHandler get authorId = ' + str(_authorId))

            _authorHash = self.get_argument("authorHash", '')
            logging.info( 'RestAuthorsListHandler get authorHash = ' + str(_authorHash))


            authorControl = Author() # вот, надо делать сохранение данных   
            # authorControl.setSearchParams(groupId, serchStr) 
            authorControl.setSearchParams(groupId=_groupId, serchStr=_serchStr, authorId=_authorId, authorHash=_authorHash)

            # result 
            authors = yield executor.submit(authorControl.makeSerch) # , config.options.tpl_categofy_id
            # authors =  authorControl.getList()
            for oneAuthor in authors:
                logging.info( 'RestAuthorsListHandler oneAuthor = ' + str(oneAuthor)) 

            # # authors = yield authorControl.getList(groupId, serchStr) # , config.options.tpl_categofy_id
            # logging.info( 'RestAuthorsListHandler get authors = ' + toStr(authors)) 
            # self.write(json.dumps(authorControl.getList()))
            # self.write(json.dumps(authors)) toJson
            self.write(toJson(authors)) 
 
        except Exception as e:
            logging.error( 'commandName:: RestAuthorsListHandler get  Exception as et = ' + str(e))
            pyTorWikiTraceback('при загрузке списка пользователей произошло что - то весьма не хорошее.')
            #отдать из сервиса на улицу нужно внятное сообщение об ошибке!!!! :-) ну, максимально... 
            # Да, походу, вот с такм сообщением от бэкэнда уже будет правильн разбираться фронту.. 
            # и делать выводы... (во всяком случае "{ \n\t \"code\": \"500\" , ... " уже транспортабельно.)
            error = Error ('500', ' при получеии списка Авторов что - то пошло не так :-( ')
            self.write(json.dumps(toStr(error)))
        



class RestAuthorHandler(BaseHandler):
    """
    
    Сервис для работы с данными  Автора (Карточка Автора)
    - поучить данные одного, 
    /rest/authors/([0-9]+) - в запос передаем ИД автора!!!!

    - создать/ отредактировать == сохранить изменения!!!!!
    
    """

    @gen.coroutine
    def get(self, authorId=None ): # 
        
        # super().get()
        logging.info( 'RestAuthorHandler:: get self!!!!! = ' ) # + str(self.curentAuthor))

        self.get_current_user()
        self.curentAuthor = self.current_user
 
        logging.info( 'RestAuthorHandler:: get self.curentAuthor = ' + str(self.curentAuthor))
        
        try:
                 
            id = authorId 
            logging.info( 'RestAuthorHandler:: authorId = ' + str(authorId))
            foundValue = None
            for item in souList:
                if int(item["dt_header_id"]) == int(authorId) :
                    foundValue = item
                    break

            logging.info( 'RestAuthorHandler:: foundValue = ' + str(foundValue))
            
            if foundValue == None:
                self.write(dict({}))
            else:
                self.write(dict(foundValue))

        except Exception as e:
            logging.info( ' RestAuthorHandler get  Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error.message))

#             self.write({"error_message": error})
    
    @gen.coroutine
    def post(self, authorId=None ): # 
        
        try:
            id = authorId # Это дополнительная проверка на персону, хотя, по - идее, при регистрации, ИД будет "Нонай"!
            body = tornado.escape.json_decode(self.request.body)
            logging.info( 'RestAuthorHandler:: body = ' + str(body))
            
            if self.tokenControl.checkToken(body['tag']):
                self.tokenControl.setHeader(body['tag'])
            else:
#                 вот тут надо что - то сделать, - Отдать какую - то команду, что "форма устарела"
                raise WikiException( ' вот тут надо что - то сделать, - Отдать какую - то команду, что "форма устарела" ' )

            authorControl = Author() # вот, надо делать сохранение данных    
                
#             if not self.get_current_user():
#                 self.current_user = authorControl.login(body['authorname'], body['password'])
# #                 logging.info( 'RestAuthorHandler:: self.current_user = ' + str(self.current_user))
                
#                 self.tokenControl.set('currentAuthor', authorControl.serializationAuthor())
#                 if body['saveMe']:
#                     self.tokenControl.setLongLifeTime()
#                 else:
#                     self.tokenControl.setShortLifeTime()
                
#             self.curentAuthor = self.current_user
            
#             outAuthor = authorControl.getPublicProfile( self.curentAuthor )
#             logging.info( 'RestAuthorHandler:: outAuthor.__dict__ = ' + str(outAuthor.__dict__))
#             self.write(json.dumps(outAuthor.__dict__))
            self.write(json.dumps(True))
            
            
        except Exception as e:
            logging.info('RestAuthorHandler:: post:: Have Error!!! '+ str(e))
            
            self.write(json.dumps("Произошло что - то печальное"))


class RestLoginHandler(BaseHandler):
    """
    
    Логин 
    пиходят логин/пароль/токен 
    Проверяем, что токен существует,  
    Получаем профиль автора (полные даные вместе с RSA-keys)
    Кладём данные в Редиску, в "токен" 
    имя отдаем на клиент.... 
     
    """
    
    @gen.coroutine
    def post(self):
        """
         self.get_current_user()
         self.curentAuthor = self.current_user
         ура у нас есть дата, (body)  из нее можно взять данные, получить логин,
         Если логин случится, тогда взять профиль пользователя, получить его РСА,
         и все это так, положить в редиску 
         и кое  - что из этого отдать на клиента!!!!!!
        """

#         {'authorname': 'developer', 'password': 'чсЧСЯЧС', 'saveMe': True, 'tag': 'ab373fb9-28d5-4bdb-b16d-242266fc3805'}

        try:
            body = tornado.escape.json_decode(self.request.body)
#             logging.info( 'RestLoginHandler:: body = ' + str(body))
            # Если при get_current_user пришел "ложь", значит пользователя нету, и надоо его логинить.
            if self.tokenControl.checkToken(body['tag']):
                self.tokenControl.setHeader(body['tag'])
            else:
#                 вот тут надо что - то сделать, - Отдать какую - то команду, что "форма устарела"
                raise WikiException( ' вот тут надо что - то сделать, - Отдать какую - то команду, что "форма устарела" ' )

            authorControl = Author() # вот, надо делать сохранение данных    
                
            if not self.get_current_user():
                self.current_user = authorControl.login(body['authorname'], body['password'])
#                 logging.info( 'RestLoginHandler:: self.current_user = ' + str(self.current_user))
                
                self.tokenControl.set('currentAuthor', authorControl.serializationAuthor())
                if body['saveMe']:
                    self.tokenControl.setLongLifeTime()
                else:
                    self.tokenControl.setShortLifeTime()
                
            self.curentAuthor = self.current_user
            
            outAuthor = authorControl.getPublicProfile( self.curentAuthor )
            logging.info( 'RestLoginHandler:: outAuthor.__dict__ = ' + str(outAuthor.__dict__))
            self.write(json.dumps(outAuthor.__dict__))
            # self.write(json.dumps(True))
            
            
        except Exception as e:
            logging.info('RestLoginHandler:: post:: Have Error!!! '+ str(e))
            
            self.write(json.dumps("Произошло что - то печальное"))

        
#         self.write(json.dumps({"author-id": 123, "name": "alec"}))



class RestLogoutHandler(BaseHandler):
    """
    Выход из системы
    Удалить данные из редиски.   
    """
    
    @gen.coroutine
    def post(self):
        

        try:
            body = tornado.escape.json_decode(self.request.body)
            logging.info( 'RestLoginHandler:: body = ' + str(body))
            # Если при get_current_user пришел "ложь", значит пользователя нету, и надоо его логинить.
            if self.tokenControl.checkToken(body['tag']):
                self.tokenControl.delete(body['tag'])
                
            self.write(json.dumps(True))
            
        except Exception as e:
            logging.info('RestLogoutHandler:: post:: Have Error!!! '+ str(e))
            
            self.write(json.dumps("Произошло что - то печальное"))





class RestHelloWorld(BaseHandler):
    """
    Проверка работоспособности системы, 
    если в ответ на запрос:
    /rest/hw
    мы получим ответ: 


    значит, система работает, и все нормально. 
    """
    
    @gen.coroutine
    def get(self):
        

        try:
            body = tornado.escape.json_decode(self.request.body)
            logging.info( 'RestHelloWorld:: body = ' + str(body))
                
            self.write(json.dumps({string: "Hello World!"}))
            
        except Exception as e:
            logging.info('RestHelloWorld:: post:: Have Error!!! '+ str(e))
            
            self.write(json.dumps("Произошло что - то печальное"))

