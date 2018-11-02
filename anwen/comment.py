# -*- coding:utf-8 -*-
from db import Share, Comment
from anwen.base import BaseHandler, CommonResourceHandler
import markdown2
import tornado.web
from utils.avatar import get_avatar
import tornado.escape


class CommentHandler(BaseHandler):

    def post(self):
        commentbody = self.get_argument("commentbody", None)
        share_id = self.get_argument("share_id", None)
        html = markdown2.markdown(commentbody)
        comment = Comment
        doc = {}
        doc['user_id'] = self.current_user["user_id"]
        doc['share_id'] = int(share_id)
        doc['commentbody'] = commentbody
        comment.new(doc)
        share = Share.by_sid(share_id)
        share.commentnum += 1
        share.save()
        name = tornado.escape.xhtml_escape(self.current_user["user_name"])
        gravatar = get_avatar(self.current_user["user_email"], 50)
        newcomment = ''.join([
            '<div class="comment">',
            '<div class="avatar">',
            '<img src="', gravatar,
            '</div>',
            '<div class="name">', name,
            '</div>',
            '<div class="date" title="at"></div>', html,
            '</div>',
        ])
        self.write(newcomment)


class CommentsHandler(CommonResourceHandler):
    res = Comment
