#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# 


# from models.model import Model
# from model import Model

from __future__ import print_function

import sys, os

import hashlib
import base64
from datetime import datetime


import logging


import json
import pickle


from tornado import gen

import tornado.options

# http://initd.org/psycopg/docs/index.html
import psycopg2

# from somewhere import namedtuple
import collections
# collections.namedtuple = namedtuple
# from psycopg2.extras import NamedTupleConnection
from psycopg2.extras import DictCursor
# NamedTupleCursor

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives.asymmetric import padding, rsa

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.primitives import serialization


from _ast import Try
# from json.decoder import NaN


#############

# import config
# sys.path.append(os.path.dirname("./../../config"))
import config
# sys.path.pop()

# sys.path.append(os.path.dirname('./../../core'))

from core.Helpers      import *
from core.WikiException import *
from core.Helpers      import *

# sys.path.pop()



#from _overlapped import NULL




# синглетон нужен для того, что бы все потредители ходил в базу через одн курсор, все здорово, 
# НО, если несколько потербителей пойдут в базу одновременно с разны нитей, получится кавардак :-( )
# в общем, надо или убирать "одиночку" + открывать МНОГО конектов к базе  - один конект - один курсор
# или, искать новый дравер, который сможет работать с несколькими курсорами, в одном конекте. 

@singleton 
class Connector:
    def __init__ (self):    
        """
        # Connect to an existing database
        """
#         logging.info('Connector postgreBase = ' + str(config.options.postgreBase))
#         logging.info('Connector postgreHost = ' + str(config.options.postgreHost))
#         logging.info('Connector postgrePort = ' + str(config.options.postgrePort))
#         logging.info('Connector postgreUser = ' + str(config.options.postgreUser))
#         logging.info('Connector postgrePwd = ' + str(config.options.postgrePwd))
        
        self._connectInstans = psycopg2.connect(
                                                database= config.options.postgreBase, 
                                                host= config.options.postgreHost,
                                                port= config.options.postgrePort,
                                                user= config.options.postgreUser, 
                                                password= config.options.postgrePwd
                                                )
#         self._cursor = self._connectInstans.cursor(cursor_factory=NamedTupleCursor) DictCursor
        self._cursor = self._connectInstans.cursor(cursor_factory=DictCursor) 
    
    def getCursor (self):
        return self._cursor




class Model: #Connector:
    """
    # Набор методов для  работы с Ревизиями!
    # - добавит ревизию
    # - получить список ревизий
    # - получить оду ревизию...
    # - узнать является ли набор данных уникальным (не похожим на текущее значение данных - значит, у нас возможны циклы!!!!!)

    """


#         mainPrimaryList = {'dt_header_id': self.dt_header_id } - стоит отправить в инициализвцию!!!!
#         sha_hash_sou =  self.author_login + self.author_name + self.author_surname + self.author_role +self.author_phon + self.author_email  
#
#         mainPrimaryList = {'primaryName': 'article_id', 'primaryValue': 123 }
#         requestParamName
#
#         
#         
# #             mainPrimaryList = {'article_id': self.article_id }
# #             self.article_id = Model.save(self, authorId, operationFlag, mainPrimaryList, sha_hash_sou, 'article_id')
    
    
    class TableDef:
        """
        Описание каждой  таблицы данных в модели - это объект класса TableDef 
        Содержит:
        _tableName - название таблицы;
        _idFieldName - Если из таблицы надо что - либо 
        _mainPrimaryList
        
        _listAttrNames - список полей таблицы;
        со списком будем сравнивать список свойств наследника класа Model 
        и из оставшегося списка будем мастырить инсерты с абдейтами. (или только инсетты, т.к. абдейтов у нас нету)
        
            self._tableName = tabName  # Название таблицы, куда будемписать данные
            self._idFieldName = idFieldName
            self._mainPrimaryList = mainPrimaryList
            self._listAttrNames = listAttrNames # Список наименований полей таблицы. 

         
        """

        def __init__ (self, tabName=None, idFieldName=None, mainPrimaryList =None, listAttrNames=None ):
            """
            принимаем параметры: 
            tabName - имя таблицы хранения данных
            idFieldName - имя поля ИД в таблице - Строковое наименование индексного поля - его будем возвращать при инсертах
            
            mainPrimaryList = ['dt_header_id', ... ] - по этому писку мы выбираем поля,  мы абдейтим устаревшие данные (Это пример для автоов).
            
            listAttrNames - список атрибутов класса, наследника модели, -он же - список полей таблицы данных.
            """    
            self._tableName = tabName  # Название таблицы, куда будемписать данные
            self._idFieldName = idFieldName
            self._mainPrimaryList = mainPrimaryList
            self._listAttrNames = listAttrNames # Список наименований полей таблицы. 

        def getTableName(self):
            return self._tableName

        def getIdFieldName(self):
            return self._idFieldName

        def getMainPrimaryList(self):
            return self._mainPrimaryList
        
        def getLisAttr(self):
            return self._listAttrNames        
        
        

