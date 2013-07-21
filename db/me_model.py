# -*- coding: utf-8 -*-
import datetime
from mongoengine import *
import options


if 'username' in options.db:
    connect(
        options.db['name'],
        host=options.db['host'],
        port=options.db['port'],
        username=options.db['username'],
        password=options.db['password'],
    )
else:
    connect(options.db['name'])


class Admin(Document):
    admin_id = IntField(required=True)
    isadmin = BooleanField(default=False)
    key = StringField(max_length=200)
    join_time = DateTimeField(default=datetime.datetime.now)
