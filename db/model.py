# -*- coding: utf-8 -*-
import time
from mongokit import Connection
from ext import BaseModel

connection = Connection()


@connection.register
class Config(BaseModel):
    __collection__ = 'Config_Col'
    structure = {
        'name': basestring,
        'value': None,
    }
    required_fields = ['name', ]

    def set(self, name, value):
        c = {'name': name}
        config = self.find_one(c) or self(c)
        config['value'] = value
        config.save()

    def by_name(self, name):
        return self.find_one({'name': name})

    def value_of(self, name):
        obj = self.by_name(name)
        if obj:
            return obj.value


@connection.register
class User(BaseModel):
    __collection__ = 'User_Col'
    structure = {
        'user_name': basestring,
        'user_pass': basestring,
        'user_email': basestring,
        'user_domain': basestring,
        'user_url': basestring,
        'user_city': basestring,
        'user_say': basestring,
        'id': int,
        'user_leaf': int,
        'user_status': int,
        'user_jointime': float,
    }
    required_fields = ['user_pass', 'user_email']
    default_values = {
        'user_url': '',
        'user_city': '',
        'user_say': '',
        'user_leaf': 20,
        'user_status': 0,
        'user_jointime': time.time,
    }

    def by_username(self, username):
        return self.find_one({'username': username})

    def by_useremail(self, useremail):
        return self.find_one({'useremail': useremail})

    def by_name_pass(self, username, userpass):
        if username and userpass:
            return self.find_one(
                {'user_name': username, 'user_pass': userpass})

    def by_email_pass(self, email, userpass):
        if email and userpass:
            return self.find_one({'user_email': email, 'user_pass': userpass})

    # def delete(self):
    #     pass


@connection.register
class Ande(BaseModel):
    __collection__ = 'Ande_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'usersay': basestring,
        'andesay': basestring,
        'chattime': float,
    }
    default_values = {
        'chattime': time.time,
    }


@connection.register
class Share(BaseModel):
    __collection__ = 'Share_Col'
    use_autorefs = True
    structure = {
        'title': basestring,
        'slug': basestring,
        'markdown': basestring,
        'sharetype': basestring,
        'tags': basestring,
        'id': int,
        'user_id': int,
        'commentnum': int,
        'likenum': int,
        'hitnum': int,
        'status': int,
        'published': float,
        'updated': float,
    }
    default_values = {
        'tags': '',
        'id': 0,
        'commentnum': 0,
        'likenum': 0,
        'hitnum': 0,
        'status': 0,
        'published': time.time,
        'updated': time.time,
    }

    def by_slug(self, slug):
        return self.find_one({'slug': str(slug)})


@connection.register
class Comment(BaseModel):
    __collection__ = 'Comment_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'share_id': int,
        'commentbody': basestring,
        'commenttime': float,
    }
    default_values = {
        'commenttime': time.time,
    }


@connection.register
class Like(BaseModel):
    __collection__ = 'Like_Col'
    use_autorefs = True
    structure = {
        'user_id': int,
        'share_id': int,
        'liketime': float,
    }
    default_values = {
        'liketime': time.time,
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
        'hitnum': 0,
        'hittime': time.time,
    }


@connection.register
class Tag(BaseModel):
    __collection__ = 'Tag_Col'
    structure = {
        'id': int,
        'name': basestring,
        'share_ids': basestring,
        'hittime': float,
    }
    default_values = {
        'share_ids': '',
        'hittime': time.time,
    }

    def new(self, tag, share_id):
        res = self.find_one({'name': tag})
        if res:
            share_list = res.share_ids.split(' ')
            if share_id in share_list:
                pass
            else:
                res.share_ids = '%s %s' % (res.share_ids, share_id)
        else:
            res = self()
            doc = {}
            doc['id'] = self.find().count() + 1
            doc['name'] = tag
            doc['share_ids'] = str(share_id)
            res.update(doc)
            res.save()
        return res