#     @property
    def __init__ (self):    
        """
        dataStruct - описание структуры данных;  
        headStruct - описание "заголовка" данных общая часть рабочего стола (таблица "dt_header") - может быть для "Авторов" и "Групп" 
        Для спска статей этот параметр отсутствует.
        
        """
        connector = Connector()
        self._cursor = connector.getCursor() # служебные параметры (те, которые не будут отбражаться в )
        
        self._dataStruct = None
        self._headStruct = None
        self._isHeaderEdit = False
        

#     def __del__(self):
#         self._cursor.close()
    
    def setDataStruct(self, dataStruct):
        self._dataStruct = dataStruct
        
    def setHeadStruct(self, headStruct):
        self._headStruct = headStruct 
            

    
#     @property
    def cursor(self):
        return self._cursor

    def begin(self, isolation= 'READ COMMITTED'):
        """
        START TRANSACTION;
        отдаем объект, который и будет делать все, до окончания трансакции 

        """
#         self._cursor.begin()
        self._cursor.execute("BEGIN")     
#         return self._cursor.xact(isolation)
#         self._cursor.xact(isolation)


    def commit(self):
        """
        commit;

        """
        self._cursor.execute("COMMIT")     
#         self._cursor.commit()   


# а вот так все описывается в документации!!!!!
# 
# 
# BEGIN;
# UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
# UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
# COMMIT;
#             self.rollback()
# 
#         self.begin()

    def rollback(self):
        """
        rollback;

        """
        self._cursor.execute("ROLLBACK")  
#         self._cursor.rollback()   


                
#     def insert(self, requestParamName = ''):
#         """
#         добавить в таблицу "tabName"  атрибуты класса, 
#         вернуть максимальный ИД, если requestParamName не пустой. 
#         
#         """
#         try:
# #             logging.info(' insert:: requestParamName = ' + str(requestParamName))
#             lCurs = self.cursor()
#             if requestParamName != '':
#                 del self.__dict__[requestParamName]
#             paramsObj = self.splitAttributes()
#             
#             
#             if requestParamName != '':
#                 sqlStr = "INSERT INTO " + self._tabName +" ( " + paramsObj.strListAttrNames + " ) VALUES ( " + paramsObj.strListAttrValues + " )  returning " + requestParamName
# #                 logging.info(' insert:: sqlStr = ' + sqlStr)
#                 lCurs.execute(sqlStr)
#                 sourse = lCurs.fetchone()
# #                 logging.info(' insert:: sourse = ' + str(sourse))
# #                 logging.info(' insert:: sourse[requestParamName] = ' + str(sourse[requestParamName]))
#                 self.__dict__[requestParamName] = sourse[requestParamName]
#                 return  sourse[requestParamName]
#             else:
#                 sqlStr = "INSERT INTO " + self._tabName +" ( " + paramsObj.strListAttrNames + " ) VALUES ( " + paramsObj.strListAttrValues + " )"
# #                 logging.info(' insert:: sqlStr = ' + sqlStr)
#                 lCurs.execute(sqlStr)
#             
#         except psycopg2.Error as error:
#             
#             logging.error (' insert exception:: ' + str (error) )
#             logging.error(' insert exception:: sqlStr = ' + sqlStr )
#             lCurs.rollback()
#             raise WikiException(error)


