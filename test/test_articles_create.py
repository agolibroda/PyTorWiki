#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import logging

logging.basicConfig(filename='test.log', level=logging.INFO)
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)


from datetime import date
import time

# import tornado.httpserver 
import tornado.httpclient 
# import tornado.ioloop 
import tornado.web 

import sys, os

sys.path.append(os.path.dirname('./../'))
# from app import * 
import config
import core.models

from core.models.article  import Article
from core.models.author   import Author

sys.path.pop()

import unittest 
         
longArticleText = """

Защитная реакция, «бей или беги», срабатывает, когда при обработке информации мы осознаём наличие проблем. Вот некоторые физиологические симптомы, которые могут сопровождать стресс:

мышечное напряжение;
учащение пульса и повышение артериального давления;
учащенное дыхание (преимущественно грудью, а не животом);
тошнота;
ощущение, что голова тяжёлая;
пониженная концентрация внимания;
безразличие ко всему.
Защитная реакция − средство поддержания нашей жизнеспособности, позволяющая на раннем этапе затормозить развитие проблем. По сути, все физические реакции нашего организма связаны со стрессом. Например, убегая от медведя в лесу, мы активизируем ресурсы перед быстрым выплеском адреналина.

Или, например, перекусы во время работы могут вызывать тошноту, потому что мозговая активность на пике и требует больше ресурсов, чем обычно, а переваривание пищи затормаживается.
"""         
         
authorId = 1
         
class TestAutors(unittest.TestCase): 
    article= None

    def setUp(self): 

        
        self.autor = Author()
        
#         self.author_login = 'log_1540895938.3078651' #'login_1'
#         self.pwdStr = '123123' #'login' 

        self.author_login = 'login_1'
        self.pwdStr = 'login' 
        self.autor.login(self.author_login, self.pwdStr)
        print( 'setUp autor = ' + str(self.autor) )
        
        
        self.article = Article()
        self.article.article_title = 'СуперНоваяСтатья ' + str(time.time())
        self.article.article_annotation = 'СуперНоваяСтатья  СуперНоваяСтатья  СуперНоваяСтатья ' + str(time.time())
        self.article.article_category_id  = 3 
        self.article.article_template_id = 5
        self.article.article_permissions = 'pbl'
        self.article.article_source = longArticleText

#             artModel.article_category_id = self.get_argument("category_id", 0)
#             article_pgroipId = self.get_argument("group_id", 0)                                

        
#         print( 'setUp 11 article = ' + str(self.article) )

    
#     def test_article_001(self):
# #         article = core.models.Article()
#         self.assertEqual(self.article.author_name, 'Name0012' )


    def test_article_save(self):
#         article = core.models.Article()

        print( 'setUp 12 article = ' + str(self.article) )
 
        self.article.save(self.autor, './tpl')

        print( 'setUp article = ' + str(self.article) )
#         self.assertEqual(self.article.author_name, 'Name0012' )


#     def test_article_list(self):
# #         article = core.models.Article()
# 
#  
#         print( 'setUp 12 article = ' + str(self.article) )
#  
#         list = self.article.list()
# 
#         print( 'setUp 12 list = ' + str(list) )
#         
#         for oneArticle in list:
#             print( 'oneArticle = ' + str(oneArticle) )
# #         self.assertEqual(self.article.author_name, 'Name0012' )


#     def test_article_update(self):
# #         article = core.models.Article()
#  
#         articleId = 43
#         self.article.get(articleId) # .article.dt_header_id = 18
#  
#         print( 'test_article_update Before article = ' + str(self.article) )
#          
#          
#         self.article.author_login = 'login_' + str(articleId)
#         self.article.author_name = 'New Name ' +str(articleId) + ' ' + str(time.time())
# #         self.article.author_create = date.fromtimestamp('2018-10-13 00:54:50.928231')
#  
#         self.article._pass_source = '333444' 
#         self.article._old_pass = '123123'  # - старе значение пароля - нужно при смене 
#          
#         print( 'test_article_update Afiet Edit article = ' + str(self.article) )
#  
#         self.article.save()
#         print( 'test_article_update AfterSave article = ' + str(self.article) )
# #         self.assertEqual(self.article.author_name, 'Name0012' )
        
        
if __name__ == '__main__': 
    unittest.main() 