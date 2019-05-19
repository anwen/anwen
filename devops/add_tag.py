#!/usr/bin/env python3
# encoding:utf-8

import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])


def check():
    for i in adb.Share_Col.find().sort('_id', 1):
        if i['status'] >= 1:
            if i['tags'] == []:
                print(i['id'])
                print(i['title'])


check()
