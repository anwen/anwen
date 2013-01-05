# -*- coding:utf-8 -*-

import string
from tool.fenci import fenci
from tool.xpinyin import Pinyin
import say


def is_cn_char(i):
    return 0x4e00 <= ord(i) < 0x9fa6


def is_cn_or_en(i):
    o = ord(i)
    return o < 128 or 0x4e00 <= o < 0x9fa6


def is_cn(i):
    is_cn = 'is_cn'
    c = i.encode('utf-8')
    if len(c) == len(i):
        is_cn = 'not_cn'
    return is_cn


def is_ascii(i):
    is_ascii = 'is_ascii'
    for c in i:
        if c not in string.ascii_letters:
            is_ascii = 'not_ascii'
            return is_ascii
    return is_ascii


class AndeSay(object):

    def get_andesay(self, usersay, userip):
        andesay = ''
        andesay += '<br/>'
        p = Pinyin()
        userfenci = fenci(usersay)
        # userfenci = json.loads(userfenci)
        # city = p.get_pinyin(self.city)

        andesay += say.weather(usersay, userip)
        andesay += say.hello(usersay)
        andesay += say.song(usersay)

        andethink = ''
        andethink += '<br/>ande-think-trace, just for study'
        # andethink += '<br/>ande ip:' + get_ande_ip()
        andethink += '<br/>' + is_cn(usersay)
        andethink += '<br/>' + is_ascii(usersay)
        andethink += '<br/>' + userfenci
        andethink += '<br/>' + p.get_pinyin(usersay)
        #status = userfenci['words'][0]['attr']

        return andesay, andethink
