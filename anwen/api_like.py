# -*- coding:utf-8 -*-
from .api_base import JsonHandler
import tornado.web
from db import Like, Share, Comment, Viewpoint


class LikeHandler(JsonHandler):

    @tornado.web.authenticated
    def post(self, action):
        entity_id = int(self.get_argument("entity_id", 0))
        entity_type = self.get_argument("entity_type", None)
        user_id = self.current_user["user_id"]
        assert action in 'addlike dellike adddislike deldislike'.split()

        _action = action[3:] + 'num'
        if entity_type == 'share':
            entity = Share.by_sid(entity_id)
            # 如果是管理员，需要将status + 1
            if user_id in (60, 63, 64) and action == 'addlike':
                entity['status'] = entity['status'] + 1
        elif entity_type == 'comment':
            entity = Comment.by_sid(entity_id)
        elif entity_type == 'viewpoint':
            entity = Viewpoint.by_sid(entity_id)
        else:
            print('entity_type', entity_type, entity_id)
            return self.write_error(422, 'error params')

        if action[:3] == 'add':
            entity[_action] += 1
        else:
            entity[_action] = 0
        entity.save()

        doc = {
            'user_id': user_id,
            'entity_id': entity_id,
            'entity_type': entity_type,
        }
        Like.change_like(doc, _action, action[:3])

        self.res = {
            'likenum': entity.likenum,
            'dislikenum': entity.dislikenum,
        }
        self.write_json()

    get = post
