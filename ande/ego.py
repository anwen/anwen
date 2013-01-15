# -*- coding:utf-8 -*-


def find_ego(usersay):
    ego_keys = ['you', 'ande', u'你', u'安德']
    ego = ''
    for i in ego_keys:
        if i in usersay:
            if 'who are' in usersay:
                ego = 'i am ande'
    return ego
