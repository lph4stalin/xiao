import routes
import socket
import sys
import urllib
sys.path.append("..")
# accept函数和recv函数都是阻塞式的。也就是说，他们一直在等待，直到有客户端连接过来或者是后者的有数据可以接收。

"""
函数1：解析 request，返回 method、route、query、body
函数2：拆分 path，返回 query 和 route
函数3：服务器运行的主函数
"""

# 定义一个 request 类，里面保存了所有的请求信息


class Request(object):
    def __init__(self, r):
        self.raw_data = r
        # 只能 split 一次，因为 body 中可能有换行
        # 把 body 放入 request 中
        header, self.body = r.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        parts = h[0].split()
        self.path = parts[1]
        # 设置 request 的 method
        self.method = parts[0]

        self.path, self.query = parsed_path(self.path)

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        返回的结果格式如下 {'a': b, 'c': d,'e': 1}
        """
        # username=g+u%26a%3F&password=
        # username=g u&a?&password=
        # TODO, 这实际上算是一个 bug，应该在解析出数据后再去 unquote
        args = self.body.split('&')
        f = {}
        for arg in args:
            arg = urllib.parse.unquote(arg)
            k, v = arg.split('=')
            f[k] = v
        return f


def request_from_connection(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        # 取到的数据长度不够 buffer_size 的时候，说明数据已经取完了。
        if len(r) < buffer_size:
            request = request.decode()
            return request


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
        with connection:
            r = request_from_connection(connection)

        buffer_size = 1025
        # r = b''
        r = connection.recv(buffer_size)
        print('收到请求', r)
        r = r.decode('utf-8')

        # 有时候会收到空请求，这里判断一下防止程序崩溃
        if len(r) > 0:
            request = Request(r)

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
        request.method, request.route, request.query, request.body = parsed_request(
            r)
        print('解析请求')
        print('method', request.method, 'route', request.route,
              'query', request.query, 'body', request.body)

        # 构造 response
        response = routes.route(request)
        print('返回页面')
        connection.sendall(response)
        connection.close()


def main():
    run()


if __name__ == '__main__':
    main()
