#
# Работа с Шаблонами!!! 
#
#
#
#
#


#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# template.py

# Это чисто работа с шаблонами 
# - выгрузить шаблон в шаблоновую директорию
# - удалить шаблон из директории



from __future__ import print_function


import logging

import tornado.options
import tornado.web


import os
import os.path

import re


        
# from _overlapped import NULL

##############
import config
from core.models.article    import Article
from core.models.file       import File
from core.models.group      import Group

from core.WikiException     import *


class Template(): #, tornado.web.RequestHandler):
    """
    Работа с шаблонами
    похоже, нужна процедура выкладки шаблона в особую директорию (ну, что бы не смешивать :-) )
    и выкладку делать будем в момент сохранения шаблона в форме :-) 
    
    self.get_template_path() - Это обращение к крассу "BaseHandler(tornado.web.RequestHandler):" 
    и где - то там, значит, надо назначать объект - "пользовательские шаблоны"  
    и вот тут его грузить :-) или, не грузить, а тут наследоватья от него....   
    
    Работа с шаблонизатром описана в документе 
    https://www.tornadoweb.org/en/stable/template.html    
    
    """
    class ParsingObject():
        """
        Объект для хранения результатов синтаксического разбора шаблона. 
        - что бы было куда подставить нйденные артефакты и полученные для них значения.   
        
        """
        pass

    def __init__(self):
        self.file_name = ''
        self.file_extension = ''
        self.error = ''
        self.tmplateTxt = ''

    
    def load(self, template_id):
        """
        Положить в директорию "внутренних" шаблонов файл шаблона,
        получив его тело из базы по ИД (если файла там нет) 
        
        """
        pass


    def realFileName(self, templateId):
        """
        Сделаем реальное имя файла.
        
        """
        file_name = str(templateId)
        temptateDir = os.path.join(config.options.templateDir, config.options.tmpTplPath)
        realFileName = os.path.join(temptateDir, str(file_name) + config.options.tplExtension)
        logging.info( 'Template:: exists realFileName =  ' + str(realFileName))
        return realFileName
    
    def exists(self, realFileName):
        """
        Проверить, есть ли файл с Этим номером в директории.
        
        """
        return os.path.exists(realFileName)
    
    
    def clean(self, templateId):
        """
        Убрать файл шаблона (по его ИД) из директории,
        в которой лежат все "внутрисистемные" шиблоны
        """
        realFileName = self.realFileName(templateId)
        logging.info( 'Template:: clean realFileName =  ' + str(realFileName))
        logging.info( 'Template:: clean self.exists(realFileName) =  ' + str(self.exists(realFileName)))
        if self.exists(realFileName):
            os.remove(realFileName) 


    def save(self, tmlFullName, tmplateTxt):
        """
        сохранить темплейт в директории... 
        
        """
#         tmlFullName = self.realFileName(templateId)
    #         logging.info( 'Template:: save 3 temptateFileName =  ' + str(temptateFileName))
#         if not self.exists(tmlFullName):
        output_file = open( tmlFullName, 'wb')
        output_file.write(bytes(tmplateTxt, 'utf-8'))
        output_file.close()


    def temtlatePrepareById(self, articleTemplateId): # article_template_id
        """
        Подготовка шаблона выбирать его будем по ИД
    
        """
        tmlFullName = self.realFileName(articleTemplateId)
        logging.info( 'temtlatePrepare:: save 3 tmlFullName =  ' + str(tmlFullName))
        if not self.exists(tmlFullName):
#             (template, tlFile) = yield executor.submit( artHelper.getArticleById, article.article_template_id )

            artControl = Article()
            template = artControl.getById( articleTemplateId )
            # проанализируем код полученного шаблона, и, если надо, тогда выгрузим все шаблоны, на которые ссылается текущий шаблон.
            #Всевызовы завершим заменами  tw_include на include с соответствующей выгрузкой шаблонов 
            template.article_source = self.temtlateParsing(template.article_source)
            
            self.save(tmlFullName, template.article_source)
        return tmlFullName

    def temtlatePrepareByName(self, articleTemplateName): # article_template_id
        """
        Шаблон выбирать будем по его ИМЕНИ, как статью. :-) 
    
        """
        logging.info( 'temtlatePrepareByName:: articleTemplateName =  ' + str(articleTemplateName))
        articleLink = articleTemplateName.strip().strip(" \t\n")
        artControl = Article()
        spectator = None
        template = artControl.get( articleLink, spectator )
        # проанализируем код полученного шаблона, и, если надо, тогда выгрузим все шаблоны, на которые ссылается текущий шаблон.
        #Всевызовы завершим заменами  tw_include на include с соответствующей выгрузкой шаблонов 
        template.article_source = self.temtlateParsing(template.article_source)
        tmlFullName = self.realFileName(template.article_id)
        self.save(tmlFullName, template.article_source)
        
        return template.article_id


    def temtlateParsing(self, templateSrc): # article_template_id
        """
        Ситаксический разбор шаблона.  именно тут найдем всякие " tw_..." конструкции
        
        Подготовка шаблона - надо пройти по шаблону, и зменить все вызовы вида
         "{% tw_include "main_site_menu" %}" на "{% include ".../tmp/334.html" %}" 
         - с имененм файла, вместо имени шаблона, и, положить все шаблоны в даректорию, где лежат все шаблоны
        Шаблон удаляется из хрнилища при редактировании, кладется  - при первом оращении.
        
        Пока меняем 2 типа операций  
        include =>> tw_include  - включение одного файла - шаблона в другой шаблон
        extends =>> tw_extends - расширение базового шаблона новыми плюшками.  
        
        Все остальное  - оставляем в рамках синтаксиса базового шаблонизатора 
        описание  - https://www.tornadoweb.org/en/stable/template.html

        и сделаем из них табличку. или, список объектов 
        ParsingObject
        
        """
#         logging.info( 'temtlateParsing IN templateSrc = ' + str(templateSrc))
        pattern = r"""\{\%[ \t]+tw_(\w+){1}[ \t]+[\'\"](.+)[\'\"][ \t]+\%\}""" 
        result = re.finditer(pattern, templateSrc)
        for item in result:
            try:
                temtlateId = self.temtlatePrepareByName(item.group(2))
                newTemplateName = str(temtlateId)+ '.html'
                newOperator = '{% ' + item.group(1) + ' "' + newTemplateName + '" %}'
                templateSrc = templateSrc.replace(item.group(0), newOperator)
            except WikiException as e:
                templateSrc = templateSrc.replace(item.group(0), '')
        return templateSrc

# @singleton
class TemplateParams:
    """
     место хранения всех параметров, которые надо передавать в шаблон        
     
    """
#     @gen.coroutine
    def make (self, author):
        """
        для работы с формами, туда надо передать некоорое количество данных. 
        все эти данные надо собрать в объкт (одиночку) TemplateParams
        и пользоваться его данными
          
        """
        logging.info( ' makeTplParametr:: author = ' + str(author))
#         if not hasattr(self, 'autorGroupList'): 

#         self.current_user = author
        groupModel = Group()
#         self.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, self.author.author_id )
        self.autorGroupList = groupModel.grouplistForAutor( author.dt_header_id )
         
#         logging.info (' makeTplParametr:: self = ' + str( self ))
    def setAuthor (self, author):
        """
        Добавить в шаблон зрителя - 
        в шаблоне называем его автором.
          
        """
        self.current_user = author

  
 
