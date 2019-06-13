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
        if i['status'] < 1:
            continue
        # post_img
        # upload_img
        print(i['post_img'])


check()
