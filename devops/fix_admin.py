#!/usr/bin/env python3
# encoding:utf-8

import options
from pymongo import MongoClient
conn = MongoClient()


def fix():
    print(options.db)
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])

    doc = adb.User_Col.find_one({'id': 60})
    print(doc)
    adb.User_Col.update({'_id': doc['_id']}, {'$set': {'user_tags': []}})


fix()
