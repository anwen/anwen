# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from utils import get_tags, get_tags_v2, get_tags_parents, get_tags_v3
# get_tags_v2_by_name
from db import Tag, Share, User
import tornado
import time
import copy
d_tags = get_tags()
d_tags_v2 = get_tags_v2()
d_tags_v3 = get_tags_v3()

d_tags_parents = get_tags_parents()


# get_tags_v2_by_name
class TagsV2Handler(JsonHandler):

    def get(self):
        ver = self.get_argument("ver", 3)
        name = self.get_argument("name", '')
        sid = self.get_argument("id", 0)
        ver = int(ver)
        sid = int(sid)
        # parents [0]
        if name or sid:
            # 具体某个标签
            if not name and sid:
                tag = Tag.by_sid(sid)
                name = tag['name']
            self.res = d_tags_v3.get(name, {})

            if self.res:
                parents = d_tags_parents.get(self.res['name'], {})
                node = d_tags_v3.get(parents, {})
                self.res['parents'] = copy.deepcopy(node)
                self.res['parents'].pop('subs')

                brothers = []
                for sub in copy.deepcopy(node)['subs']:
                    sub.pop('subs')
                    brothers.append(sub)
                self.res['brothers'] = brothers
                if parents:
                    parents_p = d_tags_parents.get(parents, {})
                    if parents_p:
                        node = d_tags_v3.get(parents_p, {})

                        self.res['parents']['parents'] = copy.deepcopy(node)
                        self.res['parents']['parents'].pop('subs')

                        parents_pp = d_tags_parents.get(parents_p, {})
                        if parents_pp:
                            node = d_tags_v3.get(parents_pp, {})
                            self.res['parents']['parents']['parents'] = copy.deepcopy(node)
                            self.res['parents']['parents']['parents'].pop('subs')

                    self.res['articleNumber'] = Share.count_by_tag(self.res['name'])
                    self.res['followerNumber'] = User.find({'user_tags': {'$in': [name]}}).count()
                    self.res['isFollowing'] = False
                    user_id = self.current_user["user_id"] if self.current_user else None
                    if user_id:
                        user = User.by_sid(user_id)
                        if user:
                            # model1
                            self.res['isFollowing'] = name in user['user_tags']
                            # model2 查看like 表
                            # self.res['isFollowing'] = name in user['user_tags']

                    print("self.res['followerNumber']", self.res['followerNumber'])
                tag = Tag.by_name(self.res['name'])

                if tag:
                    self.res['id'] = tag['id']
            else:
                self.res['id'] = -1
        else:
            # 从根节点开始
            if ver == 3:
                self.res = d_tags_v2
                self.res['parents'] = {}  # root
                self.res['articleNumber'] = Share.count_by_tag(self.res['name'])
                tag = Tag.by_name(self.res['name'])  # 7491
                self.res['id'] = -1
                if tag:
                    self.res['id'] = tag['id']
            elif ver == 2:
                self.res = d_tags_v2
                if self.current_user and 'user_id' in self.current_user:
                    user = User.by_sid(self.current_user['user_id'])
                    self.res['watched_tags'] = user['user_tags']
            else:
                self.res = d_tags
        self.write_json()

    @tornado.web.authenticated
    def post(self):
        share_id = self.get_argument("share_id", None)
        tags = self.get_argument("tags", '')
        tags = tags.strip()
        if share_id:
            share = Share.by_sid(share_id)
            if share and tags not in share.tags:
                tags = share.tags + ' ' + tags
                res = {
                    'tags': tags,
                    'updated': time.time(),
                }
                share.update(res)
                share.save()
                tags = tags.split(' ')
                tags = list(set(tags))
                for i in tags:
                    doc = {
                        'name': i,
                        'share_ids': share.id
                    }
                    Tag.new(doc)


class TagsHandler(JsonHandler):

    def get(self):
        ver = self.get_argument("ver", 2)
        ver = int(ver)
        if ver == 2:
            self.res = d_tags_v2
            if self.current_user and 'user_id' in self.current_user:
                user = User.by_sid(self.current_user['user_id'])
                self.res['watched_tags'] = user['user_tags']
        else:
            self.res = d_tags
        self.write_json()


# print(self.current_user)
# print(hasattr(self.current_user, 'user_id'))
# if hasattr(self.current_user, 'user_id'):
# user_id = self.current_user["user_id"]
