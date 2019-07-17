from Model import *
from .utils import *


def index(request):
    """
    检查登录情况，如果未登录，重定向；如果登录了，就返回 todo_index.html
    :param request:
    :return: 响应报文
    """
    print('检查登录', check_login(request))
    if check_login(request):
        from_url = ''
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


def add(request):
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


def update(request):
    pass


def delete_todo(request):
    pass
