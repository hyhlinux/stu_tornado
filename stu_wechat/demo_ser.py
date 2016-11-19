# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime
import hashlib

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=8000, type=int)


class IndexHandler(RequestHandler):

    def get(self):
        self.render("index.html")

WECHAT_TOKEN = "hyhlinux"


class WeChatHandler(RequestHandler):

    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')

        tmp = [WECHAT_TOKEN, timestamp, nonce]
        tmp.sort()
        tmp_str = "".join(tmp)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()

        if (tmp_str == signature):
            print('wechat 200')
            self.write(echostr)
        else:
            # 403 倍禁止
            print('wechat 403')
            self.send_err(403)

        # self.render("index.html")


class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器

    def open(self):
        print('open:', self.users)
        self.users.add(self)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip,
                                                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        print('on_message:', message)
        for u in self.users:  # 向在线用户广播消息
            u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip,
                                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        print('on_close:')
        self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        for u in self.users:
            u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip,
                                                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
        (r"/wechat", WeChatHandler),
        (r"/wechat8001", WeChatHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
