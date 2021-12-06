#!/usr/bin/env python3
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


import os
import os.path
################
import logging

dirModule = os.path.dirname(__file__)
nameModule = __file__
logger = logging.getLogger(nameModule)
logger.setLevel(logging.DEBUG)
###################################

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

from core.Helpers      import *

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
        self.author_name  = '' 
        self.author_surname = ''
        self.author_role = ''
        self.author_phon = '' 
        self.author_email = ''
        # если параметр "труй", то контакт 
        self.author_is_publick_contakt = False # (author_phon, author_email) доступен для просмотра.
        
        self.author_yourself_story = '' #  просто аннотация к автору, не архивим, не закрываем, отдаём как есть :-) 
        
        self.dt_header_type ='author'
        self.public_key = None # текст публичного ключа, так, как он хранится в БАЗЕ - нужно для передачи в клиента.
        self._wrkPublicKey = None # объект -для работы с публичным ключем на стороне бэкЕнда.
        
        

        # #############################
        # # Всякие нужные штуки....

        # self.autorsList = []

        Model.__init__(self)  
        self.setDataStruct(Model.TableDef( tabName='authors', 
                                      idFieldName=None,
                                      mainPrimaryList =['dt_header_id'],
                                      listAttrNames=['dt_header_id', 'author_name','author_surname','author_role','author_phon','author_email', 'author_is_publick_contakt']))
        
        self.setHeadStruct(Model.TableDef( tabName='dt_headers', 
                                      idFieldName='dt_header_id',
                                      mainPrimaryList =['dt_header_id'],
                                      listAttrNames=['dt_header_type','public_key']))

#         logging.info(' __init__:: After self = ' + str(self))
        
        
        #####################
        # END
        


    def setSearchParams(self, **serchParams):
        """
        Добавить поисковых параметров.

        надо передаь набор поисковых параметров как список. уу=11....

        serchParams = 
        {'groupId': 12, 'serchParams': 'lec', 'authorId': 123, 'authorHash': 'asdasd..asdsa'}
        
        self.groupId,  - Грппа, всех авторов которой  хочу найти
        self.serchStr - просто кусок имени автора.... - если эт параметры не "нулевые", тада надо править 
        self.authorId
        self.authorHash

        вызов выглядит:

        setSearchParams(groupId=12, serchParams='lec', authorId=123, authorHash='asdasd..asdsa')
        
        """
        
        if 'groupId' in serchParams:
            self.groupId = serchParams['groupId']

        if 'serchStr' in serchParams:
            self.serchStr = serchParams['serchStr']

        if 'authorId' in serchParams:
            self.authorId = serchParams['authorId']

        if 'authorHash' in serchParams:
            self.authorHash = serchParams['authorHash']
        

    def makeSerch(self):
        """
        Выбрать список всех авторов в системе 
        мы загружаем публичный ключ авторов для возможного дальнейшего использования.
        
        self.groupId,  - Грппа, всех авторов которой  хочу найти
        self.serchStr - просто кусок имени автора.... - если эт параметры не "нулевые", тада надо править 
        "whereStr" - ну, как  - то так....

        """

        selectStr = 'dt_headers.dt_header_id,  author_login, author_name, author_surname, author_role, author_phon, author_email, author_is_publick_contakt, author_create, dt_headers.public_key '
        fromStr = 'dt_headers' #'authors'
        anyParams = {
                    'whereStr': "  dt_headers.dt_header_id = authors.dt_header_id  AND actual_flag = 'A' ",
                    'orderStr': ' dt_header_id', # строка порядок строк
                     }
                     
        if hasattr(self, 'serchStr'):
            anyParams['whereStr'] += ' AND serchStr'

        if hasattr(self, 'authorId'):
            anyParams['whereStr'] += ' AND dt_headers.dt_header_id = ' + str(self.authorId)

        if hasattr(self, 'authorHash'):
            anyParams['whereStr'] += " AND authors.sha_hash = '" + self.authorHash + "'"

        if hasattr(self, 'serchStr'):
            anyParams['whereStr'] += " AND ( authors.author_name = '" + self.serchStr + "'" + " OR  authors.author_surname = '" + self.serchStr + "' ) " 


        # if hasattr(self, 'groupId') ]:
        #     anyParams['whereStr'] += ' AND groupId'
        #  тут надохорошо подумать, группы ищем через списки групп. - селект силно меняется!!!



        self.autorsList = []
        count = 0
        resList = self.select(selectStr, fromStr, anyParams)
        for oneAuthor in resList:
            logging.info( 'Author:: list::  oneAuthor = ' + str(oneAuthor)) 
            self.autorsList.append(self.parsingAuthor(oneAuthor))
            count += 1

        # logging.info( 'Author:: list::  self.autorsList = ' + str(self.autorsList))

        # return count
        return self.autorsList;



    def getList(self):
        return self.autorsList;



    def parsingAuthor(self, autorStruct):
        """
        Разобрать структуру, которая приходит из селекта, (словарь)
        и сделать полноценный ОБЪЕКТ  - Автора.
        (Выкинуть все скрытые аттрибуты!!!! - а вот ЭТО делать НЕ БУДУ!!!!)
        """
        newAuthor = Author()
        objValuesNameList = list(autorStruct.__dict__.keys())
        for objValue in objValuesNameList:
            newAuthor.__setattr__(objValue, autorStruct.__getattribute__(objValue) )
            _public_key = bytes(newAuthor.public_key)
            if _public_key != b'' and _public_key != None:
                newAuthor.unserializePyblicKey(_public_key)
            # if objValue.find('_') != 0:
            #     newAuthor.__setattr__(objValue, autorStruct.__getattribute__(objValue) )
            # else:
            #     del newAuthor.__dict__[objValue] 
            #     # pass
        
             
        return newAuthor                  


