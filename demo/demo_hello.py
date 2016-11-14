import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("hello world")

application = tornado.web.Application([
    (r"/", MainHandler),
])


def main():
    application.listen(9000, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
