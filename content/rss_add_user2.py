from utils import img_tools
from db import User
import feedparser
import options
import random
import string
import sys
import os
import requests
from pymongo import MongoClient
conn = MongoClient()
sys.path.append('.')
make_post_thumb = img_tools.make_post_thumb


adb = conn.anwen
if 'username' in options.db:
    adb.authenticate(options.db['username'], options.db['password'])


def random_string(len=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))


def fix_user():

    for i in adb.User_Col.find():
        # if 'user_domain' not in i:
        if 'user_rss' not in i:
            print('add `user_rss` to User')
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_rss': ''}})
        if 'user_lang' not in i:
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_lang': ''}})


def add_from_file(rss_url, rss_hostname, rss_name):
    doc = adb.User_Col.find_one({'user_domain': rss_hostname})
    if doc:
        user_name = doc['user_name']
        assert user_name == rss_name
        user_url = doc['user_url']
        assert user_url != rss_url
        # 通常情况下，已经收录的不再解析，除非需要更新字段
        user_id = doc['id']
        avatar_dir = 'static/avatar'
        size = 'raw'
        avatar_path = '%s/feed_%s_%s.jpg' % (avatar_dir, str(user_id), size)
        if os.path.isfile(avatar_path):
            return
        # return
        print(user_id)

    # return
    # rss_file = 'content/gen/qdaily_2019-04-20 15:07:12.xml'
    feeds = feedparser.parse(rss_url)
    print(feeds.keys())
    # 更新图片

    if hasattr(feeds.feed, 'image'):
        print(feeds.feed.image)
        print(type(feeds.feed.image))
        print(feeds.feed.image['href'])
        print(11)
        if feeds.feed.image.get('href'):
            href = feeds.feed.image['href']
            ext = href.split('.')[-1]
            img_name = 'feed_{}.{}'.format(user_id, ext)
            r = requests.get(href)
            href = href.replace('https', 'http')
            print(href)
            print(r.status_code)
            if r.status_code == 200:
                print(img_name)
                with open(img_name, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
                make_post_thumb(img_name, sizes=[[132, 132]])

    # <image>
    # <url>https://www.huxiu.com/static_2015/img/logo.png</url>
    # <title>虎嗅网</title>
    # <link>http://www.huxiu.com</link>
    # </image>

    return
    if hasattr(feeds.feed, 'description'):
        if feeds.feed.description != feeds.feed.subtitle:
            print('!'*88)
            print('description != subtitle')
            print(feeds.feed.description)
            print(feeds.feed.subtitle)
        # assert feeds.feed.description == feeds.feed.subtitle
    # print(feeds.description)

    email = '{}@anwensf.com'.format(rss_hostname)
    if hasattr(feeds.feed, 'title'):
        print(feeds.feed.title, rss_name)
        # assert feeds.feed.title == rss_name
        if rss_name in '创业邦 国家地理 Flipboard-Books'.split():
            pass
        else:
            assert rss_name.replace('-', '') in feeds.feed.title.replace(' ', '')
    else:
        print('no title', rss_name)
    if User.by_email(email):
        print(email)
        return
    else:
        res = User
        res['id'] = res.find().count() + 1
        res['user_name'] = rss_name
        # podcast
        # https://anyway.fm/rss.xml

        # print(dir(feeds.feed))
        # print(feeds.feed.keys())
        # print(dir(feeds))
        # print(feeds.keys())
        # print(len(feeds.entries))
        res['user_url'] = feeds.feed.link
        if hasattr(feeds.feed, 'description'):
            res['user_say'] = feeds.feed.subtitle  # feeds.feed.description
        if hasattr(feeds.feed, 'language'):
            res['user_lang'] = feeds.feed.language.lower()  # zh-cn

        res['user_pass'] = random_string()
        res['user_email'] = email
        res['user_rss'] = rss_url
        res['user_domain'] = rss_hostname
        res.new(res)


if __name__ == '__main__':
    fix_user()
    maxnum = 0
    if len(sys.argv) > 1:
        maxnum = int(sys.argv[1])
    n = 0
    box = []
    for i in open('content/rss_using.txt'):
        n += 1
        i = i.strip()
        ii = i.split()
        if len(ii) < 4:
            continue
        url, host, name, info = ii[:4]
        if 'gfw' in info:
            continue

        if host != 'huxiu':
            continue
        print(i)
        box.append(url)

        add_from_file(url, host, name)
        if maxnum and n >= maxnum:
            break
    print(len(box))
