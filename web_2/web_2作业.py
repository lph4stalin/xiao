# 2017/02/18
# 作业 2
# ========
#
#
# 请直接在我的代码中更改/添加, 不要新建别的文件
import sys
sys.path.append("..")
from urlfunc import *


# 定义我们的 log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    q = '?'
    for k, v in query.items():
        q = q + k + '=' + str(v) + '&'
    q = q[0:-1]
    q = path + q
    return q


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典
def get(url, query={}):
    # 解析 url
    protocol, host, port, path = parsed_url(url)
    # 建立 socket 实例
    s = socket_by_protocol(protocol)
    # 建立连接
    s.connect((host, port))
    # 拼接 route
    route = path_with_query(path, query)
    # 构造请求
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: Close\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\n\r\n'.format(
        route, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    # 接收响应，一次接收1025字节，直到接收完
    response = response_by_socket(s)
    response = response.decode(encoding)
    status_code, headers, body = parsed_response(response)
    if status_code == '301':
        return get(headers['Location'])
    return status_code, headers, body
print(get('http://movie.douban.com/top250'))

# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    h = ''
    for k, v in headers.items():
        h = h + k + ': ' + str(v) + '\r\n'
    return h


# 作业 2.4
#
# 为作业 2.3 写测试
def test_header_from_dict():
    headers_str = 'Content-Type: text/html\r\nContent-Length: 127\r\n'
    headers = {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    assert header_from_dict(headers) == headers_str, "测试不通过"


# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client_ssl.py 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""


# 作业 2.6
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""
