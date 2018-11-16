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

        
# from _overlapped import NULL

##############
import config
from . import Model
from .. import WikiException 
from . import Article

from core.models.group      import Group


class Template(Model): #, tornado.web.RequestHandler):
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


    def temtlatePrepare(self, articleTemplateId): # article_template_id
        """
        Подготовка шаблона - надо пройти по шаблону, и зменить все вызовы вида
         "{% tw_include "main_site_menu" %}" на "{% include ".../tmp/334.html" %}" 
         - с имененм файла, вместо имени шаблона, и, положить все шаблоны в даректорию, где лежат все шаблоны
        Шаблон удаляется из хрнилища при редактировании, кладется  - при первом оращении.
        
        Пока меняем 2 типа операций  
        include =>> tw_include  - включение одного файла - шаблона в другой шаблон
        extends =>> tw_extends - расширение базового шаблона новыми плюшками.  
        
        Все остальное  - оставляем в рамках синтаксиса базового шаблонизатора 
        описание  - https://www.tornadoweb.org/en/stable/template.html
    
        """
        tmlFullName = self.realFileName(articleTemplateId)
        logging.info( 'temtlatePrepare:: save 3 tmlFullName =  ' + str(tmlFullName))
        if not self.exists(tmlFullName):
#             (template, tlFile) = yield executor.submit( artHelper.getArticleById, article.article_template_id )
            (template, tlFile) = artHelper.getArticleById( articleTemplateId )
            # проанализируем код полученного шаблона, и, если надо, тогда выгрузим все шаблоны, на которые ссылается текущий шаблон.
            #Всевызовы завершим заменами  tw_include на include с соответствующей выгрузкой шаблонов 
            self.save(tmlFullName, template.article_source)
        return tmlFullName



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
#         logging.info( ' makeTplParametr:: author = ' + toStr(author))
#         if not hasattr(self, 'autorGroupList'): 

        self.author = author
        groupModel = Group()
#         self.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, self.author.author_id )
        self.autorGroupList = groupModel.grouplistForAutor( self.author.dt_header_id )
         
#         logging.info (' makeTplParametr:: self = ' + str( self ))

  


    
