import socket
import time
import sys
sys.path.append("..")
import routes
#accept函数和recv函数都是阻塞式的。也就是说，他们一直在等待，直到有客户端连接过来或者是后者的有数据可以接收。

"""
函数1：解析 request，返回 method、route、query、body
函数2：拆分 path，返回 query 和 route
函数3：服务器运行的主函数
"""

# 定义一个 request 类，里面保存了所有的请求信息
class Request(object):
    def __init__(self):
        self.method = 'GET'
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


request = Request()


# 解析 request
def parsed_request(request):
    header, body = request.split('\r\n\r\n', 1)
    path = header.split()[1]
    method = header.split()[0]
    if '?' in path:
        route, query = parsed_path(path)
    else:
        route = path
        query = ''
    return method, route, query, body


# 把path 中的 query 和 route 拆分出来，其中，query 是字典，route 是字符串
def parsed_path(path):
    query_dict = {}
    route, query_str = path.split('?')
    query_list = query_str.split('&')
    for query in query_list:
        k, v = query.split('=')
        query_dict[k] = v
        return route, query_dict


# 如何循环接收 request？
# 服务器主函数
def run(host='', port=2000):
    s = socket.socket()
    s.bind((host, port))

    while True:
        # 监听
        s.listen(5)
        # 建立连接，conncetion是一个 socket 实例，address是对方主机的地址
        connection, address = s.accept()

        # 接收请求
        buffer_size = 1025
        # r = b''
        r = connection.recv(buffer_size)
        print('收到请求', request)
        r = r.decode('utf-8')

        # 有时候会收到空请求，这里判断一下防止程序崩溃
        if len(r.split()) < 2:
                continue

        # 不知道为什么，使用无限循环接收 request 会卡死
        # while True:
        #     print('进入循环')
        #     request = connection.recv(buffer_size)
        #     print('收到请求')
        #     if request:
        #         r += request
        #         print('请求内容', r)
        #     else:
        #         print('断开')
        #         break

        # 解析请求，得到 method、path、body、query
        request.method, request.route, request.query, request.body = parsed_request(r)
        print('解析请求')
        print('method', request.method, 'route', request.route, 'query', request.query, 'body', request.body)

        # 构造 response
        if routes.route(request):
            response = routes.route(request)
            print('返回页面')
        else:
            response = routes.error()
            print('返回错误')
        connection.sendall(response)
        connection.close()


def main():
    run()


if __name__ == '__main__':
    main()
