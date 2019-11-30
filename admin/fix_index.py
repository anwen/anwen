#!/usr/bin/env python3
# encoding:utf-8
# import sys
import options
from pymongo import MongoClient

conn = MongoClient()
adb = conn.anwen
print(options.db)
adb.authenticate(options.db['username'], options.db['password'])


def add_index():
    print('add_index')

    # r = adb.Share_Col.ensure_index('id', -1)  # ???
    # print(r)
    r = adb.Share_Col.ensure_index('id', 1)
    print(r)
    r = adb.Share_Col.ensure_index('tags', 1)
    print(r)
    r = adb.Share_Col.ensure_index('status', 1)
    print(r)
    r = adb.Share_Col.ensure_index('suggested', -1)
    print(r)
    r = adb.User_Col.ensure_index('user_leaf', -1)
    print(r)


def show_index():
    print('show_index')
    r = adb.Share_Col.index_information()
    print(r.keys())


show_index()
# add_index()
