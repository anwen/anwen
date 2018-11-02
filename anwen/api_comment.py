# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from db import Share, Comment, User
import tornado.escape
from utils.avatar import get_avatar_by_wechat


class CommentHandler(JsonHandler):

    def get(self):  # list all comments of a article
        # log api usage
        share_id = self.get_argument("share_id", None)
        comments = []
        comment_res = Comment.find({'share_id': int(share_id)})
        for comment in comment_res:
            comment = dict(comment)
            comment['_id'] = str(comment['_id'])
            comment['commenttime'] = int(comment['commenttime'] * 1000)
            comment['avatar'] = get_avatar_by_wechat(comment['user_id'])
            # user = User.by_sid(comment['user_id'])
            # get_avatar(user.user_email, 50)

            comments.append(comment)
        self.res = {
            'comments': comments,
        }
        self.write_json()

    @tornado.web.authenticated
    def post(self):
        commentbody = self.get_argument("commentbody", None)
        share_id = self.get_argument("share_id", None)
        comment = Comment
        doc = {}
        doc['user_id'] = self.current_user["user_id"]
        user = User.by_sid(self.current_user["user_id"])
        # user_name in current_user is not the newest
        doc['user_name'] = user["user_name"]
        doc['share_id'] = int(share_id)
        doc['commentbody'] = commentbody
        comment.new(doc)
        share = Share.by_sid(share_id)
        share.commentnum += 1
        share.save()
        # name = tornado.escape.xhtml_escape(self.current_user["user_name"])
        # gravatar = get_avatar(self.current_user["user_email"], 50)
        self.res = {
            'success': True,
        }
        self.write_json()
