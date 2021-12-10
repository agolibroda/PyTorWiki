#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Goliboda
#
# article.py


from __future__ import print_function

import logging

import json
import string # string.Template

import zlib
# import markdown


import tornado.options
# import pymysql

import hashlib
import base64

import urllib 

from urllib.parse import quote

# from _overlapped import NULL


##############
import config


from . import Model, CipherWrapper
from .. import WikiException 


# from core.Helpers           import *

from core.WikiException     import *

from ..constants.data_base  import * 


# def parse_utf8(self, bytes, length_size):
# 
#     length = bytes2int(bytes[0:length_size])
#     value = ''.join(['%c' % b for b in bytes[length_size:length_size+length]])
#     return value


class Article(Model):
    """
    статья  - основной объект данных для системы;
    
    иммет 
    - автора
    - название 
    - текст
    
    название и текст могут менятся. 
     
    articles - хранилище ВСЕХ статей в системе и всех ревиий. 
    
    статья Это:
    - заглавие
    - текст стаьи (актуальный)
    - автор 
    - дата создания
    
    - категория статьи (article_category_id)
        информационная    inf - тут ИД статьи из списка!!!!
        термин            trm
        навигационная     nvg
        шабон             tpl
    - шабон статьи (article_template_id)
        по ИД шаблона выбирается шаблон, который оформляет текущий текст статьи  
    - права доступа (article_permissions)
        публичкая (свободный доступ)    pbl
        групповая (права на статью есть только у группы) grp
        персональная (исключительно авторская)    sol (solo)
    
        
    - текст хранится в виде, готовом для публикации (в хтмл-ке)
    - список ревизий названия статьи и текста 
        у каждой ревизии есть дата и автор ревизии
    
    при сохранении статьи
    1. подготовить текст 
    2 сохранить.
     
    получить список статей 
    - выбираем данные из "articles" - 
    
    получить одну статью 
    - по одному из имен (старых - новых не важно) 
    выбираем данные из  "articles" 
    данные ревизий берутся  по ХЕШУ-ам в таблицах "titles", "annotations", "texts"
    
    получить историю статьи 
    - по  ИД (одному из имен) выбрать все версии статьи из "revisions"
    
    """
 
    def __init__ (self, id=0, title = ''): 
#         logging.info('article:: __init__')

        Model.__init__(self)   
        self.article_id = id # эти параметры прилетают из формы редактирования
#         self.author_id = 0;
        self.article_title = title # эти параметры прилетают из формы редактирования
        self.article_annotation = '' # Это аннотация статьи!!!!!
        self.article_source = '' # эти параметры прилетают из формы редактирования
        self.article_category_id = config.options.info_page_categofy_id # категория страницы (служебные?) 'inf','trm','nvg','tpl'
        self.article_template_id = config.options.main_info_template
        self.article_permissions = 'pbl'
        self.article_permission_code = 200
#         self.article_link = '' 
 
        self.setDataStruct(Model.TableDef( tabName='articles', 
                                      idFieldName='article_id',
                                      mainPrimaryList =['article_id'],
                                      listAttrNames=['article_id', 'article_title','article_link', 'article_annotation','article_source','article_category_id','article_template_id','article_permissions']))
 
        

    def save(self, author, templateDir):
        """
        Обязательно:
        - Автора
        сохранить данные.
        2.1 поменятся могут:
            - название статьи
            - аннотация 
            - текст 
        2.1.1 надо проверить, является ли эта троица УНИКАЛЬНОЙ - 
        не важно ЧТО конкретно, может поменяться что - то одно, НО, 155 копий одного и тогоже нам не нужно (подозреваю!)
        значит, делает длинную строку, и берем от нее ХЭШ 
        смотрим по таблице ревизий - есть ли точно такое же, если сть, то 
        одаем автору ошибку, если все нормално, тогда записываем статью, и записываем ревизию.
        2.1.2 добавим новую запись в "articles"  
        
        2.2 Права долтупа
            'pbl' - публично
            'grp' – права определяются группой
            'sol' – персональная статья, читать и редактировать ее может только автор. 
        
        
        :param     author - Автор статьи  
        :param     templateDir - директория, в которой лежат всякие там отрендереные шаблоны и собственно статьи для представления посетителям сайта 
        :Return:   вертаем статью        
        
        """

