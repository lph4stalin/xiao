from Model import *
from .utils import *
import sys
sys.path.append('../')
import Controller.session

def route_login(request):
    """
    login 的函数，传入 POST 的 Body，返回页面
    会把原始页面中{{result}}部分替换为自定义内容
    """
    r = page(request).decode(encoding='utf-8')
    if request.method == 'POST':
         # 把 body 解析成字典
        form = request.form(request.body)
        # 生成 User 类的一个实例
        u = User(form)
        if u.validate_login():
            result = '登录成功'
            session = Controller.session.make_session(20)
            u.session = session
            print('我是当前的session', u.username, u.session)
            cookie = 'Set-Cookie: status=Login, session={}'.format(session)
            r = r.replace('Set-Cookie: status=Not Login', cookie)
            username = current_user(request)
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    r = r.replace('{{result}}', result)
    r = r.replace('{{username}}', username)
    return r.encode(encoding='utf-8')
