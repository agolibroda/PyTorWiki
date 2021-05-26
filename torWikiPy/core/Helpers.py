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
    try:
        attribList = splitAttributes(objOne) # dir(objOne) #
    #     logging.info( ' TemplateParams::__str__ attribList = ' + str(attribList))
        className = str(objOne.__class__)
        itemsList = map(lambda x, y: ' "' + str(x) + '"' + ': "' + str(y) + '" ', attribList.listAttrNames, attribList.listAttrValues) 
        objValuesNameList = '\n'+ className + ': { \n\t' + ', \n\t'.join(itemsList) + '\n}'
        return objValuesNameList
    except Exception as e:
#         logging.info( 'Get:: Exception as et = ' + toStr(e))
#         logging.info( 'Get:: Exception as traceback.format_exc() = ' + toStr(traceback.format_exc()))
        return str(objOne)


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