#     def update(self, whereSection):
#         """
#         изменить данные в таблицу "tabName"  атрибуты класса, 
#         вернуть максимальный ИД, если requestParamName не нудЁвый. 
#         """
#         try:
#             
#             lCurs = self._cursor #.cursor()
#             paramsObj = self.splitAttributes()
#             listSet = map(lambda x, y: str(x) + " = '" + str(y) + "'", paramsObj.listAttrNames, paramsObj.listAttrValues)
#             strSet =  ", ".join(listSet)
#             sqlStr = "UPDATE "+ self._tabName +" SET " + strSet + " WHERE " + whereSection
# #             logging.info(' update:: sqlStr = ' + sqlStr)
#             lCurs.execute(sqlStr)
# 
# #             self.commit()
#         except psycopg2.Error as error:
#             logging.error(' update exception:: ' + str (error) )
#             logging.error(' update exception:: sqlStr = ' + sqlStr )
#             lCurs.rollback()
#             raise WikiException(error)

    def save(self, autorId, operationFlag, revisions_sha_hash_source):
        """
        сохранение ревизии для данных.
        при сохранении ревизии стоит (наверное) делать так:
        - сказать всем ревизиям, что они устарели (сделать флаг "О")
        - попытаться добавить ревизию (с флагом "А") 
        - если не получилось, то на ревизии с тем, актуальным ХЕШЕМ, поставить фла "А"
        
        operationFlag - Флаг операции - оно или "добавить" или, "поменять" ('I' или 'U')

        revisions_sha_hash_source - Хеш по данным - это то, что определяет, мы вообще, должны сохранять, или как...

        Несколько параметров, которые имеем в атрибутах класса 
        
        self._dataStruct - описание основной таблицы даных, 
        self._headStruct - описание "заголовочной" таблицы 
        
         getTableName(self): - получить название таблицы данных
             ('author')
         getIdFieldName(self): - получить название поля ИД, которое является автоинкрементным
             ('dt_header_id')
         getMainPrimaryList(self): - получить структуру данных для правильной команды  - "старения данных"
             ({'primaryName': 'article_id', 'primaryValue': 123 } )
         getLisAttr(self): -  список всех полей таблицы - что бы этот список можно было дополнить реальными данными.
             (['dt_header_id', 'author_login','author_name','author_surname','author_role','author_phon','author_email'])
         
        INSERT INTO distributors (did, dname)
        VALUES (5, 'Gizmo Transglobal')
        ON CONFLICT (did) DO UPDATE SET dname = EXCLUDED.dname;

        Немного про транзакции:
        db.xact('SERIALIZABLE')  It will be interpolated directly into the START TRANSACTION statement. Normally, ‘SERIALIZABLE’ or ‘READ COMMITTED’:
        >>> x = db.xact(...)
            x.start()
            Start the transaction.
            x.commit()
            Commit the transaction.
            x.rollback()
            Abort the transaction.
        
        или так: 
        >>> with db.xact():
        ...  try:
        ...   ...
        ...  except postgresql.exceptions.UniqueError:
        ...   pass
            
        """
        headParamsObj = None
        if self._headStruct != None:
            headParamsObj = self.splitAttributes(self._headStruct.getLisAttr())
        
        try:
            _loDb = self.cursor()
            self.begin()

            if headParamsObj != None :
                if ( self.__dict__[self._headStruct.getIdFieldName()] == 0 or self.__dict__[self._headStruct.getIdFieldName()] == None ) :
                    # сохраним заголовок, если он определен для ЭТОГО класса объектов.
                    sqlStr = "INSERT INTO " + self._headStruct.getTableName() +" ( " + headParamsObj.strListAttrNames + ") VALUES " +\
                        "( " + headParamsObj.strListAttrValues + " ) returning " + self._headStruct.getIdFieldName() + "; "
                    headValue = self.getToInsertValue( self._headStruct.getLisAttr())    
                    _loDb.execute(sqlStr, tuple(headValue) ) # 'dt_header_type','public_key'
                    sourse = _loDb.fetchone()
                    self.__dict__[self._headStruct.getIdFieldName()] = sourse[self._headStruct.getIdFieldName()]
                    
                if self._isHeaderEdit and self.__dict__[self._headStruct.getIdFieldName()] > 0 :
                    # Заголовок Объекта поменялся! - его надо сохранить!
                    if self._headStruct.getLisAttr() != None:
                        listSet = self.splitAttributes2Update (self._headStruct.getLisAttr()) 
                        listWhere = self.splitAttributes2Update (self._headStruct.getMainPrimaryList()) # mainPrimaryList
                        if len(listSet.listAttrValues) > 0 and len(listWhere.listAttrValues) > 0:  
                            whereStr  = ' AND '.join(listWhere.listSetAttrNames) 
                            strSet = ' , '.join(listSet.listSetAttrNames)
                            sqlStr = "UPDATE " + self._headStruct.getTableName() + " SET " + strSet + " WHERE " + whereStr
                            toValueList = [] 
                            toValueList.extend(listSet.listAttrValues)
                            toValueList.extend(listWhere.listAttrValues)
                            _loDb.execute(sqlStr, tuple(toValueList))
            if self.__dict__[self._headStruct.getIdFieldName()] > 0 :
                list = []
