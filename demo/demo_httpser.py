import tornado.ioloop
import tornado.httpserver
# import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8000, type=int)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("hello world")

app = tornado.web.Application([
    (r"/", MainHandler),
])


def main():
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
