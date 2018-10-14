#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# authors.py

# from models.model import Model
# from model import Model

# from __future__ import print_function

# import sys, os, 

import logging
import json

# import pymysql
import bcrypt
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

import hashlib
import base64
from datetime import datetime

import tornado.options
import tornado.escape

##########################################

import config
from ..constants.data_base import *

from . import Model
from core.WikiException import *


class Author(Model):
    """
    Автор - сложный объект, который должен состоять из 2-х объектов, и данных "верхнего аровя"
    
     
    1 - заголовок - то, что храним в таблице "dt_headers" 
    2 - профиль Автора -  таблица "authors" 
    
    стоило бы перечислить все роли.
    author_role - admin','volunteer
    
    Отдельные поля: 
    dt_header_id
    public_key
    private_key
    
    - их загружаем при логине, и, вроде как не меняет по - жизни.
    
    при регистрации или редактировании пароля (операция сохранить - эти поля надо обрабатывать отдельно и специально.)
    
    """

#         mainPrimaryList = {'dt_header_id': self.dt_header_id } - стоит отправить в инициализвцию!!!!
#         sha_hash_sou =  self.author_login + self.author_name + self.author_surname + self.author_role +self.author_phon + self.author_email  
#         
#         
# #             mainPrimaryList = {'article_id': self.article_id }
# #             self.article_id = Model.save(self, authorId, operationFlag, mainPrimaryList, sha_hash_sou, 'article_id')


    def __init__ (self): 
        logging.info('Author:: __init__')
        
        self.dt_header_id = 0
#         author_create = datetime.now()
        self.author_login = ''
        self.author_pass = ''
#         self.authorPass = None
        self.author_name  = '' 
        self.author_surname = ''
        self.author_role = ''
        self.author_phon = '' 
        self.author_email = ''

        self.dt_header_type ='author'
        self.public_key = None
        self.private_key = None
        self.private_key_hash = None
        
        Model.__init__(self)   
        
        self.setDataStruct(Model.TableDef( tabName='authors', 
                                      idFieldName=None,
                                      mainPrimaryList =['dt_header_id'],
                                      listAttrNames=['dt_header_id', 'author_login','author_pass', 'author_name','author_surname','author_role','author_phon','author_email', 'private_key', 'private_key_hash']))
        
        self.setHeadStruct(Model.TableDef( tabName='dt_headers', 
                                      idFieldName='dt_header_id',
                                      mainPrimaryList =['dt_header_id'],
                                      listAttrNames=['dt_header_type','public_key']))

        logging.info(' __init__:: After self = ' + str(self))
        
      

    def save(self):
        """
        сохранить значение - сохраняются все значимые (без подчеркивания) 
        свойства объекта
        пароль (новый,старый) перешифровывается 
        """
        
        logging.info(' save:: BEFORE work self = ' + str(self))

        bbsalt =  config.options.salt.encode()
         
        if self.author_pass != '':
            bytePass = tornado.escape.utf8(self.author_pass) #  превратим пароль, введенный пользователем в последовательность байтов.
            self.author_pass = bcrypt.hashpw( bytePass, bbsalt ).decode('utf-8') 

            logging.info(' save:: bytePass = ' + str(bytePass))

            if ( self.dt_header_id == 0 or self.dt_header_id == None  or self.public_key == None  ):
                key = RSA.generate(2048)
                self.public_key = key.publickey().export_key() 
                pKey = key.export_key() # поучить незакрытый приватный ключ
                logging.info(' save:: pKey = ' + str(pKey))
                self.private_key_hash = bcrypt.hashpw( pKey, bbsalt ).decode('utf-8') # получим ХЕш приватного ключа - для последуюей проверки при восстановлении пароля
                logging.info(' save:: bytePass+bbsalt = ' + str(bytePass+bbsalt))
                bbWrk = (bytePass+bbsalt)[0:32]
                
                logging.info(' save:: bbWrk = ' + str(bbWrk))
                
                cipher_aes = AES.new(bbWrk, AES.MODE_EAX) # закроем приватный ключ на пароль пользователя.
                self.private_key, tag = cipher_aes.encrypt_and_digest(pKey)
                self.private_key = tornado.escape.utf8(self.private_key)

                logging.info(' save:: bbWrk = ' + str(bbWrk))
            
            
        if self.dt_header_id == 0:
            self.author_create = datetime.now()
            operationFlag = 'I'
        else:
            self.author_create =  self.author_create
            operationFlag = 'U'
            
        sha_hash_sou =  str(self.author_login) + str(self.author_name) + str(self.author_surname) + str(self.author_role) + str(self.author_phon) + str(self.author_email)  
            
        logging.info(' save:: Before-Before self = ' + str(self))
        
        self.dt_header_id = Model.save(self, self.dt_header_id, operationFlag, sha_hash_sou)
        return True
        
        

    def login(self, loginMailStr, pwdStr):
        """
        операция логина - 

        """
