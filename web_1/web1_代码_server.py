"""
简单的服务器代码（握手-通信）
功能：接收请求，返回响应
1.先告诉操作系统，我要访问网络
2.持续监听，是否有客户端访问
3.客户端连接过来的时候可以获得一个连接对象（三次握手？）
4.收到客户端发来的请求
5.解析请求（这里省略了，无论什么请求返回的都是同一个页面）（但是我可以事先定义好可访问的地址，对没有定义的返回404 Error）
6.响应（响应的内容应是预先定义好的，客户端要什么我就返回什么）
7.发送
8.关闭连接（握手完毕）
"""

import socket


# 服务器的 host 设置为空字符串，表示接受任意 ip 地址的连接
# post 是端口，这里设置为 2000，随便选的一个数字
# 127.0.0.1 是本机 ip
# 1024 以下端口为系统保留，需要管理员权限
host = ''
port = 2000

# s 是一个 socket 实例
s = socket.socket()
# s.bind 用于绑定
# 注意 bind 的参数是一个 tuple
# 这里是告诉操作系统，我接收的 host 和 我的 port
s.bind((host, port))

# 用一个无限循环来处理请求
while True:
    # 套路，先要 s.listen 开始监听
    # 参数 5 的含义不必关心
    s.listen(5)
    # 当有客户端连接过来的时候， s.accept 函数会返回 2 个值
    # 分别是 连接 和 客户端 ip 地址
    connection, address = s.accept()

    # recv 可以接收客户端发过来的数据
    # 参数是要接收的字节数
    # 返回值是一个 bytes 类型
    requsst = connection.recv(1025)

    # 用 b'' 表示这是一个 bytes 对象
    response = b'HTTP/1.1 233 OK\r\n\r\n<h1>Hello World!</h1>'
    # 用 sendall 发送给客户端
    connection.sendall(response)
    # 发送完毕后，关闭本次连接
    connection.close()
