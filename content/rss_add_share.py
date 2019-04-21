import re
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


# s = u"<![CDATA[ apache配置flask出现错误 ]]>";
rgx = re.compile("\<\!\[CDATA\[(.*?)\]\]\>")
# rgx = re.compile("<![CDATA[(.*?)]]>")


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
        if 'content' not in i or i['content'] is None:
            adb.Share_Col.update({'_id': i['_id']}, {'$set': {'content': ''}})
        if 'summary' not in i:
            adb.Share_Col.update({'_id': i['_id']}, {'$set': {'summary': ''}})

        if 'content' in i:
            if i['content'].startswith(' '):
                print(i['title'])
            pass
            # adb.Share_Col.update({'_id': i['_id']}, {'$set': {'content': ''}})


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

    rss_url = 'https://feedx.net/rss/huxiu.xml'
    rss_hostname = 'huxiu'
    rss_name = '虎嗅'

    rss_url = 'https://www.jiqizhixin.com/rss'
    rss_hostname = 'jiqizhixin'
    rss_name = '机器之心'

    # 暂时放弃
    rss_url = 'https://www.gcores.com/rss'
    rss_hostname = 'gcores'
    rss_name = '机核'

    print(rss_name)
    feeds = feedparser.parse(rss_url)
    print(feeds.keys())
    print(feeds.feed.keys())
    for post in feeds.entries[::-1]:
        # print(post.keys())
        # print(post.summary) // use it

        assert post.summary == post.description

        # 部分rss没有content
        if hasattr(post, 'content'):
            content = post.content[0]['value']
            summary = post.summary
        else:
            content = post.summary
            summary = ''

        if content.startswith('<![CDATA[') and content.endswith(']]>'):
            # m = rgx.search(content)
            # content = m.group(1)
            content = content[9:-3]
        if summary.startswith('<![CDATA[') and summary.endswith(']]>'):
            summary = summary[9:-3]

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
            assert ' ' not in category
            assert ',' not in category
            tags = [category]
        elif hasattr(post, 'tags'):
            tags = post.tags
            assert len(tags) == 1
            tags = tags[0]['term']
            category = ''
            if '-' in tags:
                print(tags)
            tags = tags.replace(' ', '-')
            tags = tags.split(',')
            # print(tags)
            for tag in tags:
                if ' ' in tag:
                    print(tag)
        else:
            print('no category')
            category = ''
            tags = []

        # print(post.author)

        sharetype = 'rss'
        markdown = html2text.html2text(content)

        res = {
            'title': title,
            'link': link,
            'source': source,
            'category': category,
            'content': content,
            'summary': summary,
            'sharetype': sharetype,
            'tags': tags,

            'markdown': markdown,
            'published': published,
            'updated': time.time(),
        }
        found = Share.find({'title': title})
        if found.count():
            if found.count() == 1 and summary:
                print(found[0].id)
                # adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_lang': ''}})
                share = Share.by_sid(found[0].id)
                if share:
                    print('title {} updated'.format(title))
                    share.update(res)
                    share.save()
            else:
                # print('title {} repeated'.format(title))
                pass
            # break
            # continue
        else:
            print('title {} adding'.format(title))
            # continue
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