# 
    def countAutors(self):
        """
        Получить количество Авторов, зарегистрированных в системе.
        """
        selectStr = " count (dt_header_id) AS cnt "

        resList = self.select(selectStr)
        for oneAuthor in resList:
            pass
            # logger.info( ' countAutors::  oneAuthor.cnt = ' + str(oneAuthor.cnt)) 

        return oneAuthor.cnt;


    def unserializePyblicKey(self, _public_key):
        """
        сделать из текстового публичного ключа объект "публичный ключ" для последующей работы

        """
        try:
            logging.info(' unserializePyblicKey lockPublic_key = ' + str(_public_key ))
            cip = CipherWrapper()
            self._wrkPublicKey = cip.rsaPubUnSerialiation(_public_key)
        except Exception as e:
            logging.error(' unserializePyblicKey exception::  = ' + str(e) )
            self._wrkPublicKey = None



class AuthorizedAuthor (Author):
    """
    
     Автор, прошедший авторизацию - 
    
     Наследник от Автора. 
     вся работа по Авторизации, Сохранении параметров выолняется именно тут.
    
    стоило бы перечислить все роли.
    author_role - 'admin','volunteer' 
    
    при регистрации или редактировании пароля 
    (операция сохранить - эти поля надо обрабатывать отдельно и специально.)
    
    """

#         mainPrimaryList = {'dt_header_id': self.dt_header_id } - стоит отправить в инициализвцию!!!!
#         sha_hash_sou =  self.author_login + self.author_name + self.author_surname + self.author_role +self.author_phon + self.author_email  
#         
#         
# #             mainPrimaryList = {'article_id': self.article_id }
# #             self.article_id = Model.save(self, authorId, operationFlag, mainPrimaryList, sha_hash_sou, 'article_id')


    def __init__ (self): 
        Author.__init__(self)     

        self.author_login = ''
        self.author_pass = ''

        self.private_key = None # закрытый приватный ключ (текст, взятый и базы.)
        self.private_key_hash = None # ????
        self._wrkPrivateKey = None #

        #############################
        #############################
        # конец описания объекта.
        #############################



        
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
                                      listAttrNames=['dt_header_id', 'author_login','author_pass', 'author_name','author_surname','author_role','author_phon','author_email', 'author_is_publick_contakt', 'private_key', 'private_key_hash']))
        
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
            self._private_key = cip.symmetricEncrypt(self._pass_source, bArrKey)
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
                self._private_key = cip.symmetricEncrypt(self._pass_source, bArrKey)
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
                self._private_key = bytes(self._private_key)#.decode(encoding="utf-8") #.decode('utf-8') 
                self.private_key_hash = bytes(self.private_key_hash)#.decode(encoding="utf-8") #.decode('utf-8') 

                if self.public_key != b'' or self.public_key != None:
                    self._openPublicKey = cip.rsaPubUnSerialiation(self.public_key)
                    
                # пока мы знаем пароль, надо получить и положить в данные пользователя, в сессию, его АСКРЫТЫЙ приватный ключик!!!!
                if self._private_key != b'' or self._private_key != None:
                    strKey = cip.symmetricDecrypt( tornado.escape.utf8(pwdStr), self._private_key) 
                    tmpHash = bcrypt.hashpw( strKey, bbsalt )
                    if tmpHash == bytes(self._private_key_hash):
                        self._openPrivateKey = cip.rsaPrivateUnSerialiation( strKey )
                    else:
                        # если ключи прочитались не верно, наверное х стоит переписать, 
                        # и Автор ваще не должен иметь возоности ключами пользоваться, 
                        # и автор должен идти в настройки профиля и редактировать из, и генерить сее новые ключи.
                        self._openPrivateKey = None
                        self._openPublicKey = None
                        self._private_key = None
                        self.public_key = None
                logging.info(' login:: END self = ' + str(self))
            except Exception as err:
                logging.error(' login:: END:: err = ' + str(err) )
                self._private_key_hash = None
                self._private_key = None
                self.public_key = None
                self._openPrivateKey = None
                self._openPublicKey = None
#                 self.public_key = None

