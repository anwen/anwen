# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
from HTMLParser import HTMLParser


#python版Bing翻译API函数，支持自动识别语言
#使用前请先到Bing Developer Center去申请一个ApiId。安德的测试可以用下面的appid
bingkey = '5853B784F9DAF5C32487D3C958510F127FF99011'


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def bingtrans(usersay, sayto='en'):
    #usersay, sayfrom = 'zh-cn', sayto = 'en'
    #base_url = 'http://api.microsofttranslator.com/V2/\
    # Http.svc/Translate?from=%s&to=%s&appId=%s&text=' %(sayfrom,sayto,bingkey)
    base_url = 'http://api.microsofttranslator.com/V2/\
    Http.svc/Translate?to=en&appId=%s&text=' % (bingkey)
    #http://api.microsofttranslator.com/V2/\
    # Http.svc/Translate?from=en&to\
    # =zh-cn&appId=5853B784F9DAF5C32487D3C958510F127FF99011&text=hello
    word = urllib2.quote(usersay)
    url = base_url + urllib2.quote(word)
    bingtrans = urllib2.urlopen(url).read()
    #.decode("utf-8")
    bingtrans = urllib2.unquote(strip_tags(bingtrans))
    #.decode("gbk").encode("utf-8")
    return bingtrans  # type(bingtrans)


def main():
    usersay = u'你好'.encode("utf-8")
    #usersay = 'salut'
    #data = bingtrans(usersay,'zh-cn','en')
    data = bingtrans(usersay, 'en')
    print data

if __name__ == '__main__':
    main()
