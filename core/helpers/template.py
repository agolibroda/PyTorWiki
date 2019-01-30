#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
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
    
    
    
    class ParsingObject(Model):
        """
        Объект для хранения результатов синтаксического разбора шаблона. 
        - что бы было куда подставить нйденные артефакты и полученные для них значения.
           
        - имя шаблона 
        - ИД шаблона
        - расширение
        - имя выходного файла
        - директоря, куда файл будет положен .....
        - флаг, что шаблон отработан, и строка для замены (<!--*main_site_menu*--!>) - типа того
        
        """
        def __init__(self, options):
            if 'expression' in options: self.expression = options['expression']
            if 'tplNane' in options: self.tplNane = options['tplNane']
            if 'tplId' in options: self.tplId = options['tplId']
            if 'tplExtent' in options: self.tplExtent = options['tplExtent'] 
            else: self.tplExtent = 'html'
            if 'targetFlag' in options: self.targetFlag = options['targetFlag']
            if 'flagOfEnd' in options: self.flagOfEnd = options['flagOfEnd'] 
            else: self.flagOfEnd = 0  # 0 - cтарт; 200 - нормальное окончание; 500 ошибка;            
    
    

    def __init__(self):
        self.file_name = ''
        self.file_extension = ''
        self.error = ''
        self.tmplateTxt = ''
        self.lexemDict = {} #  словарь объектов - лексемм
        self.lexemId = [] #  словарь объектов - лексемм

    
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
#         logging.info( 'temtlatePrepareById realFileName =  ' + str(realFileName))
#         logging.info( 'temtlatePrepareById os.path.exists(realFileName) =  ' + str(os.path.exists(realFileName)))
#         
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
        
    def getTemplateExtension(self, templateName):
        listTpl = templateName.split('.')
        if len(listTpl)>1:
            return listTpl[len(listTpl)-1]
        else:
            return config.options.tplExtension
        


    def realFileName(self, templateId, templateName, targetFlag):
        """
        Сделаем реальное имя файла.
        
        templateId = ИД статьи - шаблона  
        templateName = имя статьи, по - идее, это что - то типа "base.html"
        из имени надо выдрать расширение, и потом присовокупить его к "рабочему имени файла", с которым потом и работать!
        """
        tplExtension = self.getTemplateExtension(templateName)
        return self.doFileName(templateId, tplExtension, targetFlag)


 
    def doFileName(self, templateId, tplExtension, targetFlag):
        """
        Сделаем реальное имя файла.
        
        templateId = ИД статьи - шаблона  
        templateName = имя статьи, по - идее, это что - то типа "base.html"
        из имени надо выдрать расширение, и потом присовокупить его к "рабочему имени файла", с которым потом и работать!
        """
#         logging.info(" doFileName  templateId = " + str(templateId))
#         logging.info(" doFileName  tplExtension = " + str(tplExtension))
#         logging.info(" doFileName  targetFlag = " + str(targetFlag))
        file_name = str(templateId)
        if targetFlag == "tmp":
#             return os.path.join(config.options.tmpTplPath, str(file_name) + '.' + tplExtension)
            return os.path.join(file_name + '.' + tplExtension)
        else:
            return os.path.join(config.options.staticDir, config.options.siteDir, file_name + '.' + tplExtension)
       
        
    def setDirName(self, targetFlag ):
        """
        получить путь к директории, в которой находятся файлы шаблонов или расширений шаблона (js, css),
        путь зависит от флага.
        
        @param param: targetFlag Флаг = "tmp" или "static" - в зависмости от того, какой путь для выгрузки файлов применяется.
        @return: String - Путь в папке.
        """
        if targetFlag == "tmp":
#             return os.path.join(config.options.projectDir, config.options.templateDir, config.options.tmpTplPath)
            return os.path.join(config.options.templateDir, config.options.tmpTplPath)
        else:
