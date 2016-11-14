# coding:utf-8
import tornado.ioloop
import tornado.httpserver
import json
from tornado.web import RequestHandler, url
from tornado.options import options

# 该方法会在进入HTTP处理方法前先被调用，可以重写此方法来预先设置默认的headers。
# 注意：
# 在HTTP处理方法中使用set_header()方法会覆盖掉在set_default_headers()方法中设置的同名header。

options.define(
    "port",
    default=8000,
    type=int,
    help=("port for server"),
)


class MainHandler(RequestHandler):

    def set_default_headers(self):
        print "执行了set_default_headers()"
        # 设置get与post方式的默认响应体格式为json
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        # 设置一个名为itcast、值为python的header
        self.set_header("hyh_header", "python")

    def get(self):
        self.write("get world")
        stu = {
            'name': 'huoyinghui',
            'age': 10,
            'sex': 1
        }

        chunk = json.dumps(stu)
        # 注意此处重写了header中的itcast字段
        self.set_header("hyh_header", "i love python")
        self.write(chunk)

    def post(self):
        self.write("post world")
        stu = {
            'name': 'huoyinghui',
            'age': 10,
            'sex': 1
        }

        chunk = json.dumps(stu)
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
