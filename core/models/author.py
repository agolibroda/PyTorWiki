#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Goliboda
#
# authors.py
#
#
# from core.models.author     import Author
#
#

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

import tornado.escape
import tornado.options

import config
from core.WikiException import *

from . import Model, CipherWrapper
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
#         logging.info('Author:: __init__')
        
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
        
        self.author_yourself_story = '' #  просто аннотация к автору, не архивим, не закрываем, отдаём как есть :-) 
        
        self.dt_header_type ='author'
        self.public_key = None
        self.private_key = None
        self.private_key_hash = None
        self._openPublicKey = None
        self._openPrivateKey = None
        
        
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

#         logging.info(' __init__:: After self = ' + str(self))
        
        
        #####################
        # END
      

    def save(self):
        """
        сохранить значение - сохраняются все значимые (без подчеркивания) 
        свойства объекта
        пароль (новый,старый) перешифровывается 
        """
        
        bbsalt =  config.options.salt.encode()
        cip = CipherWrapper()
        
#             authorLoc.password_entered = passwd
#             authorLoc.author_old_pass = self.get_argument("old_pass")
        
        self._old_pass = bytes(self.author_old_pass, 'utf-8')
        self._pass_source = bytes(self.password_entered, 'utf-8')
#         self.author_pass = bytes(self.author_pass, 'utf-8')

        logging.info(' save:: BEFORE work self = ' + str(self))
         
        if self._pass_source != '' and (self.dt_header_id == 0 or self.dt_header_id == None):
            #  это новый пользователь, для него просто делаем ХЕШ
#             self._pass_source = tornado.escape.utf8(self._pass_source) #  превратим пароль, введенный пользователем в последовательность байтов.
#             self._pass_source = self._pass_source.decode('utf-8') #  превратим пароль, введенный пользователем в последовательность байтов.
            self.author_pass = bcrypt.hashpw( self._pass_source, bbsalt ).decode('utf-8') 

        # self.dt_header_id == 0 or self.dt_header_id == None) and - когда проверим  
        # здать новую приватно-публичую парочку, если ее не было раньше.
        isNotPubKey = not cip.isInstancePublicKey(self._openPublicKey)
#         logging.info(' save:: 1 isNotPubKey = ' + str(isNotPubKey))
#         logging.info(' save:: 1 self._pass_source = ' + str(self._pass_source))
        if ( self._pass_source != b'' and isNotPubKey ):
            cip.rsaInit() # сделать пару ключей 
            self._openPublicKey = cip.getPublicKey()
            self._openPrivateKey = cip.getPrivateKey() # поучить незакрытый приватный ключ
            bArrKey = cip.rsaPrivateSerialiation(self._openPrivateKey)
            self.private_key_hash = bcrypt.hashpw( bArrKey, bbsalt ).decode('utf-8') # получим ХЕш приватного ключа - для последуюей проверки при восстановлении пароля
            # закрыть приватный ключ на пароле автора.
            self.private_key = cip.symmetricEncrypt(self._pass_source, bArrKey)
            self.public_key = cip.rsaPubSerialiation(self._openPublicKey)
            
            self._isHeaderEdit = True

#         logging.info(' save:: 2 work self = ' + str(self))

        # если мы поменяли пароль, значит, я должен из формы получить 2 значения - старый пароль и новый пароль - и оба в тесте.    
        # потом я проверю, что старый пароль - совпадает ХЕШЕМ,
        # еслиДА, тогда 
        # 1 - декодировать приватный ключ старым паролем,
        # 2 закодировать - новым, сделать новый ХЕШ, и - УРА!!!!
        if self._pass_source != b'' and self._old_pass != b'' and not isNotPubKey :
            hashOldPass = bcrypt.hashpw( self._old_pass, bbsalt ).decode('utf-8')
            logging.info(' save:: 2 work self.author_pass = ' + str(self.author_pass))
            logging.info(' save:: 2 work hashOldPass = ' + str(hashOldPass))
            if hashOldPass == self.author_pass:
                #  все норм, старый пароль - верный, можно заняться сменой пароля.
