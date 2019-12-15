#!/usr/bin/env python3
# encoding:utf-8
# import sys
import options
from pymongo import MongoClient
import pymongo
from pymongo import ASCENDING, DESCENDING
# from pymongo import IndexModel
# , ASCENDING, DESCENDING

conn = MongoClient()
adb = conn.anwen
print(options.db)

if 'username' in options.db:
    adb.authenticate(options.db['username'], options.db['password'])


print(ASCENDING)
print(DESCENDING)
# ensure_index


# >>> from pymongo import IndexModel, ASCENDING, DESCENDING
# >>> index1 = IndexModel([("hello", DESCENDING),
# ...                      ("world", ASCENDING)], name="hello_world")
# >>> index2 = IndexModel([("goodbye", DESCENDING)])
# >>> db.test.create_indexes([index1, index2])

def add_index():
    print('add_index')
    # r = adb.Share_Col.drop_index('id_1')
    # print(r)
    r = adb.Share_Col.create_index('id', pymongo.ASCENDING, unique=True)
    print(r)
    r = adb.Share_Col.create_index('published', DESCENDING)
    print(r)
    r = adb.Share_Col.create_index('sharetype', DESCENDING)
    print(r)
    r = adb.Share_Col.create_index('user_id', ASCENDING)
    print(r)
    r = adb.Share_Col.create_index('title', ASCENDING)
    print(r)

    r = adb.Share_Col.create_index('tags', 1)
    print(r)
    r = adb.Share_Col.create_index('status', 1)
    print(r)
    r = adb.Share_Col.create_index('suggested', -1)
    print(r)
    r = adb.User_Col.create_index('user_leaf', -1)
    print(r)

    r = adb.User_Col.create_index('id', DESCENDING, unique=True)
    print(r)

    r = adb.User_Col.create_index('user_tags', DESCENDING)
    print('user_tags', r)

    r = adb.Hit_Col.create_index('user_id', DESCENDING)
    print(r)
    adb.Hit_Col.reindex()

    r = adb.Like_Col.create_index('user_id', DESCENDING)
    print(r)
    # adb.Like_Col.reindex()

    # index1 = IndexModel([("user_id", ASCENDING), ("entity_type", ASCENDING)], name="user_id_entity_type")
    # db.test.create_indexes([index1, index2])
    r = adb.Like_Col.create_index(
        [("user_id", ASCENDING), ("entity_type", ASCENDING)],
        name="user_id_entity_type"
    )
    print(r)


def show_index():
    print('show_index')
    print('Share:')
    r = adb.Share_Col.index_information()
    for k in r:
        print(k, r[k]['key'])
    print('User:')
    r = adb.User_Col.index_information()
    for k in r:
        print(k, r[k]['key'])
    print('Hit:')
    r = adb.Hit_Col.index_information()
    for k in r:
        print(k, r[k]['key'])


show_index()
add_index()

# https://api.mongodb.com/python/current/api/pymongo/collection.html
