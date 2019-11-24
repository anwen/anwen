# pip install opml
# pip install feedparser
import opml
import feedparser

# source
# 'http://hosting.opml.org/dave/validatorTests/clean/subscriptionList.opml'
opml_file_kindle4rss = 'Kindle4RSS-Feeds.xml'
opml_file_Reabble = 'Reabble-zh.opml'


# meta
# outline = opml.parse(opml_file_kindle4rss)
outline = opml.parse(opml_file_Reabble)
print(outline.title)
# print(outline.ownerName)
# print(outline.ownerEmail)


def read(rss_url, title):
    # d = feedparser.parse('http://www.reddit.com/r/python/.rss')
    print('\n\n====<br>')
    try:
        d = feedparser.parse(rss_url)
        title = d['feed']['title']
        # return
        # print(d['feed']['link'])  # Resolves relative links
        # d.feed.description
        # d.feed.subtitle
        # d.version
        meta = '{} 文章数：{} <br>'.format(title, len(d['entries']))
        print(meta)
        for entry in d['entries']:
            if 'weixin.sogou.com' in entry['link']:
                continue
            if 'yiding.9.cn' in entry['link']:
                continue
            # guid content:encoded pubDate
            title = entry['title']
            url = 'https://anwensf.com/share_by_get?link='+entry['link']
            print('<a href="{}">{}</a><br>'.format(url, title))
    except:
        meta = '{}  err <br>'.format(title)
        print(meta)


assert len(outline)
print(len(outline))
for one in outline:
    if hasattr(one, 'type'):
        assert one.type == 'rss'
        # print(one.type)  # rss
    print(one.text)
    if one.title != one.text:
        print(one.title)
        raise
    if not len(one):
        # 无二级分类

        read(one.xmlUrl, one.title)
        # break
        if one.htmlUrl != one.xmlUrl:
            print(one.htmlUrl)
            raise
    else:
        for line in one:
            assert not len(line)
            # print(line.text)
            if line.title != line.text:
                print(line.title)
                # raise
            # print(line.xmlUrl)
            read(line.xmlUrl, line.title)
            # if line.htmlUrl != line.xmlUrl:
            #     print('line.htmlUrl', line.htmlUrl)
