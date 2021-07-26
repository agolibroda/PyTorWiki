#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2017 Alec Golibroda
#
# from core.Helpers      import *
#



import bcrypt
import concurrent.futures

import os.path
import re
import subprocess
import unicodedata

import logging
import traceback

import json
import pickle

from datetime import datetime

import redis




##############################
import config



# from core.models.group      import Group



def splitAttributes(objOne):
    """
    разделить собственные параметры (без параметров с подчеркиваниями ) на 2 списка - 
    1 - список имен параметров
    2 - значений параметров 
    это нужно для того, что бы использовать все параметры в операции 
    добавления или изменения данных в базе данных.
    
    На выходе получим словарь из двух списков  
    """ 
#         objDict = objOne.__dict__
    objValuesNameList = list(objOne.__dict__.keys())
    listAttrNames = []
    listAttrValues = []        
    for objValue in objValuesNameList:
        if objValue.find('_') != 0:
            listAttrNames.append(objValue)
            listAttrValues.append(objOne.__getattribute__(objValue))

    
    class Out: pass   
    out = Out()
    out.listAttrNames = listAttrNames
    out.listAttrValues = listAttrValues    
    out.strListAttrNames = ", ".join(listAttrNames)
    out.strListAttrValues = "'" + "', '".join(map(str,listAttrValues)) + "'"   
#         out.strListAttrValues = "'" + "', '".join(listAttrValues) + "'"   
    return out



def toStr(objOne): 
    """
    вот.... превращение сложных данных (списка объектов, допустим,) в строку. 
    """
    try:
        attribList = splitAttributes(objOne) # dir(objOne) #
        logging.info( ' toStr TemplateParams::__str__ attribList = ' + str(attribList))
        className = str(objOne.__class__)
        # logging.info( ' toStr className = ' + str(className))
        itemsList = map(lambda x, y: ' "' + str(x) + '"' + ': "' + str(y) + '" ', attribList.listAttrNames, attribList.listAttrValues) 
        # logging.info( ' toStr itemsList = ' + str(itemsList))
        objValuesNameList = '\n'+ className + ': { \n\t' + ', \n\t'.join(itemsList) + '\n}'
        # logging.info( ' toStr TemplateParams:: objValuesNameList = ' + str(objValuesNameList))
        return objValuesNameList
    except Exception as e:
        # logging.info( 'Helpers::: toStr:: Exception as et = ' + toStr(e))
#         logging.info( 'Get:: Exception as traceback.format_exc() = ' + toStr(traceback.format_exc()))
        return str(objOne)


def toJson(objList): 
    """
    вот.... превращение сложных данных (списка объектов, допустим,) в Json. 

    Сначала проверим, что входное ОНО списк, если да, тогда к каждому элементу списка  
    применим ... 
 

         _public_key = bytes(newAuthor.public_key)
        if _public_key != b'' and _public_key != None:
            newAuthor.unserializePyblicKey(_public_key)


    """
    try:

        for oneOb in objList:
            logging.info( 'toJson oneOb = ' + str(oneOb)) 

        if type(objList) is list:
            json_list = []
            for ob in objList:
                logging.info( ' toJson::_ ob = ' + str(ob)) 
                # attribList = splitAttributes(ob) # dir(objOne) #
                # logging.info( ' toJson::__str__ attribList = ' + str(attribList.__dict__)) 
                # logging.info( ' toJson::__str__ ob = ' + str(ob.__dict__)) 
                # для каждого автора надо сериализовать его публичный ключ. для отдачи в клиента!!!!
                # public_key
                ob.serializePyblicKey()
                json_list.append(json.dumps(ob.__dict__)) 
            logging.info( ' toJson::json_list = ' + toStr(json_list)) 
            return json.dumps(json_list)
        elif type(objList) is object:
            return json.dumps(objList.__dict__)

    except Exception as e:
        logging.info( 'Helpers::: toJson:: Что - то не получилось превратить в Json : Exception as et = ' + toStr(e))
#         logging.info( 'Get:: Exception as traceback.format_exc() = ' + toStr(traceback.format_exc()))
        return str(objList)


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


def pyTorWikiTraceback(errorMessage):
    logging.error( errorMessage)
    for line in traceback.format_stack():
        print(line.strip())



# r = redis.Redis( url='rediss://:password@hostname:port/0',
#     password='password',
#     ssl_keyfile='path_to_keyfile',
#     ssl_certfile='path_to_certfile',
#     ssl_cert_reqs='required',
#     ssl_ca_certs='path_to_ca_certfile')

# r.set('foo', 'bar')
# value = r.get('foo')
# print(value)

class RedisConnector():
    
    def __init__(self):
        self._connectInstans = redis.Redis(
                                        host=config.options.redisHost, #'localhost',   
                                        port=config.options.redisPort, #6379, 
                                        db=config.options.redisDb  #0
                                        )
        # redisMaxConnections     = "1024"

    def get(self, paramName):
        """
        Возвратим уже Де-Сериализованный параметр (скорее всего, словарь)
        
        dump(name)[source] - получить значение для параметра, получаем сериализованную структуру
        её надо разобрать потом :-) 
        Return a serialized version of the value stored at the specified key. If key does not exist a nil bulk reply is returned.
        
        """
        return pickle.loads(self._connectInstans.get(paramName))


    def set(self, paramName, value):
        """
        Получаем объект (словарь) и прячем его в параметр 
        
        """
        self._connectInstans.set(paramName, pickle.dumps(value))
        
        
    def expire(self, paramName, timeValue):
        """
        Поставить параметру время жизни!
        
        """
        self._connectInstans.expire(paramName, timeValue)
        

    def delete(self, paramName):
        """
        Удалим параметр (Допустим, при логауте)
        
        """
        self._connectInstans.delete(paramName)




