# -*- coding:utf-8 -*-


def get_ego(usersay):
    ego_keys = ['you', 'ande', u'你', u'安德']
    get_ego = ''
    for i in ego_keys:
        if i in usersay:
            if 'who are' in usersay:
                get_ego = 'i am ande'
    return get_ego
