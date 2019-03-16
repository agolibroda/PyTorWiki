#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda


#  
# from core.BaseRestHandler       import *


import tornado.web
from core.BaseHandler       import *

# tornado.web.RequestHandler, 
class BaseRestHandler(BaseHandler):

    def __init__(self, *args, **kwargs):        
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        # HEADERS!
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


