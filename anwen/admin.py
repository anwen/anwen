# -*- coding: utf-8 -*-

import tornado.web
from .base import BaseHandler
from db import me_admin, Share
import utils
import options


class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user['user_id']
        if me_admin.is_admin(user_id):
            self.render('admin/admin.html')
        else:
            self.render('admin/join_admin.html')


class BecomeAdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user['user_id']
        user_name = self.current_user['user_name']
        u = self.get_argument("u", None)
        k = self.get_argument("k", None)
        if u and k:
            result = me_admin.add_admin(u, k)
            if result:
                self.render('admin/become_admin_success.html')
            return
        else:
            key = utils.make_emailverify()
            me_admin.apply_admin(user_id, key)
            send_become_admin_email(user_id, user_name, key)
            self.render('admin/become_admin_sent.html')


def send_become_admin_email(uid, name, key):

    verify_link = '%s/become_admin?u=%s&k=%s' % (
        options.site_url, uid, key)
    verify_a = '<a href="%s">%s</a>' % (verify_link, verify_link)

    subject = '申请成为安问管理者~'
    msg_body = ''.join([
        '<html>',
        '<p>Hi ', str(name), '申请成为管理者</p>',
        '<p>点击链接通过申请:</p>',
        verify_a,
        options.msg_footer,
        '</html>',
    ])
    email = options.superadmin_email
    utils.send_email(email, subject, msg_body)


class AdminShareHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user['user_id']
        share_id = self.get_argument("delete", None)
        if me_admin.is_admin(user_id):
            if share_id:
                me_admin.delete_share(share_id)
            shares = Share.find({'status': 0 and 3})
            self.render('admin/share.html', shares=shares)
        else:
            self.render('admin/join_admin.html')
