from Model import *
from .utils import *
import sys
sys.path.append('../')
import session

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
