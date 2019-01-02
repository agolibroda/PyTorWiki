# test_articles_get

import logging

logging.basicConfig(filename='test_test.log', level=logging.INFO)
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

from  core.helpers.template   import Template, TemplateParams


sys.path.pop()

import unittest 
         
         
class TestArticle(unittest.TestCase): 
    article= None

    def setUp(self): 

        self.template = Template()
        

    def test_article_get2(self):
#         article = core.models.Article()
 
        
        self.template.clean() #save(article.article_id, htmlTextOut, templateDir)
        
#         print( 'Template realFileName = ' + str(realFileName) )


        
if __name__ == '__main__': 
    unittest.main() 