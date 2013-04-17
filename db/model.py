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
        'id': int,
        'user_id': int,
        'commentnum': int,
        'likenum': int,
        'dislikenum': int,
        'hitnum': int,
        'status': int,
        'suggestscore': float,
        'score': float,
        'published': float,
        'updated': float,
    }
    default_values = {
        'tags': '',
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
        share_id = doc['share_ids']
        res = self.find_one({'name': tag})
        if res:
            share_list = res.share_ids.split(' ')
            if share_id not in share_list:
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


@connection.register
class Room(BaseModel):
    __collection__ = 'Room_Col'
    structure = {
        'id': int,
        'user1': basestring,
        'user2': basestring,
        'room_key': basestring,
        'meettime': float,
    }
    default_values = {
        'meettime': time.time,
    }

    def by_room_key(self, room_key):
        return self.find_one({'room_key': room_key})

    def get_occupancy(self):
        occupancy = 0
        if self.user1:
            occupancy += 1
        if self.user2:
            occupancy += 1
        return occupancy

    def add_user(self, user):
        if not self.user1:
            self.user1 = user
        elif not self.user2:
            self.user2 = user
        else:
            return False
            # raise RuntimeError('room is full')
        self.save()

    def __str__(self):
        return "[user1:%s user2:%s]" % (self.user1, self.user2)

    def get_other_user(self, user):
        if user == self.user1:
            return self.user2
        elif user == self.user2:
            return self.user1
        else:
            return None

    def has_user(self, user):
        return (user and (user == self.user1 or user == self.user2))

    def remove_user(self, user):
        if user == self.user2:
            self.user2 = None
        if user == self.user1:
            if self.user2:
                self.user1 = self.user2
                self.user2 = None
            else:
                self.user1 = None
        if self.get_occupancy() > 0:
            self.save()
        else:
            self.delete()


@connection.register
class VideoMsg(BaseModel):
    __collection__ = 'VideoMsg_Col'
    structure = {
        'id': int,
        'client_id': basestring,
        'msg': basestring,
        'time': float,
    }
    default_values = {
        'time': time.time,
    }


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
