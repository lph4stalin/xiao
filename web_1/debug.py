记录一次debug
bug：在接收完请求后，需要等待1-2分钟才返回接收的全部内容
原因：请求中的Connection默认值为Keep-Alive，所以在全部接收之后，不会马上断开连接，而是会等待连接超时后才断开。

产生bug的请求报文：
request = 'GET {} HTTP/1.1\r\nhost:{}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\n\r\n'.format(
    path, host)

修改后的请求报文：
request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: Close\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\n\r\n'.format(
    path, host)


如何判断报文是否发送完毕？
1.每次发送请求后都断开连接；如果返回的报文长度为0，那么就判断发送完毕
2.通过content-length的内容来判断。但是经过尝试后发现，报文的长度和content-length给出的长度不一致！
