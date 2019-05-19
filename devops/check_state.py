#!/usr/bin/env python3
# encoding:utf-8

import options
from pymongo import MongoClient
conn = MongoClient()

# print(options.db)
adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])


def check():
    # for db in client.database_names()
    for collection in adb.collection_names():
        print(collection)


# User_Col
# Share_Col

# Like_Col
# Hit_Col
# Collect_Col

# Comment_Col
# Viewpoint_Col
# Tag_Col
# Admin_Col
# Feedback_Col

# Webcache_Col

def check2():
    # print(n, n2)
    n = adb.User_Col.find().count()
    n2 = adb.User_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Share_Col.find().count()
    n2 = adb.Share_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Like_Col.find().count()
    n2 = adb.Like_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Hit_Col.find().count()
    n2 = adb.Hit_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Collect_Col.find().count()
    n2 = adb.Collect_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Comment_Col.find().count()
    n2 = adb.Comment_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Viewpoint_Col.find().count()
    n2 = adb.Viewpoint_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Tag_Col.find().count()
    n2 = adb.Tag_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Admin_Col.find().count()
    n2 = adb.Admin_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Feedback_Col.find().count()
    n2 = adb.Feedback_Col.find().sort('_id', -1)[0]['id']
    assert n == n2
    n = adb.Webcache_Col.find().count()
    n2 = adb.Webcache_Col.find().sort('_id', -1)[0]['id']
    assert n == n2


# check()
check2()
