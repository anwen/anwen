import requests
import datetime
import time
import os
import feedparser
# https://github.com/kurtmckee/feedparser
from datetime import timedelta, timezone


def down_rss(name, url):
    r = requests.get(url)
    if r.status_code != 200:
        print(r.status_code)
        return
    # datetime.datetime.now()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # datetime.datetime.strptime("2014-12-31 18:20:10", "%Y-%m-%d %H:%M:%S")
    # '2015-01-12 23:13:08'
    fname = 'gen/{}_{}.xml'.format(name, now)
    with open(fname, 'w') as f:
        f.write(r.text)


rss_name = '好奇心日报'
rss_hostname = 'qdaily'
rss_url = 'http://www.qdaily.com/feed.xml'
# down_rss(rss_hostname, rss_url)


def sort_rss():
    for root, dirs, files in os.walk("gen", topdown=False):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))


# rss_url = 'http://www.oschina.net/news/rss'
# feeds = feedparser.parse(rss_url)
rss_file = 'gen/qdaily_2019-04-20 15:07:12.xml'
feeds = feedparser.parse(rss_file)

# 获得rss版本
print(feeds.version)

# 获得Http头
# print(feeds.headers)
# print(feeds.headers.get('content-type'))

# rss的标题
# print(feeds['feed']['title'])
print(feeds.feed.title)
# 链接
print(feeds.feed.link)
# 子标题
print(feeds.feed.subtitle)
print(feeds.feed.generator)
print(feeds.feed.image)  # {}
print(feeds.feed.coding)
print(feeds.feed.language)
print(feeds.feed.description)


# 查看文章数量
print(len(feeds.entries))

# # 获得第一篇文章的标题
# print(feeds['entries'][0]['title'])
# # 获得第一篇文章的链接
# print(feeds.entries[0]['link'])
print('====')

for post in feeds.entries[:2]:
    #     print(post.title + ": " + post.link)
    print(post.title)
    print(post.link)
    # meta
    print(post.source)
    print(post.source.title)
    print(post.category_title)
    print(post.published)  # string
    published = datetime.datetime.strptime(post.published, "%Y-%m-%d %H:%M:%S %z")
    published = published.timestamp()

    # print(post.description)
    # print(post.summary)
    assert post.summary == post.description

    # print(post.published_parsed)
    # datetime.datetime.now().timetuple()
    # .timetuple() 不存储utc偏移量。它等价于纯 datetime 对象。
    # diff
    # print(datetime.datetime.fromtimestamp(published))
    # print(datetime.datetime.fromtimestamp(time.time()))

    # atimestamp = time.mktime(atime)
    # adatetime = datetime.datetime.fromtimestamp(atimestamp)
    # tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00
    # adatetime = adatetime.replace(tzinfo=tz_utc_8)  # 强制设置为UTC+8:00
    # print(datetime.datetime.fromtimestamp(atimestamp))  # 本地时间
    # print(datetime.datetime.utcfromtimestamp(atimestamp))  # UTC时间
    # print(post.links)

    # useless
    # print(post.category_id)
    # print(post.links)
    # print(post.summary_detail)
    # print(post.title_detail)
    # 'type': 'text/html', 'language': None, 'base': '', 'value':
    print(post.keys())

# __weakref__', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'keymap', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']

    print('')
