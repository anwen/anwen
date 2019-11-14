# -*- coding: utf-8 -*-
import time
from db.ext import BaseModel


# @connection.register
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

    def by_name(self, name):
        return self.find_one({'name': name})

    def by_sid(self, sid):
        return self.find_one({'id': sid})
