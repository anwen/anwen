# -*- coding:utf-8 -*-

from markdown2 import markdown
import query
import ego
import tools
from db import Ande


tool_modules = []
for tool_name in tools.__all__:
    __import__('ande.tools.%s' % tool_name)
    tool_modules.append(getattr(tools, tool_name))


def by_tools(data):
    for tool_module in tool_modules:
        try:
            if tool_module.test(data):
                return tool_module.handle(data)
        except:
            continue
    return ''


def get_andesay(usersay, userip, userlang, user_id, method):
    data = {
        'usersay': usersay,
        'userip': userip,
        'userlang': userlang,
        'user_id': user_id,
        'method': method,
    }

    # usersay_en = translate(usersay, '', 'en')
    # is_firstmeet = query.is_firstmeet(userip, user_id)
    first = query.first(usersay, userip, user_id, method)
    hello = query.hello(usersay)
    song = query.song(usersay)
    trans = query.trans(usersay, userlang)
    clock = query.clock(usersay)

    get_tools = by_tools(data)
    get_memo = query.search_memo(usersay, userip)
    get_ego = ego.find_ego(usersay)

    andesay = ''.join([
        get_tools, get_memo, get_ego, first, hello, song, trans, clock,
    ])

    doc = {
        'user_id': user_id,
        'user_ip': userip,
        'usersay': usersay,
        'andesay': andesay,
    }

    Ande.new(doc)

    return markdown(andesay), ''
