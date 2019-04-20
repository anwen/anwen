# -*- coding: utf-8 -*-
from db.ext import BaseModel
import time
# try:
#     basestring
# except NameError:
#     basestring = str
# @connection.register


class User(BaseModel):
    __collection__ = 'User_Col'
    structure = {
        'id': int,
        'user_name': str,
        'user_email': str,
        'user_pass': str,
        'user_domain': str,  # optional
        'user_url': str,
        'user_rss': str,
        'user_city': str,
        'user_say': str,
        'user_lang': str,
        'user_tags': list,
        'user_leaf': int,
        'user_status': int,   # 0=default, 1=veryfied
        'user_jointime': float,
        'emailverify': str,
    }
    required_fields = ['id', 'user_name', 'user_email', 'user_pass']
    default_values = {
        # for geek and rss-user
        'user_domain': '',
        'user_url': '',
        'user_rss': '',
        'user_say': '',
        'user_lang': '',

        'user_city': '',
        'user_tags': [],
        'user_leaf': 20,
        'user_status': 0,
        'user_jointime': time.time,
        'emailverify': '',
    }

    def by_email(self, email):
        return self.find_one({'user_email': email})

    def by_name_pass(self, username, userpass):
        if username and userpass:
            return self.find_one(
                {'user_name': username, 'user_pass': userpass})

    def by_email_pass(self, email, userpass):
        if email and userpass:
            return self.find_one({'user_email': email, 'user_pass': userpass})

    def by_email_verify(self, email, verify):
        if email and verify:
            return self.find_one({'user_email': email, 'emailverify': verify})

    def reset_pass(self, email, verify, userpass):
        if email and verify:
            doc = self.find_one({'user_email': email, 'emailverify': verify})
            doc.user_pass = userpass
            doc.emailverify = '1'
            doc.save()
            return True
        return False
