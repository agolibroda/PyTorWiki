#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2014 Mitchell Chu


from sys import version
import tornado.web
import tornado.httpserver
import tornado.ioloop
from torndsession.sessionhandler import SessionBaseHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/del', DeleteHandler),
        ]
        settings = dict(
            debug=True,
        )
        session_settings = dict(

            driver="redis",
            driver_settings=dict(
                host='localhost',
                port=6379,
                db=14,
#                 "pass"='',
                max_connections=1024,
            ),

#             driver="memory",
#             driver_settings=dict(
#                 host=self,
#             ),
            
#             driver="file",
#             driver_settings=dict(
#                 host="#_sessions",
#             ),
            
            sid_name='torndsession-mem',  # default is msid.
            session_lifetime=1800,  # default is 1200 seconds.
            force_persistence=True,
        )
        settings.update(session=session_settings)
        tornado.web.Application.__init__(self, handlers=handlers, **settings)


class MainHandler(SessionBaseHandler):
    def get(self):
        self.write("Memory Session Object Demo:<br/>")
        if "sv" in self.session:
            current_value = self.session["sv"]
        else:
            current_value = 'Memory Session Object Demo'
        if not current_value:
            self.write("current_value is None(0)<br/>")
            current_value = 'Memory Session Object DemoMemory Session Object Demo '
        else:
            current_value = current_value + '  272384728933984 '
        self.write('<br/> Current Value is: %s' % current_value)
        self.write('<br/>Current Python Version: %s' % version)
        self.session["sv"] = current_value


class DeleteHandler(SessionBaseHandler):
    def get(self):
        '''
        Please don't do this in production environments.
        '''
        self.write("Memory Session Object Demo:")
        if "sv" in self.session:
            current_value = self.session["sv"]
            self.write("current sv value is %s, and system will delete this value.<br/>" % self.session["sv"])
            self.session.delete("sv")
            if "sv" not in self.session:
                self.write("current sv value is empty")
        else:
            self.write("Session data not found")


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()