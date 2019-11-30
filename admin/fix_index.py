#!/usr/bin/env python3
# encoding:utf-8
# import sys
import options
from pymongo import MongoClient
import pymongo

conn = MongoClient()
adb = conn.anwen
print(options.db)

if 'username' in options.db:
    adb.authenticate(options.db['username'], options.db['password'])


print(pymongo.ASCENDING)
print(pymongo.DECENDING)
# ensure_index


def add_index():
    print('add_index')
    r = adb.Share_Col.create_index('id', -1)
    print(r)

    # result = db.profiles.create_index([('user_id', pymongo.ASCENDING)],
    # ...                                   unique=True)

    r = adb.Share_Col.create_index('id', 1)
    print(r)
    r = adb.Share_Col.create_index('tags', 1)
    print(r)
    r = adb.Share_Col.create_index('status', 1)
    print(r)
    r = adb.Share_Col.create_index('suggested', -1)
    print(r)

    r = adb.User_Col.create_index('user_leaf', -1)
    print(r)


def show_index():
    print('show_index')
    r = adb.Share_Col.index_information()
    # print('Share', r.keys(), r.values())
    print('Share:')
    for k in r:
        print(k, r[k]['key'])


show_index()
add_index()
