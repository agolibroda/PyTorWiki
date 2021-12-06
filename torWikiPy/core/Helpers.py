#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2017 Alec Golibroda
#
# from core.Helpers      import *
#

import os
import os.path
################
import logging

dirModule = os.path.dirname(__file__)
nameModule = __file__
logger = logging.getLogger(nameModule)
logger.setLevel(logging.DEBUG)
###################################


import bcrypt
import concurrent.futures

import re
import subprocess
import unicodedata

import traceback

import json
import pickle

from datetime import datetime

# import redis

import uuid
import config



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
        # logging.info( ' toStr TemplateParams::__str__ attribList = ' + str(attribList))
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

        # for oneOb in objList:
        #     logging.info( 'toJson oneOb = ' + str(oneOb)) 

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


