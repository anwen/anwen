# -*- coding:utf-8 -*-

from tools.fenci import fenci
from tools.xpinyin import Pinyin
import query
from markdown2 import markdown
from db import Ande


def is_cn(i):
    return 0x4e00 <= ord(i) < 0x9fa6


def is_en(i):
    return ord(i) < 128


def is_en2(i):
    c = i.encode('utf-8')
    return True if len(c) == len(i) else False


def get_ande_ip():
    pass


def get_andesay(usersay, userip, userlang, user_id, method):

    # is_cn = is_cn(usersay)
    # is_en = is_en(usersay)
    # usersay_fenci = fenci(usersay)
    # usersay_fencij = json.loads(usersay_fenci)  # ['words'][0]['attr']
    # usersay_pinyin = Pinyin().get_pinyin(usersay)
    # andeip = get_ande_ip()
    is_firstmeet = query.is_firstmeet(userip, user_id)
    hello = query.hello(usersay)
    weather = query.weather(usersay, userip)
    song = query.song(usersay)
    trans = query.trans(usersay)
    clock = query.clock(usersay)

    # andesay = '%s\n%s\n%s\n%s' % (hello, weather, song, trans)
    andesay = ''.join([
        hello, weather, song, trans, clock,
    ])

    andethink = ''.join([
        'ande-think-trace:',
        '\n\nusersay:', usersay,
        '\n\nuserip:', userip,
        '\n\nuserlang:', userlang,
        '\n\nuserid:', str(user_id),
        '\n\nmethod:', method,
        '\n\nis-firstmeet?:', is_firstmeet,
    ])

    doc = {
        'user_id': user_id,
        'user_ip': userip,
        'usersay': usersay,
        'andesay': andesay,
    }
    Ande.new(doc)

    return markdown(andesay), markdown(andethink)
