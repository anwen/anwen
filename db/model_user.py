# -*- coding: utf-8 -*-
from db.model import connection
from db.ext import BaseModel
import time

import options
from bson import ObjectId
from mongokit import Document

try:
    basestring
except NameError:
    basestring = str


# from mongokit import Connection
# import options
# if 'host' in options.db:
#     connection = Connection(
#         host=options.db['host'],
#         port=options.db['port'],
#     )
# else:
#     connection = Connection()
# db = getattr(connection, options.db['name'])
# if 'username' in options.db:
#     try:
#         db.authenticate(options.db['username'], options.db['password'])
#     except KeyError:
#         print('KeyError: Not authenticating.')


# @connection.register
class User(BaseModel):
    __collection__ = 'User_Col'
    structure = {
        'user_name': basestring,
        'user_email': basestring,
        'user_pass': basestring,
        'user_domain': basestring,
        'user_url': basestring,
        'user_city': basestring,
        'user_say': basestring,
        'emailverify': basestring,
        'id': int,
        'user_leaf': int,
        'user_status': int,   # 0=default, 1=veryfied
        'user_jointime': float,
    }
    required_fields = ['user_pass', 'user_email']
    default_values = {
        'user_url': '',
        'user_city': '',
        'user_say': '',
        'emailverify': '',
        'user_leaf': 20,
        'user_status': 0,
        'user_jointime': time.time,
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

    # def delete(self):
    #     pass
