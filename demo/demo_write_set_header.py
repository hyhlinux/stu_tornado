# coding:utf-8
import tornado.ioloop
import tornado.httpserver
# import tornado.options
from tornado.web import RequestHandler, url
from tornado.options import options

# 对比一下两种方式的响应头header中Content - Type字段，
# 自己手动序列化时为Content-Type:text/html charset = UTF-8，
# 而采用write方法时为Content-Type:application/json charset =UTF-8。

options.define(
    "port",
    default=8000,
    type=int,
    help=("port for server"),
)


class MainHandler(RequestHandler):

    def get(self):
        self.write("hello world")
        stu = {
            'name': 'huoyinghui',
            'age': 10,
            'sex': 1
        }

        import json
        # stu = json.dumps(stu)
        chunk = json.dumps(stu)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(chunk)


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
