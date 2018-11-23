# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from utils import get_tags
from db import Tag, Share
import tornado
import time


class TagsHandler(JsonHandler):

    def get(self):
        d_tags = get_tags()
        self.res = d_tags
        self.write_json()

    @tornado.web.authenticated
    def post(self):
        share_id = self.get_argument("id", None)
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
