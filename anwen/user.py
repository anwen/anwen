# -*- coding:utf-8 -*-

import time
import hashlib
import markdown2
import tornado.escape
import tornado.auth
from tornado import gen
import options
import utils
import utils.douban_auth
from utils.avatar import get_avatar
from .base import BaseHandler, CommonResourceHandler
from db import User, Share


class LoginHandler(BaseHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
        self.render('login.html')

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        password = utils.make_password(password)
        doc = User.by_email_pass(email, password)
        if doc:
            user_info = {
                'user_id': doc.id,
                'user_name': doc.user_name,
                'user_email': doc.user_email,
                'user_domain': doc.user_domain}
            self.set_secure_cookie(
                'user', tornado.escape.json_encode(user_info))
            self.redirect(self.get_argument('next', '/'))
            return
        self.authenticate_redirect()
        # self.redirect('/login')  # self.write('密码错误或用户不存在，请重新注册或登录')


class DoubanLoginHandler(BaseHandler, utils.douban_auth.DoubanMixin):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument('code', None):
            user = yield self.get_authenticated_user(
                redirect_uri='http://anwensf.com',
                client_id=options.douban['douban_api_key'],
                client_secret=options.douban['douban_api_secret'],
                code=self.get_argument('code'))
            print(user)
            self.render('/', user=user)
        else:
            self.authorize_redirect(
                redirect_uri='http://anwensf.com',
                client_id=options.douban['douban_api_key']
            )


class GoogleLoginHandler(BaseHandler, tornado.auth.GoogleMixin):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument("openid.mode", None):
            user = yield self.get_authenticated_user()
            doc = User.by_email(user['email'])
            if not doc:
                doc = User
                doc['id'] = doc.find().count() + 1
                doc['user_name'] = user['name']
                doc['user_pass'] = utils.make_emailverify()
                doc['user_email'] = user['email']
                doc['user_domain'] = user['name']
                doc.new(doc)
                send_joinus_email(user['email'], user['name'])
            user_info = {
                'user_id': doc.id,
                'user_name': doc.user_name,
                'user_email': doc.user_email,
                'user_domain': doc.user_domain}
            self.set_secure_cookie("user",
                                   tornado.escape.json_encode(user_info))
            self.redirect("/")
            return
        self.authenticate_redirect()


class JoinusHandler(BaseHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
        self.render('joinus.html')

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')
        domain = self.get_argument('domain', '')
        password = utils.make_password(password)
        if domain == '':
            domain = name
        if User.by_email(email):
            self.authenticate_redirect()
            # self.redirect('/login')  # self.write('用户已经存在，请直接登录')
        else:
            res = User
            res['id'] = res.find().count() + 1
            res['user_name'] = name
            res['user_pass'] = password
            res['user_email'] = email
            res['user_domain'] = domain
            res.new(res)
            send_joinus_email(email, name)
            user_info = {
                'user_id': res.id,
                'user_name': res.user_name,
                'user_email': res.user_email,
                'user_domain': res.user_domain}
            self.set_secure_cookie(
                'user', tornado.escape.json_encode(user_info))
            self.redirect(self.get_argument('next', '/'))


def send_joinus_email(email, name):
    subject = '欢迎来到『安问』'
    msg_body = ''.join([
        '<html>',
        '<p>Hi ', name.encode('utf-8'), '</p>',
        '<p>欢迎注册『安问』</p>',
        '<p>『安问』是一个创造和分享的社区，你将可以在这里分享打动你的东西，展示你的奇思妙想，结交志同道合的朋友，发现更多精彩</p>',
        options.msg_footer,
        '</html>',
    ]).encode('utf8')
    utils.send_email(email, subject, msg_body)


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))


class UserhomeHandler(BaseHandler):

    def get(self, name):
        user = User.find_one({'user_domain': name})
        user.user_say = markdown2.markdown(user.user_say)
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        likenum = User.find({'user_id': user._id}).count()
        user.gravatar = get_avatar(user.user_email, 100)
        self.render('userhome.html', user=user, likenum=likenum)


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
        self.render('userlike.html', user=user, likenum=likenum, likes=likes)


class SettingHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user = User.by_sid(self.current_user['user_id'])
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        user.gravatar = get_avatar(user.user_email, 100)
        self.render('setting.html', user=user)

    @tornado.web.authenticated
    def post(self):
        user = User.by_sid(self.current_user['user_id'])
        user['user_name'] = self.get_argument('name', None)
        user['user_city'] = self.get_argument('city', None)
        user['user_say'] = self.get_argument('say', None)
        user.save()
        self.redirect('/setting')


class ChangePassHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user = User.by_sid(self.current_user['user_id'])
        user.user_jointime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(user.user_jointime))
        user.gravatar = get_avatar(user.user_email, 100)
        self.render('changepass.html', user=user)

    @tornado.web.authenticated
    def post(self):
        oldpass = self.get_argument('oldpass', '')
        newpass = self.get_argument('newpass', '')
        newpass = hashlib.md5(newpass).hexdigest()
        user = User.by_sid(self.current_user['user_id'])
        if user.user_pass == hashlib.md5(oldpass).hexdigest():
            user = User.by_sid(self.current_user['user_id'])
            user['user_pass'] = newpass
            user.save()
            self.redirect('/setting')
        else:
            self.redirect('/setting')  # self.write('Wrong password')


class MemberHandler(BaseHandler):

    def get(self):
        members = User.find()
        self.render('member.html', members=members)


class UsersHandler(CommonResourceHandler):
    res = User

    def pre_post(self, json_arg):
        if self.res.by_email(json_arg['user_email']):
            self.send_error(409)
        return self.res.new(json_arg)

    def post_get(self, user_obj):
        if user_obj:
            user_obj.pop('user_pass', None)
            if 'objs' in user_obj and isinstance(user_obj['objs'], list):
                for u in user_obj['objs']:
                    if 'user_pass' in u:
                        del u['user_pass']
        return user_obj


class ForgotPassHandler(BaseHandler):

    def get(self):
        self.render('forgotpass.html')

    def post(self):
        email = self.get_argument('email', '')
        doc = User.find_one({'user_email': email})
        if doc:
            emailverify = str(utils.make_emailverify())
            doc.emailverify = emailverify
            doc.save()
            self.send_resetpass_email(emailverify, email)
        self.render('forgotpass.html')

    def send_resetpass_email(self, verifystring, email):
        subject = 'Anwen 密码找回'
        verify_link = '%s/setpass?e=%s&k=%s' % (
            options.site_url, email, verifystring)
        verify_a = '<a href="%s">%s</a>' % (verify_link, verify_link)
        msg_body = ''.join([
            '<html>',
            '<p>Hi,</p>',
            '<p>请点击下面链接进行密码重设：</p>',
            str(verify_a),
            options.msg_footer,
            '</html>',
        ])
        utils.send_email(email, subject, msg_body)


class SetPassHandler(BaseHandler):

    def get(self):
        email = self.get_argument('e', '')
        emailverify = self.get_argument('k', '')
        if User.by_email_verify(email, emailverify):
            self.render('setpass.html')
        else:
            self.render('forgotpass.html')

    def post(self):
        email = self.get_argument('e', '')
        emailverify = self.get_argument('k', '')
        password = self.get_argument('password', '')
        password = utils.make_password(password)
        if User.reset_pass(email, emailverify, password):
            self.redirect('/login')
        else:
            self.render('forgotpass.html')
