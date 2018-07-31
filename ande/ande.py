# -*- coding:utf-8 -*-

from json import dumps
from anwen.base import BaseHandler
from markdown2 import markdown
from ande.brain import get_andesay


class AndeHandler(BaseHandler):

    def get(self):
        q = self.get_argument('q', '')
        usersay = self.get_argument('usersay', '')
        userip = self.request.remote_ip
        userlang = self.get_user_lang()
        user_id = self.current_user['user_id'] if self.current_user else 0
        method = 'get'
        andesay = get_andesay(
            usersay, userip, userlang, user_id, method)
        if q:
            self.write(andesay)
        else:
            self.render('ande.html', andesay=andesay)

    # @tornado.web.asynchronous
    def post(self):
        usersay = self.get_argument('usersay', '')
        userip = self.request.remote_ip
        userlang = self.get_user_lang()
        user_id = self.current_user['user_id'] if self.current_user else 0
        method = 'post'
        andesay = get_andesay(
            usersay, userip, userlang, user_id, method)

        # print(andesay)
        andesay = {
            'andesay': andesay,
        }
        andesay = dumps(andesay)
        self.write(andesay)
