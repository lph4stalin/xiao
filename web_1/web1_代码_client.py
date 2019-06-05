import socket
import ssl


# 主机(域名或者ip)和端口
host = 'www.100tal.com'
port = 80
protocol = 'http' # 这里我直接假设了 protocol 是 http，但实际上应当从 host 中解析而得到。

# socket 是操作系统用来进行网络通信的底层方案（简单理解就是操作系统提供了socket功能，Python又调用了socket）

# 创建一个 socket 对象，参数socket.AF_INET 表示是 ipv4 协议
# 参数socket.SOCK_STREAM表示是 tcp 协议
# 根据通信协议是 http 还是 https 来判断使用哪个 socket 对象

if protocol == 'http':
    s = socket.socket() # 这里第一个socket是socket库，第二个是socket()函数
else:
    s = ssl.wrap_socket(socket.socket()) # 如果是 https 协议需要用这个对象

# 用 connect 函数连接上主机，参数是一个 tuple
s.connect((host, port))


# 连接上后，可以通过这个函数得到本机的 ip 和端口
ip, port = s.getsockname()
print('本机 ip 和 port {} {}'.format(ip, port))

# 构造一个 http 请求
http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)

# 发送 http 请求给服务器
# send 函数只接受 bytes 作为参数
# str.encode 把 str 转换为 bytes，编码是 utf-8
request = http_request.encode('utf-8')
# request = b'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
print('请求', request)
s.send(request)

# 接受服务器响应数据
# 参数是长度
response = s.recv(1025)

# 输出响应数据，bytes 类型
print('响应', response)
# 转成 str 再输出
print('响应的 str 格式', response.decode('utf-8'))
