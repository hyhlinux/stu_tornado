# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import torndb
import os
import hyh

from tornado.web import RequestHandler, url, StaticFileHandler
from tornado.options import define, options

define("port", default=8000, type=int)


class IndexHandler(RequestHandler):

    def get(self):
        user = dict(
            name=self.get_argument("name", 'hyh'),
            passwd=self.get_argument("passwd", '1'),
            mobile=self.get_argument("mobile", '12310002000'),
        )

        try:
            sql = "insert into it_user_info(ui_name, ui_passwd, ui_mobile) values(%(title)s, %(position)s, %(price)s, %(score)s, %(comments)s)"
            user_id = self.application.db.execute(sql, **user)
        except Exception as e:
            print e
        self.write(str(user_id))


class Application(tornado.web.Application):

    def __init__(self, *args, **kwarg):
        super(Application, self).__init__(*args, **kwarg)
        self.db = torndb.Connection(
            host="192.168.1.128",
            database="itcast",
            user="root",
            password="mysql"
        )
        print('db:', self.db)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    tornado.options.parse_command_line()

    # app = tornado.web.Application([
    app = Application([
        (r"/", IndexHandler),
        # url(r"/all", IndexAllHandler, name='all'),
        (r"/(.*)", StaticFileHandler,
         {'path': os.path.join(os.path.dirname(__file__), "../statics/html/")}),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "../static"),
        template_path=os.path.join(os.path.dirname(__file__), "../template"),
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
