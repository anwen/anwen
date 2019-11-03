#!/usr/bin/env python3
# encoding:utf-8
from utils.img_tools import make_post_thumb
from PIL import Image
import requests
import datetime
import sys
import options
import os
from pymongo import MongoClient
conn = MongoClient()
adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])
sys.path.append('.')
from db import Tag, Share  # noqa


def stat_img():
    n = 0
    for i in adb.Share_Col.find().sort('_id', 1):
        assert not i['upload_img']
        if i['status'] >= 1:
            continue
        post_img = i['post_img']
        if post_img:
            print('not published:s', post_img)
            print('https://anwensf.com/share/{}'.format(i['id']))
            n += 1
    print('有图片但没发布的数量:', n)
    n = 0
    n_with_tag = 0
    for i in adb.Share_Col.find().sort('_id', 1):
        if i['status'] < 1:
            continue
        post_img = i['post_img']
        if post_img:
            n += 1
            if i['tags']:
                n_with_tag += 1
    print('有图片且已发布的数量:', n)
    print('有图片且已发布且有标签的数量:', n_with_tag)
    return
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


stat_img()
