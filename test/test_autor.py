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

from core.models.author         import Author

sys.path.pop()

import unittest 
         
class TestAutors(unittest.TestCase): 
    autor= None

    def setUp(self): 
        self.autor = Author()
        self.autor.author_login = 'log_'+ str(time.time())
        self.autor.author_pass = ''
        self.autor.author_name  = 'Name001' 
        self.autor.author_surname = 'SurName001'
        self.autor.author_role = 'admin'
        self.autor.author_phon = '12345' 
        self.autor.author_email = '12345@qwerty.com'
        self._pass_source = '123123' 
        self._old_pass = ''  # - старе значение пароля - нужно при смене 


#         self.autor.public_key = ''
#         self.autor.private_key = ''
        
#         print( 'setUp 11 autor = ' + str(self.autor) )

    
#     def test_autor_001(self):
# #         autor = core.models.Author()
#         self.assertEqual(self.autor.author_name, 'Name0012' )


    def test_autor_save(self):
#         autor = core.models.Author()

        self.autor._pass_source = '123123' 
 
        print( 'setUp 12 autor = ' + str(self.autor) )
 
        self.autor.save()
        print( 'setUp autor = ' + str(self.autor) )
#         self.assertEqual(self.autor.author_name, 'Name0012' )


#     def test_autor_list(self):
# #         autor = core.models.Author()
# 
#  
#         print( 'setUp 12 autor = ' + str(self.autor) )
#  
#         list = self.autor.list()
# 
#         print( 'setUp 12 list = ' + str(list) )
#         
#         for oneAuthor in list:
#             print( 'oneAuthor = ' + str(oneAuthor) )
# #         self.assertEqual(self.autor.author_name, 'Name0012' )


#     def test_autor_update(self):
# #         autor = core.models.Author()
#  
#         autorId = 43
#         self.autor.get(autorId) # .autor.dt_header_id = 18
#  
#         print( 'test_autor_update Before autor = ' + str(self.autor) )
#          
#          
#         self.autor.author_login = 'login_' + str(autorId)
#         self.autor.author_name = 'New Name ' +str(autorId) + ' ' + str(time.time())
# #         self.autor.author_create = date.fromtimestamp('2018-10-13 00:54:50.928231')
#  
#         self.autor._pass_source = '333444' 
#         self.autor._old_pass = '123123'  # - старе значение пароля - нужно при смене 
#          
#         print( 'test_autor_update Afiet Edit autor = ' + str(self.autor) )
#  
#         self.autor.save()
#         print( 'test_autor_update AfterSave autor = ' + str(self.autor) )
# #         self.assertEqual(self.autor.author_name, 'Name0012' )
        
        
if __name__ == '__main__': 
    unittest.main() 