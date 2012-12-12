#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2


def google_search(usersay):
    base_url = 'http://ajax.googleapis.com/ajax/services/search\
    /web?v=1.0&hl=zh-cn&rsz=large&start=1\
    &key=ABQIAAAAx6QgrViEp9B9DICAytm0fBTiy65Og9q1iaKAY\
    -TXMosE48Ol9RS2aJzrKZdmC2W--xPbuSLCMHac2g&q='
    word = urllib2.quote(usersay)
    url = base_url + urllib2.quote(word)
    google_search = urllib2.urlopen(url).read().decode("utf-8")
    return google_search


def main():
    usersay = u'李白'.encode("utf-8")
    result = ''
    result = google_search(usersay)
    print result

if __name__ == '__main__':
    main()
