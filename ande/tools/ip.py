#-*-coding:utf-8-*-

import urllib
import json


def get_ande_ip():
    return urllib.urlopen('http://ifconfig.me/ip').read()


def get_ipinfo(ip=None):
    if not ip or ip == '127.0.0.1':
        ip = get_ande_ip()
    return json.loads(urllib.urlopen(
        'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip).read())

if __name__ == '__main__':

    print get_ande_ip()
    print get_ipinfo('')
