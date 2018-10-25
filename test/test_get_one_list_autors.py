# test_get_one_list_autors.py


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

from core.models.author         import Author

sys.path.pop()

import unittest 
         
class TestAutors(unittest.TestCase): 
    autor= None

    def setUp(self): 
        self.autor = Author()
        self.authorId = 8


    def test_autor_list(self):
#         autor = core.models.Author()
 
#         print( 'setUp 12 autor = ' + str(self.autor) )
 
        list = self.autor.list()
        
        for oneAuthor in list:
            print( 'oneAuthor = ' + str(oneAuthor) )

    def test_autor_one(self):
#         autor = core.models.Author()
 
#         print( 'setUp 12 autor = ' + str(self.autor) )
 
        oneAuthor = self.autor.get(self.authorId)
        
        print( 'test_autor_one oneAuthor = ' + str(oneAuthor) )


        
if __name__ == '__main__': 
    unittest.main() 