#         er = WikiException()
        if loginMailStr == '':
            raise WikiException(LOGIN_IS_ENPTY)
        if pwdStr != '':
            bbsalt =  config.options.salt.encode()
            test_pass = bcrypt.hashpw( tornado.escape.utf8(pwdStr), bbsalt ).decode('utf-8') 
        else:
            raise WikiException(PASSWD_IS_ENPTY)

#         cur = self.db().cursor()
        selectStr = 'dt_header.dt_header_id,  author_login, author_name, author_surname, author_role, author_phon, author_email, dt_header.public_key, authors.private_key, authors.private_key_hash'
        fromStr = 'dt_header' #'authors'
        anyParams = {
                    'whereStr': " dt_header.dt_header_id = authors.dt_header_id  AND " + 
                    " (author_login =  '" + loginMailStr + "' OR author_email =  '" + loginMailStr + "' )  AND author_pass =  '"  + test_pass + "' " , 
                     }
        resList = self.select(selectStr, fromStr, anyParams)
        
#         logging.info(' login:: resList = ' + str(resList))
        
        if len(resList) == 1:
            objValuesNameList = list(resList[0].__dict__.keys())
            for objValue in objValuesNameList:
                if objValue.find('_') != 0:
                    self.__setattr__(objValue,resList[0].__getattribute__(objValue) )
            return self
        else:
            raise WikiException(LOGIN_ERROR)


    def unloadRsa(self, loginMailStr, pwdStr):
        """
        Процедура - выгрузить приватный и публичный ключи поьзователя в НЕЗАКРЫТОМ виде в некую структуру, в файл на диске 
        Приватный и публичный ключи хранятся в сессии Автора, 
        при исполнении операции стоит получить данные их как - то упаковать, и выложить в файл.
        
        """
        pass
        

    def get(self, authorId):
        """
        загрузить ОДНО описание Автора - по его ИД
         
        """

        resList = self.select(
                    'dt_headers.dt_header_id, author_login, author_name,  author_surname, author_pass, author_role, author_phon, author_email, author_create, dt_headers.public_key, authors.private_key, authors.private_key_hash', # строка - чего хотим получить из селекта
                    'dt_headers', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': "  dt_headers.dt_header_id = authors.dt_header_id  AND  dt_headers.dt_header_id = " + str(authorId) + \
                     " AND actual_flag = 'A' " 
                     } #  все остальные секции селекта
                    )
        logging.info('Author:: get:: resList = ' + str(resList))
        # от ут надо будет разкрыть приватный ключ????? 
        if len(resList) == 1:
#             return resList[0]
            objValuesNameList = list(resList[0].__dict__.keys())
            for objValue in objValuesNameList:
                 if objValue.find('_') != 0:
                    self.__setattr__(objValue,resList[0].__getattribute__(objValue) )
            return self
        else:
            raise WikiException(LOAD_ONE_VALUE_ERROR)


    def list(self):
        """
        Выбрать список всех авторов в системе
        
        """
#         logging.info('Author:: list:: START!!! >>>> ')
#         cur = self.db().cursor()
        selectStr = 'dt_headers.dt_header_id,  author_login, author_name, author_surname, author_role, author_phon, author_email, author_create '
        fromStr = 'dt_headers' #'authors'
        anyParams = {
                    'orderStr': ' dt_header_id', # строка порядок строк
                     }

        return self.select(selectStr, fromStr, anyParams)
 
       
    

 
