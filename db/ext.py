# -*- coding: utf-8 -*-
import options
from bson import ObjectId
from mongokit import Document


class BaseModel(Document):
    __database__ = options.db['name']
    use_dot_notation = True

    def one_by(self, key_name, key):
        return self.find_one({key_name: key})

    def by_id(self, id):
        return self.find_one({'_id': ObjectId(id)})

    def by_sid(self, id):
        # return self.find_one({'id': int(id)}, {'_id': 0})
        assert self.find({'id': int(id)}).count() <= 1
        return self.find_one({'id': int(id)})

    def new(self, doc):
        res = self()
        if 'id' not in doc:
            doc['id'] = self.find().count() + 1
        res.update(doc)
        res.save()
        return res
