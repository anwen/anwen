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
