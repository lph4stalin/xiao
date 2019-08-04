"""
这里存放不同的 route 的 response
所有的函数都接收 Request 的实例
返回 messagess、index、login、register四个网页
返回 图片
接收 POST 的信息，根据 query 修改页面内容
"""
from Model import *
# 同一 package 中同级相互引用，在前面加 .
from .routes_login import *
from .routes_message import *
from .routes_register import *
from .routes_profile import *
from .routes_todo import *
from .utils import *


def route(request):
    """
    输入：Request 的实例
    输出：返回的函数
    """
    # 请求的 route 映射到 response 里要返回的函数
    f = route_dict_func.get(request.route, error)
    return f(request)



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
    '/todo_index': index,
    '/todo/add': add,
}