#             logging.info(' login:: END self = ' + str(self))
            return self
        else:
            raise WikiException(LOGIN_ERROR)



    def parsingAuthor(self, autorStruct):
        """
        Разобрать структуру, которая приходит из селекта, (словарь)
        и сделать полноценный ОБЪЕКТ  - Автора.
        (Выкинуть все скрытые аттрибуты!!!! - а вот ЭТО делать НЕ БУДУ!!!!)
        """
        newAuthor = AuthorizedAuthor()
        objValuesNameList = list(autorStruct.__dict__.keys())
        for objValue in objValuesNameList:
            newAuthor.__setattr__(objValue, autorStruct.__getattribute__(objValue) )
            _public_key = bytes(newAuthor.public_key)
            if _public_key != b'' and _public_key != None:
                newAuthor.unserializePyblicKey(_public_key)
            _private_key = bytes(newAuthor.private_key)
            if _private_key != b'' and _private_key != None:
                newAuthor.unserializePrivateKey(_private_key)
        
            
        return newAuthor                  


    def unserializePrivateKey(self, _private_key):
        """
        Сделать из ОТКРЫТОГО приватного ключа объект - для загрузки в Автора.
        :param _private_key - текстовый вариант приватного ключа (НЕ ЗАКРЫТ!!!!) 
        :Return: отдаем ОБЪЕКТ класса "....openssl.rsa._RSAPrivateKey" 
        
        """
        try:
            cip = CipherWrapper()
            self._wrkPrivateKey =  cip.rsaPrivateUnSerialiation( _private_key )
        except Exception as e:
            logging.error(' unserializePrivateKey exception::  = ' + str(e) )
            self._wrkPrivateKey =  None
            


    #     def parsing(self, picledAutor):
    #         """
    #         на входе у нас строка - сериализованный автор, который, пока лежит в сесии,
    #         Главное, у этого автор  - открытый приватный ключ, в текстовом виде.  
    #         его надо разобрать, и превратить в полноценного автора, с которым РАБОТАТЬ.
    #         ну, и, естественно, загрузить его в "селф"
            
    #         """
    #         newAuthor = Author()
    #         newAuthor = pickle.loads(picledAutor)
    #         self =  self.parsingAuthor() #  разберем все поля, кроме приватного ключа       

    #         _private_key = bytes(newAuthor.private_key)
    #         del newAuthor.private_key
    #         if _private_key != b'' and _private_key != None:
    #             newAuthor.unserializePrivateKey(_private_key)

                

                
    #     def serializationAuthor(self):
    #         """
    #         Подготовить к сериализации - унас 2 поля  - private_key и public_key 
    #         являются объектами, 
    #         вот их и надо превратить в текст.
    #         :Return: отдаем СТРОКУ с сериализованным объектом 
    #         """
    #         # pickle.dumps(_authorLoc.prepareForSerialization())

    # #         logging.info( 'serializationAuthor  self = ' + str(self))

    #         newAuthor = Author()
    #         cip = CipherWrapper()
    #         newAuthor = self.preparingForPicked (self)
    #         if self._openPrivateKey != None and self._openPrivateKey != b'' and cip.isInstancePrivateKey(self._openPrivateKey): 
    #             newAuthor._openPrivateKey = cip.rsaPrivateSerialiation(self._openPrivateKey)
    # #         logging.info( 'serializationAuthor  newAuthor.public_key = ' + str(newAuthor.public_key))
    # #         if newAuthor.public_key != None and newAuthor.public_key != b'' and cip.isInstancePublicKey(newAuthor.public_key):
    # #             _public_key = newAuthor.public_key
    # #             del newAuthor.public_key 
    # #             newAuthor.public_key = cip.rsaPubSerialiation(_public_key)
    # #         logging.info( 'serializationAuthor  newAuthor = ' + str(newAuthor))
    # #         logging.info( 'serializationAuthor END newAuthor = ' + str(newAuthor))

    #         return pickle.dumps(newAuthor.__dict__)    
    
    
    #     def getPublicProfile(self, authorModel):
    #         newAuthor = Author()
    #         newAuthor = self.preparingForPicked(authorModel)
    #         newAuthor.author_pass = None
    #         newAuthor.public_key = None
    #         newAuthor.private_key = None
    #         newAuthor.private_key_hash = None
    #         return newAuthor
            
            
    
    #     def unSerializationAuthor(self, authorPicle):
    #         """
    #         Получить строку, и сделать из нее Объект - Автора.
    #         Это делаем при вынимании автора из сессии.
    #         :param Строку с Сериализованым автором 
    #         :Return: отдаем ОБЪЕКТ Автора.
    #         """
    # #         logging.info( 'unSerializationAuthor  self = ' + str(self))

    #         cip = CipherWrapper()
    #         authorDict = pickle.loads(authorPicle)
    #         self.parsingOfPicked(authorDict) 
            
    #         if self._openPrivateKey != None and self._openPrivateKey != b'': 
    #             _openPrivateKey = cip.rsaPrivateUnSerialiation(self._openPrivateKey)
    #             del self._openPrivateKey
    #             self._openPrivateKey = _openPrivateKey
                    
    #         if self.public_key != None and self.public_key != b'':
    #             self._openPublicKey = cip.rsaPubUnSerialiation(self.public_key)

    # #         logging.info(' unSerializationAuthor:: END self = ' + str(self))   

