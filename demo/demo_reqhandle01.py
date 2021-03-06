# coding:utf-8
import tornado.ioloop
import tornado.httpserver
# import tornado.options
from tornado.web import RequestHandler, url
from tornado.options import options
import json

options.define(
    "port",
    default=8000,
    type=int,
    help=("port for server"),
)


class MainHandler(RequestHandler):

    def get(self):
        subject = self.get_argument('subject')
        self.write("hello world:" + subject)

    def post(self, *args, **kwargs):
        self.write('post')
        # subject = self.get_query_argument('subject')  # 只能获取header中. 不能获取body
        # subject = self.get_argument('a')
        # self.write('subject:', subject)
        # app_type = self.request.headers.get('Content-Type').startswith('application/json')
        # if app_type:
        #     json_str = self.request.body
        #     json_data = json.loads(json_str)
        # else:
        #     json_data = {}
        # print('json:', json_data)
        # self.write(str(json_data))
        # file

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
