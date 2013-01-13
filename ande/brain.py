# -*- coding:utf-8 -*-
"""
the methons we use may seem fool temporarily, we will make them better
"""

import query
import ego
from markdown2 import markdown
from db import Ande
from tools.bingtrans import translate
# from tools.fenci import fenci
# from tools.xpinyin import Pinyin


def get_ande_ip():
    pass


def get_andesay(usersay, userip, userlang, user_id, method):

    # is_cn = is_cn(usersay)
    # is_en = is_en(usersay)
    # usersay_fenci = fenci(usersay)
    # usersay_fencij = json.loads(usersay_fenci)  # ['words'][0]['attr']
    # usersay_pinyin = Pinyin().get_pinyin(usersay)
    # andeip = get_ande_ip()

    usersay_en = translate(usersay, '', 'en')
    is_firstmeet = query.is_firstmeet(userip, user_id)
    first = query.first(usersay, userip, user_id, method)
    hello = query.hello(usersay)
    weather = query.weather(usersay, userip)
    song = query.song(usersay)
    trans = query.trans(usersay, userlang)
    clock = query.clock(usersay)
    wiki = query.wiki(usersay)
    memo_last = query.memo_last(usersay, userip)
    get_ego = ego.get_ego(usersay)

    # andesay = '%s\n%s\n%s\n%s' % (hello, weather, song, trans)
    andesay = ''.join([
        first, hello, weather, song, trans, clock, wiki, memo_last, get_ego
    ])

    andethink = ''.join([
        'ande-think-trace:',
        '\n\nusersay:', usersay,
        '\n\nuserip:', userip,
        '\n\nuserlang:', userlang,
        '\n\nuserid:', str(user_id),
        '\n\nis_firstmeet?:', is_firstmeet,
        '\n\nusersay_en?:', usersay_en,
    ])

    doc = {
        'user_id': user_id,
        'user_ip': userip,
        'usersay': usersay,
        'andesay': andesay,
    }
    Ande.new(doc)

    return markdown(andesay), markdown(andethink)
