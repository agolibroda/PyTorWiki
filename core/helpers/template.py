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
from core.models            import Model
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

    
    def exists(self, realFileName):
        """
        Проверить, есть ли файл с Этим номером в директории.
        
        """
        return os.path.exists(realFileName)
    
    
    def clean(self): #  , templateId):
        """
        Убрать файл шаблона (по его ИД) из директории,
        в которой лежат все "внутрисистемные" шиблоны
        Не, уберу ВСЕ файлы!!!!!
        """
#         realFileName = self.realFileName(templateId)
#         if self.exists(realFileName):
#             os.remove(realFileName) 
        _wrkDir = os.path.join(config.options.projectDir, config.options.templateDir, config.options.tmpTplPath)
        for file in os.listdir(_wrkDir):
            os.remove(os.path.join(_wrkDir, file)) 
        _wrkDir = os.path.join(config.options.projectDir, config.options.staticDir, config.options.siteDir)
        for file in os.listdir(_wrkDir):
            os.remove(os.path.join(_wrkDir, file)) 


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
        

    def realFileName(self, templateId, templateName, targetFlag):
        """
        Сделаем реальное имя файла.
        
        templateId = ИД статьи - шаблона  
        templateName = имя статьи, по - идее, это что - то типа "base.html"
        из имени надо выдрать расширение, и потом присовокупить его к "рабочему имени файла", с которым потом и работать!
        """
        file_name = str(templateId)
        listTpl = templateName.split('.')
        if len(listTpl)>1:
            tplExtension = listTpl[len(listTpl)-1]
        else:
            tplExtension = config.options.tplExtension
        realFileName =  ''
        if targetFlag == "tmp":
#             return os.path.join(config.options.tmpTplPath, str(file_name) + '.' + tplExtension)
            return os.path.join(str(file_name) + '.' + tplExtension)
        else:
            return os.path.join(config.options.staticDir, config.options.siteDir, str(file_name) + '.' + tplExtension)
        
        logging.info( 'realFileName:: realFileName =  ' + str(realFileName))
        return realFileName
        
        
    def setDirName(self, targetFlag ):
        """
        получить путь к директории, в которой находятся файлы шаблонов или расширений шаблона (js, css),
        путь зависит от флага.
        
        @param param: targetFlag Флаг = "tmp" или "static" - в зависмости от того, какой путь для выгрузки файлов применяется.
        @return: String - Путь в папке.
        """
        if targetFlag == "tmp":
            return os.path.join(config.options.projectDir, config.options.templateDir, config.options.tmpTplPath)
        else:
            return os.path.join(config.options.projectDir)



    def temtlatePrepareById(self, articleTemplateId, articleLink, targetFlag="tmp"): # article_template_id
        """
        Подготовка шаблона выбирать его будем по ИД
        
        куда будем выкладывать подготовленные шаблоны 
        точки 2:
        - в папку "шаблоны", если работаем с шаблонами ()
        targetFlag= "tmp"
        - в папку 
        - в папку 'static' - если имеем 
        
    
        """
#         logging.info( 'temtlatePrepareById notComposeFlag =  ' + str(notComposeFlag))
        _realFileName = self.realFileName(articleTemplateId, articleLink, targetFlag)
        _wrkFullName = os.path.join(self.setDirName(targetFlag), _realFileName)
        if not self.exists(_wrkFullName):
#             (template, tlFile) = yield executor.submit( artHelper.getArticleById, article.article_template_id )

            artControl = Article()
            template = artControl.getById( articleTemplateId )
            # проанализируем код полученного шаблона, и, если надо, тогда выгрузим все шаблоны, на которые ссылается текущий шаблон.
            #Всевызовы завершим заменами  tw_include на include с соответствующей выгрузкой шаблонов 
            self.temtlateParsing(template)
            
            self.save(_wrkFullName, template.article_source)
            
        return _realFileName
    
    

    def temtlatePrepareByName(self, articleTemplateName, targetFlag = 'tmp'): # article_template_id
        """
        Шаблон выбирать будем по его ИМЕНИ, как статью. :-) 
    
        """
#         logging.info( 'temtlatePrepareByName:: articleTemplateName =  ' + str(articleTemplateName))
#         articleLink = articleTemplateName.strip().strip(" \t\n")
        artControl = Article()
        spectator = None
        template = artControl.get( articleTemplateName, spectator )
