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

import base64
from datetime import datetime

import hashlib
import bcrypt

import json
import pickle

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

import tornado.escape
import tornado.options

import config
from core.WikiException import *

from . import Model
from ..constants.data_base import *


# import pymysql
##########################################
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
        
        ########################
        # -сюда приходит пароль из формы, или, после логина - именно с ним и работаем - делаем сначала из него байты,
        # потом  - превращаес в ХКШ, и кладем на место (self.author_pass)
        # и раскрываем приватный ключ, который лежит закрытый н пароле!!!!!
        self._pass_source = '' 
        self._old_pass = ''  # - старе значение пароля - нужно при смене 
        
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
        
        
        #####################
        # END
      

    def save(self):
        """
        сохранить значение - сохраняются все значимые (без подчеркивания) 
        свойства объекта
        пароль (новый,старый) перешифровывается 
        """
        
        logging.info(' save:: BEFORE work self = ' + str(self))
        logging.info(' save:: 1 self._pass_source = ' + str(self._pass_source))
        logging.info(' save:: 1 self._old_pass = ' + str(self._old_pass))

        logging.info(' save:: 1 self.public_key = ' + str(self.public_key))
        logging.info(' save:: 1 self.private_key = ' + str(self.private_key))
        logging.info(' save:: 1 self.private_key_hash = ' + str(self.private_key_hash))

        bbsalt =  config.options.salt.encode()
         
        if self._pass_source != '' and (self.dt_header_id == 0 or self.dt_header_id == None):
            #  это новый пользователь, для него просто делаем ХЕШ
            self._pass_source = tornado.escape.utf8(self._pass_source) #  превратим пароль, введенный пользователем в последовательность байтов.
            self.author_pass = bcrypt.hashpw( self._pass_source, bbsalt ).decode('utf-8') 

#         logging.info(' save:: self._pass_source = ' + str(self._pass_source))

        # здать новую приватно-публичую парочку, если ее не было раньше.
        if ( (self.dt_header_id == 0 or self.dt_header_id == None) and self._pass_source != '' and self.public_key == None  ):
            bytePass = tornado.escape.utf8(self._pass_source)
            key = RSA.generate(2048)
            self.public_key = key.publickey().export_key() 
            pKey = key.export_key() # поучить незакрытый приватный ключ
            logging.info(' save:: PrivateKey ::: pKey = ' + str(pKey))
            self.private_key_hash = bcrypt.hashpw( pKey, bbsalt ).decode('utf-8') # получим ХЕш приватного ключа - для последуюей проверки при восстановлении пароля
            bbWrk = (bytePass+bbsalt)[0:32]
            cipher_aes = AES.new(bbWrk, AES.MODE_EAX) # закроем приватный ключ на пароль пользователя.
            ciphertext = cipher_aes.encrypt(pKey)
            self.private_key = pickle.dumps({'cipherKey': ciphertext, 'nonce': cipher_aes.nonce})

# new_reader = pickle.loads(pickle.dumps(reader))

        logging.info(' save:: self.private_key = ' + str(self.private_key))

        logging.info(' save:: self._pass_source = ' + str(self._pass_source))
        logging.info(' save:: self._old_pass = ' + str(self._old_pass))
        
        # если мы поменяли пароль, значит, я должен из формы получить 2 значения - старый пароль и новый пароль - и оба в тесте.    
        # потом я проверю, что старый пароль - совпадает ХЕШЕМ,
        # еслиДА, тогда 
        # 1 - декодировать приватный ключ старым паролем,
        # 2 закодировать - новым, сделать новый ХЕШ, и - УРА!!!!
        if self._pass_source != '' and self._old_pass != '':
            bbOldPAss = tornado.escape.utf8(self._old_pass)
            newPassbb = tornado.escape.utf8(self._pass_source)
            hashOldPass = bcrypt.hashpw( bbOldPAss, bbsalt ).decode('utf-8')
            logging.info(' save:: hashOldPass = ' + str(hashOldPass))
            logging.info(' save:: self.author_pass = ' + str(self.author_pass))
            if hashOldPass == self.author_pass:
                #  все норм, старый пароль - верный, можно заняться сменой пароля.
                bbWrk = (bbOldPAss+bbsalt)[0:32]
                tmpPrivateKey = pickle.loads(self.private_key)
                cipher_aes = AES.new(bbWrk, AES.MODE_EAX, tmpPrivateKey['nonce']) # закроем приватный ключ на пароль пользователя.

                logging.info(' save:: self.private_key = ' + str(tmpPrivateKey))

                tmpPrivate_key = cipher_aes.decrypt(tmpPrivateKey['cipherKey'])

                logging.info(' save:: tmpPrivate_key = ' + str(tmpPrivate_key))

                tmpHash = bcrypt.hashpw( tmpPrivate_key, bbsalt ).decode('utf-8') 
                logging.info(' save:: tmpHash = ' + str(tmpHash))
                logging.info(' save:: self.private_key_hash = ' + str(self.private_key_hash))
                if tmpHash == self.private_key_hash:
                    # все орм, мы нормально открыли приватный ключ, теперб его можно закрытьна новый пароль!
                    bbWrk = (newPassbb+bbsalt)[0:32]
                    cipher_aes = AES.new(bbWrk, AES.MODE_EAX) # закроем приватный ключ на пароль пользователя.
                    cipherKey = cipher_aes.encrypt(tmpPrivate_key)
                    self.private_key = pickle.dumps({'cipherKey': cipherKey, 'nonce': cipher_aes.nonce})
                    
        #             self.private_key = tornado.escape.utf8(self.private_key)
                    # на и запомним новый Хеш!!!!!
                    self.author_pass = bcrypt.hashpw( newPassbb, bbsalt ).decode('utf-8') 

            
                    
        if self.dt_header_id == 0:
            self.author_create = datetime.now()
            operationFlag = 'I'
        else:
            self.author_create =  self.author_create
            operationFlag = 'U'
            
        sha_hash_sou =  str(self.author_login) + str(self.author_name) + str(self.author_surname) + str(self.author_role) + str(self.author_phon) + str(self.author_email)  
            
        logging.info(' save:: Before-Before self = ' + str(self))

        logging.info(' save:: self.public_key = ' + str(self.public_key))
        logging.info(' save:: self.private_key = ' + str(self.private_key))
        logging.info(' save:: self.private_key_hash = ' + str(self.private_key_hash))
        
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
 
       
    

 
