#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda

# что нужно добавить до ядра ритона для нормальной работы
#
#


import tornado.web
import tornado.httpserver
import tornado.ioloop
import torndsession


# import .BaseHandler
import logging



# import pickle
import json

import config

from core.FilesControl import *

from core.ProfileControl import *
from core.ArticleControl import *
from core.ProfileControl import *
from core.DeskTopControls import *




from core.RestControl import *

if hasattr(config.options, 'logFileName'):
    logging.basicConfig(filename=config.options.logFileName, level=logging.INFO)
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)


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

            (r"/rest/([^/]+)/([0-9]+)",  RestMinHandler), # (RestControl.py) все, что вызывается из клиента AJAX... 

            (r"/([^/]+)", ArticleHandler), # (ArticleControl) Этим замыкаем список рутеров, так как он превнащает в название статьи ВСЕ!!!!

# Это походу, надо вычистить - умерло.
#             (r"/article/([^/]+)", ArticleHandler),
#             (r"/my_articles", MyArticletHandler),
#             (r"/my_group", MyGroupHandler),
#             (r"/articles", ArticleListHandler),
#             (config.options.adminPath, AdminHomeHandler, {"flag": "12345"}), # dict(flag=12345)
#             (config.options.adminPath, AdminHomeHandler),
#             (config.options.adminPath + r"/", AdminHomeHandler),
#             (config.options.adminPath + r"/articles", AdminFeedHandler),
#             (config.options.adminPath + r"/revisions", AdminRevisionsHandler),
#             (config.options.adminPath + r"/compose", AdminComposeHandler),
#             (config.options.adminPath + r"/revisionView", AdminRevisionViewHandler),
#             (config.options.adminPath + r"/article/([^/]+)", AdminArticleHandler),

        
        ]
        
        settings = dict(
            wiki_title = config.options.Project_Name,
            wiki_title_admin ="TorWiki Admin layer",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                        "Article": ArticleModule, 
                        'Revision': RevisionModule, 
                        "SimpleArticle": SimpleArticleModule,
                        'FilesList': FilesListModule,
                        },
            xsrf_cookies=True,
            cookie_secret= config.options.cookie_secret, #  "64d1c3defc5f9e829010881cfae22db38732",
            login_url="/auth/login",
            debug=True,
        )
        
        # sid_name, lifetime added in 1.1.5.0
        # sid_name: the name of session id in cookies.
        # lifetime: session default expires seconds.
        if config.options.sessions_strategy == 'redis':
            driverValue="redis"
            driverSettings=dict(
                host='localhost',
                port=6379,
                db=14,
#                 "pass"='',
                max_connections=1024,
            )
        elif config.options.sessions_strategy == 'file':
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
            sid_name='wiki_author',
            session_lifetime=1800,
        )
        settings.update(session=session_settings)
        
        super(Application, self).__init__(handlers, **settings)
        config.options.templateDir = settings['template_path']
#         config.options.__setattr__('templateDir', settings['template_path']) 

        # Have one global connection to the wiki DB across all handlers
        


def main():
#     logging.basicConfig(filename='torViki.log', level=logging.INFO)

    logging.info('Server start at .main_port = ' + str(config.options.main_port))
    
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.options.main_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
