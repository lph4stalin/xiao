import socket
from Controller.request import *
import Controller.routes
import urllib
from utils import *
# accept函数和recv函数都是阻塞式的。也就是说，他们一直在等待，直到有客户端连接过来或者是后者的有数据可以接收。


def recv_all(connection, buffer_size):
    """
    输入：connection，一个socket对象；buffer_size，一次接收的字节数
    输出：接收到的报文（bytes）格式
    用一个无限循环来接收所有的报文
    """
    r = b''
    while True:
        response = connection.recv(buffer_size)
        r += response
        if len(response) < buffer_size:
            break
    return r


def response(request):
    """
    输入：request
    返回：response
    根据不同的情形返回响应报文
    如果能够查询到路径，则返回路径对应的报文，否则返回 error
    """
    x = Controller.routes.route_dict_par.get(request.route, 'error')
    if x!= 'error':
        response = Controller.routes.route(request)
    else:
        response = Controller.routes.error(request)
    return response


# 如何循环接收 request？
# 服务器主函数
def run(host='', port=2000):
    """
    服务器运行的主函数
    """
    s = socket.socket()
    s.bind((host, port))

    while True:
        # 监听
        s.listen(5)
        # 建立连接，conncetion是一个 socket 实例，address是对方主机的地址
        connection, address = s.accept()

        r = recv_all(connection, 1025)
        r = r.decode('utf-8')
        log('接受的请求', urllib.parse.unquote(r))


        # 有时候会收到空请求，这里判断一下防止程序崩溃
        if len(r.split()) < 2:
            continue

        # 解析请求，得到 method、path、body、query
        request = Request()
        request.get_attr(r)
        log('解析的请求', request.__dict__)


        # 构造 response
        re = response(request)
        log('返回的响应', re)

        # 发送响应报文
        connection.sendall(re)
        # 关闭连接
        connection.close()


def main():
    run()


if __name__ == '__main__':
    main()