#                 logging.info(' SAVE:: UPDATE self._dataStruct.getMainPrimaryList() = ' + str(self._dataStruct.getMainPrimaryList()))  
                if self._dataStruct.getMainPrimaryList() != None:
#                     Надо построить слварь из всех полей, записанных в mainPrimaryList
                    list = self.getList2Update (self._dataStruct.getMainPrimaryList()) 
#                     logging.info(' SAVE:: UPDATE list = ' + str(list))  
                    
                    dataParamseObj = self.splitAttributes(self._dataStruct.getLisAttr())
                    
                    if len(list) > 0:    
                        whtreStr  = ' AND '.join(list)    
                        # Все ревизии ЭТОЙ записи - устарели!!!! - проабдейтим список ревизий
                        sqlStr = "UPDATE " + self._dataStruct.getTableName() + " SET actual_flag = 'O' WHERE " + whtreStr
                        logging.info(' SAVE:: sqlStr = ' + str(sqlStr))  
                        _loDb.execute(sqlStr)
            
            operation_timestamp = datetime.now() 
            sha_hash =  hashlib.sha256(
                        tornado.escape.utf8(revisions_sha_hash_source + str(operation_timestamp) )
                                                ).hexdigest()
            
            returningStr = ''
            if self._dataStruct.getIdFieldName() != None:
                returningStr = " returning " + self._dataStruct.getIdFieldName()
            # Теперь можно записать новые данные  в ревизии.    
            
            dataParamseObj = self.splitAttributes(self._dataStruct.getLisAttr())
            
            dataParamseObj.strListAttrNames += ', actual_flag, revision_author_id,  operation_flag, sha_hash, operation_timestamp '
            dataParamseObj.strListAttrValues += ", %s, %s, %s,  %s, %s "
            
            sqlStr = "INSERT INTO " + self._dataStruct.getTableName() +" ( " + dataParamseObj.strListAttrNames + ") VALUES " +\
                    "( " + dataParamseObj.strListAttrValues + " ) "  +\
                    " ON CONFLICT (sha_hash) DO UPDATE SET actual_flag = 'A' "  + returningStr +  ' ;'
            
            dataValue = self.getToInsertValue( self._dataStruct.getLisAttr())

            logging.info(' SAVE:: dataParamseObj.strListAttrNames 1 = ' + str(dataParamseObj.strListAttrNames))  
            logging.info(' SAVE:: dataValue 1 = ' + str(dataValue))  

            dataValue += ['A', autorId, operationFlag, sha_hash, operation_timestamp]

            logging.info(' SAVE:: dataValue 2 = ' + str(dataValue))  
            
            _loDb.execute(sqlStr, tuple(dataValue))
            # если Это статьи, тогда нам нужнео сохранить статью, и получить ее ИД!
            if returningStr != '':
                sourse = _loDb.fetchone()
                self.__dict__[requestParamName] = sourse[requestParamName]
                self.commit()
                return  sourse[requestParamName]
            self.commit()
        except psycopg2.Error as error:
            logging.error(' save exception:: ' + str (error) )
            logging.error(' save exception:: sqlStr = ' + sqlStr )
            logging.error("Exception occurred", exc_info=True)
