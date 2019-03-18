import opml
import sys

opml_file = 'feeds/Reabble-zh.opml'
opml_file = 'feeds/Kindle4RSS-Feeds.xml'
opml_file = 'feeds/feedly_askender.opml'

outline = opml.parse(opml_file)

# meta optional
# print(outline.title)
# print(outline.ownerName)
# print(outline.ownerEmail)
# info
# print(len(outline))

level = int(sys.argv[1])

assert len(outline)
for one in outline:
    if hasattr(one, 'type'):
        assert one.type == 'rss'

    # if not len(one):
    if level == 1 and not len(one):
        print()
        print('### {}'.format(one.text))
        if one.title != one.text:
            print(one.title)
            raise
        # 1级分类
        print('  - xml: <{}>'.format(one.xmlUrl))
        if hasattr(one, 'htmlUrl'):
            if one.htmlUrl != one.xmlUrl:
                print('  - html: <{}>'.format(one.htmlUrl))

    if level > 1 and len(one):
        print()
        print()
        print('## {}'.format(one.text))
        if one.title != one.text:
            print(one.title)
            raise

        for line in one:
            assert not len(line)  # 无3级分类
            print()
            # print(dir(line))
            if not hasattr(line, 'title'):
                continue
            if line.title != line.text:
                print(line.title)
                print(line.text)
                raise
            print('### {}'.format(line.text))
            print('  - xml: <{}>'.format(line.xmlUrl))
            if hasattr(line, 'htmlUrl'):
                if line.htmlUrl != line.xmlUrl:
                    print('  - html: <{}>'.format(line.htmlUrl))
