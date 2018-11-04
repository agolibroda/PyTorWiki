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
        
        self.autor = Author()
        
#         self.author_login = 'log_1540895938.3078651' #'login_1'
#         self.pwdStr = '123123' #'login' 

        self.author_login = 'login_1'
        self.pwdStr = 'login' 

        self.autor.login(self.author_login, self.pwdStr)
        print( 'setUp autor = ' + str(self.autor) )
        
        self.articleLink = 'суперноваястатья_1541099871.471828'
        self.article = Article()
        

    def test_article_update(self):
#         article = core.models.Article()
 
        artSou = self.article.get(self.articleLink, self.autor)

        print( 'article artSou = ' + str(artSou) )


        
if __name__ == '__main__': 
    unittest.main() 