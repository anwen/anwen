#-*-coding:utf-8-*-

"""
Copyright (c) 2012 yangzhe1991 <ud1937@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# 维基百科

import urllib2
import urllib
import re

wikihints = [u'what is', u'who is', u'什么是', u'是什么', u'是啥', u'是谁', u'谁是']


def test(data):
    for i in wikihints:
        if i in data['usersay']:
            return True
    return False


def handle(data):
    usersay = data['usersay']
    m = re.search('(?<=什么是)(.+?)(?=啊|那|呢|哈|！|。|？|\?|\s|\Z)', usersay)
    if m and m.groups():
        return wikipedia(m.groups()[0])
    for i in wikihints:
        if i in usersay:
            usersay = usersay.replace(i, '')
            usersay = usersay.replace('?', '')
            usersay = usersay.encode("utf-8")
            return wikipedia(usersay)


def remove(s):
    ans = ''
    while True:
        i = s.find('<')
        if i < 0:
            ans += s
            break
        ans += s[:i]
        s = s[i + 1:]
        s = s[s.find('>') + 1:]
    s = ans
    ans = ''
    while True:
        i = s.find('[')
        if i < 0:
            ans += s
            return ans
        ans += s[:i]
        s = s[i + 1:]
        s = s[s.find(']') + 1:]


def wikipedia(title):
    url = 'http://zh.wikipedia.org/w/index.php?%s' % urllib.urlencode(
        {'title': title, 'printable': 'yes', 'variant': 'zh-cn'})
    req = urllib2.Request(
        url,
        headers={'User-Agent': "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.354.0 Safari/533.3"})
    wp = urllib2.urlopen(req, timeout=10)
    html = wp.read()
    # 防止404，实际上似乎py会直接在urlopen的时候发现404并抛异常
    if html.find('维基百科目前还没有与上述标题相同的条目') >= 0:
        raise Exception
    i = html.find('mw-content-text')
    if i < 0:
        raise Exception
    html = html[i:]
    html = html[html.find('<p>') + 3:html.find('</p>')]
    return remove(html)


if __name__ == '__main__':
    datas = [
        {'usersay': u'李白是谁'},
        {'usersay': '什么是SVM  ????'},
        {'usersay': '什么是薛定谔方程啊'},
    ]
    for data in datas:
        print data['usersay'], handle(data)
