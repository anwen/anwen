import options
from pymongo import MongoClient
conn = MongoClient()


def fix():
    # 增加 author
    adb = conn.anwen
    if 'username' in options.db:
        adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.Tag_Col.find():
        adb.Tag_Col.update({'_id': i['_id']}, {'$set': {'likenum': 0}})
        adb.Tag_Col.update({'_id': i['_id']}, {'$set': {'dislikenum': 0}})


if __name__ == '__main__':
    fix()
