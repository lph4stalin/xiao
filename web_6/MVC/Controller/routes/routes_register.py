from Model import *


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