#             _loDb.rollback()
            self.rollback()
            raise WikiException(error)




    def select(self, 
               selectStr, # строка - чего хотим получить из селекта
               addTables,  # строка - список ДОПОЛНИТЕЛЬНЫХ таблиц (основную таблизу для объекта указываем при инициализации) 
               anyParams = {} #  все остальные секции селекта
               ):
        """
        получить данные (select)
        - ну, вынести его - и делать его из нескольких секций: 
        - селект (набор полей, котрые хотим получить из выборки)
        - фром  (набор дополнительных (кроме основной) таблиц для выборк)

               anyParams = {
                           'joinStr': '', # строка - список присоединенных таблиц
                           'whereStr': '', # строка набор условий для выбора строк
                           'groupStr': '', # строка группировка 
                           'orderStr': '', # строка порядок строк
                           'limitStr': '' # строка страница выборки
                            }
        - жоин
        - веа
        - ордер
        - групп
        - лимит вот как то так,  
        общий вид селекта, может выглядеть примерно так:
        SELECT 
            users.author_id,  
            users.author_login, 
            users.author_name, 
            users.author_role, 
            users.author_phon, 
            users.author_email, 
            users.author_external 
        FROM users 
        WHERE (author_login =  "login" OR author_email =  "login" ) 
        AND author_pass =  "$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0." 
        
              
        """
        try:
#             logging.info(' select:: addTables = ' + str(addTables))
            _loDb = self.cursor()
            sqlStr = 'SELECT '+ selectStr
            if addTables != None:
                sqlStr += ' FROM ' + self._dataStruct.getTableName() 
                if addTables  != '':  sqlStr += ', ' + str(addTables)
            
#             if addTables == '':
#                 sqlStr += ' FROM ' + self._dataStruct.getTableName() 
                
                
            if str(anyParams.get('joinStr', ''))     != '':  sqlStr += ' ' + str(anyParams.get('joinStr'))
            if str(anyParams.get('whereStr', ''))    != '':  sqlStr += ' WHERE ' + str(anyParams.get('whereStr'))
            if str(anyParams.get('groupStr', ''))    != '':  sqlStr += ' GROUP BY ' + str(anyParams.get('groupStr'))
            if str(anyParams.get('orderStr', ''))    != '':  sqlStr += ' ORDER BY ' + str(anyParams.get('orderStr'))
            if str(anyParams.get('limitStr', ''))    != '':  sqlStr += ' LIMIT ' + str(anyParams.get('limitStr'))
            logging.info(' select:: sqlStr = ' + sqlStr)

            _loDb.execute(sqlStr)
            sourse = _loDb.fetchall()
#             for one in sourse:
#                 logging.info('select:: list:: sourse = ' + str (one) )
            outListObj = self.dict2obj(sourse)    
