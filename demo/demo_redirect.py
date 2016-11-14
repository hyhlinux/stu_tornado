# coding:utf-8
import tornado.ioloop
import tornado.httpserver
import json
from tornado.web import RequestHandler, url
from tornado.options import options

options.define(
    "port",
    default=8000,
    type=int,
    help=("port for server"),
)


class IndexHandler(RequestHandler):
    """对应/"""

    def get(self):
        self.write("主页")


class LoginHandler(RequestHandler):
    """对应/login"""

    def get(self):
        self.write('<form method="post"><input type="submit" value="登陆"></form>')

    def post(self):
        self.redirect("/")

app = tornado.web.Application(
    [
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
    ],
    debug=True,
)


def main():
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
