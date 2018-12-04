# -*- coding:utf-8 -*-
import time
import tornado.escape
import tornado.auth
from utils.avatar import get_avatar
from .base import BaseHandler
from db import User


class SettingHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user = User.by_sid(self.current_user['user_id'])
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        user.gravatar = get_avatar(user.user_email.encode('u8'), 100)
        self.render('setting.html', user=user)

    @tornado.web.authenticated
    def post(self):
        user = User.by_sid(self.current_user['user_id'])
        user['user_name'] = self.get_argument('name', None)
        user['user_city'] = self.get_argument('city', None)
        user['user_say'] = self.get_argument('say', None)
        user_tags = self.get_argument('tags', '')
        user['user_tags'] = user_tags.split()
        user.save()
        self.redirect('/setting')
