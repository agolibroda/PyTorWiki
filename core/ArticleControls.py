#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda


#  Впринцепе, Это "тулБокс" - ящик с инструментами просто пользователя 
# надо сюда добавить 
# список ПОльзователей
# список Групп
#
# ArticleControl.py 


import bcrypt
import concurrent.futures

import os.path
import re
import subprocess
# import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

import logging
import traceback

import json

import config

import core.models

from core.models.author import Author
from core.models.article import Article
from core.models.file import File
from core.helpers.template import Template, TemplateParams

from core.helpers.article import HelperArticle 

from core.BaseHandlers import *
from core.WikiException import *



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class HomeHandler(BaseHandler):
    """
    Загрузка ГЛАВНОЙ сраницы сайта!!!!!
    ИД страницы указано в КОНФИГУРАЦИИ!!!
    
    вот именно тут наверое, надо загружать нужную нам страницу по ее ИД
    - с получением ее ИД щаблона, и грузить и шаблон тоже. 
    - причем, шаблон со всяческими там проверками - есть или нет, и, если есть, тогда 
    вынуть шаблон из какой - то особой папки...
    - если шаблона там етути, тогда его туда положить... 
    ну, как  - то так... 
    а пока... 
    займусь админкой.. 
    может и редактор статей сделать частью админовского слоя?
    
    """


    @gen.coroutine
    def get(self):
        try:
            artHelper = HelperArticle()
            articleId = config.options.main_page_id
            self.get_current_user()
            spectator = self.current_user
            
            (article, fileList, templateName) = yield executor.submit( artHelper.getArticleById, articleId)
#             logging.info( 'HomeHandler get article = ' + str(article))

            tplControl = TemplateParams()
#             tplControl.setAuthor(spectator)
            tplControl.article=article
            tplControl.fileList=fileList
            tplControl.link='/compose'
            tplControl.loginLink='/auth/login'
            
            tplControl.tpl_categofy_id = config.options.tpl_categofy_id
            tplControl.page_name = article.article_title 
            tplControl.project_start_data = config.options.Project_Start_Data

# article=article, fileList=fileList, link='/compose', page_name='Редактирование'

#             logging.info( 'HomeHandler get tplControl = ' + str(tplControl))
            logging.info( 'HomeHandler get templateName = ' + str(templateName))
#             logging.info( 'HomeHandler get config.options.tmpTplPath = ' + str(config.options.tmpTplPath))
#             tmlFullName = os.path.join(config.options.tmpTplPath, templateName)

#             logging.info( 'HomeHandler get tmlFullName = ' + str(tmlFullName))
            
            self.render(templateName, parameters=tplControl)
        except Exception as e:
            logging.info( 'HomeHandler:: GET Exception as et = ' + str(e))
            tplControl = TemplateParams()
            tplControl.error = Error ('500', 'что - то пошло не так :-( ')
            self.render('main_error.html', parameters=tplControl)



class ArticleListHandler(BaseHandler):
    """
    получить список статей категории "информационная статья"
    для показа списка статей
    
    """
    
    @gen.coroutine
    def get(self):
        try:
            artHelper = HelperArticle()
            articles = yield executor.submit( artHelper.getListArticles, config.options.info_page_categofy_id )
            if not articles:
                self.redirect("/compose")
                return
            self.render("articles.html", articles=articles, link='/compose', page_name='Редактирование')
        except Exception as e:
            logging.info( 'ArticleListHandler:: Exception as et = ' + str(e))
            tplControl = TemplateParams()
            tplControl.error = Error ('500', 'что - то пошло не так :-( ')
            self.render('main_error.html', parameters=tplControl)

# что - то здеся не то - 
# что - то тут надо поправить 
# и сделать в одной упаковке 
# или показужу одной отдельной категории (для пользователя)Б
# или, для Админов - или пару категорий, или все категрии статей  - это для суперадмина.

