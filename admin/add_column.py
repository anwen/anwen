import options
from pymongo import MongoClient
conn = MongoClient()

adb = conn.anwen
if 'username' in options.db:
    adb.authenticate(options.db['username'], options.db['password'])


def fix():
    for i in adb.Tag_Col.find():
        if 'likenum' not in i:
            adb.Tag_Col.update({'_id': i['_id']}, {'$set': {'likenum': 0}})
            adb.Tag_Col.update({'_id': i['_id']}, {'$set': {'dislikenum': 0}})

    for i in adb.User_Col.find():
        if 'user_tags' not in i:
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_tags': []}})


def fix2():
    for i in adb.User_Col.find():
        tags = i['user_tags']
        if tags:
            print(tags)


if __name__ == '__main__':
    fix()
    fix2()
