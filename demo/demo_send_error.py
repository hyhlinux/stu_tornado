# coding:utf-8
import tornado.ioloop
import tornado.httpserver
import json
from tornado.web import RequestHandler, url
from tornado.options import options

# 抛出HTTP错误状态码status_code，默认为500，kwargs为可变命名参数。
# 使用send_error抛出错误后tornado会调用write_error()方法进行处理，
# 并返回给浏览器处理后的错误页面

# 注意：
# 默认的write\_error()方法不会处理send\_error抛出的kwargs参数，
# 即上面的代码中content = "出现404错误"是没有意义的。

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
        self.send_error(404, content="出现404错误", title='err..404')
        # self.write("结束")  # 我们在send_error再次向输出缓冲区写内容

    def write_error(self, status_code, **kwargs):
        print(kwargs)
        self.write(u"<h1>err</h1>")
        self.write(u"<p>errr title:{}</p>".format(kwargs.get('titile', 'None')))
        self.write(u"<p>err...detail:{}</p>".format(kwargs.get('content', 'None')))

app = tornado.web.Application(
    [
        (r"/", IndexHandler),
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
