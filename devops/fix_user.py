#!/usr/bin/env python3
# encoding:utf-8
import options
from pymongo import MongoClient
conn = MongoClient()


def fix_user():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    n = 1
    for i in adb.User_Col.find().sort('_id', 1):
        idx = i['id']
        print(n, idx)
        assert n == idx
        n += 1
    print(adb.User_Col.find().count())
    r = adb.User_Col.find()
    print(len(list(r)))
    print(r.count())


if __name__ == '__main__':
    fix_user()
