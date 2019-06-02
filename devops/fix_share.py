import copy
import options
from pymongo import MongoClient
conn = MongoClient()


def fix_share_tmp1():
    # 增加编辑推荐时间
    adb = conn.anwen
    adb.authenticate(options.db['username'], options.db['password'])
    for i in adb.Share_Col.find():
        adb.Share_Col.update({'_id': i['_id']}, {'$set': {'suggested': i['published']}})


if __name__ == '__main__':
    fix_share_tmp1()