#             for one in outListObj:
#                 logging.info('select:: list:: outListObj = ' + str (one) )
 
            return outListObj

        except psycopg2.Error as error:
            logging.error(' select exception:: sqlStr = ' + sqlStr )
            self.rollback()
            raise WikiException(error)

    def rowSelect(self, 
               selectRow, # строка - селект
               ):
        """
        получить данные (select)
        - из просто самого обычного селекта, - СТРОКИ 
        
              
        """
        try:
            _loDb = self.cursor()
#             logging.info('select:: list:: selectRow = ' + str (selectRow) )
            _loDb.execute(selectRow)
            sourse = _loDb.fetchall()
            outListObj = self.dict2obj(sourse)    
 
            return outListObj

        except psycopg2.Error as error:
            logging.error(' rowSelect exception:: sqlStr = ' + sqlStr )
            self.rollback()
            raise WikiException(error)

    def getToInsertValue(self, listTableFields):
        """
        получить списокреальных значений атрибутов класса  
        в момент исполнения метода
        отдать кортежем
        
        """
        objValuesNameList = list(self.__dict__.keys())
        listAttrValues = []        
        for objValue in objValuesNameList:
            if objValue.find('_') != 0 and (objValue) in listTableFields :
                listAttrValues.append(self.__getattribute__(objValue))
        
        return listAttrValues

    def getList2Update(self, mainPrimaryList):
        """
        получить набор параметров для абдейтов значений
        
        """
        listAttrValues = []        
        for objValue in mainPrimaryList:
                listAttrValues.append(objValue + ' = ' + str(self.__getattribute__(objValue)) )
        
        return listAttrValues


    def splitAttributes(self, listTableFields):
        """
        разделить собственные параметры (без параметров с подчеркиваниями ) на 2 списка - 
        1 - список имен параметров
        2 - значений параметров 
        это нужно для того, что бы использовать все параметры в операции 
        добавления или изменения данных в базе данных.
        На входе - список полей таблицы, 
            и мы из полного набора всех атрибутов в объкте, выберем только те, что есть во входном списке. 
        
        На выходе получим словарь из двух списков  
        """ 
#         objDict = self.__dict__
        objValuesNameList = list(self.__dict__.keys())
        class Out: pass   
        out = Out()
        out.listAttrNames = []
        out.listAttrValues = []    
        for objValue in objValuesNameList:
            if objValue.find('_') != 0 and (objValue) in listTableFields :
                out.listAttrNames.append(objValue)
                out.listAttrValues.append(self.__getattribute__(objValue))
        out.strListAttrNames = ", ".join(out.listAttrNames)
        out.strListAttrValues = ", ".join([ '%s' for row in out.listAttrNames]) # "'" + "', '".join(map(str,listAttrValues)) + "'"  
        return out


    def splitAttributes2Update(self, listTableFields):
        """
        Для генерации Апдейта  
        разделить собственные параметры (без параметров с подчеркиваниями ) на 2 списка - 
        1 - список имен параметров
        2 - значений параметров 
        это нужно для того, что бы использовать все параметры в операции 
        добавления или изменения данных в базе данных.
        На входе - список полей таблицы, 
            и мы из полного набора всех атрибутов в объкте, выберем только те, что есть во входном списке. 
        
        На выходе получим объект из двух списков  
        """ 
        objValuesNameList = list(self.__dict__.keys())
        class Out: pass   
        out = Out()
        out.listAttrValues = list()   
        out.listSetAttrNames = list()
        for objValue in objValuesNameList:
            if objValue.find('_') != 0 and (objValue) in listTableFields :
                out.listAttrValues.append(self.__getattribute__(objValue))
                out.listSetAttrNames.append( ' ' + objValue + ' = %s' )
        return out


 
    def dict2obj(self, dictSou):
        """
        преобразовать словарь (допустим, кортеж данных из селекта) в объект  
        """ 
        oList = []
        if len(dictSou) == 0: return oList
        for row in dictSou:
#             logging.info(' dict2obj:: row = ' + str(row))
#             logging.info(' dict2obj:: type(row) = ' + str(type(row)))
            rowDict = dict(row)
