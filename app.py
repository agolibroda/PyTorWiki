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

from core.FilesControls     import *

from core.ProfileControls   import *
from core.ArticleControls   import *
from core.ProfileControls   import *
from core.DeskTopControls   import *
from core.GroupHandlers     import *

from core.RestControls      import *


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
            (r"/", HomeHandler),
            (r"/index.html", HomeHandler),

            (r"/compose", ComposeHandler), # (ArticleControl) редактор - в зависимости от роли запускателя (или, откуда оно запускается?) такой набор инструментов и покажем.
            (r"/compose/([^/]+)", ComposeHandler), # (ArticleControl)
            (r"/upload/([0-9]+).html",  UploadHandler), # (FilesControl) upload #filesupl

            (r"/revisionse/([0-9]+)", RevisionsHandler),# (ArticleControl) Список ревизий как отдельный список (???) 
            (r"/revision_view", RevisionViewHandler), # (ArticleControl) просмотр одной рвизи????

            (r"/auth/create", AuthCreateHandler), # (ProfileControl.py)
            (r"/auth/login", AuthLoginHandler), # (ProfileControl.py)
            (r"/auth/logout", AuthLogoutHandler), # (ProfileControl.py)
            (r"/profile", MyProfileHandler), # (ProfileControl.py) мой собственный профиль - что бы поредактировать
            (r"/profile/([0-9]+)", AuthorProfile), # (ProfileControl.py) профиль любого пользователя - по ИД - ну надо же поглядеть!

            (r"/personal_desk_top", PersonalDeskTop), # (DeskTopControls) персональный рабочий стол пользователя - 
            (r"/group_desk_top", GroupDeskTop), # (DeskTopControls) рабочий стол участника группы
            (r"/group_desk_top/([0-9]+)", GroupDeskTop), # (DeskTopControls) рабочий стол участника группы
            (r"/sys_adm_desk_top", SysAdmDeskTop), # (DeskTopControls) РС Админа СИСТЕМЫ 

            (r"/groups", GroupListHandler), # (GroupHandlers) Список всех групп в системе -
#             (r"/group/([0-9]+)", GroupProfile), # (GroupHandlers) Публичная часть группы. -
             
            (r"/authors", AuthorsList), # (ProfileControl) Список всех Авторов в системе -
#             (r"/author/([0-9]+", AuthorProfile), # (ProfileControl) Список всех Авторов в системе -

#             (r"/rest/([^/]+)/([0-9]+)",  RestMinHandler), # (RestControl.py) все, что вызывается из клиента AJAX... 

            (r"/([^/]+)", ArticleHandler), # (ArticleControl) Этим замыкаем список рутеров, так как он превращает в название статьи ВСЕ!!!!

        ]
        
        settings = dict(
            wiki_title = config.options.Project_Name,
            project_description = config.options.Project_Description,
            wiki_title_admin = config.options.wikiTitleAdmin,
#             project_dir=projectDir,
            template_path=config.options.templateDir, #os.path.join(projectDir, config.options.templateDir),
            static_path=config.options.staticDir, #os.path.join(projectDir, config.options.staticDir),
            ui_modules={
                        "Article": ArticleModule, 
                        'Revision': RevisionModule, 
                        "SimpleArticle": SimpleArticleModule,
                        'FilesList': FilesListModule,
                        },
            xsrf_cookies=True,
            cookie_secret=config.options.cookieSecret, #  "64d1c3defc5f9e829010881cfae22db38732",
            login_url="/auth/login",
            debug=True,
        )
        
        # sid_name, lifetime added in 1.1.5.0
        # sid_name: the name of session id in cookies.
        # lifetime: session default expires seconds.
        if config.options.sessionsStrategy == 'redis':
            driverValue="redis"
            driverSettings=dict(
                host='localhost',
                port=6379,
                db=14,
#                 "pass"='',
                max_connections=1024,
            )
        elif config.options.sessionsStrategy == 'file':
            driverValue="file"
            driverSettings=dict(host="#_sessions",)
        else:
            # memory
            driverValue='memory'
            driverSettings={'host': self}
        
        session_settings = dict(
            driver=driverValue,
            driver_settings=driverSettings,

            force_persistence=True,
            sid_name= config.options.sidName,
            session_lifetime=config.options.sessionLifetime,
        )
        settings.update(session=session_settings)
        
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
