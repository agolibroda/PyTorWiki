#!/usr/bin/env python
#
# Copyright 2016 Alec Goliboda
#
# group.py

from __future__ import print_function

import logging
import json

import zlib
# import markdown
from datetime import datetime


import tornado.options
# import pymysql

import hashlib
import bcrypt

import base64
        
# from _overlapped import NULL

##############
import config


from . import Model, CipherWrapper
from .. import WikiException 

from core.models.author     import Author
from ..constants.data_base  import *

# from core.models.template   import Template

from ..constants.data_base  import * 


class Group(Model):
    """
    модель - для Группы
    внутри будут:
    - список участников
    - библиотека
    
    Просмотр: 
    - список всех групп
    - одну группу Описание 
        - список участников группы
        - список статей (библиотека)
        
    - создавать группы
    - "удалять группы" - о... нужен флаг - "группа удалена"???
    
    - добавлять (удаять) участников в группу 
        - по приглашению - нужен список приглашений - соотв, у каждого автора может быть список приглашений "вступить в группу"
        - нужен список заявок на вступление - это инструмент админа группы "список заявок на вступление"
        
    - добавлять (удалять) статьи в библиотеку
        - статья моет ажодится в библиотеке и иметь флаг 
            "pbl" - для всеобщего доступа  
            "grp" - только для группы, такие стаьи будут ЗАКРЫТЫМИ!!!!  
    
    Видимость групп (group_status) 
    - публичная - 'pbl' - любой посетитель может читать публичные материалы группы 
    - закрытая - 'shut' ??? - что - то я пока не знаю.... может, в закрытых группах не может быть "публичных статей"??
    
    Процедура создания новой группы:
         При создании новой группы, Создатель группы становится ее Администратором.
        Запись о создании группы размещается в таблицах "dt_headers" и "groups" 
        Запись о вступлении в группу Администратора добавляется в таблицу "members";
                  
             Процедура работы с Ключами:
                Создается уникальная пара RSA-ключей, 
                Публичный ключ помещается в заголовок группы,  
                персональный  - размещается в списке "members", 
                Приватный ключ группы закрывается Публичным ключем Создателя группы, 
                и добавляется в соответствующее поле таблицы "members" 
            Когда Участник Группы открывает страницу группы (переходит на рабочий стол группы) 
            в профиль Участника добавляется значение его копии приватного ключа группы;
            После этого пользователь сможет читать и редактировать все статьи из групповой библиотеки, имеющие флаг "grp"
    
    
    """
    
    def __init__(self, group_title = '', group_annotation = '', group_status = 'pbl'):
        Model.__init__(self)   

        self.dt_header_id = 0
#         self.author_id = 0
        self.group_title = group_title
        self.group_annotation = group_annotation
        self.group_status = group_status
        self.public_key = ''
        self.private_key = ''
        self.private_key_hash = ''

#         self.group_create_date = datetime.now()

        self.setDataStruct(Model.TableDef( tabName='groups', 
                                      idFieldName=None,
                                      mainPrimaryList =['dt_header_id'],
                                      listAttrNames=['dt_header_id', 'group_title', 'group_annotation', 'group_status']))
        
        self.setHeadStruct(Model.TableDef( tabName='dt_headers', 
                                      idFieldName='dt_header_id',
                                      mainPrimaryList =['dt_header_id'],
                                      listAttrNames=['dt_header_type', 'public_key']))
        
        
    class Member(Model):
        def __init__(self):        
            Model.__init__(self)   
            self.group_id = 0
            self.author_id = 0
            self.member_role_type = 'M'
            
            self.setDataStruct(Model.TableDef( tabName='members', 
                                      idFieldName=None,
                                      mainPrimaryList =None,
                                      listAttrNames=['group_id', 'author_id', 'member_role_type', 'private_key']))
        


        def save(self, authorId ):

            operationFlag = 'I'

            revisions_sha_hash_sou = str(self.group_id) + str(self.author_id) + self.member_role_type 
            logging.info(' Member save:: self = ' + str(self))
            Model.save(self, authorId, operationFlag, revisions_sha_hash_sou)


        def getGroupMembersleList(self, groupId):
            """
            Получить список всех соучастников одной группы
            
            """

            getRez = self.select(
                    'dt_headers.dt_header_id, author_name, author_surname, author_role, author_phon, author_email, author_create, dt_headers.public_key ',
                    'authors, dt_headers',
                        {
                    'whereStr': " members.dt_header_id = authors.dt_header_id AND dt_headers.dt_header_id = authors.dt_header_id AND " +\
                    " members.actual_flag = 'A' AND authors.actual_flag = 'A' AND "
                    " members.group_id = " + str(groupId) , # строка набор условий для выбора строк
                    'orderStr': ' author_name, author_surname ', # строка порядок строк
                                     }
                                    )

