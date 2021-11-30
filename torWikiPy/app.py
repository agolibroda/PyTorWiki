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

# import .BaseHandler
import logging

# import pickle
import json

import argparse


# import tornado.web
# import tornado.httpserver
# import tornado.ioloop
# import torndsession

import config

# import core

from core.RestAuthorsControls   import *
from core.RestArticlesControls  import *
from core.RestGroupsControls    import *

from core.RestTokenControls   import *

from core.Helpers      import *


hasattr(config.options, 'logFileName')

if hasattr(config.options, 'logFileName'):
    logging.info(" app  config.options.logFileName = " + str(config.options.logFileName))  
    logging.basicConfig(filename=config.options.logFileName, level=logging.INFO)
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logging.info(" app  hasattr(config.options, 'logFileName') = " + str(hasattr(config.options, 'logFileName')))  

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

            (r"/rest/token",            RestTokenHandler), # (RestTokenControls.py) все, что ... 
            
            (r"/rest/check_token/([^/]+)",      RestCheckTokenHandler), # (RestTokenControls.py) все, что ... 

            (r"/([^/]+)",      RestAnyBoduHandler), # (RestAuthorsControls.py) все, что ... 

             
#################################################################################################

        ]
        
        settings = dict(
#             wiki_title = config.options.Project_Name,
#             project_description = config.options.Project_Description,
#             wiki_title_admin = config.options.wikiTitleAdmin,
# #             project_dir=projectDir,
#             template_path=config.options.templateDir, #os.path.join(projectDir, config.options.templateDir),

            static_path=config.options.staticDir, #os.path.join(projectDir, config.options.staticDir),
            
#             ui_modules={
#                         "Article": ArticleModule, 
#                         'Revision': RevisionModule, 
#                         "SimpleArticle": SimpleArticleModule,
#                         'FilesList': FilesListModule,
#                         },
#             xsrf_cookies=True,
            cookie_secret=config.options.cookieSecret, #  "64d1c3defc5f9e829010881cfae22db38732",
#             login_url="/auth/login",
            debug=True,
        )
        
# вот тут похоже.... 


        # if not hasattr(options, 'redis_host'):
        #     define("redis_host", default="localhost", help="Redis host")
        # if not hasattr(options, 'redis_port'):
        #     define("redis_port", default=6379, help="Redis port number")
        # if not hasattr(options, 'redis_session_db'):
        #     try:
        #         default_db = options.redis_db
        #     except AttributeError:
        #         default_db = 0
        #     define("redis_session_db", default=default_db, help="Redis sessions database")
        # if not hasattr(options, 'session_length'):

        # sid_name, lifetime added in 1.1.5.0
        # sid_name: the name of session id in cookies.
        # lifetime: session default expires seconds.
#         if config.options.sessionsStrategy == 'redis':
#             driverValue="redis"
#             driverSettings=dict(
#                 host=config.options.redisHost,
#                 port=config.options.redisPort,
#                 db=config.options.redisDb,
# #                 "pass"='',
#                 max_connections=config.options.redisMaxConnections,
#             )
#             
#         elif config.options.sessionsStrategy == 'file':
#             driverValue="file"
#             driverSettings=dict(host="#_sessions",)
#         else:
#             # memory
#             driverValue='memory'
#             driverSettings={'host': self}
#         
#         session_settings = dict(
#             driver=driverValue,
#             driver_settings=driverSettings,
# 
#             force_persistence=True,
#             sid_name= config.options.sidName,
#             session_lifetime=config.options.sessionLifetime,
#         )
#         settings.update(session=session_settings)
        
        super(Application, self).__init__(handlers, **settings)
        
        config.options.projectDir = os.path.dirname(__file__)
        
#         config.options.__setattr__('templateDir', settings['template_path']) 

        # Have one global connection to the wiki DB across all handlers
        


def main():
#     logging.basicConfig(filename='torViki.log', level=logging.INFO)

    logging.info('Надо сделать проверку, есть ли в системе Постгрис- сервер - и можно ли к нему прицепиться :-) ')
    logging.info('Надо сделать проверку, есть ли в системе Редиска - сервер - и можно ли к нему прицепиться :-) ')
    logging.info('Если их нет, тогда цепляться некчему, и стоить остановить процесс с соответствующими словами!!!! ')
    
    #  для вызова сервера торнадо на неком определенном порту, надо сделат вот такой вызов:

    # процедура разбора командной строки запуска сервера, 
    # $ python3 app.py --port=8888 --host=127.0.0.1
    
    # нам надо получить пока только номер порта; если порта нет, 
    # тогда используется стандартный порт из конфига.

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default= config.options.main_port )
    parser.add_argument('-hh', '--host', type=str, default= config.options.main_addr) 
    args = parser.parse_args()

    logging.info('Server start at args = ' + toStr(args))

    http_server = tornado.httpserver.HTTPServer(Application())
    # стоит проверить, а не занят ли ЭТОТ порт и адрес, и не стартовать, если что ...
    # http_server.listen(args.port, address=args.host) #- Эта шняга почему то не работает!!!!
    http_server.listen(args.port, args.host) #- Эта шняга почему то не работает!!!!
    # http_server.listen(args.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    # pass
    main()
