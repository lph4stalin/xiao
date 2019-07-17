from Model import *

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
