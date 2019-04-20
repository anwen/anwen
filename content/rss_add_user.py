from db import User, Share
# , Comment, Hit, Tag, Feedback, Admin, Like
import feedparser
import options
import random
import string
from pymongo import MongoClient
conn = MongoClient()
# orm??
# sys.path.append('.')


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
            print('add `user_rss` to Share')
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_rss': ''}})
        if 'user_lang' not in i:
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_lang': ''}})

# 'id': int,
# 'user_name': str,
# 'user_email': str,
# 'user_pass': str,
# 'user_domain': str,  # optional
# 'user_url': str,
# 'user_city': str,
# 'user_say': str,
# 'user_tags': list,
# 'user_leaf': int,
# 'user_status': int,   # 0=default, 1=veryfied
# 'user_jointime': float,
# 'emailverify': str,


def add_from_file():
    n = Share.find().count()
    print(n)
    rss_file = 'content/gen/qdaily_2019-04-20 15:07:12.xml'
    feeds = feedparser.parse(rss_file)
    # print(feeds.feed.title)
    # print(feeds.feed.link)
    # print(feeds.feed.subtitle)
    # print(feeds.feed.generator)
    # print(feeds.feed.image)  # {}
    # print(feeds.feed.coding)
    # print(feeds.feed.language)
    # print(feeds.feed.description)
    assert feeds.feed.description == feeds.feed.subtitle

    rss_hostname = 'qdaily'
    rss_name = '好奇心日报'
    rss_url = 'http://www.qdaily.com/feed.xml'
    # down_rss(rss_hostname, rss_url)
    email = '{}@anwensf.com'.format(rss_hostname)
    assert feeds.feed.title == rss_name
    if User.by_email(email):
        print(email)
        return
    else:
        res = User
        res['id'] = res.find().count() + 1
        res['user_name'] = rss_name
        res['user_url'] = feeds.feed.link
        res['user_say'] = feeds.feed.subtitle
        res['user_lang'] = feeds.feed.language.lower()  # zh-cn

        res['user_pass'] = random_string()
        res['user_email'] = email
        res['user_rss'] = rss_url
        res['user_domain'] = rss_hostname
        res.new(res)


if __name__ == '__main__':
    fix_user()
    add_from_file()
