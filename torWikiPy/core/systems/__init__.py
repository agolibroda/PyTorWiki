# -*- coding: UTF-8 -*-
# Copyright 2021 Alec Golibroda


import os
import os.path
################
import logging

dirModule = os.path.dirname(__file__)
nameModule = __file__
logger = logging.getLogger(nameModule)
logger.setLevel(logging.DEBUG)
###################################


from core.systems.sessions import *

from core.models.author     import Author




def redisCheck():
    """
    # проверим, работает ли сервер редиски, заодно почистим его.
    ТО есть, надо прочистить ВСЮ рабочую базу!!!!!!

    """
    # logger.info(" redisCheck :: config.options.redis_db = " + str(config.options.redis_db) ) 
    # logger.info(" redisCheck :: config.options.redis_session_db = " + str(config.options.redis_session_db) ) 

    try:
        
        # logger.info(" redisCheck :: new_id = " + str(new_id) ) 
        new_id = uuid.uuid4().hex
        session = Session(new_id)
        session['session_id'] = str(new_id)
        session.save()

        session.store.flushdb()
        logger.info(" redisCheck: \n All fine! Redis is working! " ) 
        
    except Exception:
        logger.error('Печально, Редиска не откликается, может упала? (работать дальше нииизя!!) :-(  ')
        raise 



def postgreeCheck():
    """
    проверим, работает ли сервер, 
    заодно полуим количество зарезирвированных Авторов.

    
    """

    
    try:
        
        authorControl = Author() # вот, надо делать сохранение данных   

        # (????) почему то престала работать вот ЭТО
        # authorsCount = yield executor.submit(authorControl.countAutors) 
        authorsCount = authorControl.countAutors()
        
        # logging.info( 'postgreeCheck authorsCount = ' + str(authorsCount)) 
        logger.info(" postgreeCheck: \n All fine! Postgree is working! \n " +
                    " The number of Authors who registered in the system:: " + str(authorsCount))
        
    except Exception:
        logger.error('Печально, Postgree не откликается, может упала? (работать дальше нииизя!!) :-(  ')
        raise 



