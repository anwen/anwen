# -*- coding: utf-8 -*-
import time
from mongokit import Connection
from .ext import BaseModel
import options
if 'host' in options.db:
    connection = Connection(
        host=options.db['host'],
        port=options.db['port'],
    )
else:
    connection = Connection()
db = getattr(connection, options.db['name'])
# print(options.db)
if 'username' in options.db:
    try:
        db.authenticate(options.db['username'], options.db['password'])
    except KeyError:
        print('KeyError: Not authenticating.')


@connection.register
class Admin(BaseModel):
    __collection__ = 'Admin_Col'
    structure = {
        'id': int,
        'isadmin': bool,
        'issuperadmin': bool,
        'key': str,
        'join_time': float,
    }
    default_values = {
        'isadmin': False,
        'issuperadmin': False,
        'join_time': time.time,
    }


@connection.register
class Viewpoint(BaseModel):
    __collection__ = 'Viewpoint_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'share_id': int,
        'likenum': int,
        'dislikenum': int,
        'aview': str,
        'create_time': float,
    }
    default_values = {
        'likenum': 0,
        'create_time': time.time,
    }


@connection.register
class Comment(BaseModel):
    __collection__ = 'Comment_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'share_id': int,
        'likenum': int,
        'dislikenum': int,
        'user_name': str,
        'commentbody': str,
        'commenttime': float,
    }
    default_values = {
        'likenum': 0,
        'dislikenum': 0,
        'commenttime': time.time,
    }


@connection.register
class Relationship(BaseModel):
    __collection__ = 'Relationship_Col'
    use_autorefs = True
    structure = {
        'from_user': int,
        'to_user': int,
    }


@connection.register
class Hit(BaseModel):
    __collection__ = 'Hit_Col'
    structure = {
        'id': int,
        'user_id': int,
        'share_id': int,
        'hitnum': int,
        'hittime': float,
    }
    default_values = {
        'user_id': 0,
        'share_id': 0,
        'hitnum': 1,
        'hittime': time.time,
    }


@connection.register
class Feedback(BaseModel):
    __collection__ = 'Feedback_Col'
    structure = {
        'id': int,
        'user_email': str,
        'content': str,
        'time': float,
    }
    default_values = {
        'time': time.time,
    }


@connection.register
class Ande(BaseModel):
    __collection__ = 'Ande_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'user_ip': str,
        'usersay': str,
        'andesay': str,
        'chattime': float,
    }
    default_values = {
        'user_id': 0,
        'user_ip': '',
        'chattime': time.time,
    }

    def by_ip(self, ip):
        return self.find({'user_ip': ip}).count()

    def by_uid(self, uid):
        return self.find({'user_id': uid}).count()


@connection.register
class Talk(BaseModel):
    __collection__ = 'Talk_Col'
    structure = {
        'id': int,
        'user_id': int,
        'body': str,
        'talktime': float,
    }
    default_values = {
        'user_id': 0,
        'body': '',
        'talktime': time.time,
    }


@connection.register
class Webcache(BaseModel):
    __collection__ = 'Webcache_Col'
    structure = {
        'id': int,
        'url': str,
        'title': str,
        'markdown': str,
    }
    default_values = {
    }
