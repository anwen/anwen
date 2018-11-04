# -*- coding:utf-8 -*-
import json
from db import Feedback, Share, Viewpoint, User
from pymongo import DESCENDING
from anwen.base import BaseHandler, CommonResourceHandler
import datetime
import markdown2


class ViewPointHandler(BaseHandler):

    def post(self):
        aview = self.get_argument("aview", None)
        share_id = self.get_argument("share_id", None)
        if aview:
            doc = {}
            doc['share_id'] = int(share_id)
            doc['aview'] = aview
            if Viewpoint.find_one(doc):
                print('repeat')
                return
            doc['user_id'] = self.current_user["user_id"]
            # doc['aview'] = aview
            Viewpoint.new(doc)
            self.write(aview)


class FeedHandler(BaseHandler):

    def get(self):
        share_res = Share.find()
        shares = []
        for share in share_res:
            user = User.by_sid(share.user_id)
            share.name = user.user_name
            share.published = datetime.datetime.fromtimestamp(share.published)
            share.updated = datetime.datetime.fromtimestamp(share.updated)
            share.domain = user.user_domain
            share.content = markdown2.markdown(share.markdown)
            shares.append(share)

        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", shares=shares)


class EditHandler(BaseHandler):

    def get(self):
        self.render("edit.html")


class ErrHandler(BaseHandler):

    def get(self):
        self.render('error.html', status_code=404)


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

    def get(self):
        action = self.request.path[7:]
        share_res = Share.find()
        if 'add' in action:
            do, share_id, suggestscore = action.split('!')
            share = Share.by_sid(share_id)
            share.suggestscore = float(suggestscore)
            share.save()
        for share in share_res:
            share.score = 0.001 * share.hitnum + share.likenum - \
                share.dislikenum + 0.5 * share.commentnum - \
                share.status + share.suggestscore + 0.5 * share.id
            share.save()
        # self.write_json({'objs': list(Share.find().sort('score',
        # DESCENDING))})
        share_res = Share.find().sort('score', DESCENDING)
        display = ''
        display += '<p>score sugg hit like dis comment status title id</p>'
        for share in share_res:
            display += '<p>%s  %s  %s  %s  %s  %s  %s  %s  %s</p>' % (
                share.score,
                share.suggestscore,
                share.hitnum,
                share.likenum,
                share.dislikenum,
                share.commentnum,
                share.status,
                share.title,
                share.id)
        self.write(display)


class AppHandler(BaseHandler):

    def get(self):
        self.render("pages/app.html")


class TogetherHandler(BaseHandler):

    def get(self):
        self.render("pages/together.html")
