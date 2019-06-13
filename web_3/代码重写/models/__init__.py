import json


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    json 的形式类似字典，但是格式是字符串，'{'a':'b','c':'d'}'
    json.dumps() 将 Python 对象编码成 JSON 字符串，dict to str
    """
    # json 是一个序列化/反序列化(上课会讲这两个名词) list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    # s 是字符串, data 是dict
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        print('save', path, s, data)
        print(type(s), type(data))
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    json.loads() 用于解码 JSON 数据。该函数返回 Python 字段的数据类型，str to dict
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        print('load', s)
        return json.loads(s)


# Model 是用于存储数据的基类
class Model(object):
    # @classmethod 说明这是一个 类方法
    # 类方法的调用方式是  类名.类方法()
    # 可以不实例化直接用类的方法
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是 class
        # 所以我们可以得到 class 的名字
        classname = cls.__name__
        # 在类名.txt 里面存储了数据(例如，User.txt)
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        path 是文件地址
        models 是读取的文件内容
        ms 是
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        print(ms)
        return ms

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        print('models', models)
        models.append(self)
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        这是一个 魔法函数
        不明白就看书或者 搜
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v)
                      for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


# print(Model.db_path()) → Model.txt
save({'a': 1, 'b': 2, 'c': 3}, '../db/Model.txt')
Model.all()


# 以下两个类用于实际的数据处理
# 因为继承了 Model
# 所以可以直接 save load


class User(Model):
    def new(self, form):
        # form 是个字典
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        # 返回值是 True 或者 False
        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        # 返回值是 True 或者 False
        return len(self.username) > 2 and len(self.password) > 2


# 定义一个 class 用于保存 message
class Message(Model):
    def new(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')
