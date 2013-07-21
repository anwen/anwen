# -*- coding: utf-8 -*-

from .me_model import Admin
from . import Share


def apply_admin(user_id, key):
    if user_id:
        res = Admin.objects(admin_id=int(user_id))
        if res.count():
            doc = res.first()
        else:
            doc = Admin()
        doc.admin_id = user_id
        doc.key = key
        doc.save()
        return doc
    return


def add_admin(user_id, key):
    if user_id and key:
        res = Admin.objects(admin_id=int(user_id), key=key)
        if res.count():
            doc = res.first()
            doc.key = None
            doc.isadmin = True
            doc.save()
            return True
    return False


def is_admin(user_id):
    if user_id:
        res = Admin.objects(admin_id=int(user_id))
        if res.count():
            doc = res.first()
            if doc.isadmin:
                return True
    return False


def delete_share(share_id):
    if share_id:
        share = Share.by_sid(share_id)
        if not share:
            return False
        share['status'] = 3  # means deleted
        share = share.save()
