#!/usr/bin/env python3
# encoding:utf-8
# import os
# import hashlib
# import requests
import sys
from pymongo import MongoClient
conn = MongoClient()
sys.path.append('.')
# from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like
import options

# 对于like, 冗余储存


def fix_like():
    print(options.db)
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])

    # 数据库修复，默认为0
    for i in adb.Comment_Col.find():
        if 'likenum' not in i:
            adb.Comment_Col.update({'_id': i['_id']}, {'$set': {'likenum': 0}})
            adb.Comment_Col.update({'_id': i['_id']}, {'$set': {'dislikenum': 0}})
            print('done')

    # 修正喜欢次数
    print('like special case both 0')
    for i in adb.Like_Col.find():
        assert i['likenum'] in (0, 1)
        assert i['dislikenum'] in (0, 1)
        if i['likenum'] == i['dislikenum'] == 0:
            print(i)
    print('like special case both 1')
    for i in adb.Like_Col.find():
        if i['likenum'] == i['dislikenum'] == 1:
            print(i)
    print('dislike')
    for i in adb.Like_Col.find({}, {'_id': 0}):
        if i['dislikenum']:
            print(i)
    print('like')
    for i in adb.Like_Col.find({}, {'_id': 0}):
        if i['likenum']:
            print(i)
    print('like share')
    for i in adb.Like_Col.find({}, {'_id': 0}):
        if i['likenum'] and i['entity_type'] == 'share':
            print(i)

    # for i in adb.Like_Col.find():
    #     if i['entity_type'] == 'comment':
    #         print(i)
    #         entity_id = i['entity_id']
    #         d = adb.Comment_Col.find_one({'id': entity_id})
    #         print(d)
    #         adb.Comment_Col.update({'id': entity_id}, {'$inc': {'likenum': i['likenum']}})
    #         d = adb.Comment_Col.find_one({'id': entity_id})
    #         print(d)


if __name__ == '__main__':
    fix_like()
