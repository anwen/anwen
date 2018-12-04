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
class Like(BaseModel):
    __collection__ = 'Like_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'entity_id': int,
        'likenum': int,
        'dislikenum': int,
        'entity_type': str,
        'create_time': float,
    }
    default_values = {
        'likenum': 0,
        'dislikenum': 0,
        'create_time': time.time,
    }

    def change_like(self, doc, _action, action):
        res = self.find_one(doc)
        if not res:
            doc[_action] = 1
            self.new(doc)
            return True
        if action == 'add':
            if res[_action] == 1:
                return False  # alert
            else:
                res[_action] = 1
        else:
            if res[_action] == 0:
                return False  # alert
            else:
                res[_action] = 0
        res.save()
        return True


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
        'hitnum': 0,
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


@connection.register
class Tag(BaseModel):
    __collection__ = 'Tag_Col'
    structure = {
        'id': int,
        'name': str,
        'share_ids': str,
        'hittime': float,
    }
    default_values = {
        'share_ids': '',
        'hittime': time.time,
    }

    def new(self, doc):
        tag = doc['name']
        if not tag:
            return
        share_id = doc['share_ids']
        res = self.find_one({'name': tag})
        if res:
            share_list = res.share_ids.split(' ')
            # share_list = list(set(share_list)) # TODO
            if share_id not in share_list:
                res.share_ids = '%s %s' % (res.share_ids, share_id)
                res.save()
        else:
            res = self()
            doc = {}
            doc['id'] = self.find().count() + 1
            doc['name'] = tag
            doc['share_ids'] = str(share_id)
            res.update(doc)
            res.save()
        return res
