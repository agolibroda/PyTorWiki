#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2019 Alec Golibroda
#
# Модель для работы с токенами 
#
#  from core.models.token      import Token
#
#


import json

import uuid

import unicodedata

import logging

import config

from core.Helpers           import *
from core.WikiException     import *



class Token:
    """
    Работа с токенами  - 
    - создать токен (и положить его в редиску)
    - под токеном (именем)скрывается структура данных (словарь), "аналогичная" сессии. 
    - положить в токен новые данные :-) 
        (в словарь, хранящийся в редиске под именем токена добавить новые данные)
    - изменить время жизни токена (при любом обращении к токену время его жизни обновляется.)
     
    - проверить наличие токена в редиске. - просто есть/нет
     
    - получить токен из редиски (отдать данные, по имени ключа)
    
    """
    
    def __init__(self, tokenHeader = None):
        """
        Сздать Токен, 
        добавить в РЕДИСКУ, как объект, наверное,
        каждый токен имеет параметр "leftTime", 
        в котором хранится время его жизни :-) 
        Первоначально, всем токенам выставляется время жизни 
        30 минут: config.options.sessionLifetime
        НО, если при логине автор скажет "запомнить его", то время выставим иное:
        один год: config.options.sessionLongLifetime
  
        """
        
                # make a random UUID
        # добавить Этот токен в РЕДИСКУ, как объект, наверное,   
        # и туда надо будет добавить профиль АВТОРА
        
        self.redisConnector = RedisConnector()


    def setLongLifeTime(self):
        """
        Установить новое время жизни токена
        """
        self.tokenBody["leftTime"] = config.options.sessionLongLifetime


    def setShortLifeTime(self):
        """
        Установить новое время жизни токена
        """
        self.tokenBody["leftTime"] = config.options.sessionLifetime


    def header(self):
        """
        Вернуть заголовок, который, "uuid" типа "cacc3eb6-bc56-4a1d-aff7-aea936ed68b4"
        """
        self.tokenHeader = str(uuid.uuid4())
        tokenData = { 
            "createToken": str(datetime.today()), 
            "leftTime": config.options.sessionLifetime
            }
        self.redisConnector.set(self.tokenHeader, tokenData )
        self.redisConnector.expire(self.tokenHeader, config.options.sessionLifetime ) # вроде как считаем в секундах.


        return self.tokenHeader
    

    def setHeader(self, tokenHeader):
        """
        Вернуть заголовок, который, "uuid" типа "cacc3eb6-bc56-4a1d-aff7-aea936ed68b4"
        """
        self.tokenHeader = tokenHeader
    
    
    def checkToken(self, locTokenHeader):
        """
        Проверить наличие токена в Редиске, 
        Если нет, тогда вернуть False 
          
        """
#         logging.info('checkToken locTokenHeader = '+ locTokenHeader)
        try:
            self.tokenBody = self.redisConnector.get(locTokenHeader)
#             logging.info('checkToken self.tokenBody = '+ str(self.tokenBody))
            # Переставим время жизни, каждый токен имеет параметр "leftTime", в котором хранится время его жизни :-) 
            self.redisConnector.expire(locTokenHeader, self.tokenBody['leftTime'] ) # вроде как считаем в секундах.
            # по- идее, токен
            return True
        
        except Exception as e:
            logging.info( 'RestCheckTokenHandler checkToken Exception as et = ' + str(e))
            error = Error ('500', 'Нету Токена в Редиске!!!! :-( ')
            return False
        

    def set(self, name, data):
        """
        Положить в токен новые данные (переписать то, что есть) 
        Желательно в токен класть данные, которые легко можно сериализовать 
        (из объектов заранее сделать словари)
          
        """
        try:
#             logging.info( 'RestCheckTokenHandler set self.tokenHeader = ' + str(self.tokenHeader))
            self.tokenBody = self.redisConnector.get(self.tokenHeader)
#             logging.info( 'RestCheckTokenHandler set self.tokenBody = ' + str(self.tokenBody))
            self.tokenBody[name] = data;
            self.redisConnector.expire(self.tokenHeader, self.tokenBody['leftTime'] ) # вроде как считаем в секундах.
            self.redisConnector.set(self.tokenHeader, self.tokenBody )
            return True
        
        except Exception as e:
            logging.info( 'RestCheckTokenHandler "set" Exception as et = ' + str(e))
            error = Error ('500', 'Нету Токена в Редиске!!!! :-( ')
            return False
        
        
    def get(self, name):
        """
        Получить из токена данные, 
        получим по-имени, если они там есть :-)  
          
        """
#         logging.info('checkToken token = '+ token)
        try:
            self.tokenBody = self.redisConnector.get(token)
#             logging.info('checkToken self.tokenBody = '+ str(self.tokenBody))
            self.redisConnector.expire(token, self.tokenBody['leftTime'] ) # вроде как считаем в секундах.
            # по- идее, токен
            return self.tokenBody[name]
        
        except Exception as e:
            logging.info( 'RestCheckTokenHandler get Exception as et = ' + str(e))
            error = Error ('500', 'Нету Данных в Редиске!!!! :-( ')
            return False
  
  
        