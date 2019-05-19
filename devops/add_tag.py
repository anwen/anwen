#!/usr/bin/env python3
# encoding:utf-8

import sys
import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])
sys.path.append('.')

from db import Tag, Share  # noqa
# User, Share, Comment, Hit, Tag, Feedback, Admin, Like

# 96 zhihu
# 120 sspai 软件

# 2
# 67 kunpeng
# 70 alferd
# 69 heroxie


def get_tags(doc):
    title = doc['title']
    tags = []
    if '触乐' in title:
        tags.append('游戏')
    if 119 == doc['user_id']:  # 触乐
        tags.append('游戏')
    if 115 == doc['user_id']:  # one TODO 图片
        tags.append('读书')
    if 114 == doc['user_id']:  # youyans
        tags.append('游戏')
    if 97 == doc['user_id']:  # 机器之心
        tags.append('科技')
    if 105 == doc['user_id']:  # geekpark
        tags.append('科技')
    if 95 == doc['user_id']:  # solidot
        tags.append('科技')
    if 120 == doc['user_id']:  # sspai
        tags.append('软件')
    if 113 == doc['user_id']:  # geo
        tags.append('图片')
        tags.append('地理')

    return tags


def check():
    # share_num = Share.find().count()
    # share_with_tag_num = share_num - Share.find({'tags': []}).count()

    for i in adb.Share_Col.find().sort('_id', 1):
        if i['status'] < 1:
            continue
        # if i['tags'] == []:
        if i['tags']:
            continue
        # print(i['id'], i['title'])
        print(i['user_id'])

        # adb.Share_Col.update().sort('_id', 1):
        tags = get_tags(i)
        adb.Share_Col.update({'_id': i['_id']}, {'$set': {'tags': tags}})
        for tag in tags:
            doc = {
                'name': tag,
                'share_ids': i['id']
            }
            Tag.new(doc)

    share_without_tag_num = Share.find({'tags': []}).count()
    print(share_without_tag_num)


check()
