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


def check2():
    n = adb.User_Col.find().count()
    n2 = adb.User_Col.find().sort('_id', -1)[0]['id']
    print(n)
    print(n2)


# check()
check2()
