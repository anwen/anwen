#!/usr/bin/env python3
# encoding:utf-8

import sys
import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])


def fix():
    n = 1
    for i in adb.Hit_Col_v2.find().sort('_id', 1):
        i['id'] = n
        i['hitnum'] = 1
        adb.Hit_Col.insert(i)
        n += 1


fix()
