# coding: utf-8

import socket
import ssl
import datetime

"""
一、解析url
函数1：解析 protocol
函数2：解析 host
函数3：解析 port
函数4：解析 path
二、网络连接
函数5：调用socket
函数6：建立连接、构造请求、发送请求
函数7：接收响应
函数8：解析响应
"""


# 1
# 补全函数
def protocol_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表协议的字符串, 'http' 或者 'https'
    """
    # 前 8 个字符是 "https://"，protocol 为 https，其余的 protocol 为 http
    if url[0:8] == 'https://':
        protocol = 'https'
    else:
        protocol = 'http'
    return protocol


# 2
# 补全函数
def host_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表主机的字符串, 比如 'g.cn'
    """
    # 1.检查是否有 '://'，即是否有协议，如果有，把协议部分切除掉
    # 2.再在剩余的文本中检查是否有 ':'，即是否有端口，如果有，把端口及之后部分切除掉
    # 3.再检查剩余的文本中是否有 '/'，即路径，如果有，把路径及之后的内容切除掉

    # 如果没有 '://'，host从开头直接取
    if url.find('://') == -1:
        u = url
    # 否则需要先切割掉 '://' 之前的内容
    else:
        u = url.split('://')[1]
    # 如果有':'，切除冒号及之后
    if u.find(':') != -1:
        u = u.split(':')[0]
    # 如果有 '/'，切除正斜杠及之后
    if u.find('/') != -1:
        u = u.split('/')[0]
    host = u
    return host


# 3
# 补全函数
def port_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表端口的字符串, 比如 '80' 或者 '3000'
    注意, 如上课资料所述, 80 是默认端口
    """
    # 有没有冒号，有冒号的冒号后面是端口，否则是默认端口
    # 切除协议头，避免冒号干扰
    if url.find('://') != -1:
        u = url.split('://')[1]
    else:
        u = url
    # 判断有没有冒号
    if u.find(':') != -1:
        u = u.split(':')[1]
        # 判断有没有 path
        if u.find('/') != -1:
            port = int(u.split('/')[0])
        else:
            port = int(u)
    else:
        if protocol_of_url(url) == 'http':
            port = 80
        if protocol_of_url(url) == 'https':
            port = 443
    return port


# 4
# 补全函数
def path_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表路径的字符串, 比如 '/' 或者 '/search'
    注意, 如上课资料所述, 当没有给出路径的时候, 默认路径是 '/'
    """
    # 切除掉协议后，'/' 后面的就是路径
    # 如果没有 '/'，路径就是 '/'
    if url.find('://') != -1:
        u = url.split('://')[1]
    else:
        u = url
    if u.find('/') != -1:
        path = '/' + u.split('/')[1]
    else:
        path = '/'
    return path


# 4
# 补全函数
def parsed_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    """
    protocol = protocol_of_url(url)
    host = host_of_url(url)
    port = port_of_url(url)
    path = path_of_url(url)
    return protocol, host, port, path


# ——————————————————————————————————————————————————————————————————————————————
def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        # 除此之外无其他差别
        s = ssl.wrap_socket(socket.socket())
    return s


# 接收 response
def response_by_socket(s):
    r = b''
    buffer_size = 1024
    while True:
        print('start')
        response = s.recv(buffer_size) # why?为啥会卡在这儿？
        print('start2')
        # 每次判断 recv 的长度是否等于0，如果等于0，那么说明已经接收完了
        r += response
        print(r.split(b'Content-Length: '))
        c_l = r.split(b'Content-Length: ')[1]
        c_l = int(c_l.split(b'\r\n')[0])
        print(c_l)
        print(len(r))
        if len(r) == c_l:
            break
    return r



# 解析响应，把 response 拆分成 状态码(int)、Headers(字典)、Body(str)
def parsed_response(response):
    pass


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    """
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    """
    # 解析 url
    protocol, host, port, path = parsed_url(url)
    print(protocol, host, port, path)

    # 调用 socket
    s = socket_by_protocol(protocol)
    print(s)

    # 建立连接
    s.connect((host, port))
    print(1, datetime.datetime.now())

    # 构造请求
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\n\r\n'.format(
        path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    # 接收响应，一次接收1025字节，直到接收完
    response = response_by_socket(s)
    print(3, datetime.datetime.now())

    # s.close() 客户端不需要断开连接，服务器需要断开连接
    return response


# url = 'http://movie.douban.com/top250'
url = 'http://www.100tal.com/'
print(get(url))