# categories 
# Это новая таблица  - все категории, которые только озможны, и пока там  
# вот такие категрии (служебные?) 'inf','trm','nvg','tpl'

        authorId = 0
        if author != None:
            authorId = author.dt_header_id
       
        if int(self.article_category_id) == int(config.options.tpl_categofy_id):
            htmlTextOut = self.article_source

        article_title = self.article_title.strip().strip(" \t\n")
        article_link = article_title.lower().replace(' ','_')
        self.article_link = article_link.replace('__','_')

#         logging.info( 'article Before Save 1 self.article_id = ' + str(self) )
        
        del self.article_permission_code 
        
        self.articleEncode(author)

#         base64.b64encode(tornado.escape.utf8(article_source)).decode(encoding='UTF-8') 

#         
# вот тут по - идее, надо начать трансакцию... 
# - почитать про трансакции в постгрисе. 
# 
# BEGIN;
# UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
# UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
# COMMIT;
#             self.rollback()
        
        try:
        
            if int(self.article_id) == 0:
                operationFlag = 'I'
            else:
                operationFlag = 'U'

            sha_hash_sou = self.article_title + self.article_link + self.article_annotation + str(self.article_source)
            
#             logging.info( 'save:: sha_hash_sout = '  + str(sha_hash_sou))

            self.article_id = Model.save(self, authorId, operationFlag, sha_hash_sou)

#             logging.info( 'save:: After SAVE = '  + str(self))
        
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            logging.info( 'Save:: Exception as traceback.format_exc() = ' + toStr(traceback.format_exc()))
            self.rollback()
             
#         logging.info( 'save:: save self.article_link! = ' + self.article_link )
                
        return self 

    def articleEncode(self, readerMan=None):
        """
        Закодиоровать статью, подготовить к сохранению!!!!!
        - работа с Данными класса, 
        В астности, 
        Обработка "article_source"... 

        :param readerMan - читатель статьи - посетитеь, который читает - из его профиля берутся RSA ключи ... 
        
        """
#         article_title = base64.b64encode(tornado.escape.utf8(self.article_title)).decode(encoding='UTF-8')
#         article_link = base64.b64encode(tornado.escape.utf8(self.article_link)).decode(encoding='UTF-8')
#         article_annotation = base64.b64encode(tornado.escape.utf8(self.article_annotation)).decode(encoding='UTF-8')    
#         article_source = base64.b64encode(
#                                     zlib.compress(
#                                         tornado.escape.utf8(self.article_source)
#                                                 )
#                                                     ).decode(encoding='UTF-8')

        # если флаг доступа не "паблик", тогда надо все зарывать 
        # если файл персональный, тогда закрываем его на публичном ключе, 
        # если файл для группы, тогда его надо закрыть на тубличный ключ группы.  
        if self.article_permissions == 'pbl':
            articteSou = tornado.escape.utf8(self.article_source)
        elif self.article_permissions == 'sol':
            cip = CipherWrapper()
            articteSou = cip.rsaEncrypt(readerMan._openPublicKey, bytes(self.article_source, 'utf-8') )
        article_source = zlib.compress( articteSou )
        self.article_source = article_source
         
         
    def articleDecode(self, artStructure, readerMan=None):
        """
        нормальный декодирований нормальной статьи!!!!!
        
        :param artStructure - Структура, которая получена из Селекта - сырая - сырая....
        :param readerMan - читатель статьи - посетитеь, который читает - из его профиля берутся RSA ключи ... 
        :Return: отдаем уже раскодированную статью       
         
        """
        outArt = artStructure
        unZipText = zlib.decompress(outArt.article_source)
