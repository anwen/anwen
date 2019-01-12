# -*- coding: utf-8 -*-
import time
from db.ext import BaseModel


class Collect(BaseModel):
    __collection__ = 'Collect_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'user_id': int,
        'entity_id': int,
        'collectnum': int,
        'entity_type': str,
        # notebook todo
        'create_time': float,
    }
    default_values = {
        'collectnum': 0,
        'create_time': time.time,
    }

    def change_collect(self, doc, _action, action):
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
