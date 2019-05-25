import re
from db import User, Share, Tag
import datetime
import html2text
import feedparser
import options
import time
import sys
from pymongo import MongoClient
import random
conn = MongoClient()


# s = u"<![CDATA[ apache配置flask出现错误 ]]>";
rgx = re.compile("\<\!\[CDATA\[(.*?)\]\]\>")


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


def add_from_file(rss_url, rss_hostname, rss_name):
    # rss_file = 'content/gen/qdaily_2019-04-20 15:07:12.xml'
    n = Share.find().count()
    print(n)
    print(rss_name)
    feeds = feedparser.parse(rss_url)
    for post in feeds.entries[::-1]:
        if hasattr(post, 'summary'):
            summary = post.summary
            assert post.summary == post.description
        else:
            summary = ''
        # 部分rss没有content
        if hasattr(post, 'content'):
            content = post.content[0]['value']
        else:
            if hasattr(post, 'summary'):
                content = post.summary
            else:
                print('no content', rss_url, rss_hostname, rss_name)
                continue
        if content.startswith('<![CDATA[') and content.endswith(']]>'):
            # m = rgx.search(content)
            # content = m.group(1)
            content = content[9:-3]
        if summary.startswith('<![CDATA[') and summary.endswith(']]>'):
            summary = summary[9:-3]

        if hasattr(post, 'published'):
            if 'GMT' == post.published[-3:]:
                published = datetime.datetime.strptime(post.published, "%a, %d %b %Y %H:%M:%S GMT")
            elif ',' in post.published:
                published = datetime.datetime.strptime(post.published, "%a, %d %b %Y %H:%M:%S %z")
                # Thu, 18 Apr 2019 19:32:58 +0800
            elif '/' in post.published:
                published = datetime.datetime.strptime(post.published, "%Y/%m/%d %H:%M:%S %z")
            elif 'Z' == post.published[-1]:
                post.published = post.published.replace('.000Z', 'Z')
                published = datetime.datetime.strptime(post.published, "%Y-%m-%dT%H:%M:%SZ")
            else:
                published = datetime.datetime.strptime(post.published, "%Y-%m-%d %H:%M:%S %z")
            published = published.timestamp()
        else:
            if random.random() > 0.9:
                print('no published time')
            published = time.time()

        title = post.title
        link = post.link
        if hasattr(post, 'source'):
            source_title = post.source.title
            # print(source_title)
            assert rss_name in source_title
            # assert rss_name == source_title
        source = rss_name

        if hasattr(post, 'category_title'):
            category = post.category_title
            assert ' ' not in category
            assert ',' not in category
            tags = [category]
        elif hasattr(post, 'tags'):
            tags = post.tags
            # print(tags)
            # assert len(tags) == 1
            # tags = tags[0]['term']
            tags = ','.join([t['term'] for t in tags])
            category = ''
            if '-' in tags:
                print(tags)
            tags = tags.replace(' ', '-')
            tags = tags.split(',')
            for tag in tags:
                if ' ' in tag:
                    print(tag)
        else:
            # print('no category')
            category = ''
            tags = []
        sharetype = 'rss'
        try:
            markdown = html2text.html2text(content)
        except Exception as e:
            print('error in html-to-markdown: {}'.format(e))
            continue
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
        print(post.author)
        print(dir(post))
        print(post.keys())

        # 去重方案
        # - 标题重复
        found = Share.find({'title': title})
        if found.count():
            if found.count() > 1:
                print('!! repeated article title: {}'.format(title))
            elif found.count() == 1:
                # continue
                share = Share.by_sid(found[0].id)
                if share and summary:
                    print('title {} updated'.format(title))
                    # share.update(res)
                    # share.save()
        else:
            print('title {} adding'.format(title))
            email = '{}@anwensf.com'.format(rss_hostname)
            auser = User.by_email(email)
            assert auser
            share = Share
            user_id = auser.id
            res['user_id'] = user_id  # just use 1 as default
            share = share.new(res)

            # pass
            # 修正内容
            # <enclosure type="audio/mpeg" url="https://kernelpanic.fm/55/audio.mp3"/>
            # <itunes:duration>6957</itunes:duration>

            user = User.by_sid(user_id)
            user.user_leaf += 10
            user.save()
            for i in tags:
                doc = {
                    'name': i,
                    'share_ids': share.id
                }
                Tag.new(doc)


if __name__ == '__main__':
    fix_share()
    # maxnum = 0
    # if len(sys.argv) > 1:
    #     maxnum = int(sys.argv[1])

    key = ''
    if len(sys.argv) > 1:
        key = sys.argv[1]

    n = 0
    while True:
        for i in open('content/rss_using.txt'):
            n += 1
            i = i.strip()
            ii = i.split()
            if len(ii) < 4:
                continue
            url, host, name, info = ii[:4]
            if 'gfw' in info:
                continue
            print(i)
            # if maxnum and n >= maxnum:
            #     break
            if not key or (key and key == host):
                add_from_file(url, host, name)
        print('start sleep for 3600s')
        time.sleep(3600*1)