#         logging.info( 'Decode:: unZipText = ' + str(unZipText))
        
        if outArt.article_permissions == 'pbl':
            # все норм, статья  - паблик, бери- читай!
            outArt.article_source = unZipText.decode("utf-8")
        elif outArt.article_permissions == 'grp':
            # Статья писана для группы - чичтать могут только участники - у каждого из них в "мемберсах" есть персональный ключик.
            pass
        elif outArt.article_permissions == 'sol':
            # статья закрыта персональным ключем АВТОРА - открывать ее надо посоответственно!
            try:
                cip = CipherWrapper() 
                outArt.article_source = cip.rsaDecrypt(readerMan._openPrivateKey, unZipText ).decode("utf-8")
            except Exception as error: # cip.CipherErorr as error:
                logging.info( 'articleDecode:: Exception as et = ' + str(error))
#                 logging.info( 'Decode:: Exception as traceback.format_exc() = ' + toStr(traceback.format_exc()))
                outArt.article_source = '403 -  у Вас нет доступа к данным! '

        return outArt


    def get(self, articleLink, spectatorAuthor = None):
        """
         получить статью по названию (одну) - функция для пердставления данных (!!!) 
         получить ОЛЬКО опубликованный текст  (активную статью) - для редактирования получаем статью иным образом! 
    
         - по одному из имен (старых - новых не важно) 
         выбираем данные из "article" и "articles" берем как ХТМЛ, так и РТФ ну и активный тайтл (ил "articles")
         имя ищем по ХЕШУ в таблице "titles"
         
         Кстати, статьи бывают не только "публичными" а и групповыми и ЛИЧНЫМИ!!!
         
         """
#         logging.info( 'Article ::: get articleLink  = ' + str(articleLink))
#         logging.info( 'Article ::: get spectatorAuthor  = ' + str(spectatorAuthor))
    
#         article_link = base64.b64encode(tornado.escape.utf8(articleLink)).decode(encoding='UTF-8')
        article_link = articleLink

#          articleLink = hashlib.sha256(
#                                      tornado.escape.utf8(articleLink)
#                                      ).hexdigest()  #.decode(encoding='UTF-8')
        spectatorId = 0
        if spectatorAuthor != None:
            spectatorId = spectatorAuthor.dt_header_id
            
        if int(spectatorId) == 0:
            getRez = self.select(
                                """
                                 DISTINCT articles.article_id, articles.article_title, articles.article_link,  
                                articles.article_annotation, articles.article_source, 
                                articles.article_category_id, articles.revision_author_id,  
                                articles.article_template_id, articles.article_permissions 
                                """,
                                ' articles lfind ',
                                    {
                                'whereStr': " articles.article_id = lfind.article_id " +\
                                            " AND articles.actual_flag = 'A' " +\
                                             " AND lfind.article_link = '" + article_link  + "' " , # строка набор условий для выбора строк
                                 }
                                )
        else:

            strTpl = """
                    SELECT 
                       articles.article_id, articles.article_title, articles.article_link, 
                       articles.article_annotation, articles.article_source, 
                       articles.article_category_id, articles.revision_author_id, 
                       articles.article_template_id, articles.article_permissions
                       FROM articles 
                       WHERE articles.actual_flag = 'A' 
                       AND articles.article_id =  (
                           SELECT DISTINCT article_id FROM articles WHERE article_link = '${aLink}' )
                       UNION
                       SELECT 
                       articles.article_id, articles.article_title, articles.article_link, 
                       articles.article_annotation,  
                       articles.article_source, 
                       articles.article_category_id, articles.revision_author_id, 
                       articles.article_template_id, articles.article_permissions  
                       FROM articles, groups, librarys, articles lfind 
                       WHERE  articles.actual_flag = 'A' 
                       AND groups.revision_author_id = articles.revision_author_id
                       AND groups.revision_author_id = $sId
                       AND groups.dt_header_id = librarys.group_id
                       AND librarys.article_id = articles.article_id
                       AND articles.article_id = lfind.article_id 
                       AND lfind.article_link = '${aLink}'                       
                    """
                    
