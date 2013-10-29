#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import urllib


def g_search(usersay):
    q = urllib.urlencode({'q': usersay})
    # url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % q
    url = ''.join([
        'http://ajax.googleapis.com/ajax/services/search/web?v=1.0',
        '&hl=zh-cn&rsz=large&start=0&key=',
        'ABQIAAAAx6QgrViEp9B9DICAytm0fBTiy65Og9q1iaK',
        'AY-TXMosE48Ol9RS2aJzrKZdmC2W--xPbuSLCMHac2g&', q
    ])
    # print url
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    # print 'Total results: %s' % data['cursor']['estimatedResultCount']
    hits = data['results']
    # print 'Top %d hits:' % len(hits)
    for h in hits:
        if u'。' in h['content']:
            r = h['content']  # 'via', h['url']
            break
    return r
    # print 'For more results, see %s' % data['cursor']['moreResultsUrl']


if __name__ == '__main__':
    usersay = u'李白'.encode("utf-8")
    usersay = u'六四wiki'.encode("utf-8")
    result = g_search(usersay)
    print(result)
