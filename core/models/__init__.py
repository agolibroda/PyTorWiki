#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# 


# from models.model import Model
# from model import Model

from __future__ import print_function

# import sys, os, 

import hashlib
import base64
from datetime import datetime


import logging


import json

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



from _ast import Try
from json.decoder import NaN


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

        Что и как делаем:
        
            
        """
        headParamsObj = None
        if self._headStruct != None:
            headParamsObj = self.splitAttributes(self._headStruct.getLisAttr())
        
        try:
            _loDb = self.cursor()
            self.begin()

            if headParamsObj != None and ( self.__dict__[self._headStruct.getIdFieldName()] == 0 or self.__dict__[self._headStruct.getIdFieldName()] == None ) :
                # сохраним заголовок, если он определен для ЭТОГО класса объектов.
                sqlStr = "INSERT INTO " + self._headStruct.getTableName() +" ( " + headParamsObj.strListAttrNames + ") VALUES " +\
                    "( " + headParamsObj.strListAttrValues + " ) returning " + self._headStruct.getIdFieldName() + "; "
                headValue = self.getToInsertValue( self._headStruct.getLisAttr())    
                _loDb.execute(sqlStr, tuple(headValue) ) # 'dt_header_type','public_key'
                sourse = _loDb.fetchone()
                self.__dict__[self._headStruct.getIdFieldName()] = sourse[self._headStruct.getIdFieldName()]
            else :
                list = []
                logging.info(' SAVE:: UPDATE self._dataStruct.getMainPrimaryList() = ' + str(self._dataStruct.getMainPrimaryList()))  
                if self._dataStruct.getMainPrimaryList() != None:
                    
#                     Надо построить слварь из всех полей, записанных в mainPrimaryList
                    list = self.getWhereList2Update (self._dataStruct.getMainPrimaryList()) 

                logging.info(' SAVE:: UPDATE list = ' + str(list))  
                            
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

    def getWhereList2Update(self, mainPrimaryList):
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
        listAttrNames = []
        listAttrValues = []        
        for objValue in objValuesNameList:
            if objValue.find('_') != 0 and (objValue) in listTableFields :
                listAttrNames.append(objValue)
                listAttrValues.append(self.__getattribute__(objValue))

        logging.info('splitAttributes:: listAttrNames = ' + str (listAttrNames) )
        
        class Out: pass   
        out = Out()
        out.listAttrNames = listAttrNames
        out.listAttrValues = listAttrValues    
        out.strListAttrNames = ", ".join(listAttrNames)
        out.strListAttrValues = ", ".join([ '%s' for row in listAttrNames]) # "'" + "', '".join(map(str,listAttrValues)) + "'"  
        
        
        
#                     dataParamseObj.strListAttrNames += ', actual_flag, revision_author_id,  operation_flag, sha_hash, operation_timestamp '
#             dataParamseObj.strListAttrValues += ", 'A', %d, %s,  %s, %s "
#             dataParamseObj.strParams += (autorId, operationFlag, sha_hash, operation_timestamp, )

#          вот тут: out.strListAttrValues - заменить все 'None' на NULL !!!!!
#         out.strListAttrValues = "'" + "', '".join(listAttrValues) + "'"   
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





 




