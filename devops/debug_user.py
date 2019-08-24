#!/usr/bin/env python3
# encoding:utf-8

import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])


r = adb.User_Col.find({'user_leaf': {'$gt': 0}}).count()
print(r)
