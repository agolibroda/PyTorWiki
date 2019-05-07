#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda



# import .BaseHandler
import logging

# import pickle
import json


# import tornado.web
# import tornado.httpserver
# import tornado.ioloop
# import torndsession

import config

# import core

from core.RestAuthorsColtrols   import *
from core.RestArticlesColtrols  import *
from core.RestGroupsColtrols    import *
from core.RestProfileColtrols   import *

from core.RestTokenControls   import *




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
            (r"/rest/authors",          RestAuthorsListColtrolHandler), # (RestAuthorsColtrols.py) все, что вызывается из клиента AJAX... 
            (r"/rest/authors/([0-9]+)", RestAuthorColtrolHandler), # (RestAuthorsColtrols.py) все, что вызывается из клиента AJAX... 

            (r"/rest/groups",           RestGroupsListColtrolHandler), # (RestGroupsColtrols.py) все, что вызывается из клиента AJAX... 
            (r"/rest/groups/([0-9]+)",  RestGroupColtrolHandler), # (RestGroupsColtrols.py) все, что вызывается из клиента AJAX... 

            (r"/rest/articles",         RestArticlesListColtrolHandler), # (RestArticlesColtrols.py) все, что вызывается из клиента AJAX... 
            (r"/rest/articles/([^/]+)", RestArticleColtrolHandler), # (RestArticlesColtrols.py) все, что вызывается из клиента AJAX...

            (r"/rest/login",            RestLoginHandler), # (RestProfileColtrols.py) все, что вызывается из клиента AJAX... 
            (r"/rest/logout",           RestLogoutHandler), # (RestProfileColtrols.py) все, что вызывается из клиента AJAX... 

            (r"/rest/token",            RestTokenHandler), # (RestTokenControls.py) все, что ... 
            
            (r"/rest/check_token/([^/]+)",      RestCheckTokenHandler), # (RestTokenControls.py) все, что ... 
             
#################################################################################################

        ]
        
        settings = dict(
#             wiki_title = config.options.Project_Name,
#             project_description = config.options.Project_Description,
#             wiki_title_admin = config.options.wikiTitleAdmin,
# #             project_dir=projectDir,
#             template_path=config.options.templateDir, #os.path.join(projectDir, config.options.templateDir),
#             static_path=config.options.staticDir, #os.path.join(projectDir, config.options.staticDir),
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

    logging.info('Server start at .main_port = ' + str(config.options.main_port))
    logging.info('Надо сделать проверку, есть ли в системе Постгрис- сервер - и можно ли к нему прицепиться :-) ')
    
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.options.main_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
