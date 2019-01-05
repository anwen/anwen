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
    d_parent = get_tags_parent()
    print(d_parent)
    for i in adb.Share_Col.find():
        if i['tags']:
            tags = i['tags']
            new_tags = copy.deepcopy(tags)
            new_tags.append('|')
            for tag in tags:
                if tag in d_parent and d_parent[tag] not in new_tags:
                    new_tags.append(d_parent[tag])
            if new_tags[-1] != '|':
                if i['status'] >= 1:
                    print(' '.join(new_tags))
                    adb.Share_Col.update({'_id': i['_id']}, {'$set': {'tags': new_tags}})
    return
    for i in adb.Share_Col.find():
        if isinstance(i['tags'], str):
            print(i['tags'])
            # adb.Share_Col.update({'_id': i['_id']}, {'$set': {'tags': i['tags'].split()}})
        if not i['sharetype']:
            print(i['id'])
            print(i['title'])
            print(i['link'])
            print(i['sharetype'])


if __name__ == '__main__':
    fix_share()
