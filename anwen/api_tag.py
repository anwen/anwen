# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from utils import get_tags, get_tags_v2
from db import Tag, Share, User
import tornado
import time

d_tags = get_tags()
d_tags_v2 = get_tags_v2()


class TagsHandler(JsonHandler):

    def get(self):
        ver = self.get_argument("ver", 2)
        ver = int(ver)
        if ver == 2:
            self.res = d_tags_v2
            print(self.current_user)
            # print(hasattr(self.current_user, 'user_id'))
            # if hasattr(self.current_user, 'user_id'):
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
        # user_id = self.current_user["user_id"]
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
