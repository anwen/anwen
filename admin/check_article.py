#!/usr/bin/env python3
# encoding:utf-8

import sys
import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])


def check():
    for i in adb.Share_Col.find().sort('_id', 1):
        print('\t'.join([str(i['id']), i['title']]))


check()
