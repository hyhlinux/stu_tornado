# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import hyh

from tornado.web import RequestHandler, url
from tornado.options import define, options

define("port", default=8000, type=int)


class IndexHandler(RequestHandler):

    def get(self):
        hyh.get_head_info()
        self.render("nav_index.html")


class IndexAllHandler(RequestHandler):

    def get(self):
        houses = [
            {
                "price": 398,
                "title": "宽窄巷子+160平大空间+文化保护区双地铁",
                "score": 5,
                "comments": 6,
                "position": "北京市丰台区六里桥地铁"
            },
            {
                "price": 398,
                "title": "宽窄巷子+160平大空间+文化保护区双地铁",
                "score": 5,
                "comments": 6,
                "position": "北京市丰台区六里桥地铁"
            },
            {
                "price": 398,
                "title": "宽窄巷子+160平大空间+文化保护区双地铁",
                "score": 5,
                "comments": 6,
                "position": "北京市丰台区六里桥地铁"
            },
            {
                "price": 398,
                "title": "宽窄巷子+160平大空间+文化保护区双地铁",
                "score": 5,
                "comments": 6,
                "position": "北京市丰台区六里桥地铁"
            },
            {
                "price": 398,
                "title": "宽窄巷子+160平大空间+文化保护区双地铁",
                "score": 5,
                "comments": 6,
                "position": "北京市丰台区六里桥地铁"
            }]
        self.render("all.html", houses=houses)


if __name__ == '__main__':
    # tornado.options.parse_command_line()
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        # (r"/all", IndexAllHandler),
        url(r"/all", IndexAllHandler, name='all'),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "../static"),
        template_path=os.path.join(os.path.dirname(__file__), "../template"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
