#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import tornado.web
import tornado.httpserver
import tornado.ioloop
import torndsession


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            debug=True,
        )
        # sid_name, lifetime added in 1.1.5.0
        # sid_name: the name of session id in cookies.
        # lifetime: session default expires seconds.
        session_settings = dict(
            driver='memory',
            driver_settings={'host': self},
            force_persistence=True,
            sid_name='torndsessionID',
            session_lifetime=1800
        ),
        settings.update(session=session_settings)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(torndsession.sessionhandler.SessionBaseHandler):
    def get(self):
        self.write("Hello, Session.<br/>")
        if 'data' in self.session:
            data = self.session['data']
        else:
            data = 0
        self.write('data=%s' % data)
        self.session["data"] = data + 1


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()