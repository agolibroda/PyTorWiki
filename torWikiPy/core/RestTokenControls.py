#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019 Alec Golibroda
# 
# 
# RestTokenControls.py
#
# from core.RestTokenControls       import *
# 
# Набор контроллеров для работы с профилями пользователей
#
#
#


import bcrypt
import concurrent.futures

import os.path
import re
import subprocess

import json

import core.models

from core.BaseHandler       import *
from core.WikiException     import *

from core.models.author     import Author

from core.models.token      import Token



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)




class RestTokenHandler(BaseHandler):
    """
    
    создать новый токен, положить его в сессию (в )
     
    """
    
    @gen.coroutine
    def get(self):
        """
        Получить новый токен и отдать его клиенту
        
        """
        
        try:
            token = self.tokenControl.header()
            self.write(json.dumps(token))

        except Exception as e:
            logging.info( 'commandName:: '+ str(commandName)+' Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))
        




class RestCheckTokenHandler(BaseHandler):
    """
    Проверим наличие токена в редиске.
    
    """


    @gen.coroutine
    def get(self, tokenTitle):
        """
        Проверить, существует ли токен в редиске, если его нет, 
        тогда вернуть False.
        
        """
        
        try:
            logging.info('RestCheckTokenHandler get tokenTitle = '+ str(tokenTitle))
            self.write(json.dumps(self.tokenControl.checkToken(tokenTitle)))

        except Exception as e:
            logging.info( 'RestCheckTokenHandler get Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.write(json.dumps(error))
        
    
