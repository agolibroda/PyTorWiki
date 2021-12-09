#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda
#
#
# начинаю продолжать..
# 
# процедура запуска сервера в исполнении выглядит так: 
# параметры - работает только "port" :-) пока, наверное :-) 
# python3 app.py port=8000 host=127.0.0.1 
#


import sys

import os
import os.path
################
import logging

dirModule = os.path.dirname(__file__)
nameModule = __file__
logger = logging.getLogger(nameModule)
logger.setLevel(logging.DEBUG)
###################################

# import pickle
import json
import uuid


import argparse
from cryptography.fernet import Fernet


# import tornado.web
# import tornado.httpserver
# import tornado.ioloop
# import torndsession


from tornado.options import define, options

import config

# import core

# from core.systems.sessions import Session # session, SessionHandler
# from core.systems import redisCheck # session, SessionHandler



from core.RestAuthorsControls   import *
from core.RestArticlesControls  import *
from core.RestGroupsControls    import *

from core.RestTokenControls   import *

# from core.Helpers      import *

from core.systems import *


# hasattr(config.options, 'logFileName')

# from tornado.options import define, options



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
#################################################################################################
# как  - то интересно тут работает!!!!! - надо все пересмотреть!!!!
# - если выбор БЕЗ ИД автора, то, должен выбираться СПИСОК, но, нет.. :-( 
    #  в общем, проблемка, разбираться надоть!!!!!

            (r"/rest/authors/([0-9]+)", RestAuthorHandler), # (RestAuthorsControls.py) все, что вызывается из клиента AJAX... 
            (r"/rest/authors",          RestAuthorsListHandler), # (RestAuthorsControls.py) все, что вызывается из клиента AJAX... 

            (r"/rest/groups/([0-9]+)",  RestGroupHandler), # (RestGroupss.py) все, что вызывается из клиента AJAX... 
            (r"/rest/groups",           RestGroupsListHandler), # (RestGroupss.py) все, что вызывается из клиента AJAX... 

            (r"/rest/articles/([^/]+)", RestArticleHandler), # (RestArticless.py) все, что вызывается из клиента AJAX...
            (r"/rest/articles",         RestArticlesListHandler), # (RestArticless.py) все, что вызывается из клиента AJAX... 

            (r"/rest/login",            RestLoginHandler), # (RestAuthorsControls.py) все, что вызывается из клиента AJAX... 
            (r"/rest/logout",           RestLogoutHandler), # (RestAuthorsControls.py) все, что вызывается из клиента AJAX... 
            (r"/rest/hw",               RestHelloWorld), # (RestAuthorsControls.py) просто проверка работы системы.

            # (r"/rest/token",            RestTokenHandler), # (RestTokenControls.py) все, что ... 
            
            (r"/rest/check_token/([^/]+)",      RestCheckTokenHandler), # (RestTokenControls.py) все, что ... 

            (r"/([^/]+)",      RestAnyBoduHandler), # (RestAuthorsControls.py) все, что ... 

             
#################################################################################################

        ]
        
        settings = dict(
#             wiki_title = config.options.Project_Name,

            mediaDir=config.options.mediaDir, #путь к кртинкам текстам..
                        
            # xsrf_cookies=True,
            # cookie_secret=config.options.cookieSecret, #  "64d1c3defc5f9e829010881cfae22db38732",
            cookie_secret=uuid.uuid4().hex,
            debug=True,
        )
        


        super(Application, self).__init__(handlers, **settings)
        
        # config.options.projectDir = os.path.dirname(__file__)
        
#         config.options.__setattr__('templateDir', settings['template_path']) 

        # Have one global connection to the wiki DB across all handlers
        

def main():
    

    logger.info('Проверить наличие Серверов: Постгри и Редиса; \n ' +
                    ' и если их нет, стоит остановить процесс с соответствующими словами!!!! ')
  
    redisCheck() # проверим, работает ли сервер, заодно почистим его.

    postgreeCheck() 

    # symmetricEncrypt(self, key, data):
    _instanceKey = Fernet.generate_key()
    define("instanceKey",   default=_instanceKey,        help="instanceKey")

    logger.info('Server start at config.options.instanceKey = ' + toStr(config.options.instanceKey))

    #  для вызова сервера торнадо на неком определенном порту, надо сделат вот такой вызов:

    # процедура разбора командной строки запуска сервера, 
    # $ python3 app.py --port=8888 --host=127.0.0.1
    
    # нам надо получить пока только номер порта; если порта нет, 
    # тогда используется стандартный порт из конфига.

    parser = argparse.ArgumentParser()
    parser.add_argument('-pt', '--port', type=int, default= config.options.main_port )
    parser.add_argument('-ht', '--host', type=str, default= config.options.main_addr) 
    args = parser.parse_args()

    logger.info('Server start at args = ' + toStr(args))

    http_server = tornado.httpserver.HTTPServer(Application())
    # стоит проверить, а не занят ли ЭТОТ порт и адрес, и не стартовать, если что ...
    # http_server.listen(args.port, address=args.host) #- Эта шняга почему то не работает!!!!
    http_server.listen(args.port, args.host) #- Эта шняга почему то не работает!!!!
    # http_server.listen(args.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    # pass
    main()
