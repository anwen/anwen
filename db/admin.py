# -*- coding: utf-8 -*-

from . import Share, Admin


def apply_admin(user_id, key):
    doc = Admin.by_sid(user_id)
    if not doc:
        doc = Admin()
        doc['id'] = user_id
    doc['key'] = key
    doc.save()


def add_admin(user_id, key, s):
    if user_id and key:
        doc = Admin.by_sid(user_id)
        if doc['key'] == key:
            doc.key = None
            if s:
                doc.issuperadmin = True
            doc.isadmin = True
            doc.save()
            return True
    return False


def is_admin(user_id):
    doc = Admin.by_sid(user_id)
    return doc['isadmin'] if doc else False


def is_superadmin(user_id):
    doc = Admin.by_sid(user_id)
    return doc['issuperadmin'] if doc else False


def delete_share(share_id):
    if share_id:
        share = Share.by_sid(share_id)
        if not share:
            return False
        share['status'] = 3  # means hide
        share = share.save()


def delete_share_by_s(share_id):
    if share_id:
        share = Share.by_sid(share_id)
        if not share:
            return False
        share.delete()
