# pip install opml
# pip install feedparser
import opml
import feedparser

# source
# 'http://hosting.opml.org/dave/validatorTests/clean/subscriptionList.opml'
opml_file_kindle4rss = 'Kindle4RSS-Feeds.xml'
opml_file_Reabble = 'Reabble-zh.opml'


# meta
outline = opml.parse(opml_file_kindle4rss)
# outline = opml.parse(opml_file_Reabble)
print(outline)
print(outline.title)
# print(outline.ownerName)
# print(outline.ownerEmail)


def read(rss_url):
    # d = feedparser.parse('http://www.reddit.com/r/python/.rss')
    d = feedparser.parse(rss_url)
    print(d['feed']['title'])
    print(d['feed']['link'])  # Resolves relative links
    print(d.feed.subtitle)
    print(d.version)
    print(len(d['entries']))
    for entry in d['entries']:
        print(entry['title'])
        print(entry['link'])


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
        print(one.xmlUrl)
        read(one.xmlUrl)
        break
        if one.htmlUrl != one.xmlUrl:
            print(one.htmlUrl)
            raise
    else:
        for line in one:
            assert not len(line)
            print(line.text)
            if line.title != line.text:
                print(line.title)
                raise
            print(line.xmlUrl)
            # if line.htmlUrl != line.xmlUrl:
            #     print('line.htmlUrl', line.htmlUrl)
