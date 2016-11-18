# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError

define("port", default=8000, type=int, help="run server on the given port.")


class IndexHandler(RequestHandler):

    def initialize(self):
        print "调用了initialize()"

    def prepare(self):

        '''
        处理数据: 
            get/post 都可以直接获取数据.
        '''

        data_type = self.request.headrs.get('Content-Type', '').startswith('application/json')
        if data_type:
            import json
            data = self.request.body
            self._data = json.loads(data)
        # self.write()
        print "调用了prepare()"

    def set_default_headers(self):
        print "调用了set_default_headers()"

    def write_error(self, status_code, **kwargs):
        print "调用了write_error()"

    def get(self):
        print "调用了get()", self._data
        # self.write(self._data)

    def post(self):
        print "调用了post()", self._data
        self.send_error(200)  # 注意此出抛出了错误

    def on_finish(self):
        print "调用了on_finish()"


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

# hyh...('HTTPServerRequest.__init__: (arguments)', {})
# hyh...('_parse_body:', {})
# headrs: <tornado.httputil.HTTPHeaders object at 0x7fa76de29090>
# body:
# 调用了set_default_headers()
# hyh...('RequestHandler:', {})
# 调用了initialize()
# 调用了prepare()
# 调用了get()
# 调用了on_finish()
# 在正常情况未抛出错误时，调用顺序为：

# set_defautl_headers()
# initialize()  #
# prepare()     #已经获取了浏览器的请求  header/body
# HTTP方法
# on_finish()   #是数据已经发送到浏览器，才会调用.


# 在有错误抛出时，调用顺序为：
# set_default_headers()
# initialize()
# prepare()
# HTTP方法 post中调用senderr
# set_default_headers()  会重置headers
# write_error()
# on_finish()
