# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import time
import datetime
import hashlib
import xmltodict
# datetime 可以运算
import datetime


from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
from tornado.httpclient import AsyncHTTPClient
define("port", default=8000, type=int)


class IndexHandler(RequestHandler):

    def get(self):
        self.render("index.html")


class QRcodeHandler(object):
    """docstring for QRcodeHandler"""

    def get(self):
        print('qr...get...test AccessToken')
        try:
            access_token = AccessToken.get_access_token()
        except Exception as e:
            raise e

        self.write(access_token)


class AccessToken(object):
    """docstring for AccessToken --> weichat"""
    _access_token = {
        "data": "",
        "ctime": datetime.datetime.now()
    }

    APPID = "wxd9efdd569e8973db"
    SECRET = "b36029adda7ee9738abaa48192f3693c"

    @tornado.gen.coroutine
    @classmethod
    def _update_access_token(cls):
        client = AsyncHTTPClient()
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
            APPID, SECRET)

        resp = yield client.fetch(url)  # 真正只阻塞一次.
        json_data = resp.body
        json_dic = json.dumps(json_data)
        print('json_dic', json_dic)

        if json_dic.get("errcode", False):
            # ok
            cls._access_token['data'] = json_dic.get("access_token")
            cls._access_token['ctime'] = datetime.datetime.now()
            raise tornado.gen.Return(cls._access_token["data"])

        else:
            # err
            raise Exception("get access_token err")

    #@tornado.gen.coroutine
    @classmethod
    def get_access_token(cls):
        print("get_access_token...")
        if cls._access_token.get("data", None) and ((datetime.datetime.now() - cls._access_token.get('ctime', 0).seconds) < 7200):
            return cls._access_token["data"]
        else:
            # 返回的是生成器.
            # yield cls._update_access_token()
            return cls._update_access_token()


WECHAT_TOKEN = "hyhlinux"


class WeChatHandler(RequestHandler):

    # def prepare(self):
        # signature = self.get_argument('signature')
        # timestamp = self.get_argument('timestamp')
        # nonce = self.get_argument('nonce')
        # echostr = self.get_argument('echostr')

        # tmp = [WECHAT_TOKEN, timestamp, nonce]
        # tmp.sort()
        # tmp_str = "".join(tmp)
        # tmp_str = hashlib.sha1(tmp_str).hexdigest()

        # if (tmp_str == signature):
        #     print('wechat 200')
        #     self.write(echostr)
        # else:
        #     # 403 倍禁止
        #     print('wechat 403')
        #     self.send_err(403)

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
    def post(self):
        data = self.request.body
        print('Postdata:', data)
        xml_args = xmltodict.parse(data)
        print('xml_args:', xml_args)

        to = xml_args["xml"]["ToUserName"]
        fr = xml_args["xml"]["FromUserName"]
        msg_type = xml_args["xml"]["MsgType"]

        if "text" == msg_type:
            content = xml_args["xml"]["Content"]
            resp_dict = {
                "xml": {
                    "ToUserName": fr,
                    "FromUserName": to,
                    "CreateTime": time.time(),
                    "MsgType": "text",
                    "Content": content,
                }
            }
        elif "image" == msg_type:
            MediaId = xml_args["xml"]["MediaId"]
            PicUrl = xml_args["xml"]["PicUrl"]

            resp_dict = {
                "xml": {
                    "ToUserName": fr,
                    "FromUserName": to,
                    "CreateTime": time.time(),
                    "MsgType": "image",
                    "MediaId": MediaId,
                    "PicUrl": PicUrl,
                }
            }
        elif "voice" == msg_type:
            resp_dict = {
                "xml": {
                    "ToUserName": fr,
                    "FromUserName": to,
                    "CreateTime": time.time(),
                    "MsgType": "voice",
                }
            }
        else:
            resp_dict = {
                "xml": {
                    "ToUserName": fr,
                    "FromUserName": to,
                    "CreateTime": time.time(),
                    "MsgType": "text",
                    "Content": 'hi',
                }
            }

        xml_str = xmltodict.unparse(resp_dict)
        self.write(xml_str)


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
        (r"/qr", QRcodeHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
