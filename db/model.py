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


print(options.db)
if 'username' in options.db:
    try:
        db.authenticate(options.db['username'], options.db['password'])
    except KeyError:
        print('KeyError: Not authenticating.')


try:
    basestring
except NameError:
    basestring = str


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


@connection.register
class Share(BaseModel):
    __collection__ = 'Share_Col'
    use_autorefs = True
    structure = {
        'title': basestring,
        'slug': basestring,
        'markdown': basestring,
        'content': basestring,
        'sharetype': basestring,
        'tags': basestring,
        'upload_img': basestring,
        'post_img': basestring,
        'link': basestring,
        'id': int,
        'user_id': int,
        'commentnum': int,
        'likenum': int,
        'dislikenum': int,
        'hitnum': int,
        'status': int,  # 0=public, 1=draft, 3=deleted
        'suggestscore': float,
        'score': float,
        'published': float,
        'updated': float,
    }
    default_values = {
        'tags': '',
        'link': '',
        'id': 0,
        'commentnum': 0,
        'likenum': 0,
        'dislikenum': 0,
        'hitnum': 0,
        'status': 0,  # 0=published,1=draft,2=deleted
        'suggestscore': 0.0,
        'score': 0.0,
        'published': time.time,
        'updated': time.time,
    }

    def by_slug(self, slug):
        return self.find_one({'slug': slug})


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
        'id': int,
        'user_id': int,
        'share_id': int,
        'likenum': int,
        'dislikenum': int,
        'liketime': float,
    }
    default_values = {
        'likenum': 0,
        'dislikenum': 0,
        'liketime': time.time,
    }

    def change_like(self, doc, liketype):
        res = self.find_one(doc) or self()
        if 'id' not in doc:
            doc['id'] = self.find().count() + 1
        res.update(doc)
        res[liketype] += 1
        res.save()
        return res


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

    def new(self, doc):
        tag = doc['name']
        if not tag:
            return
        share_id = doc['share_ids']
        res = self.find_one({'name': tag})
        if res:
            share_list = res.share_ids.split(' ')
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


@connection.register
class Feedback(BaseModel):
    __collection__ = 'Feedback_Col'
    structure = {
        'id': int,
        'user_email': basestring,
        'content': basestring,
        'time': float,
    }
    default_values = {
        'time': time.time,
    }


@connection.register
class Admin(BaseModel):
    __collection__ = 'Admin_Col'
    structure = {
        'id': int,
        'isadmin': bool,
        'issuperadmin': bool,
        'key': basestring,
        'join_time': float,
    }
    default_values = {
        'isadmin': False,
        'issuperadmin': False,
        'join_time': time.time,
    }


@connection.register
class Ande(BaseModel):
    __collection__ = 'Ande_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'user_ip': basestring,
        'usersay': basestring,
        'andesay': basestring,
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
        'body': basestring,
        'talktime': float,
    }
    default_values = {
        'user_id': 0,
        'body': '',
        'talktime': time.time,
    }
