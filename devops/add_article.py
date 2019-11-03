#!/usr/bin/env python3
# encoding:utf-8
import json
import sys
import options
from pymongo import MongoClient
from db import User, Share
import time


from opencc import OpenCC
cc = OpenCC('t2s')
cc_s2t = OpenCC('s2t')


conn = MongoClient()

adb = conn.anwen
f1 = sys.argv[1]
share_id = None
if len(sys.argv) == 3:
    share_id = sys.argv[2]
    share_id = int(share_id)


def fix():
    # for i in adb.Hit_Col.find().sort('_id', 1):
    for i in open(f1):
        i = i.strip()
        idx, title, ajson = i.split('\t')
        slug = title
        markdown = json.loads(ajson)['md']

        # markdown = markdown.replace(' BULLET::::', '\n')
        markdown = markdown.replace('BULLET::::', '†\n')
        markdown = markdown.replace('\n†\n', '\n')
        markdown = markdown.replace('†\n', '\n')
        markdown = markdown.replace('1.\n', '1. ')
        markdown = markdown.replace('2.\n', '2. ')
        markdown = markdown.replace('3.\n', '3. ')
        markdown = markdown.replace('4.\n', '4. ')
        markdown = markdown.replace('5.\n', '5. ')
        markdown = markdown.replace('6.\n', '6. ')
        markdown = markdown.replace('7.\n', '7. ')
        markdown = markdown.replace('8.\n', '8. ')
        markdown = markdown.replace('9.\n', '9. ')
        markdown = markdown.replace('0.\n', '0. ')

        markdown = markdown.replace('（\n）', '')
        markdown = markdown.replace('（，', '（')
        markdown = markdown.replace('（）', '')
        markdown = markdown.replace('（； ，）', '')

        markdown = markdown.replace('\n!\n', '\n\n')

        # markdown = markdown.replace('## 三顾茅庐', '### 三顾茅庐')

        if title == '伍迪·艾伦':
            print(markdown)

        new_md = []
        for j in markdown.split('\n'):
            # 特殊例子
            # if cc_s2t.convert('三顾茅庐') in j:
            if '## 三顧茅廬' in j:
                j = j.replace('## 三顧茅廬', '### 三顧茅廬')
                print(j)
            if cc_s2t.convert('## 军事发明') in j:
                # 军事发明
                j = j.replace('### 軍事發明', '## 軍事發明')
                print(j)
            j = j.replace('! colspan="2" colspan="2" 袁', '袁')

            if '!-' in j:
                j = j.split('!-')[0]
            if 'style=' in j:
                j = j.split('style=')[0]
            if '|valign' in j:
                j = j.split('|valign')[0]
            if 'align=' in j:
                j = j.split('align=')[0]
            if '! width' in j:
                j = j.split('! width')[0]
            if '! colspan="7"' in j:
                j = j.split('! colspan="7"')[0]
            if '! scope="col"' in j:
                j = j.split('! scope="col"')[0]

            j = j.strip()

            if j.startswith('BULLET::::'):
                j = j[10:]
            # print(repr(j), 1111, j.startswith('BULLET::::'))
            # assert i.endswith('.')
            # i = i[:-1]
            # i = i.replace('BULLET::::-', '<li>') + '</li>'

            new_md.append(j)
        new_md = '\n'.join(new_md)
        markdown = cc.convert(new_md)
        sharetype = 'goodlink'
        link = 'https://zh.wikipedia.org/wiki?curid={}'.format(idx)
        user_id = 1
        res = {
            'title': title,
            'markdown': markdown,
            'sharetype': sharetype,
            'slug': slug,
            'link': link,
            'updated': time.time(),
        }

        if share_id:
            share = Share.by_sid(share_id)
            # print(share['title'], title)
            if share['title'] != title:
                continue
            if not share:
                raise
            share.update(res)
            share.save()
        else:
            share = Share.by_title(title)
            if share:
                print('fix', title)
                share.update(res)
                share.save()
                continue

            share = Share
            res['user_id'] = user_id
            share = share.new(res)
            print(idx)

            user = User.by_sid(user_id)
            # print(user)
            user.user_leaf += 10
            user.save()
        # break


fix()


# ! 年份 !! 片名 !! 演员
