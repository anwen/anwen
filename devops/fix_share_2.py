#!/usr/bin/env python3
# encoding:utf-8
# import os
# import hashlib
# import requests
import copy
import options
from pymongo import MongoClient
from utils import get_tags_parent
# import sys
conn = MongoClient()
# sys.path.append('.')
# from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like


def fix_share():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    # for i in adb.Share_Col.find():
    for idx in range(5694):
        doc = adb.Share_Col.find_one({'id': idx})
        print(doc['id'])


if __name__ == '__main__':
    fix_share()