#                 tmpPrivate_key = cip.symmetricDecrypt(self._old_pass, self.private_key)
                bArrKey = cip.rsaPrivateSerialiation(self._openPrivateKey)
#                 tmpHash = bcrypt.hashpw( bArrKey, bbsalt ).decode('utf-8') 
#                 if tmpHash == self.private_key_hash:
                    # все орм, мы нормально открыли приватный ключ, теперб его можно закрытьна новый пароль!
#                 cip.setKey(self._pass_source)
                self.private_key = cip.symmetricEncrypt(self._pass_source, bArrKey)
                # на и запомним новый Хеш пароля!!!!!
                self.author_pass = bcrypt.hashpw( self._pass_source, bbsalt ).decode('utf-8') 
            else:
                # все плохо, стрый пароль не верный, ничего сохранять нельзя!!!!
                raise WikiException(OLD_PASSWORD_IS_BAD) 

        logging.info(' save:: 3 work self = ' + str(self))
                    
        if self.dt_header_id == 0:
            self.author_create = datetime.now()
            operationFlag = 'I'
        else:
            self.author_create =  self.author_create
            operationFlag = 'U'
            
        sha_hash_sou =  str(self.author_login) + str(self.author_name) + str(self.author_surname) + str(self.author_role) + str(self.author_phon) + str(self.author_email)  
#         вот тут  self.private_key должен быть, и должен быть закрытым!!!!
        logging.info(' save:: 99 self = ' + str(self)) 
           
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
        selectStr = 'dt_headers.dt_header_id, author_login, author_name,  author_surname, author_pass, author_role, author_phon, author_email, dt_headers.public_key, authors.private_key, authors.private_key_hash' # строка - чего хотим получить из селекта
        fromStr = 'dt_headers' #'authors'
        anyParams = {
                    'whereStr': " dt_headers.dt_header_id = authors.dt_header_id AND authors.actual_flag = 'A' AND  " + 
                    " (author_login =  '" + loginMailStr + "' OR author_email =  '" + loginMailStr + "' )  AND author_pass =  '"  + test_pass + "' " , 
                     }
        resList = self.select(selectStr, fromStr, anyParams)
        
        if len(resList) == 1:
            objValuesNameList = list(resList[0].__dict__.keys())
            for objValue in objValuesNameList:
                if objValue.find('_') != 0:
                    self.__setattr__(objValue,resList[0].__getattribute__(objValue) )
            #  вот тут надо посмотреть - что у нс с данными пользователя происходит - и посмотреть - что ложится в сесию. :-) 
            
#             logging.info(' login:: After Load self = ' + str(self))
            
            try:
                cip = CipherWrapper()
#                 .decode('utf-8')
                self.public_key = bytes(self.public_key)#.decode(encoding="utf-8") #.decode('utf-8') 
                self.private_key = bytes(self.private_key)#.decode(encoding="utf-8") #.decode('utf-8') 
                self.private_key_hash = bytes(self.private_key_hash)#.decode(encoding="utf-8") #.decode('utf-8') 

                if self.public_key != b'' or self.public_key != None:
                    self._openPublicKey = cip.rsaPubUnSerialiation(self.public_key)
                    
                # пока мы знаем пароль, надо получить и положить в данные пользователя, в сессию, его АСКРЫТЫЙ приватный ключик!!!!
                if self.private_key != b'' or self.private_key != None:
                    strKey = cip.symmetricDecrypt( tornado.escape.utf8(pwdStr), self.private_key) 
                    tmpHash = bcrypt.hashpw( strKey, bbsalt )
                    if tmpHash == bytes(self.private_key_hash):
                        self._openPrivateKey = cip.rsaPrivateUnSerialiation( strKey )
                    else:
                        # если ключи прочитались не верно, наверное х стоит переписать, 
                        # и Автор ваще не должен иметь возоности ключами пользоваться, 
                        # и автор должен идти в настройки профиля и редактировать из, и генерить сее новые ключи.
                        self._openPrivateKey = None
                        self._openPublicKey = None
                        self.private_key = None
                        self.public_key = None
                logging.info(' login:: END self = ' + str(self))
            except Exception as err:
                logging.error(' login:: END:: err = ' + str(err) )
                self.private_key_hash = None
                self.private_key = None
                self.public_key = None
                self._openPrivateKey = None
                self._openPublicKey = None