# class AdminHomeArticlesCategory(BaseHandler):
#     """
#     получить список всех статей одной категори
#     
#     """
#     
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self, categoryId):
#         try:
#             logging.info( 'AdminHomeArticlesCategory:: get ')
#             artHelper = HelperArticle()
#             articles = yield executor.submit( artHelper.getListArticlesCategory, categoryId)
#     
#             self.render(config.options.adminTplPath+"articles.html", articles=articles, link='/compose', page_name='Редактирование')
#         except Exception as e:
#             logging.info( 'AdminHomeArticlesCategory:: Exception as et = ' + str(e))
#             error = Error ('500', 'что - то пошло не так :-( ')
#             self.render('error.html', error=error, link='/compose', page_name='Редактирование')



class ArticleHandler(BaseHandler):
    """
    загрузка страницы по ее названию (линке) 
    может именно тут и менять пробелы на подчеркивания? 
    потом будет логичнее прописывать линки в тексте (как вижу, так и пою)
    это на "совсем потом" - тогда, когда надо будет делать новые страницы через 
    добавление линков на не существующие страницы
    
    """

    @gen.coroutine
    def get(self, articleName):
#         logging.info( 'ArticleHandler get articleName = ' + str(articleName))

        try:
            
            self.get_current_user()
            spectator = self.current_user
#             logging.info( 'ArticleHandler get spectator = ' + str(spectator))
            
            artHelper = HelperArticle()
            arr = articleName.lower().split()
            articleLink = '_'.join(arr)# articleLink.lower().replace(' ','_')
            notComposeFlag = True
            (article, fileList, tmlFullName) = yield executor.submit( artHelper.getArticleByName, spectator, articleLink, notComposeFlag )
       
            tplControl = TemplateParams()
            tplControl.make(spectator)

            tplControl.page_name = 'Редактирование' + article.article_title
            tplControl.link='/compose'
            tplControl.article=article
            tplControl.fileList=fileList
            tplControl.project_start_data = config.options.Project_Start_Data
    
#             logging.info( 'ArticleHandler get tmlFullName = ' + str(tmlFullName))
#             logging.info( 'ArticleHandler get tplControl = ' + str(tplControl))
#             tmlFullName = os.path.join(config.options.tmpTplPath, tmlFullName)
            self.render(tmlFullName, parameters=tplControl)
        except ArticleNotFound:
                self.redirect("Страница не найдена") 
            
        except Exception as e:
            logging.info( 'ArticleHandler Get:: Exception as et = ' + str(e))

            tplControl = TemplateParams()
            tplControl.error = Error ('500', 'что - то пошло не так :-( ')
            self.render('main_error.html', parameters=tplControl)


class ComposeHandler(BaseHandler):
    """
    Редактирование статей 
    
    """
    
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, articleName = ''):
        """
        редактирование статьи 
        приходит НАЗВАНИЕ (articleName) 
        надо найти статью по ее назвнию, 
        после этого надо загрузить статью для редактирования
        если статьи нет, тогда можно загрузить в тайтл название, по которому искали...
        а если этого "articleName" нет, зито есть  self.get_argument("hash", None) - вот тогда
        можно искать серди ревизий нужную, и ее загружать - и название и аннотацию и текст.!!!!
        
        """
        
#         logging.info( 'ComposeHandler Get:: config.options. = ' + str(e))
        
        try:
            hash = self.get_argument("hash", "")
            groupId = self.get_argument("gid", 0)
            
            self.get_current_user()
            self.autor = self.current_user
            
            
            article = Article()
            fileList = []
            artHelper = HelperArticle()
            artHelper.setArticleCategiry (config.options.info_page_categofy_id) 
            
            pageName='Редактирование статьи'

            
            if articleName != '' and hash == '':
#                 logging.info( 'ComposeHandler get articleName = ' + str(articleName))
                
                articleLink = articleName.strip().strip(" \t\n")
                articleLink =  articleLink.lower().replace(' ','_')
                articleLink =  articleLink.replace('__','_')
                notComposeFlag = False
                (article, fileList, tplName) = yield executor.submit( artHelper.getArticleByName, self.autor, articleLink, notComposeFlag )
                
            elif hash != '':
                """
                Выберем статью по ее ХЕШУ - это, скорее всего, будет одна из старых версий.... 
                """
#                 logging.info( 'ComposeHandler get hash = ' + str(hash))
#                 logging.info( 'ComposeHandler get self.autor = ' + str(self.autor))
                (article, fileList) = yield executor.submit( artHelper.getArticleHash, self.autor, hash )