#         logging.info( 'temtlatePrepareByName:: template =  ' + str(template))
        
        _realFileName = self.realFileName(template.article_id, template.article_title, targetFlag)
        _wrkFullName = os.path.join(self.setDirName(targetFlag), _realFileName)
        if not self.exists(_wrkFullName):
            # проанализируем код полученного шаблона, и, если надо, тогда выгрузим все шаблоны, на которые ссылается текущий шаблон.
            #Всевызовы завершим заменами  tw_include на include с соответствующей выгрузкой шаблонов 
            self.temtlateParsing(template)
        
        # тут надо добавить и директорию 
        self.save(_wrkFullName, template.article_source)
        
        return _realFileName 



    def temtlateConvert(self, targetFlag, pattern, template): # article_template_id
        """
        Ситаксический разбор шаблона.  именно тут найдем всякие "<!--%(\w+){1}%--!>" конструкции
        
        ......................................................................................
         <link type="text/css" rel="stylesheet" href="<!--%animate_template%--!>"> 
         - конструкцию - <!--%animate_template_css%--!> - издать статью в ..../static/site_templates/12345.css 
         
         {% include "<!--*main_site_menu*--!>" %} 
         - конструкцию <!--*main_site_menu*--!> - издать статью в ..../tmp/334.html
        
        targetFlag: 
            'tmp' -- <!--*(\w+){1}*--!> - 
            'static' -- <!--%animate_template%--!>
            
        """
#         logging.info( 'temtlateParsing IN templateSrc = ' + str(templateSrc))
#         pattern = r"""\"<!--*(\w+){1}*--!>" """ 
# template.article_source, articleLink !!! templateSrc, articleLink
        result = re.finditer(pattern, template.article_source)
        for item in result:
            try:
#                 logging.info(" temtlateConvert  item.group = " + str(item.group())) 
#                 logging.info(" temtlateConvert  item.group(0) = " + str(item.group(0))) 
#                 logging.info(" temtlateConvert  item.group(1) = " + str(item.group(1))) 
#                 logging.info(" temtlateConvert  item.groups = " + str(item.groups())) 
                
#                 # Узнаем ИД шаблона по его названию (заодно и выложим шаблон в папку.) 
                newTemplateName = self.temtlatePrepareByName(item.group(1), targetFlag)
#                 logging.info(" temtlateConvert 1 item.group(0) = " + str(item.group(0))) 
#                 logging.info(" temtlateConvert 1 newTemplateName = " + str(newTemplateName)) 

                result = template.article_source.replace(item.group(0), '"' +newTemplateName + '"')
#                 logging.info(" temtlateConvert 2 result = " + str(result))
                template.article_source = result 
                
            except WikiException as e:
                logging.info(" temtlateConvert WikiException item.group = " + str(item.group())) 
                template.article_source = template.article_source.replace(item.group(0), '')


    def temtlateParsing(self, template): 
        """
        Ситаксический разбор шаблона.  именно тут найдем всякие "<!--%(\w+){1}%--!>" конструкции
        
        ......................................................................................
         <link type="text/css" rel="stylesheet" href="<!--%animate_template%--!>"> 
         - конструкцию - <!--%animate_template_css%--!> - издать статью в ..../static/site_templates/12345.css 
         
         {% include "<!--*main_site_menu*--!>" %} 
         - конструкцию <!--*main_site_menu*--!> - издать статью в ..../tmp/334.html
        
            targetFlag: 
        'tmp' -- <!--*(\w+){1}*--!> - 
        'static' -- <!--%animate_template%--!>

        Делаю 2 прохода 
        - сначала  - выбираем все  "include" и "extends" (выделеные символами "<!--*(\w+){1}*--!>" )
        - и издаем их в tmp
        
        - торой поход - выбрать все шаблоны, которые будут загружаться по линкам (выделеные символами "<!--%(\w+){1}%--!>" ) 
        - и издаем их в static/site_templates - тут по - дее, надо разбирать имя шаблона, брать поледний сегмент "css" и "js" 

        Все остальное  - оставляем в рамках синтаксиса базового шаблонизатора 
        описание  - https://www.tornadoweb.org/en/stable/template.html
        
        \\"\<\!--\*(\w+)\*--\!\>\"
        
        
        """
#         logging.info( 'temtlateParsing IN template = ' + str(template))
#         pattern = r'\"\<\!\-\-\*(\w+)\*\-\-\!\>\"' 
#         pattern = r'[\'\"]\*(.+)\*[\'\"]' 
        pattern = r'[\'\"]<!--\*(.+)\*--!>[\'\"]' 
        self.temtlateConvert('tmp', pattern, template)
        
        pattern = r'[\'\"]<!--%(.+)\%--!>[\'\"]' 
        self.temtlateConvert('static', pattern, template)
        

# @singleton
class TemplateParams(Model):
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
#         logging.info( ' make TplParametr:: author = ' + str(author))
#         if not hasattr(self, 'autorGroupList'): 

#         self.current_user = author
        self.autorGroupList = list()
        groupModel = Group()
#         self.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, self.author.author_id )
        if author != None:# если автор вообще есть, и он
            self.autorGroupList = groupModel.grouplistForAutor( author.dt_header_id )
         
#         logging.info (' makeTplParametr:: self = ' + str( self ))
    def setAuthor (self, author):
        """
        Добавить в шаблон зрителя - 
        в шаблоне называем его автором.
          
        """
        self.current_user = author

  
 
