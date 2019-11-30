# -*- coding:utf-8 -*-
import tornado.web
from anwen.api_base import JsonHandler
from db import Like, Share, Comment, Viewpoint, Tag
import time
# from log import logger
admin_ids = (1, 4, 60, 63, 64, 65, 69, 86)


class LikeHandler(JsonHandler):

    @tornado.web.authenticated
    def post(self, action):
        entity_id = int(self.get_argument("entity_id", 0))
        entity_type = self.get_argument("entity_type", None)
        user_id = self.current_user["user_id"]
        assert action in 'addlike dellike adddislike deldislike'.split()
        assert entity_type in 'share comment viewpoint tag'.split()
        _action = action[3:] + 'num'
        doc = {
            'user_id': user_id,
            'entity_id': entity_id,
            'entity_type': entity_type,
        }
        is_changed = Like.change_like(doc, _action, action[:3])
        # 冗余储存 没有做成事件绑定，需要定期校验修复
        if entity_type == 'share':
            entity = Share.by_sid(entity_id)
            # 如果是管理员，需要将status + 1
            # 64=kp 65=kp email
            # 63=lb # 60=xie
            if is_changed and user_id in admin_ids:
                if action == 'addlike':
                    if entity['status'] == 0:
                        entity['suggested'] = time.time()
                    entity['status'] += 1
                elif action == 'adddislike':
                    entity['status'] -= 1
                elif action == 'deldislike':
                    entity['status'] += 1
                else:
                    entity['status'] -= 1
        elif entity_type == 'comment':
            entity = Comment.by_sid(entity_id)
        elif entity_type == 'viewpoint':
            entity = Viewpoint.by_sid(entity_id)
        elif entity_type == 'tag':
            entity = Tag.by_sid(entity_id)
        if action[:3] == 'add':
            entity[_action] += 1
        else:
            entity[_action] -= 1
        entity.save()
        self.res = {
            'likenum': entity.likenum,
            'dislikenum': entity.dislikenum,
        }
        self.write_json()

    get = post


def fix_share(share):  # time
    if share['post_img']:
        share['post_img'] = 'https://anwensf.com/static/upload/img/' + \
            share['post_img'].replace('_1200.jpg', '_260.jpg')
    share['published'] = int(share['published'] * 1000)
    share['updated'] = int(share['updated'] * 1000)
    return share


class MyLikeHandler(JsonHandler):

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
            'likenum': 1,
        }
        number = Like.find(cond, {'_id': 0}).count()
        collects = Like.find(cond, {'_id': 0}).sort(
            '_id', -1).limit(per_page).skip((page - 1) * per_page)
        res = []
        for collect in collects:
            # 'status': {'$gte': 1},
            share = Share.find_one({'id': collect.id}, {'_id': 0})
            share = fix_share(share)
            res.append(share)
        self.res = {'likes': res}
        return self.write_json(number=number)