#             elif articleName != '':
#                 artHelper.setArticleTitle (articleName)
#                 pageName='Редактирование ' + articleName
                
            if hasattr(article, 'article_title')  and article.article_title != '':
                pageName= 'Редактирование ' + article.article_title
    #         else:
    #             pass    
             
            tplControl = TemplateParams()
            tplControl.make(self.autor)
            tplControl.article=article
            tplControl.fileList=fileList
            tplControl.groupId=groupId
            tplControl.link='/compose'
            
            tplControl.tpl_categofy_id = config.options.tpl_categofy_id
            tplControl.project_start_data = config.options.Project_Start_Data
            
            
            
            tplControl.page_name = pageName 

            categoryList = [Article(0, 'Выберите значение ')]

            artHelper = HelperArticle()
            categoryList += yield executor.submit(artHelper.getListArticles, config.options.list_categofy_id)
            tplControl.categoryList = categoryList
            tplControl.selectedCategoryId = article.article_category_id
            
            templatesList = [Article(0, 'Выберите значение ')]
            templatesList += yield executor.submit(artHelper.getListArticles, config.options.tpl_categofy_id)
            tplControl.templatesList = templatesList
            tplControl.templateWrkId = article.article_template_id
            
            tplControl.actionLink ='/compose'

# {{ parameters.article.article_id }}

#             logging.info( ' ComposeHandler: GET: tplControl = ' + toStr(tplControl))
#             logging.info( ' ComposeHandler: GET: tplControl.article = ' + toStr(tplControl.article))
            self.render("compose.html", parameters= tplControl)
        except Exception as e:
            logging.info( 'ComposeHandler Get:: Exception as et = ' + toStr(e))
            logging.info( 'Get:: Exception as traceback.format_exc() = ' + toStr(traceback.format_exc()))
            error = Error ('500', 'что - то пошло не так :-( ')
            tplControl = TemplateParams()
            tplControl.make(self.autor)
            tplControl.error=error
            tplControl.link='/compose'
            tplControl.page_name='редактирование статьи'
            self.render('error.html', parameters = tplControl )



    @tornado.web.authenticated
    @gen.coroutine
    def post(self, articleName = ''):
        """
        Получить статью из формы редактирования,
        Разобрать и проверить данные, заполнить ВСЕ, то нжно, и
        сохранить.
        """
        try:
#             logging.info( 'ComposeHandler:: post articleName = ' + str(articleName))
    
            self.get_current_user()
            self.autor = self.current_user
            
#             logging.info( 'ComposeHandler:: post self.autor = ' + str(self.autor))
            
            if not self.autor or not self.autor.dt_header_id: return None
    
            artModel = Article()
    
            artModel.article_id = self.get_argument("id", 0)
            if artModel.article_id == 0:
                artModel.dt_header_id = self.autor.dt_header_id
            artModel.article_title = self.get_argument("title")
            artModel.article_annotation = self.get_argument("annotation")
            artModel.article_source = self.get_argument("sourse")
            artModel.article_category_id = self.get_argument("category_id", 0)
            artModel.article_template_id = int(self.get_argument("template_id", 0))
            artModel.article_permissions = self.get_argument("permissions", 'pbl')                                
            article_pgroipId = self.get_argument("group_id", 0)                                
            
#             logging.info( 'ComposeHandler:: Before Save! artModel = ' + str(artModel))
            
            article_link =  artModel.article_title.lower().replace(' ','_')
            templateDir = self.get_template_path()
            
            helperArticle = HelperArticle()
            helperArticle.setModel(artModel)

            afterSaveArticle = yield executor.submit( helperArticle.сomposeArticleSave, self.autor, templateDir, article_pgroipId )

            # стоит проерить, если мы сохранили шаблон, тогда ндо удалить старый шаблон из директории, где лежат все пользовательские шаблоны!!!!!
            if afterSaveArticle != None and int(afterSaveArticle.article_category_id) == int(config.options.tpl_categofy_id):
                templateEnginer = Template()
                templateEnginer.clean()
            
            logging.info( 'ComposeHandler:: afterSaveArticle = ' + str(afterSaveArticle))
            
            #  поучить ссылку н страничку, откуда был переход на нынешню...
            if afterSaveArticle != None:
