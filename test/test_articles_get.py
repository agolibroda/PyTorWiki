#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


# test_articles_get

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
         
         
class TestArticle(unittest.TestCase): 
    article= None

    def setUp(self): 
        
        self.autor1 = Author()
        self.autor2 = Author()

        self.author_login1 = 'login_1'
        self.pwdStr1 = 'login' 

        self.author_login2 = 'log_1540895938.3078651' #'login_1'
        self.pwdSt2r = '123123' #'login' 

        self.autor1.login(self.author_login1, self.pwdStr1)
        print( 'setUp autor = ' + str(self.autor) )

        self.autor2.login(self.author_login2, self.pwdStr2)
        print( 'setUp autor = ' + str(self.autor2) )
        
#         self.articleLink = 'суперноваястатья_1541099871.471828' 
        self.articleLink = 'суперноваястатья_персонаьно_tue,_06_nov_2018_09:04:05_+0000'
        self.article = Article()
        

    def test_article_get1(self):
#         article = core.models.Article()
 
        artSou = self.article.get(self.articleLink, self.autor1)

        print( 'article artSou = ' + str(artSou) )

    def test_article_get2(self):
#         article = core.models.Article()
 
        artSou = self.article.get(self.articleLink, self.autor2)

        print( 'article artSou = ' + str(artSou) )


        
if __name__ == '__main__': 
    unittest.main() 