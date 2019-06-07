"""
一、预习
server.py 思路

建立 host 和端口
监听请求
接受请求
解析请求：method、path、query、body
目前需要处理的场景有：GET + path & query、 POST + path + body(内容是query)
处理请求
获取路由字典
path和字典处理请求并获得返回页面
返回响应内容
发送响应内容
关闭连接

url中能够使用的字符是有限的，所以有的字符需要转码，比如'空格'转码为'%20'
"""
