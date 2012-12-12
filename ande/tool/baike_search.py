#!/usr/bin/env python
# -*- coding: utf-8 -*-


from google_search import google_search


def baike_search(usersay):
    usersay = usersay + u' 百科'
    baike_search = google_search(usersay)
    return baike_search


def main():
    usersay = u'李白'
    result = ''
    result = baike_search(usersay)
    print result

if __name__ == '__main__':
    main()
