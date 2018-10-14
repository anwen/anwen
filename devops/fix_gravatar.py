#!/usr/bin/env python3
# encoding:utf-8
from pymongo import MongoClient
import sys
conn = MongoClient()
sys.path.append('.')
from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like
import options


def fix_ol_gravatar():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    adb = adb.User_Col
    for i in adb.find():
        print(i['user_email'])
        # adb.update({'_id': i['_id']}, {'$set': {'user_name': '...'}})


if __name__ == '__main__':
    fix_ol_comment_user_name()
