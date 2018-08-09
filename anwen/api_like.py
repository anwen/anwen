# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from db import Like, Share, Comment, Viewpoint


class LikeHandler(JsonHandler):

    def get(self, action):
        # return self.post(action)
        entity_id = int(self.get_argument("entity_id", 0))
        entity_type = self.get_argument("entity_type", None)
        print(action, entity_id, entity_type)
        user_id = self.current_user["user_id"]
        doc = {
            'user_id': user_id,
            'entity_id': entity_id,
            'entity_type': entity_type,
        }
        newlikes = None
        assert action in 'addlike dellike adddislike deldislike'.split()
        _action = action[3:] + 'num'
        Like.change_like(doc, _action)
        if entity_type == 'share':
            entity = Share.by_sid(entity_id)
        elif entity_type == 'comment':
            entity = Comment.by_sid(entity_id)
        elif entity_type == 'viewpoint':
            entity = Viewpoint.by_sid(entity_id)
        else:
            print('entity_type', entity_type, entity_id)
            return self.write_error(422, 'error params')
        if action == 'addlike':
            entity.likenum += 1
            newlikes = str(entity.likenum)
        elif action == 'dellike':
            entity.likenum -= 1
            newlikes = str(entity.likenum)
        elif action == 'adddislike':
            entity.dislikenum += 1
            newlikes = str(entity.dislikenum)
        elif action == 'deldislike':
            entity.dislikenum -= 1
            newlikes = str(entity.dislikenum)
        entity.save()
        self.res = {'newlikes': newlikes}
        self.write_json()

    def post(self, action):
        return self.get(action)
        self.res = {'ok': 1}
        self.write_json()
        return
