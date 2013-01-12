# -*- coding:utf-8 -*-
import tornado.web
from json import dumps
from anwen.base import BaseHandler
from brain import get_andesay


class AndeHandler(BaseHandler):

    @tornado.web.asynchronous
    def get(self):
        usersay = self.get_argument('usersay', '')
        userip = self.request.remote_ip
        userlang = self.get_user_lang()
        user_id = self.current_user['user_id'] if self.current_user else 0
        method = 'get'
        andesay, andethink = get_andesay(
            usersay, userip, userlang, user_id, method)
        self.render('ande.html', andesay=andesay, andethink=andethink)

    # @tornado.web.asynchronous
    def post(self):
        usersay = self.get_argument('usersay', '')
        userip = self.request.remote_ip
        userlang = self.get_user_lang()
        user_id = self.current_user['user_id'] if self.current_user else 0
        method = 'post'
        andesay, andethink = get_andesay(
            usersay, userip, userlang, user_id, method)

        # print andesay
        # print andethink
        andesay = {
            'andesay': andesay,
            'andethink': andethink,
        }
        andesay = dumps(andesay)
        self.write(andesay)
