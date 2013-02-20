# -*- coding:utf-8 -*-

import json
from base import BaseHandler, CommonResourceHandler
from db import Feedback


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
