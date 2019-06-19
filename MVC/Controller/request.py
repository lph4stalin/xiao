"""请求和解析请求"""
"""
函数1：把 body 中字符串格式转换为字典格式
函数2：解析 request，返回 method、route、query、body
"""
import urllib
from flask import Flask


# 定义一个 request 类，里面保存了所有的请求信息
class Request(object):
    def __init__(self):
        self.method = ''
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        # username=g+u%26a%3F&password=
        # username=g u&a?&password=
        # TODO, 这实际上算是一个 bug，应该在解析出数据后再去 unquote
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

    # 解析 request
    def parsed_request(self, request):
        self.header, self.body = request.split('\r\n\r\n', 1)
        self.path = self.header.split()[1]
        self.method = self.header.split()[0]
        if '?' in self.path:
            self.route, self.query = self.path.split('?', 1)
        else:
            self.route = self.path
            self.query = ''