#                 [ LIMIT { number | ALL } ] [ OFFSET number ]
                    #   article_id 
            tplWrk = string.Template(strTpl) # strTpl
            strSelect = tplWrk.substitute(sId=str(spectatorId), aLink=article_link)
#             logging.info( 'Article ::: get strSelect  = ' + str(strSelect))
            getRez = self.rowSelect(str(strSelect)) 

    
        if len(getRez) == 0:
            logging.info( 'Article :::  ARTICLE_NOT_FOUND get articleLink  = ' + str(articleLink))
            locEx = ArticleNotFound()
            logging.info( 'Article :::  locEx  = ' + str(locEx))
            raise ArticleNotFound()
        elif len(getRez) == 1:   
            outArt = self.articleDecode(getRez[0], spectatorAuthor)
#             logging.info( 'Article ::: >>>>> get outArt  = ' + str(outArt))
            return outArt


    def getById(self, articleId):
         """
         получить статью по ID (одну) - функция для пердставления данных (!!!) 
         получить ОЛЬКО опубликованный текст  (активную статью) - для редактирования получаем статью иным образом! 
    
         """
#          logging.info( 'Article ::: getById articleId  = ' + str(articleId))
    
         getRez = self.select(
                                'articles.article_id, articles.article_title, articles.article_link, '+
                                'articles.article_annotation,  articles.article_source, articles.article_category_id, '+ 
                                'articles.revision_author_id, articles.article_template_id, articles.article_permissions',
                                '',
                                    {
                                'whereStr': ' articles.article_id = ' + str(articleId) +\
                                            " AND articles.actual_flag = 'A' "  ,
                                 }
                                )
    
         if len(getRez) == 0:
            logging.info( 'Article :::  ARTICLE_NOT_FOUND getById articleId  = ' + str(articleId))
            raise ArticleNotFound()
         elif len(getRez) == 1:   
#              logging.info( ' getById getRez = ' + str(getRez[0]))
            outArt = self.articleDecode(getRez[0])
#              logging.info( ' getById outArt = ' + str(outArt))
            return outArt



    def getByUsingHash(self, spectatorId, hash):
        """
        получить статью (ВЕРСИЮ) по hash (одну) 
        а вот что показать? 
        ну, походу, все, из ТОЙ версии, которую заказал пользователь!!! 
    
        """
#         logging.info( 'Article ::: getByUsingHash hash  = ' + str(hash))
    
 
        strTpl = """
               SELECT 
               lfind.article_id, lfind.article_title, lfind.article_link, 
               lfind.article_annotation, lfind.article_source, 
              
               lfind.article_category_id, lfind.revision_author_id, 
               lfind.article_template_id, lfind.article_permissions, lfind.actual_flag
               FROM articles lfind 
               WHERE lfind.sha_hash = '${aHash}'
               UNION
               SELECT 
               lfind.article_id, lfind.article_title, lfind.article_link, 
               lfind.article_annotation,  lfind.article_source, lfind.article_category_id, lfind.revision_author_id, 
               lfind.article_template_id, lfind.article_permissions, lfind.actual_flag  
               FROM groups, librarys, articles lfind 
               WHERE  lfind.article_permissions = 'grp'
               AND groups.revision_author_id = lfind.revision_author_id
               AND groups.revision_author_id = $sId
               AND groups.dt_header_id = librarys.group_id
               AND librarys.article_id = lfind.article_id
               AND lfind.sha_hash = '${aHash}'        
                """
                #   article_id 
        tplWrk = string.Template(strTpl) # strTpl
        strSelect = tplWrk.substitute(sId=str(spectatorId), aHash=hash)
