# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os

from tornado.web import RequestHandler
from tornado.options import define, options

define("port", default=8000, type=int)


class IndexHandler(RequestHandler):

    def get(self):
        self.render("index.html")

if __name__ == '__main__':
    tornado.options.parse_command_line()
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "../static"),
        template_path=os.path.join(os.path.dirname(__file__), "../template"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
