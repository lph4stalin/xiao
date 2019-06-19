"""
这里存放不同的 route 的 response
所有的函数都接收 Request 的实例
返回 messagess、index、login、register四个网页
返回 图片
接收 POST 的信息，根据 query 修改页面内容
"""
import sys
sys.path.append('../')
from Model import *


def route(request):
    """
    输入：Request 的实例
    输出：返回的函数
    """
    # 请求的 route 映射到 response 里要返回的函数
    f = route_dict_func.get(request.route, error)
    print('3.1')
    return f(request)


# ————————————————————————————————————————————————
# 这一块是拼装 header 和 body 的组件函数
def templates(request):
    """
    response 的组件函数，返回被 open 的网页内容，作为 response 的 body
    """
    path = 'View/' + route_dict_par.get(request.route, '')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def headers_of_page():
    """
    标准的 page 的 Header
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    return header


def page(request):
    """
    没有交互的网页的 response
    """
    header = headers_of_page()
    body = templates(request)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def pic(request):
    """
    图片的 response
    例：接收"/static/doge.gif"，返回img
    """
    path = 'View/' + route_dict_par.get(request.route, '')
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
    return img


def error(request):
    """
    找不到路径的 response
    """
    response = b'HTTP/1.1 404 Error\r\n\r\n<h1>404 Not Found</h1>'
    return response
# ——————————————————————————————————————————————————


def route_login(request):
    """
    login 的函数，传入 POST 的 Body，返回页面
    会把原始页面中{{result}}部分替换为自定义内容
    """
    if request.method == 'POST':
        # 把 body 解析成字典
        form = request.form()
        u = User(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    r = page(request).decode(encoding='utf-8')
    r = r.replace('{{result}}', result)
    return r.encode(encoding='utf-8')


def route_register(request):
    print('3.2')
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User(form)
        if not u.validate_register_1():
            result = '用户名或者密码长度必须大于2'
        elif u.validate_register_2():
            print('daolu2')
            result = '用户名已存在'
        else:
            print('daolu3')
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(form)
    else:
        result = ''
    print('3.3')
    r = page(request).decode(encoding='utf-8')
    r = r.replace('{{result}}', result)
    return r.encode(encoding='utf-8')


def route_messages(request):
    messages_list = Message.all()
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        messages_list.append(msg)
        msg.save()
        # 应该在这里保存 messages_list
    r = page(request).decode(encoding='utf-8')
    # '#'.join(['a', 'b', 'c']) 的结果是 'a#b#c'
    msgs = '<br>'.join([str(m) for m in messages_list])
    r = r.replace('{{messagess}}', msgs)
    return r.encode(encoding='utf-8')
# ——————————————————————————————————————————————————


# 每个路径对应的返回函数
route_dict_func = {
    '/': page,
    '/static/doge.gif': pic,
    '/static/doge1.jpg': pic,
    '/static/doge2.gif': pic,
    '/messages': route_messages,
    '/register': route_register,
    '/login': route_login,
}


# 每个路径对应的参数
route_dict_par = {
    '/': 'index.html',
    '/static/doge.gif': 'static/doge.gif',
    '/static/doge1.jpg': 'static/doge1.jpg',
    '/static/doge2.gif': 'static/doge2.gif',
    '/messages': 'messages.html',
    '/register': 'register.html',
    '/login': 'login.html',
}

# a = User.all()
# for i in a:
#     print(type(i))
# b = User({'username':1,'password':2})
# b.all()
# b.save()
