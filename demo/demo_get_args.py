# coding:utf-8
import tornado.ioloop
import tornado.httpserver
from tornado.web import RequestHandler, url
from tornado.options import options
import json

# 前两类方法的整合
# get_argument(name, default=_ARG_DEFAULT, strip=True)
# get_arguments(name, strip=True)

options.define(
    "port",
    default=8000,
    type=int,
    help=("port for server"),
)


class MainHandler(RequestHandler):

    def get(self):
        self.write('get')
        subject = self.get_argument('subject')
        self.write("hello world:" + subject)

    def post(self):
        self.write('post\n')
        subject = self.get_argument('subject')
        subject_list = self.get_arguments('subject')
        self.write('\nsubject:' + subject)
        self.write('\nsubjects:' + str(subject_list))


app = tornado.web.Application(
    [
        (r"/", MainHandler),
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