#         logging.info( 'Article ::: getByUsingHash strSelect  = ' + str(strSelect))
        getRez = self.rowSelect(str(strSelect)) 
    
        if len(getRez) == 0:
            logging.info( 'getByUsingHash :::  ARTICLE_NOT_FOUND getByUsingHash hash  = ' + str(hash))
            raise ArticleNotFound()
        elif len(getRez) == 1:   
            outArt = self.articleDecode(getRez[0])
            return outArt

    
    def list(self, serchOptions = None):
        """
         получить список статей
         упорядочивать потом будем
    
         получить список статей 
         - выбираем данные из "articles" - получить при этом АКТАЛЬНЫЕ ИД ревизий!
                 
        """
        whereStr = ''
        
        if serchOptions != None and hasattr(serchOptions, 'categoryId') and serchOptions.categoryId > 0 :
            whereStr = ' articles.article_category_id = ' + str(serchOptions.categoryId)
             
        if whereStr == '':
            whereStr += " articles.actual_flag = 'A' "
        else:
            whereStr += " AND articles.actual_flag = 'A' "
             
        getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_source) ',
                                'articles.article_id, articles.article_title, articles.article_link, ' +
                                'articles.article_annotation, articles.article_category_id, articles.revision_author_id, '+ 
                                ' articles.article_template_id, articles.article_permissions ',
                                '',
                                    {
                                'whereStr': whereStr, # строка набор условий для выбора строк
                                'orderStr': ' articles.article_title ', # строка порядок строк
    #                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                 }
                                )
    
#          logging.info( 'list:: getRez = ' + str(getRez))
        if len(getRez) == 0:
#            raise WikiException( ARTICLE_NOT_FOUND )
           return []
         
#          for oneObj in getRez:
#              oneObj.article_title = base64.b64decode(oneObj.article_title).decode(encoding='UTF-8')
#              oneObj.article_link = base64.b64decode(oneObj.article_link).decode(encoding='UTF-8')
#              articleTitle = oneObj.article_title.strip().strip(" \t\n")
#              oneObj.article_link  =  articleTitle.lower().replace(' ','_')
#              oneObj.article_annotation =  base64.b64decode(oneObj.article_annotation).decode(encoding='UTF-8')
#              logging.info( 'list:: After oneArt = ' + str(oneObj))
    
        return getRez
 
    def listByAutorId(self, authorId = 0, spectatorId = 0):
        """
        получить список статей
        одного автор - все статьи, всех категорий!
        
        получить список статей 
        - выбираем данные из "articles" - получить при этом АКТАЛЬНЫЕ ИД ревизий!
        
        authorId - ИД автора статей,  
        spectatorId - ИД зрителя - посмотреть статьи из "закрытых" групп - может только соучастник 
        Если authorId == spectatorId Значит это сам автор просматривает свои материалы.  
        
        ТЕХ групп.... а если нет, то - не показывать!!! 
        то есть, показываем 
            - "паблик" статьи
            - групповые из ОТКРЫТЫХ групп
            - групповые из ЗАКРЫТЫХ групп (там, куда вхож ЗРИТЕЛЬ)
            - Е показывать все остальное!!!!!
            
            а, ну если сам себя зритель?????? - показать то, что идет для незареганого пользователя!!!!!
            потому что все статьи - пользователь может видеть на свей странице!!!!!
            
            пока в селекте про зрителя нет ничего!!!!!!
                
        """
        if int(authorId) > 0 and int(spectatorId) == 0:
            strTpl = """
                   SELECT 
                   articles.article_id, articles.article_title, articles.article_link, articles.article_annotation, 
                   articles.article_category_id, 
                   articles.revision_author_id,  articles.article_template_id, articles.article_permissions,
                   groups.group_title, groups.group_annotation, groups.dt_header_id AS group_id 
                   FROM articles 
                   LEFT JOIN librarys ON  librarys.article_id = articles.article_id
                   LEFT JOIN groups ON groups.dt_header_id = librarys.group_id 
                   WHERE articles.article_id  IN  
                           (SELECT DISTINCT articles.article_id FROM articles WHERE articles.revision_author_id  =  $aId) 
                   AND articles.actual_flag = 'A' 
                   
                   ORDER BY 2 
        
                    """
