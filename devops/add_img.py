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


def check():
    for i in adb.Share_Col.find().sort('_id', 1):
        upload_img = i['upload_img']
        assert not upload_img
        if i['status'] >= 1:
            continue
        post_img = i['post_img']
        if post_img:
            print('not published:s', post_img)
            print('https://anwensf.com/share/{}'.format(i['id']))

    for i in adb.Share_Col.find().sort('_id', 1):
        if i['status'] < 1:
            continue
        post_img = i['post_img']
        if post_img:
            continue
        markdown = i['markdown']
        if not markdown:
            print(1, i['title'])
            print('https://anwensf.com/share/{}'.format(i['id']))


check()
