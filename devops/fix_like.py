#!/usr/bin/env python3
# encoding:utf-8
import os
import hashlib
import requests
import sys
from pymongo import MongoClient
conn = MongoClient()
sys.path.append('.')
from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like
import options


def fix_like():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    adb = adb.Like_Col
    for i in adb.find():
        print(i)


if __name__ == '__main__':
    fix_like()