#                 self.public_key = None

#             logging.info(' login:: END self = ' + str(self))
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
        Это загрузка ИСКЛЮЧИТЕЛЬНО не "себя". 
        Себя мы загружаем ТОЛЬКО при логине, и тянем в сессии!!!!!!
        мы загружаем публичный ключ автора для возможного дальнейшего использования.
         
        """

        resList = self.select(
                    'dt_headers.dt_header_id, author_login, author_name,  author_surname, author_pass, author_role, author_phon, author_email, author_create, dt_headers.public_key', # строка - чего хотим получить из селекта
                    'dt_headers', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': "  dt_headers.dt_header_id = authors.dt_header_id  AND  dt_headers.dt_header_id = " + str(authorId) + \
                     " AND actual_flag = 'A' " 
                     } #  все остальные секции селекта
                    )
#         logging.info('Author:: get:: resList = ' + str(resList))
        # от ут надо будет разкрыть приватный ключ????? 
        if len(resList) == 1:
#             return resList[0]
            objValuesNameList = list(resList[0].__dict__.keys())
            for objValue in objValuesNameList:
                 if objValue.find('_') != 0:
                    self.__setattr__(objValue,resList[0].__getattribute__(objValue) )
                    
#             self.author_pass =  bytes(self.author_pass, 'utf-8')                  
            _public_key = bytes(self.public_key)
            if _public_key != b'' and _public_key != None:
                self.unserializePyblicKey(_public_key)
            return self
        else:
            raise WikiException(LOAD_ONE_VALUE_ERROR)


    def list(self):
        """
        Выбрать список всех авторов в системе 
        мы загружаем публичный ключ авторов для возможного дальнейшего использования.
        
        """
        selectStr = 'dt_headers.dt_header_id,  author_login, author_name, author_surname, author_role, author_phon, author_email, author_create, dt_headers.public_key '
        fromStr = 'dt_headers' #'authors'
        anyParams = {
                    'whereStr': "  dt_headers.dt_header_id = authors.dt_header_id  AND actual_flag = 'A' ",
                    'orderStr': ' dt_header_id', # строка порядок строк
                     }

        res = []
        resList = self.select(selectStr, fromStr, anyParams)
        for oneAuthor in resList:
            res.append(self.parsingAuthor(oneAuthor))
        return res
 
    def unserializePyblicKey(self, _public_key):
        try:
            del self._openPublicKey
            cip = CipherWrapper()
            self._openPublicKey = cip.rsaPubUnSerialiation(_public_key)
        except :
#             logging.error(' insert exception:: sqlStr = ' + sqlStr )
            self._openPublicKey = None


    def unserializePrivateKey(self, _private_key):
        """
        Сделать из ОТКРЫТОГО приватного ключа объект - для загрузки в Автора.
        :param _private_key - текстовый вариант приватного ключа (НЕ ЗАКРЫТ!!!!) 
        :Return: отдаем ОБЪЕКТ класса "....openssl.rsa._RSAPrivateKey" 
        
        """
        try:
            del self._openPrivateKey
            cip = CipherWrapper()
            self._openPrivateKey =  cip.rsaPrivateUnSerialiation( _private_key )
        except :
            self._openPrivateKey =  None
            

#     def serializeKeys(self):
#         """
#         Сделать из РАБОЧЕГО приватного ключа строковеое предствление, 
#         Для последующего хранения в сесии, допустим.
#         :param _private_key - ОБЪЕКТ класса "....openssl.rsa._RSAPrivateKey"  
#         :Return: отдаем текстовый вариант приватного ключа (НЕ ЗАКРЫТ!!!!) 
#         
#         """
#         try:
#             cip = CipherWrapper()
#             tmp = cip.rsaPrivateSerialiation( self.public_key )
#             del self.public_key
#             self.public_key = tmp
#             tmp = cip.rsaPrivateSerialiation( self._openPrivateKey )
#             del self.public_key
#             del self.public_key
#         except :
#             
#             return ''
        

    def parsingAuthor(self, autorStruct):
        """
        Разобрать структуру, которая приходит из селекта,
        и сделать полноценный ОБЪЕКТ  - Автора.
        """
        newAuthor = Author()
        objValuesNameList = list(autorStruct.__dict__.keys())
        for objValue in objValuesNameList:
             if objValue.find('_') != 0:
                newAuthor.__setattr__(objValue, autorStruct.__getattribute__(objValue) )
        _public_key = bytes(newAuthor.public_key)
        if _public_key != b'' and _public_key != None:
            newAuthor.unserializePyblicKey(_public_key)
             
        return newAuthor                  


    def publicKey(self):
        return self._openPublicKey       


    def privateKey(self):
        return self._openPrivateKey       
    

    def parsing(self, picledAutor):
        """
        на входе у нас строка - сериализованный автор, который, пока лежит в сесии,
        Главное, у этого автор  - открытый приватный ключ, в текстовом виде.  
        его надо разобрать, и превратить в полноценного автора, с которым РАБОТАТЬ.
        ну, и, естественно, загрузить его в "селф"
        
        """
        newAuthor = Author()
        newAuthor = pickle.loads(picledAutor)
        self =  self.parsingAuthor() #  разберем все поля, кроме приватного ключа       

        _private_key = bytes(newAuthor.private_key)
        del newAuthor.private_key
        if _private_key != b'' and _private_key != None:
            newAuthor.unserializePrivateKey(_private_key)

            

            
    def serializationAuthor(self):
        """
        Подготовить к сериализации - унас 2 поля  - private_key и public_key 
        являются объектами, 
        вот их и надо превратить в текст.
        :Return: отдаем СТРОКУ с сериализованным объектом 
        """
        # pickle.dumps(_authorLoc.prepareForSerialization())

