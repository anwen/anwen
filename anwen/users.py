# -*- coding:utf-8 -*-
# import time
# import markdown2
# import hashlib
# import tornado.escape
# import tornado.auth
# from tornado import gen
# import options
# import utils
# import utils.douban_auth
# from utils.avatar import get_avatar
# , CommonResourceHandler
from .base import BaseHandler
# , Share, Like
from db import User, Share

# 用户展示
# 发了多少文章
# 头像 user_name user_say user_lang user_tags


class UsersHandler(BaseHandler):

    # @tornado.web.authenticated
    def get(self):
        users = User.find({'user_leaf': {'$gt': 20}}).sort('user_leaf', -1)
        l_users = []
        for user in users:
            # print(user)
            # user.user_say = markdown2.markdown(user.user_say)
            # user.user_jointime = time.strftime(
            #     '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
            # likenum = User.find({'user_id': user._id}).count()
            # user.gravatar = get_avatar(user.user_email, 100)
            # contents = Share.find({'user_id': user.id})
            # if contents.count():
            auser = {}
            auser['user_domain'] = user.user_domain
            auser['user_name'] = user.user_name
            auser['article_num'] = int((user.user_leaf-20)/10)  # contents.count()
            l_users.append(auser)

        self.render('users.html', users=l_users)
