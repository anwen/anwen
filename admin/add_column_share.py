import copy
import options
from pymongo import MongoClient
conn = MongoClient()


def fix_share_tmp1():
    # 增加编辑推荐时间
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.Share_Col.find():
        if 'suggested' in i:
            continue
        adb.Share_Col.update({'_id': i['_id']}, {'$set': {'suggested': i['published']}})


def fix_share_tmp2():
    # 增加 author
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.Share_Col.find():
        if 'author' in i:
            continue
        adb.Share_Col.update({'_id': i['_id']}, {'$set': {'author': ''}})


if __name__ == '__main__':
    fix_share_tmp2()
