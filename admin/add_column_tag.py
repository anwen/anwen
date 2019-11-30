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
        if 'user_tags' not in i or i['user_tags'] is None:
            adb.User_Col.update({'_id': i['_id']}, {'$set': {'user_tags': []}})


def fix2():
    for i in adb.User_Col.find():
        tags = i['user_tags']
        if not tags:
            continue
        print(tags)
        continue
        for tag in tags:
            doc = adb.Tag_Col.find_one({'name': tag})
            if not doc:
                print('tag not exist:', tag)
                continue

            continue
            adb.Tag_Col.update({'_id': doc['_id']}, {'$inc': {'likenum': 1}})
            n = adb.Like_Col.find().count()
            adb.Like_Col.insert(
                {
                    'id': n+1,
                    'user_id': i['id'],
                    'entity_id': doc['id'],
                    'likenum': 1,
                    'entity_type': 'tag',
                    'entity_type': 'tag',
                }
            )


# tag in
# user []  第一个接口
# like likenum  以这个接口为准
# tag  likenum  冗余储存

if __name__ == '__main__':
    fix()
    fix2()