#                    AND articles.article_permissions = 'pbl' 
                    
                    #   article_id 
            tplWrk = string.Template(strTpl) # strTpl
            strSelect = tplWrk.substitute(aId=str(authorId), sId=str(spectatorId))
#             logging.info('listByAutorId:: strSelect = ' + str (strSelect) )            
            getRez = self.rowSelect(str(strSelect)) 
        else:
            autorIdStr = '';
            if authorId > 0 :
                autorIdStr = ' articles.revision_author_id  = ' + str(authorId)
                
            if autorIdStr == '':
                autorIdStr += " articles.actual_flag = 'A' "
            else:
                autorIdStr += " AND articles.actual_flag = 'A' "
                
            getRez = self.select(
        #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_source) ',
                   " articles.article_id, articles.article_title, articles.article_link, " +
                   " articles.article_annotation, articles.article_category_id, articles.revision_author_id, "+
                   " articles.article_template_id, articles.article_permissions, " +
                   " groups.group_title, groups.group_annotation, groups.dt_header_id AS group_id " ,
                   "",
                       {
                   "joinStr": "LEFT JOIN librarys ON librarys.article_id = articles.article_id LEFT JOIN groups ON groups.dt_header_id = librarys.group_id",
                   "whereStr": autorIdStr , # строка набор условий для выбора строк
                   "orderStr": " 2 ", #  articles.article_id строка порядок строк
        #                                "orderStr": "FROM_BASE64( articles.article_title )", # строка порядок строк
                    }
                   )
        
                
#         logging.info( 'listByAutorId:: getRez = ' + str(getRez))
        if len(getRez) == 0:
        #             raise WikiException( ARTICLE_NOT_FOUND )
           return []
        
        return getRez
 
   
    def getListArticlesAll (self, spectatorId = 0):
        """
        получить поный списк статей, не только своих, 
        а вообще всех, ДОСТУПНЫХ
        """
        if int(spectatorId) > 0: # and int(spectatorId) != int(authorId):
            strTpl = """
                   SELECT 
                   articles.article_id, articles.article_title, articles.article_link, articles.article_annotation, 
                   articles.article_category_id, 
                   articles.revision_author_id,  articles.article_template_id, articles.article_permissions,
                   groups.group_title, groups.group_annotation, groups.dt_header_id AS group_id 
                   FROM articles 
                       LEFT JOIN librarys ON librarys.article_id = articles.article_id
                       LEFT JOIN groups ON groups.revision_author_id = articles.revision_author_id
                                AND groups.dt_header_id = librarys.group_id
                   WHERE articles.actual_flag = 'A'
                   AND  ( articles.article_permissions != 'sol' OR  
                   articles.article_id IN 
                   (SELECT DISTINCT articles.article_id FROM articles WHERE articles.revision_author_id  =  $sId) 
                   )
                   ORDER BY 2 
        
                    """
                    #   article_id 
            tplWrk = string.Template(strTpl) # strTpl
            strSelect = tplWrk.substitute( sId=str(spectatorId))
#             logging.info( 'getListArticlesAll::  strSelect = ' + str(strSelect))
            getRez = self.rowSelect(str(strSelect)) 
        else:
            autorIdStr = " articles.article_permissions != 'sol' AND articles.actual_flag = 'A' ";
                
            getRez = self.select(
        #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_source) ',
                   " articles.article_id, articles.article_title, articles.article_link, " +
                   " articles.article_annotation, articles.article_category_id,  "+
                   " articles.article_template_id, articles.article_permissions, " +
                   " groups.group_title, groups.group_annotation, groups. group_id " ,
                   "",
                       {
                   "joinStr": "LEFT JOIN librarys ON librarys.article_id = articles.article_id " + 
                              " LEFT JOIN groups ON groups.dt_header_id AS group_id = librarys.group_id",
                   "whereStr": autorIdStr , # строка набор условий для выбора строк
                   "orderStr": " 2 ", #  articles.article_id строка порядок строк
        #                                "orderStr": "FROM_BASE64( articles.article_title )", # строка порядок строк
                    }
                   )
                
