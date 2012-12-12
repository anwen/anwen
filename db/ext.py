# -*- coding: utf-8 -*-
import json
import options
from bson import ObjectId
from mongokit import Document
from mongokit import CustomType


class DynamicType(CustomType):
    mongo_type = unicode
    python_type = unicode
    init_type = unicode

    def __init__(self, func, base_type=unicode):
        super(DynamicType, self).__init__()
        self.func = func
        self.mongo_type = base_type
        self.python_type = base_type
        self.init_type = base_type

    def to_bson(self, value):
        """convert type to a mongodb type"""
        return None

    def to_python(self, value):
        """convert type to a python object"""
        return self.func()

    def validate(self, value, path):
        pass


class BaseModel(Document):
    __database__ = options.db['name']
    use_dot_notation = True

    def by_id(self, id):
        return self.find_one({'_id': ObjectId(id)})

    def by_sid(self, id):
        return self.find_one({'id': int(id)})

    def update_by_id(self, id, update):
        m = self.by_id(id)
        update.pop('_id', None)
        for k, v in update.iteritems():
            m[k] = v
        m.save()

    def to_json(self):
        json_str = super(BaseModel, self).to_json()
        if '$oid' in json_str:
            obj = json.loads(json_str)
            _id = obj.pop('_id')['$oid']
            obj['id'] = _id
        return json.dumps(obj)

    def new(self, doc):
        if 'id' not in doc:
            doc['id'] = self.find().count() + 1
        self.update(doc)
        return self.save()
