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


def headers_of_page(request):
    """
    标准的 page 的 Header
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\nSet-Cookie: {}\r\n'.format(request.cookie)
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
     return request.cookie == 'status=Not Login'
# ——————————————————————————————————————————————————


def route_login(request):
    """
    login 的函数，传入 POST 的 Body，返回页面
    会把原始页面中{{result}}部分替换为自定义内容
    """
    if request.method == 'POST':
        form = request.form()
        # 把 body 解析成字典
        u = User(form)
        if u.validate_login():
            result = '登录成功'
            cookie = 'Set-Cookie: status=Login, username={}'.format(form.get('username', ''))
        else:
            result = '用户名或者密码错误'
            cookie = 'Set-Cookie: status=Not Login'
    else:
        result = ''
        cookie = 'Set-Cookie: status=Not Login'
    r = page(request).decode(encoding='utf-8')
    r = r.replace('{{result}}', result)
    r = r.replace('Set-Cookie: status=Not Login', cookie)
    return r.encode(encoding='utf-8')


def route_register(request):
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User(form)
        if not u.validate_register_1():
            result = '用户名或者密码长度必须大于2'
        elif u.validate_register_2():
            result = '用户名已存在'
        else:
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(form)
    else:
        result = ''
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


def route_profile(request):
    """
    检查 cookie，如果登录了，则返回username，password 和 note
    如果没有登录，则返回 302 重定向
    """
    if check_login(request):
        return redirect('http://localhost:2000/login')
    else:
        path = User.db_path()
        users = load(path)
        username = request.cookie.split('username=')[1]

        for user in users:
            if user['username'] == username:
                password = user['password']
                note = user.get('note', '')
                result = 'username:{}<br>password:{}<br>note:{}'.format(username, password, note)
                r = page(request).decode(encoding='utf-8')
                r = r.replace('{{result}}', result)
                return r.encode(encoding='utf-8')
        return redirect('http://localhost:2000/login')


def route_todo(request):
    """
    检查登录情况，如果未登录，重定向；如果登录了，就返回 todo_index.html
    :param request:
    :return: 响应报文
    """
    if check_login(request):
        return redirect('http://localhost:2000/login')
    else:
        print('abcosjk', User.all())
        todos_list = Todo.all()
        print(todos_list)
        t_list = []
        for t in todos_list:
            print('1', t.get('username', ''))
            print('2', request.cookie.split('username=')[1])
            if t.get('username', '') == request.cookie.split('username=')[1]:
                todo = '{}: {}'.format(t.get('id', ''), t.get('title', ''))
                t_list.append(todo)
                print(t_list)
        todos = '<br>'.join(t_list)
        print('todos', todos)
        r = page(request).decode(encoding='utf-8')
        r = r.replace('{{todos}}', todos)
        return r.encode(encoding='utf-8')


def route_todo_add(request):
    """
    把 add form 里的内容 POST 给服务器，返回 todo_index
    :param request:
    :return:
    """
    todo_list = Todo.all()
    print('todo_list', todo_list)
    form = request.form
    todo = Todo(form, request.cookie)
    print('todo', todo)
    todo_list.append(todo)
    todo.save()
    return redirect('http://localhost:2000/todo_index')
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


