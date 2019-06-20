"""
一、提问的智慧
提问之前要把思路整理好，并给出问题的必要条件。
目标：提出一个帮你解决问题的问题。

一、url
route: /search?a=b&c=d#anchor
path: /search
query: ?a=b&c=d
anchor: #anchor


二、代码解析
1.服务器运行的主程序：监听 → 接收请求 → 解析请求 → 生成响应报文 → 发送响应报文 → 关闭连接
2.解析请求：把请求拆分成 method、route、query 和 body 4 部分
3.生成响应报文：
① 根据 route 返回对应的页面
② 根据 method、query 个性化返回报文
如果请求是 POST，那么请求的 Body 里就会包含 query。所以需要解析 body。形如"name=xiao&password=123"，那么我们需要把它解析成"name=xiao"和"password=123"，然后分别去数据库中验证，根据验证结果返回不同的页面。


三、MVC 设计模式
将一个程序分为三个部分
Model       数据
View        显示
Controller  控制器
V 是前端显示的内容
M 是后端存储的数据
C 沟通 M 和 V

四、代码重写
功能：①能够根据地址返回 html_basic、index、login、register四个网页
②对 login 和 register，接收到的对话框中的内容，要能够进行验证（收到→解析→验证→返回）

代码：① server 是服务器运行的模块
② routes 是网页地址和响应函数的映射
③ db 是服务器存储数据的文件夹
④ models是服务器存储响应函数的模块


五、package
package里有一个__in__.py文件的文件夹，import包等价于import __init__.py 的内容。package里可以放其他的py文件，可以通过点记法来引用。

六、Python知识
self.__class__ 获取当前实例对应的类
self.__class__.__name__ 获取当前实例对应的类的类名

self.__dict__
以字典的格式获取类/实例下所有属性(实例只读取__init__中的属性，类会读取所有class 下的对象，包括属性和方法)
父类和子类各有其__dict__，不会影响

class Parent(object):
    # 类的属性
    a = 0
    b = 1

    # 类的方法
    def __init__(self):
        # __init__方法下保存的是实例的属性
        self.a = 2
        self.b = 3

    def p_test(self):
        pass


class Child(Parent):
    a = 4
    b = 5

    def __init__(self):
        super(Child, self).__init__()
        # self.a = 6
        # self.b = 7

    def c_test(self):
        pass

    def p_test(self):
        pass


p = Parent()
c = Child()
print(Parent.__dict__)
print(Child.__dict__)
print(p.__dict__)
print(c.__dict__)

{'__module__': '__main__', 'a': 0, 'b': 1, '__init__': <function Parent.__init__ at 0x00000263D6767AE8>, 'p_test': <function Parent.p_test at 0x00000263D6767A60>, '__dict__': <attribute '__dict__' of 'Parent' objects>, '__weakref__': <attribute '__weakref__' of 'Parent' objects>, '__doc__': None}
{'__module__': '__main__', 'a': 4, 'b': 5, '__init__': <function Child.__init__ at 0x00000263D677C1E0>, 'c_test': <function Child.c_test at 0x00000263D677C268>, 'p_test': <function Child.p_test at 0x00000263D677C2F0>, '__doc__': None}
{'a': 2, 'b': 3}
{'a': 2, 'b': 3}

七、__repr__
print出来的内容会是__repr__的返回值
"""
