# coding:utf-8
import tornado.ioloop
import tornado.httpserver
from tornado.web import RequestHandler, url
from tornado.options import options
import json

# get_query_argument(name, default=_ARG_DEFAULT, strip=True)
# 从请求的查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
# default为设值未传name参数时返回的默认值，如若default也未设置，则会抛出tornado.web.MissingArgumentError异常。
# strip表示是否过滤掉左右两边的空白字符，默认为过滤。

options.define(
    "port",
    default=8000,
    type=int,
    help=("port for server"),
)


class MainHandler(RequestHandler):

    # http://192.168.1.128:8000/?subject=python&subject=c ---> c
    def get(self):
        self.write('get')
        subject = self.get_query_argument('subject')
        self.write("hello world:" + subject)

    def post(self):
        self.write('post\n')
        subject = self.get_body_argument('subject')
        subject_list = self.get_body_arguments('subject')
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
