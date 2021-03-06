#!/usr/bin/env python3
# encoding:utf-8
# import os
# import hashlib
# import requests
import options
from pymongo import MongoClient
conn = MongoClient()
# from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like
# 对于like, 冗余储存


def fix_like():
    print(options.db)
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])

    if 0:
        # 数据库修复，默认为0
        for i in adb.Comment_Col.find():
            if 'likenum' not in i:
                adb.Comment_Col.update({'_id': i['_id']}, {'$set': {'likenum': 0}})
                adb.Comment_Col.update({'_id': i['_id']}, {'$set': {'dislikenum': 0}})
                print('done')

    # 验证喜欢次数
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

    print('Share_Col')
    for i in adb.Share_Col.find():
        if i['status'] == -999:
            continue
        # if i['status'] == 0:
        #     continue
        # print(i['status'], i['title'], i['id'])
        # if i['status'] == -1:
        # if i['status'] < 1:
        # adb.Share_Col.update({'_id': i['_id']}, {'$set': {'status': 0}})
        n = 0
        for j in adb.Like_Col.find({'entity_type': 'share', 'entity_id': i['id']}):
            if j['user_id'] in (1, 60, 63, 64, 65, 69):
                if j['dislikenum'] == 0:
                    adb.Like_Col.update({'_id': j['_id']}, {'$set': {'likenum': 1}})
            if j['user_id'] in (1, 60, 63, 64, 65, 69) and j['likenum'] > 0:
                if j['likenum'] > 0:
                    n += 1
        if n != i['status']:
            print(n, i['status'], i['title'], i['id'])
            # adb.Share_Col.update({'_id': i['_id']}, {'$set': {'status': n}})

    # for i in adb.Like_Col.find():
    #     if i['entity_type'] == 'comment':
    #         print(i)
    #         entity_id = i['entity_id']
    #         d = adb.Comment_Col.find_one({'id': entity_id})
    #         print(d)
    #         adb.Comment_Col.update({'id': entity_id}, {'$inc': {'likenum': i['likenum']}})
    #         d = adb.Comment_Col.find_one({'id': entity_id})
    #         print(d)

    print('user_id 1 like:')
    for j in adb.Like_Col.find({'entity_type': 'share'}):
        if j['user_id'] == 1 and j['likenum'] > 0:
            doc = adb.Share_Col.find({'id': j['entity_id']})[0]
            if doc['user_id'] != 1:
                print(doc['id'], doc['title'])


if __name__ == '__main__':
    fix_like()