#             return os.path.join(config.options.projectDir)
            return ""


    def temtlateParsing(self, articleTemplateObj):
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

         похоже, вот тут надо сначала сделать некую таблицу замен
         - имя статьи-шаблона - то, что получается при выборке по шаблону
         - ИД статьи-шаблона и расширение названия для последующей замены  
         после того, как вс поля таблицы будут заполнены, можно делать полную замену всех вхождений во всем тексте ()
         (открыть текст, дважды из него выбрать лексеммы, потом поменять в тексте все, что нужно :-) )
         вот, возмжно, мне нужен селект по статьям - получить ИД статей по их именам. 
         (приводить имена статей к линкам и в таблице и в поисковом слове))
         да, в таблице сделать поле "прокомпилено" - так как в таблицу могут попадать тексты постепенно 
        
        """
#         logging.info(" temtlateParsing  articleTemplateObj = " + str(articleTemplateObj)) 

        artControl = Article()
        template = artControl.getById( articleTemplateObj.tplId )
#         logging.info(" temtlateParsing  template = " + str(template)) 

#         logging.info(" temtlateParsing  template.article_id = " + str(template.article_id)) 
#         logging.info(" temtlateParsing  template.article_title = " + str(template.article_title)) 
        _realFileName = self.realFileName(template.article_id, template.article_title, articleTemplateObj.targetFlag)
#         logging.info(" temtlateParsing  _realFileName = " + str(_realFileName) ) 
        _wrkFullName = os.path.join(self.setDirName(articleTemplateObj.targetFlag), _realFileName)
#         logging.info(" temtlateParsing  _wrkFullName = " + str(_wrkFullName) + "; not self.exists(_wrkFullName) = " + str(not self.exists(_wrkFullName)) ) 
        if not self.exists(_wrkFullName):
            listNames = {} # словарь словарь расширений шаблона собраный по именам
            listNames2serch = [] # [] - #список имен шаблонов для выборки их ИД
    
            token_specification = [
                ( r'[\'\"]<!--\*(.+)\*--!>[\'\"]'),     # проверим наличие "включенных шаблонов"
                ( r'[\'\"]<!--\%(.+)\%--!>[\'\"]'),   # проверим наличие JS и CSS - документов внутри шаблона
            ]
            tok_regex = '|'.join('(%s)' % pair for pair in token_specification)
            
            result= re.finditer(tok_regex, template.article_source)
#             logging.info(" temtlateParsing  result = " + str(result)) 
             
            for mo in result:
                # вот тутнадо все полученые лексеммы добавить в объект 
                targetFlag = self.getTargetFlag (mo.group(0))
                
                tplNane = ''
                if targetFlag == 'tmp':
                    tplNane = mo.group(2)
                    tplExtent = self.getTemplateExtension(mo.group(2))
                if targetFlag == 'static':
                    tplNane = mo.group(4)
                    tplExtent = self.getTemplateExtension(mo.group(4))
                
                tplOne = Template.ParsingObject({
                                                "expression": mo.group(0),
                                                "tplNane": tplNane, 
                        #                         "tplId": 0,
                                                "tplExtent": tplExtent,
                                                "targetFlag": targetFlag
                                                   })
#                 logging.info(" temtlateParsing  tplOne = " + str(tplOne)) 
                if not tplOne.tplNane in listNames:
#                     logging.info(" temtlateParsing  not tplOne.tplNane in listNames!!!! = " ) 
                    listNames[tplNane] = tplOne 
                    listNames2serch.append(tplNane)
                    
                    
            listResult = artControl.getIdListOfNames(listNames2serch)
            for oneRow in listResult:
#                 logging.info(" temtlateParsing  oneRow = " + str(oneRow)) 
                tmpTpl = listNames[oneRow.article_title]
                tmpTpl.tplId = oneRow.article_id
                if not tmpTpl.tplId in self.lexemId:
                    self.lexemDict[tmpTpl.tplId] = tmpTpl
                    self.lexemId.append(tmpTpl)
                    
#                 logging.info(" temtlateParsing  tmpTpl = " + str(tmpTpl)) 

                _fn2Replase = self.realFileName(tmpTpl.tplId, tmpTpl.tplNane, tmpTpl.targetFlag)
#                 logging.info(" temtlateParsing  replace _fn2Replase = " + str(_fn2Replase)) 
                result = template.article_source.replace(tmpTpl.expression, '"' +_fn2Replase + '"')
#                 _fullName2replase = os.path.join(self.setDirName( tmpTpl.targetFlag ), _fn2Replase)
#                 logging.info(" temtlateParsing  replace _fullName2replase = " + str(_fullName2replase)) 
#                 result = template.article_source.replace(tmpTpl.expression, '"' +_fullName2replase + '"')
                template.article_source = result
                
#             logging.info(" temtlateParsing  self.lexemDict = " + str(self.lexemDict)) 
#             logging.info(" temtlateParsing  _wrkFullName = " + str(_wrkFullName)) 
#             logging.info(" temtlateParsing  template.article_source = " + str(template.article_source)) 
            self.save(_wrkFullName, template.article_source)
#         тут нужен цыкл проверки все ли добавленные в словарь "self.lexemDict" обработаны. 
        while True:
            try:
                self.temtlateParsing(self.lexemId.pop())
            except:
                break



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
        opt = {"tplId": articleTemplateId, "tplExtent": 'html', "targetFlag": "tmp"} 
#         tets = 'asdasasdasdasd'
        tplOne = Template.ParsingObject(opt)
        self.lexemDict[articleTemplateId] = tplOne
        self.temtlateParsing(tplOne)

        _realFileName = self.realFileName(articleTemplateId, articleLink, targetFlag)
#         _wrkFullName = os.path.join(self.setDirName(targetFlag), _realFileName)
        return _realFileName


          
    def getTargetFlag (self, stringForTest):
#         keywords = {'tmp', 'static'}
        if  stringForTest.find('-*') > -1:
            return 'tmp'
        if  stringForTest.find('-%') > -1:
            return 'static'

        
        

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

  
 
