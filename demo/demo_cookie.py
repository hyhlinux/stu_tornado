# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import os
import torndb

from tornado.web import RequestHandler, url, StaticFileHandler
from tornado.options import define, options

define("port", default=8000, type=int)

'''
    if hasattr(self, "_new_cookie"):
    for cookie in self._new_cookie.values():
        self.add_header("Set-Cookie", cookie.OutputString(None))

cookie --> 写在header中
strftime
strptime
'''


class BaseHandler(RequestHandler):

    def prepare(self):
        pass

    def write_error(self, status_code, **kwargs):
        pass

    def set_default_headers(self):
        pass

    def initialize(self):
        pass

    def on_finish(self):
        pass


class IndexHandler(BaseHandler):

    def get(self):
        self.set_cookie('dome', 1)
        # self.set_header('Set-Cookie', )
        # self.set_cookie("n4", "v4", expires=time.mktime(
        #     time.strptime("2016-11-11 23:59:59", "%Y-%m-%d %H:%M:%S")))
        # self.write(ret["ui_name"])


class CookieCountHandler(BaseHandler):

    def get(self)
        count = self.get_secure_cookie('page_count')
        if not count:
            count = 1
            self.set_secure_cookie('page_count', int(count))
        else:
            self.set_secure_cookie('page_count', int(count) + 1)

        self.write('cookiecount' + count)


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = torndb.Connection(
            host="127.0.0.1",
            database="itcast",
            user="root",
            password="mysql"
        )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    current_path = os.path.dirname(__file__)
    settings = dict(
        static_path=os.path.join(current_path, "static"),
        template_path=os.path.join(current_path, "template"),
        debug=True,
    )
    # app = tornado.web.Application([
    #         (r"/", IndexHandler),
    #     ], **settings)
    # app.db =  torndb.Connection(
    #         host="127.0.0.1",
    #         database="itcast",
    #         user="root",
    #         password="mysql"
    # )
    app = Application([
        (r"/", IndexHandler),
        (r"", CookieCountHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
