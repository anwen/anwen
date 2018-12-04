#!/usr/bin/env python3
# encoding:utf-8
# import os
# import hashlib
# import requests
import options
from pymongo import MongoClient
# import sys
conn = MongoClient()
# sys.path.append('.')
# from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like


def fix_share():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])

    for i in adb.Share_Col.find():
        if isinstance(i['tags'], str):
            print(i['tags'])
            adb.Share_Col.update({'_id': i['_id']}, {'tags': i['tags'].split()})
        if 0 and not i['sharetype']:
            print(i['id'])
            print(i['title'])
            print(i['link'])
            print(i['sharetype'])


if __name__ == '__main__':
    fix_share()
