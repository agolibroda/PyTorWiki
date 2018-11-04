

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
# вот тут все работает!
#         self.author_login = 'log_1540379436.686734' 
#         self._pass_source = '123123' 

 # а вот тут   НЕТ!!!! - значитЬ, надо поверитьдля пользователя №6, и правильно отредактировать данные, или поправить...
 
        self.author_login = 'login_1'
        self._pass_source = 'login' 


    def test_autor_login(self):
        autor = Author()
        autor.login(self.author_login, self._pass_source )
        print( 'After Login  autor = ' + str(autor) )


        
if __name__ == '__main__': 
    unittest.main() 