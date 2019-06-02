#!/usr/bin/env python3
# encoding:utf-8

import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])


r = adb.Share_Col.ensure_index('id', 1)
print(r)
r = adb.Share_Col.ensure_index('id', -1)  # ???
print(r)
r = adb.Share_Col.ensure_index('tags', 1)
print(r)
r = adb.Share_Col.ensure_index('status', 1)
print(r)
r = adb.Share_Col.index_information()
print(r.keys())
