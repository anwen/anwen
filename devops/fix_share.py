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
    print(options.db)
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])

    for i in adb.Share_Col.find():
        if 0 and not i['sharetype']:
            print(i['id'])
            print(i['title'])
            print(i['link'])
            print(i['sharetype'])


if __name__ == '__main__':
    fix_share()