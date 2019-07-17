# 对给定的用户名，每次登陆时返回一个 session。
# session 是一个随机字符串。暂定 20 位，由数字和字符组成
import random


def make_session(num):
    session = ''
    for i in range(num):
        rand_char = random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
        rand_int = random.randint(1,9)
        rand_dict = {
        1: rand_char,
        2: rand_int,
        }
        i = rand_dict[random.randint(1,2)]
        session += str(i)
    return session
