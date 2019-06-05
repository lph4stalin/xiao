#coding: utf-8

import socket
import ssl

"""
2017/02/16
作业 1


资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
其他请参考上课内容, 不懂在群里发问, 不要憋着
"""


# 1
# 补全函数
def protocol_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表协议的字符串, 'http' 或者 'https'
    '''
    # 前 8 个字符是 "https://"，protocol 为 https，其余的 protocol 为 http
    if url[0:8] == 'https://':
        protocol = 'https'
    else:
        protocol = 'http'
    return protocol


# 2
# 补全函数
def host_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表主机的字符串, 比如 'g.cn'
    '''
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
    '''
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
    '''
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
    '''
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
    '''
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
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    protocol = protocol_of_url(url)
    host = host_of_url(url)
    port = port_of_url(url)
    path = path_of_url(url)
    return protocol, host, port, path


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    # 解析 url
    protocol, host, port, path = parsed_url(url)
    # print(protocol, host, port, path)
    # 判断协议类型
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
    else:
        s = socket.socket()

    # 建立连接
    s.connect((host, port))

    # 构造请求
    http_request = 'GET {} HTTP/1.1\r\n\r\nhost:{}\r\n\r\n'.format(path, host)
    request = http_request.encode()

    # 发送请求
    s.send(request)

    # 接收响应，一次接收1025字节，直到接收完
    # 每次判断 recv 的长度是否等于1025，如果不足，那么说明已经接收完了
    r = b''
    buffer_size = 1025
    while True:
        response = s.recv(buffer_size)
        if len(response) == 0:
            break
        r = r + response

    # s.close() 客户端不需要断开连接，服务器需要断开连接
    return r


# 使用
def main():
    url = 'http://movie.douban.com/top250'
    r = get(url)
    print(r)


if __name__ == '__main__':
    main()
    assert protocol_of_url('g.cn') == 'http', 'bug'
    assert protocol_of_url('g.cn:3000') == 'http', 'bug'
    assert protocol_of_url('http://g.cn') == 'http', 'bug'
    assert protocol_of_url('https://g.cn') == 'https', 'bug'
    assert protocol_of_url('http://g.cn/') == 'http', 'bug'
    assert host_of_url('g.cn') == 'g.cn', 'bug'
    assert host_of_url('g.cn:3000') == 'g.cn', 'bug'
    assert host_of_url('http://g.cn') == 'g.cn', 'bug'
    assert host_of_url('https://g.cn') == 'g.cn', 'bug'
    assert host_of_url('http://g.cn/') == 'g.cn', 'bug'
    assert port_of_url('g.cn') == 80, 'bug'
    assert port_of_url('g.cn:3000') == 3000, 'bug'
    assert port_of_url('http://g.cn') == 80, 'bug'
    assert port_of_url('https://g.cn') == 443, 'bug'
    assert port_of_url('http://g.cn/') == 80, 'bug'
    assert path_of_url('g.cn') == '/', 'bug'
    assert path_of_url('g.cn:3000') == '/', 'bug'
    assert path_of_url('http://g.cn') == '/', 'bug'
    assert path_of_url('https://g.cn') == '/', 'bug'
    assert path_of_url('http://g.cn/abc') == '/abc', 'bug'