# 'whereStr': " groups.author_id = authors.author_id AND  groups.group_id = " + str(group_id)            
        
#             logging.info( 'getGroupMembersleList:: getRez = ' + str(getRez))
            if len(getRez) == 0:
    #             raise WikiException( ARTICLE_NOT_FOUND )
               return []

            authorList = []
            author = Author()
            for autorStruct in getRez:
               authorList.append(author.parsingAuthor(self, autorStruct))
            return authorList


    class Library(Model):
        
        def __init__(self, groupId = 0, articleId=0, libraryPermissionType = 'W' ):        
            Model.__init__(self)   
            self.group_id = groupId
            self.article_id = articleId
            self.library_permission_type = libraryPermissionType
            
            self.setDataStruct(Model.TableDef( tabName='librarys', 
                                      idFieldName=None,
                                      mainPrimaryList =['group_id','article_id' ],
                                      listAttrNames=['group_id', 'author_id', 'library_permission_type']))
            

        def save(self, autorId):

            operationFlag = 'I'

            revisionsShaHashSou =  str(self.group_id) + str(self.article_id) + self.library_permission_type 
#             logging.info(' Library save:: self = ' + str(self))
            Model.save(self, autorId, operationFlag, revisionsShaHashSou)

#         self.dt_header_id = Model.save(self, self.dt_header_id, operationFlag, sha_hash_sou)


        def getGroupArticleList(self, groupId):
            """
            Получить список всех статей одной группы
            
            """

            getRez = self.select(
                    ' articles.article_id, articles.article_title, articles.article_link, ' +
                    ' articles.article_annotation, articles.article_category_id, ' + 
                    ' articles.article_template_id, ' +
                    ' null AS group_title, null AS group_annotation,  librarys AS group_id, librarys.library_permission_type ',
                    'articles',
                        {
                    'whereStr': " librarys.article_id = articles.article_id AND " +\
                    " articles.actual_flag = 'A' AND librarys.actual_flag = 'A' AND " +\
                    " librarys.group_id = " + str(groupId) , # строка набор условий для выбора строк
                    'orderStr': ' articles.article_id ', # строка порядок строк
                                     }
                                    )

# 'whereStr': " groups.dt_header_id = authors.dt_header_id AND  groups.group_id = " + str(group_id)            
#             for item in getRez:
#                 logging.info( 'getGroupArticleList:: getRez = ' + str(item))
            
            if len(getRez) == 0:
    #             raise WikiException( ARTICLE_NOT_FOUND )
               return []
             
            return getRez
    


    def get(self, groupId):
        """
        загрузить ОДНО значение - по ИД группы
        """
        
        resList = self.select(
                    'dt_headers.dt_header_id,  group_title, group_annotation ' , # строка - чего хотим получить из селекта
                    'dt_headers', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " groups.actual_flag = 'A' AND  groups.dt_header_id = dt_headers.dt_header_id AND  dt_headers.dt_header_id = " + str(groupId)
                     } #  все остальные секции селекта
                    )
