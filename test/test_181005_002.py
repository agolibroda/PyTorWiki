#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import tornado.httpserver 
import tornado.httpclient 
import tornado.ioloop 
import tornado.web 

import unittest 

class MainHandler(tornado.web.RequestHandler): 
    def get(self): 
        self.write('Hello, world')
        
         
class TestTornadoWeb(unittest.TestCase): 
    http_server = None                                                                                                                                                                                                                                                                                                                                                    
    response = None
     
    def setUp(self): 
        application = tornado.web.Application([ 
                (r'/', MainHandler), 
                ])  
        self.http_server = tornado.httpserver.HTTPServer(application) 
        self.http_server.listen(8888)
         
    def tearDown(self):
        self.http_server.stop()
        
    def handle_request(self, response): 
        self.response = response 
        tornado.ioloop.IOLoop.instance().stop() 
        
    def testHelloWorldHandler(self): 
        http_client = tornado.httpclient.AsyncHTTPClient() 
        http_client.fetch('http://localhost:8888/', self.handle_request) 
        tornado.ioloop.IOLoop.instance().start()
        resp = self.response.body
        print('!!!!!!!!resp = ' + str(resp))
#         self.failIf(self.response.error) 
#         self.assertEqual(resp, 'Hello, world') 
        
#     def testHelloWorldHandler2(self): 
#         http_client = tornado.httpclient.AsyncHTTPClient() 
#         http_client.fetch('http://localhost:8888/', self.handle_request) 
#         tornado.ioloop.IOLoop.instance().start() 
#         self.failIf(self.response.error) 
#         self.assertEqual(self.response.body, 'Hello, world') 
        
if __name__ == '__main__': 
    unittest.main() 