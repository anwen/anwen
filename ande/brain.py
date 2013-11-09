# -*- coding:utf-8 -*-

from . import ego
from . import ip
from . import query
from .skills import search
from db import Ande



def get_andesay(usersay, userip, userlang, user_id, method):
    doc = {
        'user_id': user_id,
        'user_ip': userip,
        'usersay': usersay,
        'usersay_low': usersay.lower(),
    }
    # usersay_en = translate(usersay, '', 'en')
    # is_firstmeet = query.is_firstmeet(userip, user_id)
    ego_info = ego.find_ego(usersay)
    ip_info = ip.find_ip(doc)
    first = query.first(usersay, userip, user_id, method)
    hello = query.hello(usersay)
    song = query.song(usersay)
    trans = query.trans(usersay, userlang)
    clock = query.clock(usersay)
    get_memo = query.search_memo(usersay, userip)
    #search = search.search(usersay)

    andesay = ''.join([
        ego_info, ip_info, get_memo, first, hello, song, trans, clock,
        #search,
    ])
    doc['andesay'] = andesay
    doc.pop('usersay_low')
    Ande.new(doc)
    #return doc
    return andesay
