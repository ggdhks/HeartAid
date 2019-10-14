#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
import random
import config
from lsqlite import db
import models
from handler import DataHandler, HeartHandler, LoginHandler, MainHandler, ModelHandler, PasswordHandler, PredictHandler, RegisterHandler, LogoutHandler, ResultHandler
from server_socket import SocketHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/data",DataHandler),
            (r"/heart",HeartHandler),
            (r"/login",LoginHandler),
            (r"/main",MainHandler),
            (r"/model",ModelHandler),
            (r"/password",PasswordHandler),
            (r"/predict",PredictHandler),
            (r"/register",RegisterHandler),
            (r"/result",ResultHandler),
            (r'/logout', LogoutHandler)
        ]
        settings = config.settings
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == "__main__":
    db.create_engine(config.database)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.webport)
    tornado.ioloop.IOLoop.instance().start()