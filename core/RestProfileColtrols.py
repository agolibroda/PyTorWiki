#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2019 Alec Golibroda
# 
# 
# RestProfileColtrols.py
#
# from core.RestProfileColtrols       import *
#
# 

from core.BaseHandler       import *
from core.WikiException     import *


from core.models.author     import Author

from core.models.token      import Token

# from core.models.article    import Article
# from core.models.article import Article
# from core.models.file import File
# from core.models.group      import Group

class RestLoginHandler(BaseHandler):
    """
    
    Логин 
    пиходят логин/пароль/токен 
    Проверяем, что токен существует,  
    Получаем профиль автора (полные даные вместе с RSA-keys)
    Кладём данные в Редиску, в "токен" 
    имя отдаем на клиент.... 
     
    """
    
    @gen.coroutine
    def post(self):
        """
         self.get_current_user()
         self.curentAuthor = self.current_user
         ура у нас есть дата, (data)  из нее можно взять данные, получить логин,
         Если логин случится, тогда взять профиль пользователя, получить его РСА,
         и все это так, положить в редиску 
         и кое  - что из этого отдать на клиента!!!!!!
        """

#         {'authorname': 'developer', 'password': 'чсЧСЯЧС', 'saveMe': True, 'tag': 'ab373fb9-28d5-4bdb-b16d-242266fc3805'}

        try:
            data = tornado.escape.json_decode(self.request.body)
#             logging.info( 'RestLoginHandler:: data = ' + str(data))
            # Если при get_current_user пришел "ложь", значит пользователя нету, и надоо его логинить.
            if self.tokenControl.checkToken(data['tag']):
                self.tokenControl.setHeader(data['tag'])
            else:
#                 вот тут надо что - то сделать, - Отдать какую - то команду, что "форма устарела"
                raise WikiException( ' вот тут надо что - то сделать, - Отдать какую - то команду, что "форма устарела" ' )
                
            if not self.get_current_user():
                authorControl = Author()
                self.current_user = authorControl.login(data['authorname'], data['password'])
#                 logging.info( 'RestLoginHandler:: self.current_user = ' + str(self.current_user))
                
                self.tokenControl.set('currentAuthor', authorControl.serializationAuthor())
                if data['saveMe']:
                    self.tokenControl.setLongLifeTime()
                else:
                    self.tokenControl.setShortLifeTime()
                
            self.curentAuthor = self.current_user
            
            outAuthor = authorControl.getPublicProfile( self.curentAuthor )
#             logging.info( 'RestLoginHandler:: outAuthor.__dict__ = ' + str(outAuthor.__dict__))
            self.write(json.dumps(outAuthor.__dict__))
            
        except Exception as e:
            logging.info('RestLoginHandler:: post:: Have Error!!! '+ str(e))
            
            self.write(json.dumps("Произошло что - то печальное"))

        
#         self.write(json.dumps({"author-id": 123, "name": "alec"}))



class RestLogoutHandler(BaseHandler):
    """
    Выход из системы
    Удалить данные из редиски.   
    """
    
    @gen.coroutine
    def post(self):
        

        try:
            data = tornado.escape.json_decode(self.request.body)
            logging.info( 'RestLoginHandler:: data = ' + str(data))
            # Если при get_current_user пришел "ложь", значит пользователя нету, и надоо его логинить.
            if self.tokenControl.checkToken(data['tag']):
                self.tokenControl.delete(data['tag'])
                
            self.write(json.dumps(True))
            
        except Exception as e:
            logging.info('RestLogoutHandler:: post:: Have Error!!! '+ str(e))
            
            self.write(json.dumps("Произошло что - то печальное"))

