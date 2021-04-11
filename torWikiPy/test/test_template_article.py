#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_articles_get

import logging

# logging.basicConfig(filename='test_test.log', level=logging.INFO)
# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT)


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

from  core.helpers.template   import Template, TemplateParams


sys.path.pop()

import unittest 
         
         
class TestArticle(unittest.TestCase): 
    article= None

    def setUp(self): 
        
        self.listNames2serch = ['base.html', 'menu_site.html']

        self.artControl = Article()
        

    def test_article_get2(self):
#         article = core.models.Article()
 
        print( 'Template self.listNames2serch = ' + str(self.listNames2serch) )
        
        listResult = self.artControl.getIdListOfNames( self.listNames2serch )
        print( 'Template listResult = ' + str(listResult) )


        
if __name__ == '__main__': 
    unittest.main() 