"""
解析请求，并保存在一个 class 中
method: POST
path: /login?a=b&c=d
route: path 中？前面的部分（/login）
query: path 中？后面的‘a=b&c=d’，query会把它转换成{a: b, c: d}的形式
header: 转换成一个字典存储
body: 形如‘a=b&c=d’，转换成字典形式保存
cookie: header 的一个部分

"""
import urllib


# 定义一个 request 类，里面保存了所有的请求信息
class Request(object):
    def __init__(self):
        pass


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


    # 解析 header
    def parsed_header(self):
        header_list = self.header.split('\r\n')[1:]
        self.header_dict = {}
        for i in header_list:
            k, v = i.split(': ')
            self.header_dict[k] = v
        # return self.header_dict



    # 解析 cookie，预期如果登录了，会有一个 session
    def parsed_cookie(self):
        self.cookie = self.header_dict.get('Cookie', 'status=Not Login')
        if 'session' in self.cookie:
            self.session = self.cookie.split('session=')[1]

    def form(self, query):
        """
        有可能传入 body，或者是 query
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        # username=g+u%26a%3F&password=
        # username=g u&a?&password=
        # TODO, 这实际上算是一个 bug，应该在解析出数据后再去 unquote
        query = urllib.parse.unquote(query)
        if '&' in query:
            args = query.split('&')
            f = {}
            for arg in args:
                k, v = arg.split('=')
                f[k] = v
            return f


    def get_attr(self, request):
        try:
            self.parsed_request(request)
            self.parsed_header()
            self.parsed_cookie()
        except Exception as e:
            print('出错了', e)




# 这是一个请求示例
# request = 'POST /login HTTP/1.1\r\nHost: localhost:2000\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: http://localhost:2000/\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9\r\nCookie: status=Not Login\r\n\r\nusername=hollowlph&password=123'
