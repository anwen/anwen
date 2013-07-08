# -*- coding: utf-8-*-


def md5_file(name):
    from hashlib import md5
    m = md5()
    with open(name, 'rb') as a_file:
        m.update(a_file.read())
    return m.hexdigest()
