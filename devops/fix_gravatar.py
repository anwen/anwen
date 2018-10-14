#!/usr/bin/env python3
# encoding:utf-8
from pymongo import MongoClient
import sys
import os
conn = MongoClient()
sys.path.append('.')
from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like
import options


def fix_ol_gravatar():
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    adb = adb.User_Col
    for i in adb.find():
        email = i['user_email']
        if email.endswith('@wechat'):
            continue
        print(email)
        user_id = i['id']
        size = 132
        # default gravatar
        # http://www.gravatar.com/avatar/?d=404
        # http://www.gravatar.com/avatar/?d=identicon
        # http://www.gravatar.com/avatar

        avatar_dir = 'static/avatar'
        avatar_path = '%s/%s_%s.jpg' % (avatar_dir, user_id, size)
        if os.path.isfile(avatar_path):
            print(avatar_path)
        else:
            gravatar_id = hashlib.md5(email.lower().encode('u8')).hexdigest()
            link = "http://www.gravatar.com/avatar/%s?size=%s&d=404" % (
                gravatar_id, size)
            try:
                r = requests.get(link)
                if r.status_code == 200:
                    with open(avatar_path, 'wb') as f:
                        for chunk in r.iter_content():
                            f.write(chunk)
            except Exception as e:
                print('Error:', e)
            if os.path.isfile(avatar_path):
                print(avatar_path)


if __name__ == '__main__':
    fix_ol_gravatar()
