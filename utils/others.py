# -*- coding: utf-8-*-

from hashlib import md5


def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')  # 需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()
