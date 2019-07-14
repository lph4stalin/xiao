"""
这里存放不同的 route 的 response
所有的函数都接收 Request 的实例
返回 messagess、index、login、register四个网页
返回 图片
接收 POST 的信息，根据 query 修改页面内容
"""
from Model import *
import routes_function


def route(request):
    """
    输入：Request 的实例
    输出：返回的函数
    """
    # 请求的 route 映射到 response 里要返回的函数
    f = route_dict_func.get(request.route, error)
    return f(request)


# ————————————————————————————————————————————————
# 这一块是拼装 header 和 body 的组件函数
def templates(request):
    """
    response 的组件函数，返回被 open 的网页内容，作为 response 的 body
    """
    path = 'View/templates/' + route_dict_par.get(request.route, '')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def headers_of_page(request):
    """
    标准的 page 的 Header
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\nSet-Cookie: {}\r\n'.format(request.cookie)
    print('cookie', request.cookie)
    return header


def page(request):
    """
    没有交互的网页的 response
    """
    header = headers_of_page(request)
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

def redirect(location):
    """
    重定向的response
    传入重定向的 location
    """
    # bytes 不能用 format
    response = 'HTTP/1.1 302 Temporarily Moved\r\nLocation: {}\r\n\r\n'.format(location)
    response = response.encode(encoding='utf-8')
    return response


def check_login(request):
    """
    :param request 请求信息
    :return: True 未登录；False 登录
    """
    return request.cookie == 'status=Not Login'
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
    '/profile': route_profile,
    '/todo_index': route_todo,
    '/todo/add': route_todo_add,
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
    '/profile': 'profile.html',
    '/todo_index': 'todo_index.html',
    '/todo/add': '',
}
