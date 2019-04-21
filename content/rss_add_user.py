from db import User
import feedparser
import options
import random
import string
from pymongo import MongoClient
conn = MongoClient()


def random_string(len=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))


def fix_user():
    adb = conn.anwen
    if 'username' in options.db:
        adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.User_Col.find():
        # if 'user_domain' not in i:
        if 'user_rss' not in i:
            print('add `user_rss` to User')
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_rss': ''}})
        if 'user_lang' not in i:
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_lang': ''}})


def add_from_file(rss_url, rss_hostname, rss_name):
    # rss_file = 'content/gen/qdaily_2019-04-20 15:07:12.xml'
    feeds = feedparser.parse(rss_url)
    print(feeds.keys())
    if hasattr(feeds.feed, 'description'):
        assert feeds.feed.description == feeds.feed.subtitle
        print(feeds.feed.description)
    # print(feeds.description)

    email = '{}@anwensf.com'.format(rss_hostname)
    if hasattr(feeds.feed, 'title'):
        print(feeds.feed.title, rss_name)
        # assert feeds.feed.title == rss_name
        assert rss_name in feeds.feed.title
    else:
        print('no title', rss_name)
    if User.by_email(email):
        print(email)
        return
    else:
        res = User
        res['id'] = res.find().count() + 1
        res['user_name'] = rss_name
        res['user_url'] = feeds.feed.link
        if hasattr(feeds.feed, 'description'):
            res['user_say'] = feeds.feed.description
        if hasattr(feeds.feed, 'language'):
            res['user_lang'] = feeds.feed.language.lower()  # zh-cn

        res['user_pass'] = random_string()
        res['user_email'] = email
        res['user_rss'] = rss_url
        res['user_domain'] = rss_hostname
        res.new(res)


if __name__ == '__main__':
    fix_user()
    # add_from_file()
    for i in open('content/rss_using.txt'):
        url, host, name, info = i.split()
        if 'gfw' in info:
            print(i)
            continue
        add_from_file(url, host, name)