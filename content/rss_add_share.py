from db import User, Share, Tag
# , Comment, Hit, Tag, Feedback, Admin, Like
import datetime
import html2text
import feedparser
import options
import time
# import markdown2
from pymongo import MongoClient
conn = MongoClient()
# orm??
# sys.path.append('.')


def fix_share():
    adb = conn.anwen
    if 'username' in options.db:
        adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.Share_Col.find():
        if 'source' not in i:
            print('add `source` to Share')
            adb.Share_Col.update({'_id': i['_id']}, {'$set': {'source': ''}})
        if 'category' not in i:
            adb.Share_Col.update({'_id': i['_id']}, {'$set': {'category': ''}})


def add_from_file():
    n = Share.find().count()
    print(n)
    # rss_file = 'content/gen/qdaily_2019-04-20 15:07:12.xml'
    rss_url = 'http://www.qdaily.com/feed.xml'
    rss_hostname = 'qdaily'

    rss_url = 'https://www.solidot.org/index.rss'
    rss_hostname = 'solidot'
    rss_name = 'Solidot'

    rss_url = 'https://www.zhihu.com/rss'
    rss_hostname = 'zhihu'
    rss_name = '知乎每日精选'

    print(rss_name)
    feeds = feedparser.parse(rss_url)
    for post in feeds.entries[::-1]:
        # print(published)
        assert post.summary == post.description

        # published = datetime.datetime.strptime(post.published, "%Y-%m-%d %H:%M:%S %z")
        published = datetime.datetime.strptime(post.published, "%a, %d %b %Y %H:%M:%S %z")
        # Thu, 18 Apr 2019 19:32:58 +0800
        published = published.timestamp()

        # continue
        title = post.title
        link = post.link
        if hasattr(post, 'source'):
            source = post.source.title
            assert rss_name == source
        else:
            source = rss_name

        if hasattr(post, 'category_title'):
            category = post.category_title
        else:
            print('no category')
            category = ''

        content = post.summary
        sharetype = 'rss'
        markdown = html2text.html2text(content)
        assert ' ' not in category
        tags = [category]

        res = {
            'title': title,
            'link': link,
            'source': source,
            'category': category,
            'content': content,
            'sharetype': sharetype,
            'tags': tags,

            'markdown': markdown,
            'published': published,
            'updated': time.time(),
        }
        found = Share.find({'title': title})
        if found.count():
            print('title {} is added'.format(title))
            break
            pass
        else:
            # continue
            rss_hostname
            email = '{}@anwensf.com'.format(rss_hostname)
            auser = User.by_email(email)
            assert auser

            share = Share
            user_id = auser.id
            res['user_id'] = user_id  # just use 1 as default
            share = share.new(res)

            user = User.by_sid(user_id)
            user.user_leaf += 10
            user.save()
        # continue
        for i in tags:
            doc = {
                'name': i,
                'share_ids': share.id
            }
            Tag.new(doc)


if __name__ == '__main__':
    fix_share()
    add_from_file()
