#!/usr/bin/env python3
# encoding:utf-8

import sys
import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])
sys.path.append('.')

from db import Tag  # noqa
# User, Share, Comment, Hit, Tag, Feedback, Admin, Like


def get_tags(doc):
    title = doc['title']
    tags = []
    if '触乐' in title:
        tags.append(tags)
    return tags


def check():
    for i in adb.Share_Col.find().sort('_id', 1):
        # if i['status']  1:
        # if i['tags'] == []:
        if i['tags']:
            continue
        print(i['id'])
        print(i['title'])

        # adb.Share_Col.update().sort('_id', 1):
        tags = get_tags(i)
        adb.Share_Col.update({'_id': i['_id']}, {'$set': {'tags': tags}})
        for i in tags:
            doc = {
                'name': i,
                'share_ids': i['id']
            }
            Tag.new(doc)


check()
