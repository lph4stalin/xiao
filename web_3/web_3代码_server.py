import socket
import urllib.parse


# 定义一个 class 用来保存请求的数据


# 定义一个接收全部请求的函数
def request_from_client(connection):
    r = b''
    buffer_size = 1025
    while True:
        request = connection.recv(buffer_size)
        # 每次判断 recv 的长度是否等于0，如果等于0，那么说明已经接收完了
        if len(request) == 0:
            break
        r += request
    return r


# 服务器主程序
def run(host='', port=3000):
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        # 用无限循环来处理请求
        while True:
            # 监听
            s.listen(5)
            connection, address = s.accept()
            r = request_from_client(connection)
            r.decode('utf-8')
            print(r)
            print(r.split())
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里判断一下防止程序崩溃
            # continue 语句会跳过循环剩下的语句，直接执行下一个循环
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            print(path)


run()
