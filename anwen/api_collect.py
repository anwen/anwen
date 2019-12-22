# -*- coding:utf-8 -*-
# 收藏接口，从like接口fork而来
import tornado.web
from anwen.api_base import JsonHandler
from db import Collect, Share


class CollectHandler(JsonHandler):

    @tornado.web.authenticated
    def post(self, action):
        entity_id = int(self.get_argument("entity_id", 0))
        entity_type = self.get_argument("entity_type", None)
        user_id = self.current_user["user_id"]
        assert action in 'addcollect delcollect'.split()
        assert entity_type in 'share comment viewpoint'.split()
        _action = action[3:] + 'num'
        doc = {
            'user_id': user_id,
            'entity_id': entity_id,
            'entity_type': entity_type,
        }
        is_changed = Collect.change_collect(doc, _action, action[:3])
        assert is_changed
        self.write_json()

    # get = post


def fix_share(share):  # time
    if share['post_img']:
        share['post_img'] = 'https://anwensf.com/static/upload/img/' + \
            share['post_img'].replace('_1200.jpg', '_260.jpg')
    share['published'] = int(share['published'] * 1000)
    share['updated'] = int(share['updated'] * 1000)
    return share


class MyCollectHandler(JsonHandler):

    @tornado.web.authenticated
    def get(self):
        page = self.get_argument("page", 1)
        per_page = self.get_argument("per_page", 10)
        per_page = int(per_page)
        page = int(page)
        entity_type = self.get_argument("entity_type", 'share')
        user_id = self.current_user["user_id"]
        assert entity_type in 'share comment viewpoint'.split()
        cond = {
            'user_id': user_id,
            'entity_type': entity_type,
            'collectnum': 1,
        }
        number = Collect.find(cond, {'_id': 0}).count()
        collects = Collect.find(cond, {'_id': 0}).sort(
            '_id', -1).limit(per_page).skip((page - 1) * per_page)
        res = []
        print(collects.count())
        for collect in collects:
            # 'status': {'$gte': 1},
            share = Share.find_one({'id': collect.id}, {'_id': 0})
            share = fix_share(share)
            res.append(share)
        self.res = {'articles': res}
        # number=number
        return self.write_json()
