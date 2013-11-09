# -*- coding:utf-8 -*-
import requests

keys = ['ip', u'网络地址']
#http://ip.taobao.com/service/getIpInfo.php?ip=180.166.109.197

def find_ip(doc):
    usersay_low = doc['usersay_low']
    ego_is = ''
    for i in keys:
        if i in usersay_low:
            return get_ip(doc)

def get_ip(doc):
    if doc['user_ip'] == '127.0.0.1':
        user_ip = requests.get('http://httpbin.org/ip').json()
        return user_ip['origin']
    return doc['user_ip']
