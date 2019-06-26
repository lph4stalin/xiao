"""
这里存放不同的 route 的 response
接收 route
返回 html_basic、index、login、register四个网页
返回 图片
接收 POST 的信息，根据 query 修改页面内容
"""
from models import *
from models.user import *


# 以下所有函数的输入内容都是 request，可以自行从 request 中获取需要的字段
def route(request):
    # 请求的 route 映射到 response 里要返回的函数
    print('1')
    response = {
        '/': page,
        '/static/doge.gif': pic,
        '/static/doge1.jpg': pic,
        '/static/doge2.gif': pic,
        '/html_basic': page,
        '/register': route_register,
        '/login': page,
    }
    # 调用的函数
    r = response.get(request.route, error)
    print('2')
    return r(request)


# 打开网页所在地址的函数
def templates(request):
    route = route_dict.get(request.route, '')
    path = 'templates/' + route
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# 生成模板报文 header 函数
def headers_of_page():
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    return header


def page(request):
    """
    :param route: 输入路径（字符串格式）
    :return: header 和 body 的报文（bytes 格式）
    """
    header = headers_of_page()
    body = templates(request)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def pic(request):
    """
    例：接收"/static/doge.gif"，返回img
    """
    path = route_dict.get(request.route, '')
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
    return img


# error 的 response
def error(request):
    response = b'HTTP/1.1 404 Error\r\n\r\n<h1>404 Not Found</h1>'
    return response


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        # 把字典作为 User 类的参数
        u = User.new(form)
        print('u1', u)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    print('result', result)
    body = templates(request)
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# login 的函数，传入 POST 的 Body，返回页面
# 会把原始页面中{{result}}部分替换为自定义内容
def route_login(request):
    header = headers_of_page()
    if request.method == 'POST':
        # 把 body 解析成字典
        # form 是一个字典 {username: 'sss', password: '123'}
        form = request.form()
        u = User.new(form)
        print('u', u)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = templates(request)
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post', form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template(request)
    # '#'.join(['a', 'b', 'c']) 的结果是 'a#b#c'
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': 'index.html',
    '/static/doge.gif': 'static/doge.gif',
    '/static/doge1.jpg': 'static/doge1.jpg',
    '/static/doge2.gif': 'static/doge2.gif',
    '/html_basic': 'html_basic.html',
    '/register': 'register.html',
    '/login': 'login.html',
}
