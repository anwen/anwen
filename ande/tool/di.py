#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2


def di(usersay):
    base_url = 'http://dict.qq.com/sug?'
    word = urllib2.quote(usersay)
    url = base_url + urllib2.quote(word)
    google_search = urllib2.urlopen(url).read().decode("utf-8")
    return google_search


def main():
    usersay = u'李白'.encode("utf-8")
    result = ''
    result = di(usersay)
    #result = type(result)
    print result

if __name__ == '__main__':
    main()
