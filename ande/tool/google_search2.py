#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2


def search(word):
    url = r'http://www.google.cn/search?\
        hl=zh-CN&newwindow=1&q=' + word + "&start=10&sa=N"
    req = urllib2.Request(url)
    req.add_header("User-Agent", 'Mozilla\
        /4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322)')
    opener = urllib2.build_opener()
    text = opener.open(req).read()
    return text

word = u'李白'
search(word)
