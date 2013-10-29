# -*- coding:utf-8 -*-

import urllib
import urllib2


def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()


def fenci(usersay):
    posturl = "http://www.ftphp.com/scws/api.php"
    usersay = usersay.encode("utf-8")
    data = {'data': usersay, 'respond': 'json'}
    fenci = post(posturl, data)
    return fenci


def main():
    posturl = "http://www.ftphp.com/scws/api.php"
    nihao = u'你是谁'
    nihao = nihao.encode("utf-8")
    data = {'data': nihao}
    data = post(posturl, data).decode("utf-8")
    print(data)


if __name__ == '__main__':
    main()