#             logging.info(' dict2obj:: rowDict = ' + str(rowDict))
            oneObj = self.__class__()
            for key in rowDict.items(): #.__getattribute__(name):
#                 logging.info(' dict2obj:: key = ' + str(key))
                oneObj.__setattr__(key[0], key[1])
            oList.append(oneObj)
                
        return oList

    def splitAttributes2Str(self):
        """
        разделить собственные параметры (без параметров с подчеркиваниями ) на 2 списка - 
        1 - список имен параметров
        2 - значений параметров 
        это нужно для того, что бы использовать все параметры в операции 
        добавления или изменения данных в базе данных.
        
        На выходе получим словарь из двух списков  
        """ 
#         objDict = self.__dict__
        objValuesNameList = list(self.__dict__.keys())
        listAttrNames = []
        listAttrValues = []        
        for objValue in objValuesNameList:
            if objValue.find('_') != 0:
                listAttrNames.append(objValue)
                listAttrValues.append(self.__getattribute__(objValue))

        
        class Out: pass   
        out = Out()
        out.listAttrNames = listAttrNames
        out.listAttrValues = listAttrValues    
        out.strListAttrNames = ", ".join(listAttrNames)
        out.strListAttrValues = "'" + "', '".join(map(str,listAttrValues)) + "'"   
#         out.strListAttrValues = "'" + "', '".join(listAttrValues) + "'"   
        return out


    def __str__(self): 
        attribList = self.splitAttributes2Str()
        className = str(self.__class__)
        itemsList = map(lambda x, y: ' "' + str(x) + '"' + ': "' + str(y) + '" ', attribList.listAttrNames, attribList.listAttrValues) 
        objValuesNameList = '\n'+ className + ': { \n\t' + ', \n\t'.join(itemsList) + '\n}'
        return objValuesNameList





class CipherWrapper:
    """
    Класс - обертка для процедур шифрования
    
    """
    bbsalt =  config.options.salt.encode()
    
    def __init__(self):
        self.backend = default_backend()
    
    def setKey(self, key):
        self._key = (key+self.bbsalt)[0:32]
    
    def symmetricEncrypt(self, key, data):
        """
        Зашифровать текст
        
        :param На входе - просто текст.  
        :Return: структуру вида {'ciphertext': ciphertext, 'iv': iv, 'tag': tag, 'associated_data': associated_data}, 
                сериализованную. (готова к передаче или сохранению в файл) (бинарник, по - идее.)
        """
        self.setKey(key) # .encode('utf-8')
        iv = os.urandom(12)
        associated_data = os.urandom(24)
