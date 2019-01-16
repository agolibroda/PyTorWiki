#!/usr/bin/env python
#
# Copyright 2016 Alec Goliboda
#
# article.py
# контроллер для загрузки и сохранению статей...



import logging
import json

import bcrypt
import concurrent.futures

import os.path
import re
import subprocess


import config

import core.models


from core.models.author     import Author
from core.models.article    import Article
from core.models.file       import File
from core.models.group      import Group

from .template   import Template, TemplateParams

from core.WikiException     import *


class HelperArticle():
    """
    загрузить и сохранить статью
    
    """
    
    def __init__(self):
        self.artModel = Article()
        
    def setArticleTitle(self, articleName):
        self.artModel.article_title = articleName
        
    def setArticleCategiry(self, articleCategoryId):
        self.artModel.category_article_id = articleCategoryId
        
    def getModel(self):
        return self.artModel
    
    def setModel(self, article):
        self.artModel = article


    def getArticleById(self, articleId):
#         logging.info( ' getArticleById:: articleId = ' + str(articleId))
        article = self.artModel.getById( articleId )
        if not article: raise tornado.web.HTTPError(404)
        targetFlag="tmp"
        templator = Template()
        templateName = templator.temtlatePrepareById(article.article_template_id, article.article_title, targetFlag) # article_template_id
#         logging.info( 'getArticleById:: tplateName = ' + str(templateName))
#         logging.info( 'getArticleById:: article.article_template_id = ' + str(article.article_template_id))
#         logging.info( 'getArticleById:: article.article_title = ' + str(article.article_title))
        
        if targetFlag == "tmp":
            templateName =  os.path.join(config.options.tmpTplPath, templateName)
        
        fileModel = File()
# вот тут надо посмотреть - что - то не работает выбор файлов!!!!!!!
        fileList = fileModel.getFilesListForArticle( articleId, config.options.to_out_path)
            
#         logging.info( 'getArticleById:: tplateName = ' + str(templateName))
#             logging.info( 'getArticleById:: article = ' + str(article))
#             logging.info( 'getArticleById:: fileList = ' + str(fileList))
        return (article, fileList, templateName)
     
     
    
    def getListArticles(self, categoryId = 0):
    
        try:
            rezult = self.artModel.list (categoryId)
            if not rezult: rezult = []
            logging.info( 'getListArticles:: rezult = ' + str(rezult))
            return  rezult #.result()
        except Exception as e:
            logging.info( 'getListArticles:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            return []


    def getListArticlesByAutorId(self, authorId = 0, spectatorId = 0):
        """
        получить список статей одного автора
        
        """
        rezult = self.artModel.listByAutorId (authorId, spectatorId)
        if not rezult: rezult = []
#         logging.info( 'getListArticles:: rezult = ' + str(rezult))
        return  rezult #.result()


    def getListArticlesAll(self, spectatorId = 0):
        """
        получить Полный список статей для одного зрителя
        
        """
        rezult = self.artModel.getListArticlesAll (spectatorId)
        if not rezult: rezult = []
#         logging.info( 'getListArticles:: rezult = ' + str(rezult))
        return  rezult #.result()


    def getArticleByIdRevId(self, articleId, revId):
        """
        получить определенную ревизию статьи
        
        """
 
        if articleId and revId:
            fileModel = File()
            article =  self.artModel.get2Edit(articleId, revId)
           
            fileList = fileModel.getFilesListForArticle( articleId, config.options.to_out_path)
            return (article, fileList)
            

        
    def getArticleByName(self, spectator, articleName, notComposeFlag=True):
        """
        получить статью по ее названию (не линка, а название!!!!! )
        хотя, по - идее, надо поредакитровать и сначала превратить навание в линку...
        
        articleName - базе64 - кодированное имя статьи
        spectatorId - ИД пользователя, которые ищет/смотрит статью!!!!!
        
        """
#         logging.info( 'getArticleByName notComposeFlag = ' + str(notComposeFlag))
        
        fileModel = File()
        articleLink = articleName.strip().strip(" \t\n")
        article = self.artModel.get( articleLink, spectator )
        
        templateName = ''
        targetFlag = "tmp"
        
        # показать статью в шаблоне нам нужно только для пользователя (НЕ для редактирования)
        if notComposeFlag:
            templator = Template()
            templateName = templator.temtlatePrepareById(article.article_template_id, articleLink, targetFlag) # article_template_id
#             logging.info( 'getArticleByName 1 templateName = ' + str(templateName))

        fileList =  fileModel.getFilesListForArticle( article.article_id, 
                                                    config.options.to_out_path)
        
        if targetFlag == "tmp":
            templateName =  os.path.join(config.options.tmpTplPath, templateName)
        
#         logging.info( 'getArticleByName article = ' + str(article))
#         logging.info( 'getArticleByName fileList = ' + str(fileList))
#         logging.info( 'getArticleByName templateName = ' + str(templateName))
        return (article, fileList, templateName)


    def getArticleHash(self, spectator, articleHash):
        """
        получить статью по ее ХЕШУ (не линка, а название!!!!! )
        хотя, по - идее, надо поредакитровать и сначала превратить навание в линку...
        
        """
        fileModel = File()
        article = self.artModel.getByUsingHash( spectator, articleHash )
        fileList =  fileModel.getFilesListForArticle( article.article_id, 
                                                    config.options.to_out_path)
        return (article, fileList)


    def сomposeArticleSave(self, author, templateDir, article_pgroipId):
        """
        сохранить статью
        
        """
        try:
            self.artModel.begin()

            article = self.artModel.save(author, templateDir)
#             logging.info( 'сomposeArticleSave:: author = ' + str(author))
#             logging.info( 'сomposeArticleSave:: article_pgroipId = ' + str(article_pgroipId))
#             logging.info( 'сomposeArticleSave:: article.article_id = ' + str(article.article_id))
      
            # а вот сдесь я и грохну старый отрендериный шаблон!!!! и будет все НОРМ!!!!!
            if int(article.article_category_id) == int(config.options.tpl_categofy_id):
                wrkTpl = Template()
                wrkTpl.clean() #save(article.article_id, htmlTextOut, templateDir)
                
            
            if int(article_pgroipId) > 0 :
                groupModel = Group()
                groupModel.librarySave(int(authorId), int(article_pgroipId), int(article.article_id), 'W')
                
            self.artModel.commit()                
            return article
        except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
            logging.info( 'сomposeArticleSave:: e = ' + str(e))
            return None

        

