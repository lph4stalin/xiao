"""用来存储后端所需的组件函数"""
import socket
import ssl


# 函数1：解析 url。返回值：protocol、host、port、path
def parsed_url(url):
        default_port = {
        'http' : 80,
        'https' : 443,
        }
        # 先处理 protocol
        if url.find('://') == -1:
            u = url
            protocol = 'http'
        # 否则需要先切割掉 '://' 之前的内容
        else:
            u = url.split('://')[1]
            protocol = url.split('://')[0]

        # 再处理 path
        if u.find('/') == -1:
            path = '/'
            u = u
        else:
            path = '/' + u.split('/', 1)[1]
            u = u.split('/', 1)[0]

        # 再处理 port，切除 port 后，剩余的是 host
        if ':' not in u:
            port = default_port[protocol]
            host = u
        else:
            port = int(u.split(':')[1])
            host = u.split(':')[0]
        return protocol, host, port, path


# 函数2：生成 socket 实例。根据不同的 protocol，返回对应的 socket 实例。
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


# 函数3：接收返回的数据。无限循环，直到接收完毕
def response_by_socket(s):
    r = b''
    buffer_size = 1024
    while True:
        response = s.recv(buffer_size)
        # 每次判断 recv 的长度是否等于0，如果等于0，那么说明已经接收完了
        if len(response) == 0:
            break
        r += response
    return r


# 函数4：解析响应，把 response 拆分成 状态码(int)、Headers(字典)、Body(str)
# 状态码：第 1 个 \r\n 的第 1 个空格的第 2 个。
# Hearers：第 1 个 \r\n 和第 1 个 \r\n\r\n 之间的内容，还需要转换成字典格式
# Body：第 1 个 \r\n\r\n 之后的内容
def parsed_response(response):
    s = response.split('\r\n', 1)[0]
    # 解析出状态码
    status_code = s.split(' ')[1]
    # 解析出 headers
    h = response.split('\r\n', 1)[1]
    # 解析出 body
    body = h.split('\r\n\r\n', 1)[1]
    # 把 headers 转换成字典格式
    h = h.split('\r\n\r\n', 1)[0]
    headers = {}
    for i in h.split('\r\n'):
        headers[i.split(': ', 1)[0]] = i.split(': ', 1)[1]
    return status_code, headers, body

# 测试函数
def test(f, a, b):
    assert f(a) == b, "没有通过测试"


# 主函数，所有的函数调用都在这里进行
def main():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
        'Content-Type: text/html\r\n' \
        'Location: https://movie.douban.com/top250\r\n' \
        'Content-Length: 178\r\n\r\n' \
        'test body'
    url_1 = 'www.douban.com/movie/top250'
    url_2 = 'https://www.douban.com/movie/top250'
    url_3 = 'http://www.douban.com'
    url_4 = 'www.douban.com:80/'
    test(parsed_url, url_1, ('http', 'www.douban.com', 80, '/movie/top250'))
    parsed_response(response)

if __name__ == '__main__':
    main()