#         logging.info(' Model:: symmetricEncrypt data = ' + str(data))

        # Construct an AES-GCM Cipher object with the given key and a
        # randomly generated IV.
        encryptor = Cipher(
            algorithms.AES(self._key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()
     
        # associated_data will be authenticated but not encrypted,
        # it must also be passed in on decryption.
        encryptor.authenticate_additional_data(associated_data)
     
        # Encrypt the plaintext and get the associated ciphertext.
        # GCM does not require padding.
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return  pickle.dumps({'ciphertext': ciphertext, 
                              'iv': iv, 
                              'tag': encryptor.tag, 
                              'associated_data': associated_data})
    
    def symmetricDecrypt(self, key, cipherPickle):
        """
        Расшифровать текст
        
        :param cipherPickle - Это сериализованная структура типа 
                {'ciphertext': ciphertext, 'iv': iv, 'tag': tag, 'associated_data': associated_data}
        :Return: отдаем уже готовый текст        
        """
        self.setKey(key)
        cipherData = pickle.loads(cipherPickle)

#         logging.info(' symmetricDecrypt:: key = ' + str(key))
#         logging.info(' symmetricDecrypt:: self._key = ' + str(self._key))
#         logging.info(' symmetricDecrypt:: cipherData = ' + str(cipherData))
        
        # Construct a Cipher object, with the key, iv, and additionally the
        # GCM tag used for authenticating the message.
        decryptor = Cipher(
            algorithms.AES(self._key),
            modes.GCM(cipherData['iv'], cipherData['tag']),
            backend=default_backend()
        ).decryptor()
     
        # We put associated_data back in or the tag will fail to verify
        # when we finalize the decryptor.
        decryptor.authenticate_additional_data(cipherData['associated_data'])
     
        # Decryption gets us the authenticated plaintext.
        # If the tag does not match an InvalidTag exception will be raised.
        return decryptor.update(cipherData['ciphertext']) + decryptor.finalize()




    def rsaInit(self):
        """
        Создаем пару ключей.
        """

        self.openPrivateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )        
        self.public_key = self.openPrivateKey.public_key()
        


    def rsaSet(self, publicKey, openPrivateKey):
        """
        Откуда  - то у меня ключи взлисЮ и их просто надо пережать в объект.
        
        """
        self.public_key = publicKey
        self.openPrivateKey = openPrivateKey
 
    def getPublicKey(self):
        return self.public_key 

    def getPrivateKey(self):
        return self.openPrivateKey 
    
    
    def rsaEncrypt(self, publicKey, data):
        """
        Зашифровать текст по процедуре RSA
        Все не просто - 
        1 - делаем сессионный ключ
        2 на ключе закрываем текст  
        3 на publicKey закрываем сессионный ключ 
        4 все это укладываем в некую структуру, которую ПОТОМ сериализуем, и будем щасливы!!!
        
        """
        session_pwd = Fernet.generate_key()
        ciphertext = self.symmetricEncrypt(session_pwd, data)

        cipherPwd = publicKey.encrypt(
            session_pwd,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=b'None'
            )
        )
        return  pickle.dumps({'ciphertext': ciphertext, 'cipherPwd': cipherPwd})
    
    
    def rsaDecrypt(self, cipherPickle):
        """
        Расшифровать текст по процедуре RSA
        """
        cipherData = pickle.loads(cipherPickle)
 
        plainPwd = self.openPrivateKey.decrypt(
            cipherData['cipherPwd'],
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=b'None'
            )
        )
        return symmetricDecrypt(self, plainPwd, cipherData['ciphertext'])
    
    

    def rsaPrivateSerialiation(self, pKey):
        """
        Сериализуем ключ 
        - что бы отдать его текстом.
        """
        pem = pKey.private_bytes(
           encoding=serialization.Encoding.PEM,
           format=serialization.PrivateFormat.TraditionalOpenSSL,
           encryption_algorithm=serialization.NoEncryption()
        )
        return pem # b''.join(pem.splitlines()) #[0]

    def rsaPubSerialiation(self, pKey):
        """
        Сериализуем ключ 
        - что бы отдать его текстом.
        """
        pem = pKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem # b''.join(pem.splitlines()) #[0]


    def rsaPrivateUnSerialiation(self, strKey):
        """
        Прекратить сериализованный ключ в нормальный.
        """
        pkey = serialization.load_pem_private_key(
                                    strKey,
                                    password=None,
                                    backend=default_backend()
                                    )
        return pkey

    def rsaPubUnSerialiation(self, strKey):
        """
        Прекратить сериализованный ключ в нормальный.
        """
#         logging.info(' rsaPubUnSerialiation :::: strKey = ' + str(strKey))

        pkey = serialization.load_pem_public_key(
                                    strKey,
                                    backend=default_backend()
                                    )
#         logging.info(' rsaPubUnSerialiation :::: pkey = ' + str(pkey))
#         logging.info(' rsaPubUnSerialiation :::: isinstance(pkey, rsa.RSAPublicKey) = ' + str(isinstance(pkey, rsa.RSAPublicKey)))
        
        return pkey
    
    def isinstance(self, pkey):
        return isinstance(pkey, rsa.RSAPublicKey)

