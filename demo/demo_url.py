import tornado.ioloop
import tornado.httpserver
# import tornado.options
from tornado.web import RequestHandler, url
from tornado.options import options


options.define(
    "port",
    default=9001,
    type=int,
    help=("port for server"),
)


class MainHandler(RequestHandler):

    def get(self):
        self.write("hello world")


class SubjectHandler(RequestHandler):

    def initialize(self, subject):
        self.subject = subject
        print('subject:', subject)

    def get(self):
        self.write('hi ' + self.subject)
        self.write("<a>" + self.reverse_url(self.subject) + "</a>")

app = tornado.web.Application(
    [
        (r"/", MainHandler),
        url(r"/python", SubjectHandler, {'subject': 'python'}, name='python'),
        url(r"/c", SubjectHandler, {'subject': 'c'}, name='c'),
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
