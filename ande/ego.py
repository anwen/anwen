# -*- coding:utf-8 -*-
import random

ego_keys = ['you', 'ande', u'你', u'安德']
ego_is_keys = ['who are', u'是谁', u'谁是']
ego_is_ans = ['I am ande.', u'我是安德.']
is_keys = ['what is', u'是什么', u'什么是']


def find_ego(usersay):
    usersay_low = usersay.lower()
    ego_is = ''
    for i in ego_keys:
        if i in usersay_low:
            ego_is = get_ego_is(usersay_low)
    andesay = ''.join([
        ego_is,
    ])
    return andesay


def get_ego_is(usersay):

    for j in ego_is_keys:
        if j in usersay:
            return random.choice(ego_is_ans).encode('utf-8')
