# -*- coding:utf-8 -*-
import tornado.web
from options import site_url
from anwen.api_base import JsonHandler
from db import Like, Share, Comment, Viewpoint, Tag, User
import time
# from log import logger
admin_ids = (1, 4, 60, 63, 64, 65, 69, 86)
IMG_BASE = '{}/static/upload/img/'.format(site_url)


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
            user = User.by_sid(user_id)
            if action == 'addlike' and entity.name not in user.user_tags:
                user.user_tags.append(entity.name)
            elif action == 'dellike' and entity.name in user.user_tags:
                user.user_tags.pop(entity.name)
            user.save()

        if action[:3] == 'add':
            entity[_action] += 1
        else:
            entity[_action] -= 1
        entity.save()
        if entity.dislikenum < 0:
            entity.dislikenum = 0
        if entity.likenum < 0:
            entity.likenum = 0
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


class DeletedMyLikeHandler(JsonHandler):

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
        # number = Like.find(cond, {'_id': 0}).count()
        collects = Like.find(cond, {'_id': 0}).sort(
            '_id', -1).limit(per_page).skip((page - 1) * per_page)
        res = []
        for collect in collects:
            # 'status': {'$gte': 1},
            share = Share.find_one({'id': collect.id}, {'_id': 0})
            share = fix_share(share)
            res.append(share)
        self.res = {'articles': res}
        # number=number
        return self.write_json()


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

        # token = self.request.headers.get('Authorization', '')
        # user = self.get_user_dict(token)
        meta_info = self.get_argument("meta_info", 1)

        cond = {
            'user_id': user_id,
            'entity_type': entity_type,
            'likenum': 1,
        }

        likes = Like.find(cond, {'_id': 0}).sort(
            '_id', -1).limit(per_page).skip((page - 1) * per_page)
        new_shares = []

        filter_d = {}
        filter_d['_id'] = 0
        # 白名单里的属性才展示
        filter_d['id'] = 1
        filter_d['images'] = 1
        filter_d['title'] = 1
        filter_d['user_id'] = 1
        filter_d['tags'] = 1
        filter_d['published'] = 1
        filter_d['post_img'] = 1
        for like in likes:
            # 'status': {'$gte': 1},  {'_id': 0}
            share = Share.find_one({'id': like.id}, filter_d)
            user = User.by_sid(share.user_id)
            share['author'] = user.user_name

            share['type'] = 1
            if share.get('post_img'):
                share['type'] = 2
                share['images'] = [IMG_BASE + share['post_img'].replace('_1200.jpg', '_260.jpg')]
                share.pop('post_img')
            else:
                share['images'] = []
            share['published'] = int(share['published'] * 1000)
            new_shares.append(share)

        if meta_info:
            meta = {}
            number = Like.find(cond, {'_id': 0}).count()
            meta['number'] = number

        self.res = {'articles': new_shares}
        self.meta = meta
        return self.write_json()
