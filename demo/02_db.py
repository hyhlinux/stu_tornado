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
        # self.write("aaa")
        ret = self.application.db.get(
            "select ui_name from it_user_info where ui_user_id=1")
        self.write(ret["ui_name"])


class InsertHandler(BaseHandler):

    def post(self):
        name = self.get_argument("name")
        passwd = self.get_argument("passwd")
        mobile = self.get_argument("mobile")
        sql = "insert into it_user_info(ui_name, ui_passwd, ui_mobile) values(%(name)s, %(passwd)s, %(mobile)s)"
        try:
            user_id = self.application.db.execute(
                sql, name=name, passwd=passwd, mobile=mobile)
        except Exception as e:
            print e
            return self.write("DB error:%s" % e)
            # return self.write({"error": 1, "errmsg": "db_error", "data":
            # None})
        self.write(str(user_id))


class HouseHandler(BaseHandler):

    def get(self):
        user_id = self.get_argument('user_id')
        print user_id
        # sql = "select ui_name from it_user_info where ui_user_id =
        # (%(user_id)s)"
        sql = "select ui_name, ui_mobile, hi_name, hi_price, hi_address from it_user_info inner join it_house_info on ui_user_id = hi_user_id  where ui_user_id = (%(user_id)s)"

        try:
            query_list = self.application.db.query(sql, user_id=user_id)
            print query_list
        except Exception as e:
            print e
            return self.write({"error": 1, "errmsg": "db_error", "data": None})

        houses = []
        if query_list:
            for l in query_list:  # l-->line
                house = {
                    'uname': l['ui_name'],
                    'mobile': l['ui_mobile'],
                    'hname': l['hi_name'],
                    'hprice': l['hi_price'],
                    'haddress': l['hi_address'],
                }
                houses.append(house)
        self.write({"error": 1, "errmsg": "db_error"})
        self.write({"data": houses})


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db=torndb.Connection(
            host="127.0.0.1",
            database="itcast",
            user="root",
            password="mysql"
        )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    current_path=os.path.dirname(__file__)
    settings=dict(
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
    app=Application([
        (r"/", IndexHandler),
        (r"/insert", InsertHandler),
        (r"/house", HouseHandler),
    ], **settings)
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
