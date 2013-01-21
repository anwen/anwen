# -*- coding:utf-8 -*-

import hashlib
import markdown2
import time
import tornado.escape

from utils.avatar import get_avatar
from base import BaseHandler
from db import User, Share
from base import CommonResourceHandler


class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/")
        self.render("login.html")

    def post(self):
        email = self.get_argument("email", '')
        password = self.get_argument("password", '')
        password = hashlib.md5(password).hexdigest()
        res = User.by_email_pass(email, password)
        if res:
            user = {'user_id': res.id,
                    'user_name': res.user_name,
                    'user_email': res.user_email,
                    'user_domain': res.user_domain}
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.write('密码错误或用户不存在，请重新注册或登录')


class JoinusHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/")
        self.render("joinus.html")

    def post(self):
        name = self.get_argument("name", '')
        password = self.get_argument("password", '')
        password = hashlib.md5(password).hexdigest()
        email = self.get_argument("email", '')
        domain = self.get_argument("domain", '')
        if domain == '':
            domain = name
        if User.find({'user_email': email}).count() > 0:
            self.write('用户已经存在，请直接登录')
            self.redirect("/login")
        else:
            res = User
            res['id'] = res.find().count() + 1
            res['user_name'] = name
            res['user_pass'] = password
            res['user_email'] = email
            res['user_domain'] = domain
            res.new(res)
            user = {'user_id': res.id,
                    'user_name': res.user_name,
                    'user_email': res.user_email,
                    'user_domain': res.user_domain}
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.redirect(self.get_argument("next", "/"))


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument("next", "/"))

    def post(self):
        self.get()


class UserhomeHandler(BaseHandler):
    def get(self, name):
        user = User.find_one({'user_domain': name})
        user.user_say = markdown2.markdown(user.user_say)
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        likenum = User.find({'user_id': user._id}).count()
        user.gravatar = get_avatar(user.user_email, 100)
        self.render("userhome.html", user=user, likenum=likenum)

    def post(self):
        self.get()


class UserlikeHandler(BaseHandler):
    def get(self, name):
        user = User.find_one({'user_domain': name})
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        likes = User.find({'user_id': user._id})
        likenum = likes.count()
        for like in likes:
            share = Share.by_id(like.share_id)
            like.title = share.title
            like.id = share.id
            like.type = share.sharetype
        user.gravatar = get_avatar(user.user_email, 100)
        self.render("userlike.html", user=user, likenum=likenum, likes=likes)

    def post(self):
        self.get()


class SettingHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = User.by_sid(self.current_user["user_id"])
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        user.gravatar = get_avatar(user.user_email, 100)
        self.render("setting.html", user=user)

    @tornado.web.authenticated
    def post(self):
        user = User.by_sid(self.current_user["user_id"])
        user['user_name'] = self.get_argument("name", None)
        user['user_city'] = self.get_argument("city", None)
        user['user_say'] = self.get_argument("say", None)
        user.save()
        self.redirect("/setting")


class ChangePassHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = User.by_sid(self.current_user["user_id"])
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        user.gravatar = get_avatar(user.user_email, 100)
        self.render("changepass.html", user=user)

    @tornado.web.authenticated
    def post(self):
        oldpass = self.get_argument("oldpass", '')
        newpass = self.get_argument("newpass", '')
        newpass = hashlib.md5(newpass).hexdigest()
        user = User.by_sid(self.current_user["user_id"])
        if user.user_pass == hashlib.md5(oldpass).hexdigest():
            user = User.by_sid(self.current_user["user_id"])
            user['user_pass'] = newpass
            user.save()
            self.redirect("/setting")
        else:
            self.write('Wrong password')


class MemberHandler(BaseHandler):
    def get(self):
        members = User.find()
        self.render("member.html", members=members)


class UsersHandler(CommonResourceHandler):
    res = User

    def pre_post(self, json_arg):
        if self.res.by_useremail(json_arg['user_email']):
            self.send_error(409)
