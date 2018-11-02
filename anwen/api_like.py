# -*- coding:utf-8 -*-
import tornado.web
from anwen.api_base import JsonHandler
from db import Like, Share, Comment, Viewpoint


class LikeHandler(JsonHandler):

    @tornado.web.authenticated
    def post(self, action):
        entity_id = int(self.get_argument("entity_id", 0))
        entity_type = self.get_argument("entity_type", None)
        user_id = self.current_user["user_id"]
        assert action in 'addlike dellike adddislike deldislike'.split()
        assert entity_type in 'share comment viewpoint'.split()

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
            # 63=lb
            # 60=xie
            if is_changed and user_id in (1, 60, 63, 64, 65):
                if action == 'addlike':
                    entity['status'] += 1
                else:
                    entity['status'] -= 1
        elif entity_type == 'comment':
            entity = Comment.by_sid(entity_id)
        elif entity_type == 'viewpoint':
            entity = Viewpoint.by_sid(entity_id)
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

    # get = post
