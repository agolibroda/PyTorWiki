#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



# test_autor_login


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

from core.BaseHandler           import *
from core.WikiException         import *



sys.path.pop()

import unittest 
         
class TestAutors(unittest.TestCase): 
    autor= None

    def setUp(self): 
        self.autor = Author()
        
        self.author_login = 'login_1'
        self.pwdStr = 'login' 



    def testAutorLogin(self):
#         autor = core.models.Author()

 
        self.autor.login(self.author_login, self.pwdStr)
        print( 'setUp autor = ' + str(self.autor) )
#         self.assertEqual(self.autor.author_name, 'Name0012' )



        
if __name__ == '__main__': 
    unittest.main() 