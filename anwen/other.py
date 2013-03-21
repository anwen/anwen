# -*- coding:utf-8 -*-

import json
from base import BaseHandler, CommonResourceHandler
from db import Feedback, Share
from pymongo import DESCENDING


class EditHandler(BaseHandler):
    def get(self):
        self.render("edit.html")


class ErrHandler(BaseHandler):
    def get(self):
        self.render("404.html")


class FeedbackHandler(CommonResourceHandler):
    res = Feedback

    def post(self):
        user_email = self.current_user.get(
            "user_email") if self.current_user else None
        content = self.get_argument("content", None)
        doc = {
            'user_email': user_email,
            'content': content
        }
        self.res.new(doc)
        data = {}
        data['status'] = 'y'
        data = json.dumps(data)
        self.write(data)

    def post_get(self, obj):
        if self.current_user and self.current_user.get("user_id") == 1:
            return obj


class ScoreHandler(BaseHandler):
    res = Share

    def get(self, action):
        action = self.request.path[7:]
        print action
        share_res = Share.find()
        # print share_res.count()
        if 'add' in action:
            do, share_id, suggestscore = action.split('!')
            share = Share.by_sid(share_id)
            print suggestscore
            share.suggestscore = float(suggestscore)
            print share.suggestscore
            share.save()
        # if action == 'update':
        for share in share_res:
            share.score = 0.001 * share.hitnum + share.likenum - \
                share.dislikenum + 0.5 * share.commentnum - \
                share.status + share.suggestscore + 0.5 * share.id
            print share.score, share.title
            share.save()
        # self.write_json({'objs': list(Share.find().sort('score',
        # DESCENDING))})
        share_res = Share.find().sort('score', DESCENDING)
        display = ''
        display += '<p>score  suggest hit like dislike comment status title id </p>'
        for share in share_res:
            display += '<p>%s  %s  %s  %s  %s  %s  %s  %s  %s</p>' % (
                share.score, share.suggestscore, share.hitnum, share.likenum, share.dislikenum, share.commentnum, share.status, share.title, share.id)
        self.write(display)
