# test_roup.py


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

from core.models.group         import Group

sys.path.pop()

import unittest 
         
class TestAutors(unittest.TestCase): 
    autor= None

    def setUp(self): 
        self.group = Group()
        
#     def __init__(self, group_title = '', group_annotation = '', group_status = 'pbl'):
#         Model.__init__(self, 'groups')   
# 
        self.group.dt_header_id = 0
        self.group.public_key = ''
        self.group.private_key = ''

        self.group.group_title = 'Group_'+ str(time.time())
        self.group.group_annotation = 'Group_annotation_'+ str(time.time())
        self.group.group_status = 'pbl'

#         print( 'setUp 11 autor = ' + str(self.autor) )

#     def test_autor_001(self):
# #         autor = core.models.Author()
#         self.assertEqual(self.autor.author_name, 'Name0012' )


    def test_group_save(self):
#         autor = core.models.Author()
 
        authorId = 1
        print( 'setUp 12 group = ' + str(self.group) )
 
        self.group.save(authorId)
        print( 'setUp group = ' + str(self.group) )
#         self.assertEqual(self.autor.author_name, 'Name0012' )


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