#!/usr/bin/env python3
# encoding:utf-8
# import os
# import hashlib
# import requests
import time
import copy
import options
from pymongo import MongoClient
from utils import get_tags_parent
# import sys
conn = MongoClient()
# sys.path.append('.')
# from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like


def fix_user_1():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.User_Col.find().sort('_id', 1):
        adb.User_Col_2.insert(i)


def fix_share_1():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    adb2 = conn.anwen2
    adb2.authenticate(options.db['username'], options.db['password'])
    # for i in adb.Share_Col.find():
    # for idx in range(1364, 5694):
    # for idx in range(5277, 5694):
    for idx in range(5694):
        doc = adb.Share_Col.find_one({'id': idx})
        if doc:
            print(doc['id'])
            adb2.Share_Col_10.insert(doc)
        else:
            print('error: {}'.format(idx))


def fix_share():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    adb2 = conn.anwen2
    adb2.authenticate(options.db['username'], options.db['password'])
    # for i in adb.Share_Col.find():
    # for idx in range(5694):
    # for idx in range(1364, 5694):

    for idx in range(1, 1364):
        doc = adb.Share_Col.find_one({'id': idx})
        assert doc
        print(doc['id'])
        # doc['content'] = ''
        adb2.Share_Col_8.insert(doc)
    for idx in range(1364, 5278):
        doc = adb2.Share_Col_2.find_one({'id': idx})
        assert doc
        print(doc['id'])
        # if doc['id'] > 2610:
        #     time.sleep(0.01)
        # doc['content'] = ''
        adb2.Share_Col_8.insert(doc)
    for idx in range(5277, 5694):
        doc = adb2.Share_Col_3.find_one({'id': idx})
        assert doc
        print(doc['id'])
        # doc['content'] = ''
        adb2.Share_Col_8.insert(doc)


if __name__ == '__main__':
    # fix_share_1()
    fix_user_1()