#         logging.info( 'serializationAuthor  self = ' + str(self))

        newAuthor = Author()
        cip = CipherWrapper()
        newAuthor = self.preparingForPicked (self)
        if self._openPrivateKey != None and self._openPrivateKey != b'' and cip.isInstancePrivateKey(self._openPrivateKey): 
            newAuthor._openPrivateKey = cip.rsaPrivateSerialiation(self._openPrivateKey)
#         logging.info( 'serializationAuthor  newAuthor.public_key = ' + str(newAuthor.public_key))
#         if newAuthor.public_key != None and newAuthor.public_key != b'' and cip.isInstancePublicKey(newAuthor.public_key):
#             _public_key = newAuthor.public_key
#             del newAuthor.public_key 
#             newAuthor.public_key = cip.rsaPubSerialiation(_public_key)
#         logging.info( 'serializationAuthor  newAuthor = ' + str(newAuthor))
#         logging.info( 'serializationAuthor END newAuthor = ' + str(newAuthor))

        return pickle.dumps(newAuthor.__dict__)    
 
 
    def getPublicProfile(self, authorModel):
        newAuthor = Author()
        newAuthor = self.preparingForPicked(authorModel)
        newAuthor.author_pass = None
        newAuthor.public_key = None
        newAuthor.private_key = None
        newAuthor.private_key_hash = None
        return newAuthor
        
        
 
    def unSerializationAuthor(self, authorPicle):
        """
        Получить строку, и сделать из нее Объект - Автора.
        Это делаем при вынимании автора из сессии.
        :param Строку с Сериализованым автором 
        :Return: отдаем ОБЪЕКТ Автора.
        """
#         logging.info( 'unSerializationAuthor  self = ' + str(self))

        cip = CipherWrapper()
        authorDict = pickle.loads(authorPicle)
        self.parsingOfPicked(authorDict) 
        
        if self._openPrivateKey != None and self._openPrivateKey != b'': 
            _openPrivateKey = cip.rsaPrivateUnSerialiation(self._openPrivateKey)
            del self._openPrivateKey
            self._openPrivateKey = _openPrivateKey
                
        if self.public_key != None and self.public_key != b'':
            self._openPublicKey = cip.rsaPubUnSerialiation(self.public_key)

#         logging.info(' unSerializationAuthor:: END self = ' + str(self))   

