#!/usr/bin/env python3
# encoding:utf-8
import copy
import options
from pymongo import MongoClient
from utils import get_tags_parent
conn = MongoClient()


def fix_user():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.Share_Col.find().sort('_id', 1):
        print(i['id'])


if __name__ == '__main__':
    fix_user()