#         logging.info( 'listByAutorId:: getRez = ' + str(getRez))
        if len(getRez) == 0:
           return []
 
        return getRez
    

    def IsUniqueRevision(self, titleHash, annotationHash, articleHash):
        """
        проверить, является ли данная ревизия уникальной 
        - может поменятся все, 
        - пожет - заглавие
        - может текст
        """
        revControl = self.RevisionLoc()
        return revControl.IsUniqueRevision(titleHash, annotationHash, articleHash)

 
#     def select(self, 
#                selectStr, # строка - чего хотим получить из селекта
#                addTables,  # строка - список ДОПОЛНИТЕЛЬНЫХ таблиц (основную таблизу для объекта указываем при инициализации) 
#                anyParams = {} #  все остальные секции селекта
#                ):
        
# вот тут надо добавить к списку того, что может придти из наследной модели :-)  
# "чисто" ревизные вещи - дату, автора, флаг 
# и уже в таком порядке все и выбирать... 
        
    def getRevisionsList(self, articleId, spectatorId):
        """
        получить список ревизий для одной статей
        упорядочивать по дате ревизии - в начале - самые последние
        Обязательно - автора!


        - выбираем данные из "texts"  и "annotations"  и "titles"  и "authors" 
        
        """
        getRez = self.select(
                               """
                               articles.article_id, articles.article_title, 
                               articles.article_annotation, 
                               articles.article_title AS rev_article_title,  
                               articles.article_link, articles.article_annotation,
                                
                               CASE WHEN  articles.article_permissions = 'pbl' OR articles.revision_author_id = """ +
                               str(spectatorId) +   
                                """ THEN articles.article_source
                                   ELSE '403' END AS article_source, 
                                 
                               articles.operation_timestamp AS operation_timestamp,  
                               articles.sha_hash, 
                               articles.revision_author_id AS author_id, 
                               authors.author_name AS author_name, 
                               authors.author_surname AS author_surname, 
                               articles.article_permissions, 
                               articles.actual_flag 
                                """,
                               
                               ' authors ',
                               
                                   {
                               'whereStr': ' articles.revision_author_id =  authors.dt_header_id '  +\
                                        ' AND articles.article_id =  ' + str(articleId) ,  # строка набор условий для выбора строк
                               'orderStr': ' articles.operation_timestamp DESC ', # строка порядок строк
#                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                }
                               )

        if len(getRez) == 0:
            logging.info( 'getByUsingHash :::  ARTICLE_NOT_FOUND getRevisionsList articleId  = ' + str(articleId))
            raise ArticleNotFound()
        
        for oneObj in getRez:
            oneObj = self.articleDecode(oneObj)
            oneObj.article_source = base64.b64encode(tornado.escape.utf8(oneObj.article_source)).decode(encoding='UTF-8') 

        return getRez



    def getIdListOfNames(self, nemesArticlesList):
        """
         получить список статей
          по списку имен, 
                 
        """
        logging.info(" getIdListOfNames  nemesArticlesList = " + str(nemesArticlesList)) 
        
        whereStr = " articles.article_title in( '" + "', '".join(nemesArticlesList) + "' )"
        
        whereStr += " AND articles.actual_flag = 'A' "
             
        getRez = self.select(
                                'articles.article_id, articles.article_title ' ,
                                '',
                                    {
                                'whereStr': whereStr, # строка набор условий для выбора строк
                                'orderStr': ' articles.article_title ', # строка порядок строк
                                 }
                                )
        if len(getRez) == 0:
           return []
        return getRez