#         for item in resList:
#             logging.info('Author:: get:: resList = ' + str(item))
            
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
        загрузить список всех групп
        
        """
        resList = self.select(
                    'dt_headers.dt_header_id,  group_title, group_annotation,  group_status  ' , # строка - чего хотим получить из селекта
                    'dt_headers', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " groups.actual_flag = 'A' "
                     } #  все остальные секции селекта
                    )
#         logging.info('Author:: get:: resList = ')
#         logging.info(resList)
        return resList
        

        
    def grouplistForAutor(self, authorId):
        """
        Получить список групп для одного автора - все руппы, которые АВТОР создал, 
        и в которых АВТОР является участником
       
        вот тут возможно, надо будет все поправить - 
        и показывать только ПАБЛИК группы, и/или приватные группы, 
        в которых участвуют оба  - и зритель, и автор 
        
        """
        try:
            resList = self.select(
                        ' DISTINCT dt_headers.dt_header_id,  groups.group_title, groups.group_annotation,  groups.group_status, ' + 
                        ' members.member_role_type ' , # строка - чего хотим получить из селекта
                        '  members, dt_headers ', #'authors',  # строка - список таблиц 
                        {
                         'whereStr': " groups.actual_flag = 'A' AND groups.dt_header_id = dt_headers.dt_header_id AND " +  
                             " members.author_id = " + str(authorId) + 
                             " AND  members.group_id = groups.dt_header_id ",
                         'orderStr': '  groups.group_title ' 
                         } #  все остальные секции селекта
                        )
            
#             logging.info( 'grouplistForAutor:: resList =  ' + str(resList))
            return resList
        except Exception as e:        
#         except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
            logging.info( 'grouplistForAutor::Have ERROR!!!  ' + str(e))
            if not article: raise tornado.web.HTTPError(404)
            else: return (article, [])
     
    
    def getGroupArticleList(self, groupId):
        """
        Получить список всех статей одной группы
        
        """
        libControl = self.Library ()
        return libControl.getGroupArticleList( groupId)


    def getGroupMembersleList(self, groupId):
        """
        Получить список всех Участников одной группы
        
        """
        memberControl = self.Member ()
        return memberControl.getGroupMembersleList( groupId)

    
    def save(self, authorId ):
        """
        сохранить группу, 
        пользователя, который создал группу надо воткнуть не только в авторы группы,
        но, и в "members" да еще и АДМИНОМ!!!
        
        """
        bbsalt =  config.options.salt.encode()
        cip = CipherWrapper()

        logging.info(' save:: before SAVE = ' + str(self)) 
               
        if self.dt_header_id == 0:
#             self.group_create_date = datetime.now()
            operationFlag = 'I'
            
            autotControl = Author()
            creator = autotControl.get(authorId)

            cip.rsaInit() # сделать пару ключей 
            self.public_key = cip.rsaPubSerialiation(cip.getPublicKey())
            pKey = cip.getPrivateKey() # поучить незакрытый приватный ключ
#             self.private_key_hash = bcrypt.hashpw(cip.rsaPrivateSerialiation(pKey), bbsalt).decode('utf-8') # получим ХЕш приватного ключа - для последуюей проверки при восстановлении пароля
#             logging.info(' save:: before SAVE creator.publicKey() = ' + str(creator.publicKey())) 
            pkTmp = cip.rsaEncrypt(creator.publicKey(), cip.rsaPrivateSerialiation(pKey))
#             logging.info(' save:: before SAVE pkTmp = ' + str(pkTmp)) 
            self.private_key = pkTmp
            
        else:
            operationFlag = 'U'
        
        self.begin()    
        revisions_sha_hash_sou = str(self.group_title) + str(self.group_annotation) + str(self.group_status)
        
#         self.dt_header_id = 
        Model.save(self, authorId, operationFlag, revisions_sha_hash_sou )
        # теперь сохранить автора группы как ее админа.
#         logging.info(' SAVE:: GROUPPPPP authorId = ' + str(authorId))  
#         logging.info(' SAVE:: GROUPPPPP 2 = ' + str(self))  

        if operationFlag == 'I':
            memberControl = self.Member()
            memberControl.author_id = authorId
            memberControl.group_id = self.dt_header_id
            memberControl.member_role_type = 'A'
            memberControl.private_key = self.private_key

#             bbWrk = (bytePass+bbsalt)[0:32]
#             cipher_aes = AES.new(bbWrk, AES.MODE_EAX) # закроем приватный ключ на пароль пользователя.
#             ciphertext = cipher_aes.encrypt(pKey)
#             self.private_key = pickle.dumps({'cipherKey': ciphertext, 'nonce': cipher_aes.nonce})
            
            memberControl.save(authorId)
        
        self.commit()
        return True


    def librarySave(self, authorId = 0, groupId = 0, article_id=0, library_permission_type = 'W'):
        """
        Добавить статью к группе 
        
        """
        libControl = self.Library(groupId, authorId, library_permission_type)
        libControl.save(authorId)

    