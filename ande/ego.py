# -*- coding:utf-8 -*-
import random


def find_ego(usersay):
    usersay_low = usersay.lower()
    ego_keys = ['you', 'ande', u'你', u'安德']
    for i in ego_keys:
        if i in usersay_low:
            ego_is = get_ego_is(usersay_low)

    andesay = ''.join([
        ego_is,
    ])
    return andesay


def get_ego_is(usersay):
    ego_is_keys = ['who are', u'是谁', u'谁是']
    ego_is_ans = ['I am ande.', u'我是安德.']
    for j in ego_is_keys:
        if j in usersay:
            return random.choice(ego_is_ans).encode('utf-8')
