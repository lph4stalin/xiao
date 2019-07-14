import sys
sys.path.append('../')
from Model import *

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


def route_login(request):
    """
    login 的函数，传入 POST 的 Body，返回页面
    会把原始页面中{{result}}部分替换为自定义内容
    """
    r = page(request).decode(encoding='utf-8')
    if request.method == 'POST':
        form = request.form()
        # 把 body 解析成字典
        u = User(form)

        if u.validate_login():
            result = '登录成功'
            cookie = 'Set-Cookie: status=Login, username={}'.format(form.get('username', ''))
            r = r.replace('Set-Cookie: status=Not Login', cookie)
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    r = r.replace('{{result}}', result)
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



def route_todo(request):
    """
    检查登录情况，如果未登录，重定向；如果登录了，就返回 todo_index.html
    :param request:
    :return: 响应报文
    """
    print('检查登录', check_login(request))
    if check_login(request):
        return redirect('http://localhost:2000/login')
    else:
        todos_list = Todo.all()
        t_list = []
        for t in todos_list:
            if t.get('username', '') == request.username:
                todo = '{}: {}'.format(t.get('id', ''), t.get('title', ''))
                t_list.append(todo)
        todos = '<br>'.join(t_list)
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
    print('Todo_list',todo_list)
    form = request.form()
    todo = Todo(form, request.cookie)
    print('todo', todo)
    this_user_todos = []
    for i in todo_list:
        print('hahah', i)
        if i['username'] == request.username:
            this_user_todos.append(i)
    print(todo.id)
    todo.id = len(this_user_todos) + 1
    todo_list.append(todo)
    todo.save()
    return redirect('http://localhost:2000/todo_index')