#                self.redirect("/" + tornado.escape.url_escape(article_link)) 
# 
#                 self.redirect("/personal_desk_top" )
                self.redirect("/compose/" + afterSaveArticle.article_title )
                
            else:
                logging.info( 'ComposeHandler:: rez = ' + str(rez))
    #             как - то надо передать данные и ошибку - что - то пошло же не так... 
    #             да, и можно и ошибку то получить... 
    #             тоько КАК  - если эксепшин тут не работает... :-( )
    #             self.redirect("/compose" ) 
        except Exception as e:
            logging.info( 'ComposeHandler POST!!! (Save):: Exception as et = ' + str(e))
            logging.info( 'Post:: Exception as traceback.format_exc() = ' + toStr(traceback.format_exc()))
            
            self.redirect("/compose")
            
#             artHelper = HelperArticle()
#             categoryList += yield executor.submit(artHelper.getListArticles, config.options.list_categofy_id)
#             tplControl.categoryList = categoryList
#             tplControl.selectedCategoryId = article.article_category_id
#             
#             templatesList = [Article(0, 'Выберите значение ')]
#             templatesList += yield executor.submit(artHelper.getListArticles, config.options.tpl_categofy_id)
#             tplControl.templatesList = templatesList
#             tplControl.templateWrkId = article.article_template_id
# 
#             logging.info( ' ComposeHandler: GET: tplControl = ' + toStr(tplControl))
#             self.render("compose.html", parameters= tplControl)



class RevisionsHandler(BaseHandler):
    """
    показать список ревизий одного документа 
     Список может отдать на редактирование 
     любую из ревизий документа
     
    
    """
    @gen.coroutine
    def get(self, articleId):
        try:
#             articleId = self.get_argument("id", None)
            self.get_current_user()
            self.autor = self.current_user
            artModel = Article()
            revisions = yield executor.submit( artModel.getRevisionsList, articleId, self.autor.dt_header_id)
            
            tplControl = TemplateParams()
            tplControl.make(self.autor)
            tplControl.revisions=revisions
            tplControl.article_title = revisions[0].article_title
            tplControl.page_name = 'Revisions List' # _("Revisions List")
            tplControl.link='/compose'
            tplControl.project_start_data = config.options.Project_Start_Data
            
            
            
            self.render("revisionses_dt.html", parameters=tplControl )
        except Exception as e:
            logging.info( 'RevisionsHandler:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error, link='/compose', page_name='Список ревизий')
   
   

class RevisionViewHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
            articleId = self.get_argument("aid", None)
            revId = self.get_argument("rid", None)
            revModel = Revision()
            revision = yield executor.submit( revModel.get2Edit, articleId, revId )
    #         if not article:
    #             self.redirect("/compose")
    #             return
            fileControl = File()
    
#             logging.info( 'RevisionViewHandler:: revision = ' + str(revision))
            self.render("revision.html", revision=revision, link='/compose', page_name='Редактирование')
        except Exception as e:
            logging.info( 'RevisionViewHandler:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error, link='/compose', page_name='Редактирование')





class FeedHandler(BaseHandler):
    """
    просмотр списка материалов в другом формате
    - стоит сделать вызов процедуры из хелпера.
    
    """
    
    
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        try:
            artHelper = HelperArticle()
            articles = yield executor.submit( artHelper.getListArticles )
            self.set_header("Content-Type", "application/atom+xml")
            self.render("feed.xml", articles=articles, link='/compose', page_name='Редактирование')
        except Exception as e:
            logging.info( 'FeedHandler:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error, link='/compose', page_name='Редактирование')




 
class ArticleModule(tornado.web.UIModule):
    def render(self, article, fileList):
#         logging.info( 'ArticleModule:: fileList = ' + str(fileList))
        return self.render_string("modules/article.html", article=article, fileList=fileList, link='/compose', page_name='Редактирование')
 
  
class RevisionModule(tornado.web.UIModule):
    def render(self, revision):
        return self.render_string("modules/revision.html", revision=revision, link='/compose', page_name='Редактирование')
 
 
 
class SimpleArticleModule(tornado.web.UIModule):
    def render(self, article):
        return self.render_string("modules/simple_article.html", article=article, link='/compose', page_name='Редактирование')
